# Dazai Robot

![Dazai](https://files.catbox.moe/jmw2pf.jpg)

DazaiRobot is a powerful Telegram bot designed to help you manage your Telegram groups efficiently. With DazaiRobot, you can automate various tasks, moderate discussions, and enhance the overall experience for your group members.

## Features

- **Member Management**: Add, remove, and ban members easily.
- **Role Management**: Assign roles and permissions to group members.
- **Automated Moderation**: Set up rules to automatically warn or mute members for inappropriate behavior.
- **Custom Commands**: Create custom commands tailored to your group's needs.
- **Polls and Surveys**: Create polls to engage with your group members.
- **Welcome Messages**: Send automated welcome messages to new members.
- **Statistics**: Get insights into group activity and member engagement.

## Getting Started

### Prerequisites

- A Telegram account.
- A group where you have admin privileges.
- Python 3.6 or higher.

━━━━━━━━━━━━━━━━━━━━

<p align="center">
  <img src="https://files.catbox.moe/288b2j.jpg">
</p>

<h3 align="center">
    『 ᴅᴇᴩʟᴏʏ ᴏɴ ʜᴇʀᴏᴋᴜ 』
</h3>

<p align="center"><a href="https://dashboard.heroku.com/new?template=https://github.com/TechDigitalTeam/DazaiRobot"> <img src="https://img.shields.io/badge/Deploy%20On%20Heroku-black?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>

## Installation

1. Clone the repository:

   bash
   git clone https://github.com/yourusername/DazaiRobot.git
   
2. Navigate to the project directory:

   bash
   cd DazaiRobot
   
3. Install the required dependencies:

   bash
   pip install -r requirements.txt
   
4. Set up your environment variables:

   Create a .env file in the root directory and add your credentials:

   env
   TELEGRAMBOTTOKEN=yourtelegrambot_token
   
### Usage

1. Run the bot:

   bash
   python bot.py
   
2. Add the bot to your Telegram group and grant it admin privileges.
3. Start using the bot's commands in your group.

### Commands

- /start: Start the bot and get a welcome message.
- /help: List all available commands.
- /add_member @username: Add a member to the group.
- /remove_member @username: Remove a member from the group.
- /ban @username: Ban a member from the group.
- /unban @username: Unban a previously banned member.
- /set_welcome_message <message>: Set a custom welcome message for new members.
- /create_poll <question>: Create a new poll for group members.

## Contributing

Contributions are welcome! If you'd like to contribute to DazaiRobot, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeature).
3. Make your changes and commit them (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the Telegram Bot API wrapper.

---

Feel free to reach out if you have any questions or suggestions!
