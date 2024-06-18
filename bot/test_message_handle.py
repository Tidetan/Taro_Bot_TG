import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Message, Chat, User
from telegram.ext import CallbackContext
from bot import message_handle, db, user_semaphores, user_tasks

@pytest.mark.asyncio
async def test_message_handle_bot_not_mentioned():
    update = AsyncMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    update.message.chat.type = "private"
    update.message.text = "Test message"
    
    async def is_bot_mentioned(update, context):
        return False

    await message_handle(update, context)
    assert not context.bot.send_message.called

@pytest.mark.asyncio
async def test_message_handle_empty_message():
    update = AsyncMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    update.message.chat.type = "private"
    update.message.text = ""

    async def is_bot_mentioned(update, context):
        return True

    await message_handle(update, context)
    context.bot.send_message.assert_called_once_with(chat_id=update.message.chat_id, text="🥲 You sent <b>empty message</b>. Please, try again!", parse_mode="HTML")

@pytest.mark.asyncio
async def test_message_handle_new_dialog_timeout():
    update = AsyncMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    update.message.chat.type = "private"
    update.message.text = "Test message"
    update.message.from_user.id = 123
    db.get_user_attribute = MagicMock(return_value=(datetime.now() - timedelta(seconds=100)))
    db.get_dialog_messages = MagicMock(return_value=["message1", "message2"])
    db.start_new_dialog = MagicMock()
    db.set_user_attribute = MagicMock()
    
    async def is_bot_mentioned(update, context):
        return True

    await message_handle(update, context)
    db.start_new_dialog.assert_called_once_with(123)

@pytest.mark.asyncio
async def test_message_handle_tarot_forecaster():
    update = AsyncMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    update.message.chat.type = "private"
    update.message.text = "Test message"
    update.message.from_user.id = 123
    db.get_user_attribute = MagicMock(side_effect=lambda user_id, attr: {
        "current_chat_mode": "tarot_forecaster",
        "last_interaction": datetime.now() - timedelta(seconds=10),
        "current_model": "test_model"
    }[attr])
    db.get_dialog_messages = MagicMock(return_value=["message1", "message2"])
    db.set_user_attribute = MagicMock()
    db.update_n_used_tokens = MagicMock()
    openai_utils.ChatGPT = MagicMock()
    chatgpt_instance = openai_utils.ChatGPT.return_value
    chatgpt_instance.send_message = AsyncMock(return_value=("Response message", (10, 20), 0))
    
    async def is_bot_mentioned(update, context):
        return True

    await message_handle(update, context)
    context.bot.edit_message_text.assert_called_once_with("Response message", chat_id=update.message.chat_id, message_id=Any(), parse_mode="HTML")

@pytest.mark.asyncio
async def test_message_handle_dialog_too_long():
    update = AsyncMock(spec=Update)
    context = MagicMock(spec=CallbackContext)
    update.message.chat.type = "private"
    update.message.text = "Test message"
    update.message.from_user.id = 123
    db.get_user_attribute = MagicMock(side_effect=lambda user_id, attr: {
        "current_chat_mode": "tarot_forecaster",
        "last_interaction": datetime.now() - timedelta(seconds=10),
        "current_model": "test_model"
    }[attr])
    db.get_dialog_messages = MagicMock(return_value=["message" + str(i) for i in range(10)])
    db.set_user_attribute = MagicMock()
    db.update_n_used_tokens = MagicMock()
    openai_utils.ChatGPT = MagicMock()
    chatgpt_instance = openai_utils.ChatGPT.return_value
    chatgpt_instance.send_message = AsyncMock(return_value=("Response message", (10, 20), 1))
    
    async def is_bot_mentioned(update, context):
        return True

    await message_handle(update, context)
    context.bot.edit_message_text.assert_called_with("Response message", chat_id=update.message.chat_id, message_id=Any(), parse_mode="HTML")
    context.bot.send_message.assert_called_with(chat_id=update.message.chat_id, text="✍️ <i>Note:</i> Your current dialog is too long, so your <b>first message</b> was removed from the context.\n Send /new command to start new dialog", parse_mode="HTML")