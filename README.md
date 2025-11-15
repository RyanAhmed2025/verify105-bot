# Telegram Group Verification Bot

A simple Telegram bot that automatically verifies new members joining a group by asking them to provide a specific keyword.

## Features

- Automatically prompts new members to enter a registration number
- Verifies users based on keyword "105"
- Kicks unverified users after 60 seconds
- Sends welcome message to verified users
- Sends notification to kicked users

## Setup Instructions

### 1. Get Your Bot Token

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the instructions to create your bot
4. Copy the bot token that BotFather gives you

### 2. Get Your Group ID

1. Add your bot to your Telegram group
2. Make the bot an admin (required for kicking members)
3. Send a message in the group
4. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   (Replace `<YOUR_BOT_TOKEN>` with your actual token)
5. Look for `"chat":{"id":-1001234567890}` in the response
6. Copy the ID (including the minus sign)

### 3. Configure the Bot

Open `main.py` and edit these lines:

```python
BOT_TOKEN = "PLACE_YOUR_TOKEN_HERE"  # Replace with your bot token
TARGET_GROUP_ID = "PLACE_YOUR_GROUP_ID_HERE"  # Replace with your group ID
```

### 4. Run the Bot

The bot will start automatically in Replit. You can also run it manually:

```bash
python main.py
```

## How It Works

1. When a new member joins your Telegram group, the bot sends:
   > "Enter Barasat College Registration Number to join the Helpdesk Central."

2. The new member has 60 seconds to send a message containing "105"

3. If they send the correct keyword:
   > "Verification successful! Welcome to the Helpdesk Central! 🎉"

4. If they fail or don't respond in time:
   - They are removed from the group
   - They receive a private message: "Verification failed. Please rejoin with a valid registration number."

## Requirements

- Python 3.11+
- python-telegram-bot 22.5+

## Notes

- The bot must be an admin in the group with permission to ban/kick users
- Make sure to keep your bot token secret and never share it publicly
