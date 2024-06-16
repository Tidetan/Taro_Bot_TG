## Key Features

- Lightning-fast responses (typically within 3-5 seconds)
- No request limits – chat as much as you want
- Seamless message streaming (see the demo)
- Powered by GPT-4 Turbo
- Group chat support (/help_group_chat for instructions)
- DALLE 2 integration (select 👩‍🎨 Artist mode for image generation)
- Voice message recognition
- Code highlighting for developers
- 15 special chat modes: 👩🏼‍🎓 Assistant, 👩🏼‍💻 Code Assistant, 👩‍🎨 Artist, 🧠 Psychologist, 🚀 Elon Musk, and more. Customize your chat modes by editing `config/chat_modes.yml`
- Utilize the [ChatGPT API](https://platform.openai.com/docs/guides/chat/introduction)
- Control access with a list of authorized Telegram users
- Keep track of your OpenAI API spending


---


## Bot Commands

- `/retry` – Regenerate the last response from the bot
- `/new` – Start a new conversation
- `/mode` – Choose a chat mode
- `/balance` – Check your OpenAI API balance
- `/settings` – View and adjust bot settings
- `/help` – Get assistance with using the bot

## Getting Started

1. Obtain your [OpenAI API key](https://openai.com/api/).

2. Get your Telegram bot token from [@BotFather](https://t.me/BotFather).

3. Pre-requirements Installation [For Debian Based Environment only, for other system please install manually: Docker, Docker-compose, Python, pip]

   ```bash
   sudo apt -y update
   sudo apt -y install ca-certificates curl gnupg lsb-release docker-compose docker docker.io docker-compose python3 python3-pip apt-utils
   ```

4. Clone the repository:

   ```bash
   git clone https://github.com/yesbhautik/Master-AI-BOT
   ```
   
5. Go to the project directory:

   ```bash
   cd Master-AI-BOT
   ```
   
6. Install dependencies:
   
   ```bash
   pip3 install -r requirements.txt
   ```
   
7. Install dependencies:

   ```bash
   cp config/config-example.env config/config.env
   cp config/config-example.yml config/config.yml
   ```
8. Edit the configuration file `config/config.yml` to set your tokens. You can also edit `config/config.env` if you're an advanced user.

9. 🔥 Now, it's time to **run**:

    ```bash
    docker-compose --env-file config/config.env up --build -d
    ```

## References

1. Learn more about how we built ChatGPT from GPT-3: [Build ChatGPT from GPT-3](https://learnprompting.org/docs/applied_prompting/build_chatgpt)

## Contributing 🤝
Contributions are welcome! Please follow these steps to contribute to the project:

1. Fork the repository🍴
2. Create a new branch for your feature or bug fix 🌿
3. Make your changes and commit them 💻
4. Push your changes to your fork 🚀
5. Create a pull request to the main repository 📥




