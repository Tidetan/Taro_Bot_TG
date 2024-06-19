import io
import logging
import asyncio
import traceback
import html
import json
from datetime import datetime
import openai

import telegram
from telegram import (
    Update,
    User,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    AIORateLimiter,
    filters
)
from telegram.constants import ParseMode, ChatAction
from bot.tarot_utils import get_daily_tarot_card

import config
import database
import openai_utils


# setup
db = database.Database()
logger = logging.getLogger(__name__)

user_semaphores = {}
user_tasks = {}

HELP_MESSAGE = """Команды:

⚪ /new – Начать новый чат
⚪ /retry – Повторно сгенерировать последний ответ
⚪ /balance – Показать баланс
⚪ /cancel – Отменяет последнее сообщение если долго создается
⚪ /help – Показать команды

🎤 Ты можешь отправить <b>голосовое сообщение</b> вместо текста!

"""


#Важно разбивает текст на чанки

def split_text_into_chunks(text, chunk_size): 
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]

#Важно регистрирует нового пользователя если он существует

async def register_user_if_not_exists(update: Update, context: CallbackContext, user: User):
    if not db.check_if_user_exists(user.id):
        db.add_new_user(
            user.id,
            update.message.chat_id,
            username=user.username,
            first_name=user.first_name,
            last_name= user.last_name
        )
        db.start_new_dialog(user.id)

    if db.get_user_attribute(user.id, "current_dialog_id") is None:
        db.start_new_dialog(user.id)

    if user.id not in user_semaphores:
        user_semaphores[user.id] = asyncio.Semaphore(1)

    if db.get_user_attribute(user.id, "current_model") is None:
        db.set_user_attribute(user.id, "current_model", config.models["available_text_models"][0])

        # Set default chat mode to tarot_forecaster
    if db.get_user_attribute(user.id, "current_chat_mode") is None:
        db.set_user_attribute(user.id, "current_chat_mode", "tarot_forecaster")

    # back compatibility for n_used_tokens field
    n_used_tokens = db.get_user_attribute(user.id, "n_used_tokens")
    if isinstance(n_used_tokens, int) or isinstance(n_used_tokens, float):  # old format
        new_n_used_tokens = {
            "gpt-3.5-turbo": {
                "n_input_tokens": 0,
                "n_output_tokens": n_used_tokens
            }
        }
        db.set_user_attribute(user.id, "n_used_tokens", new_n_used_tokens)

    # voice message transcription
    if db.get_user_attribute(user.id, "n_transcribed_seconds") is None:
        db.set_user_attribute(user.id, "n_transcribed_seconds", 0.0)

    # image generation
    if db.get_user_attribute(user.id, "n_generated_images") is None:
        db.set_user_attribute(user.id, "n_generated_images", 0)


# Обрабатывает команду /start

async def start_handle(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)
    user_id = update.message.from_user.id

    db.set_user_attribute(user_id, "last_interaction", datetime.now())
    db.start_new_dialog(user_id)

    reply_text = "Привет! Я <b>PocketTaro</b> бот реализованный с помощью OpenAI 🃏\n\n"
    reply_text += HELP_MESSAGE

    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)

# Обрабатывает команду /help

async def help_handle(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)
    user_id = update.message.from_user.id
    db.set_user_attribute(user_id, "last_interaction", datetime.now())
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.HTML)


# Обрабатывает команду /retry

async def retry_handle(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)
    if await is_previous_message_not_answered_yet(update, context): return

    user_id = update.message.from_user.id
    db.set_user_attribute(user_id, "last_interaction", datetime.now())

    dialog_messages = db.get_dialog_messages(user_id, dialog_id=None)
    if len(dialog_messages) == 0:
        await update.message.reply_text("No message to retry 🤷‍♂️")
        return

    last_dialog_message = dialog_messages.pop()
    db.set_dialog_messages(user_id, dialog_messages, dialog_id=None)  # last message was removed from the context

    await message_handle(update, context, message=last_dialog_message["user"], use_new_dialog_timeout=False)

# Обрабатывает входящие сообщения.
async def message_handle(update: Update, context: CallbackContext, message=None, use_new_dialog_timeout=True):
    # Проверка, было ли сообщение отредактировано
    if update.edited_message is not None:
        await edited_message_handle(update, context)
        return

    _message = message or update.message.text

    # Регистрация пользователя и проверка предыдущих сообщений
    await register_user_if_not_exists(update, context, update.message.from_user)
    if await is_previous_message_not_answered_yet(update, context):
        return

    user_id = update.message.from_user.id

    # Обработка сообщения
    async def message_handle_fn():
        # Новый диалог по таймауту
        if use_new_dialog_timeout:
            if (datetime.now() - db.get_user_attribute(user_id, "last_interaction")).seconds > config.new_dialog_timeout and len(db.get_dialog_messages(user_id)) > 0:
                db.start_new_dialog(user_id)
                await update.message.reply_text(f"Начинаем новый диалог из-за таймаута (<b>{config.chat_modes['tarot_forecaster']['name']}</b> режим) ✅", parse_mode=ParseMode.HTML)
        db.set_user_attribute(user_id, "last_interaction", datetime.now())

        n_input_tokens, n_output_tokens = 0, 0
        current_model = db.get_user_attribute(user_id, "current_model")

        try:
            placeholder_message = await update.message.reply_text("...")

            await update.message.chat.send_action(action="typing")

            if _message is None or len(_message) == 0:
                await update.message.reply_text("🥲 Вы отправили <b>пустое сообщение</b>. Пожалуйста, попробуйте снова!", parse_mode=ParseMode.HTML)
                return

            dialog_messages = db.get_dialog_messages(user_id, dialog_id=None)
            parse_mode = {
                "html": ParseMode.HTML,
                "markdown": ParseMode.MARKDOWN
            }[config.chat_modes['tarot_forecaster']['parse_mode']]

            chatgpt_instance = openai_utils.ChatGPT(model=current_model)
            tarot_query = f"Предсказание на картах Таро для запроса: {_message}"

            if config.enable_message_streaming:
                gen = chatgpt_instance.send_message_stream(tarot_query, dialog_messages=dialog_messages, chat_mode="tarot_forecaster")
            else:
                answer, (n_input_tokens, n_output_tokens), n_first_dialog_messages_removed = await chatgpt_instance.send_message(
                    tarot_query,
                    dialog_messages=dialog_messages,
                    chat_mode="tarot_forecaster"
                )

                async def fake_gen():
                    yield "finished", answer, (n_input_tokens, n_output_tokens), n_first_dialog_messages_removed

                gen = fake_gen()

            prev_answer = ""
            async for gen_item in gen:
                status, answer, (n_input_tokens, n_output_tokens), n_first_dialog_messages_removed = gen_item

                answer = answer[:4096]  # Лимит сообщения в Telegram

                if abs(len(answer) - len(prev_answer)) < 100 and status != "finished":
                    continue

                try:
                    await context.bot.edit_message_text(answer, chat_id=placeholder_message.chat_id, message_id=placeholder_message.message_id, parse_mode=parse_mode)
                except telegram.error.BadRequest as e:
                    if str(e).startswith("Message is not modified"):
                        continue
                    else:
                        await context.bot.edit_message_text(answer, chat_id=placeholder_message.chat_id, message_id=placeholder_message.message_id)

                await asyncio.sleep(0.01)

                prev_answer = answer

            new_dialog_message = {"user": _message, "bot": answer, "date": datetime.now()}
            db.set_dialog_messages(
                user_id,
                db.get_dialog_messages(user_id, dialog_id=None) + [new_dialog_message],
                dialog_id=None
            )

            db.update_n_used_tokens(user_id, current_model, n_input_tokens, n_output_tokens)

        except asyncio.CancelledError:
            db.update_n_used_tokens(user_id, current_model, n_input_tokens, n_output_tokens)
            raise

        except Exception as e:
            error_text = f"Произошла ошибка во время выполнения. Причина: {e}"
            logger.error(error_text)
            await update.message.reply_text(error_text)
            return

        if n_first_dialog_messages_removed > 0:
            if n_first_dialog_messages_removed == 1:
                text = "✍️ <i>Примечание:</i> Ваш текущий диалог слишком длинный, поэтому ваше <b>первое сообщение</b> было удалено из контекста.\n Отправьте команду /new для начала нового диалога"
            else:
                text = f"✍️ <i>Примечание:</i> Ваш текущий диалог слишком длинный, поэтому <b>{n_first_dialog_messages_removed} первых сообщений</b> были удалены из контекста.\n Отправьте команду /new для начала нового диалога"
            await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    async with user_semaphores[user_id]:
        task = asyncio.create_task(message_handle_fn())
        user_tasks[user_id] = task

        try:
            await task
        except asyncio.CancelledError:
            await update.message.reply_text("✅ Отменено", parse_mode=ParseMode.HTML)
        finally:
            if user_id in user_tasks:
                del user_tasks[user_id]



async def is_previous_message_not_answered_yet(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)

    user_id = update.message.from_user.id
    if user_semaphores[user_id].locked():
        text = "⏳ Пожалуйста <b>подождите</b> дождитесь ответ на предыдущее сообщение\n"
        text += "Или вы можете отменить его использовав /cancel"
        await update.message.reply_text(text, reply_to_message_id=update.message.id, parse_mode=ParseMode.HTML)
        return True
    else:
        return False

# Обрабатывает голосовые сообщения

async def voice_message_handle(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)
    if await is_previous_message_not_answered_yet(update, context): return

    user_id = update.message.from_user.id
    db.set_user_attribute(user_id, "last_interaction", datetime.now())

    voice = update.message.voice
    voice_file = await context.bot.get_file(voice.file_id)
    
    # store file in memory, not on disk
    buf = io.BytesIO()
    await voice_file.download_to_memory(buf)
    buf.name = "voice.oga"  # file extension is required
    buf.seek(0)  # move cursor to the beginning of the buffer

    transcribed_text = await openai_utils.transcribe_audio(buf)
    text = f"🎤: <i>{transcribed_text}</i>"
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    # update n_transcribed_seconds
    db.set_user_attribute(user_id, "n_transcribed_seconds", voice.duration + db.get_user_attribute(user_id, "n_transcribed_seconds"))

    await message_handle(update, context, message=transcribed_text)

#Генерирует изображения на основе текстовых сообщений.

async def generate_image_handle(update: Update, context: CallbackContext, message=None):
    await register_user_if_not_exists(update, context, update.message.from_user)
    if await is_previous_message_not_answered_yet(update, context): return

    user_id = update.message.from_user.id
    db.set_user_attribute(user_id, "last_interaction", datetime.now())

    await update.message.chat.send_action(action="upload_photo")

    message = message or update.message.text

    try:
        image_urls = await openai_utils.generate_images(message, n_images=config.return_n_generated_images, size=config.image_size)
    except openai.error.InvalidRequestError as e:
        if str(e).startswith("Your request was rejected as a result of our safety system"):
            text = "🥲 Your request <b>doesn't comply</b> with OpenAI's usage policies.\nWhat did you write there, huh?"
            await update.message.reply_text(text, parse_mode=ParseMode.HTML)
            return
        else:
            raise

    # token usage
    db.set_user_attribute(user_id, "n_generated_images", config.return_n_generated_images + db.get_user_attribute(user_id, "n_generated_images"))

    for i, image_url in enumerate(image_urls):
        await update.message.chat.send_action(action="upload_photo")
        await update.message.reply_photo(image_url, parse_mode=ParseMode.HTML)

# Начинает новый диалог

# Начинает новый диалог
async def new_dialog_handle(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)
    if await is_previous_message_not_answered_yet(update, context): return

    user_id = update.message.from_user.id
    db.set_user_attribute(user_id, "last_interaction", datetime.now())

    db.start_new_dialog(user_id)
    
    chat_mode = db.get_user_attribute(user_id, "current_chat_mode")
    welcome_message = config.chat_modes[chat_mode]['welcome_message']

    # Создаем инлайн-кнопку
    keyboard = [
        [InlineKeyboardButton("Карта дня", callback_data='daily_card')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

# Обрабатывает нажатие на инлайн-кнопку
async def button_handle(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'daily_card':
        await generate_daily_card(query, context)

# Генерирует карту дня
async def generate_daily_card(query, context):
    user_id = query.from_user.id
    card = get_daily_tarot_card()
    card_description = f"Ваша карта дня: <b>{card['name']}</b>\n{card['description']}"

    await query.edit_message_text(card_description, parse_mode=ParseMode.HTML)


# Отменяет текущую задачу

async def cancel_handle(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)

    user_id = update.message.from_user.id
    db.set_user_attribute(user_id, "last_interaction", datetime.now())

    if user_id in user_tasks:
        task = user_tasks[user_id]
        task.cancel()
    else:
        await update.message.reply_text("<i>Нечего отменять сообщение уже сгенерировалось...</i>", parse_mode=ParseMode.HTML)

# Показывает баланс пользователя

async def show_balance_handle(update: Update, context: CallbackContext):
    await register_user_if_not_exists(update, context, update.message.from_user)

    user_id = update.message.from_user.id
    db.set_user_attribute(user_id, "last_interaction", datetime.now())

    # count total usage statistics
    total_n_spent_dollars = 0
    total_n_used_tokens = 0

    n_used_tokens_dict = db.get_user_attribute(user_id, "n_used_tokens")
    n_generated_images = db.get_user_attribute(user_id, "n_generated_images")
    n_transcribed_seconds = db.get_user_attribute(user_id, "n_transcribed_seconds")

    details_text = "🏷️ Details:\n"
    for model_key in sorted(n_used_tokens_dict.keys()):
        n_input_tokens, n_output_tokens = n_used_tokens_dict[model_key]["n_input_tokens"], n_used_tokens_dict[model_key]["n_output_tokens"]
        total_n_used_tokens += n_input_tokens + n_output_tokens

        n_input_spent_dollars = config.models["info"][model_key]["price_per_1000_input_tokens"] * (n_input_tokens / 1000)
        n_output_spent_dollars = config.models["info"][model_key]["price_per_1000_output_tokens"] * (n_output_tokens / 1000)
        total_n_spent_dollars += n_input_spent_dollars + n_output_spent_dollars

        details_text += f"- {model_key}: <b>{n_input_spent_dollars + n_output_spent_dollars:.03f}$</b> / <b>{n_input_tokens + n_output_tokens} tokens</b>\n"

    # image generation
    image_generation_n_spent_dollars = config.models["info"]["dalle-2"]["price_per_1_image"] * n_generated_images
    if n_generated_images != 0:
        details_text += f"- DALL·E 2 (image generation): <b>{image_generation_n_spent_dollars:.03f}$</b> / <b>{n_generated_images} generated images</b>\n"

    total_n_spent_dollars += image_generation_n_spent_dollars

    # voice recognition
    voice_recognition_n_spent_dollars = config.models["info"]["whisper"]["price_per_1_min"] * (n_transcribed_seconds / 60)
    if n_transcribed_seconds != 0:
        details_text += f"- Whisper (voice recognition): <b>{voice_recognition_n_spent_dollars:.03f}$</b> / <b>{n_transcribed_seconds:.01f} seconds</b>\n"

    total_n_spent_dollars += voice_recognition_n_spent_dollars


    text = f"You spent <b>{total_n_spent_dollars:.03f}$</b>\n"
    text += f"You used <b>{total_n_used_tokens}</b> tokens\n\n"
    text += details_text

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

# Обрабатывает отредактированные сообщения

async def edited_message_handle(update: Update, context: CallbackContext):
    if update.edited_message.chat.type == "private":
        text = "🥲 Unfortunately, message <b>editing</b> is not supported"
        await update.edited_message.reply_text(text, parse_mode=ParseMode.HTML)

# Обрабатывает ошибки

async def error_handle(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    try:
        # collect error message
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            f"An exception was raised while handling an update\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        # split text into multiple messages due to 4096 character limit
        for message_chunk in split_text_into_chunks(message, 4096):
            try:
                await context.bot.send_message(update.effective_chat.id, message_chunk, parse_mode=ParseMode.HTML)
            except telegram.error.BadRequest:
                # answer has invalid characters, so we send it without parse_mode
                await context.bot.send_message(update.effective_chat.id, message_chunk)
    except:
        await context.bot.send_message(update.effective_chat.id, "Some error in error handler")

# Устанавливает команды бота после его инициализации

async def post_init(application: Application):
    await application.bot.set_my_commands([
        BotCommand("/new", "Начать новый чат"),
        BotCommand("/retry", "Повторно сгенерировать последний ответ"),
        BotCommand("/balance", "Показать баланс"),
        BotCommand("/help", "Показать команды"),
        BotCommand("/cancel", "Отменяет последнее сообщение если долго создается")
    ])

# Запускает бота

def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config.telegram_token)
        .concurrent_updates(True)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .post_init(post_init)
        .build()
    )

    # add handlers
    user_filter = filters.ALL
    if len(config.allowed_telegram_usernames) > 0:
        usernames = [x for x in config.allowed_telegram_usernames if isinstance(x, str)]
        any_ids = [x for x in config.allowed_telegram_usernames if isinstance(x, int)]
        user_ids = [x for x in any_ids if x > 0]
        group_ids = [x for x in any_ids if x < 0]
        user_filter = filters.User(username=usernames) | filters.User(user_id=user_ids) | filters.Chat(chat_id=group_ids)

    application.add_handler(CommandHandler("start", start_handle, filters=user_filter))
    application.add_handler(CommandHandler("help", help_handle, filters=user_filter))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & user_filter, message_handle))
    application.add_handler(CommandHandler("retry", retry_handle, filters=user_filter))
    application.add_handler(CommandHandler("new", new_dialog_handle, filters=user_filter))
    application.add_handler(CommandHandler("cancel", cancel_handle, filters=user_filter))

    application.add_handler(MessageHandler(filters.VOICE & user_filter, voice_message_handle))


    application.add_handler(CommandHandler("balance", show_balance_handle, filters=user_filter))
    application.add_handler(CallbackQueryHandler(button_handle, pattern='daily_card'))

    application.add_error_handler(error_handle)

    # start the bot
    application.run_polling()


if __name__ == "__main__":
    run_bot()