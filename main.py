"""
Barasat College Helpdesk Verification Bot
Private verification system with working hours (6 AM - 6 PM IST)
"""

from flask import Flask, request
import threading
import asyncio
import os
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ============================================
# CONFIGURATION - Edit these values or use environment variables
# ============================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "PLACE_YOUR_TOKEN_HERE")
GROUP_ID = os.getenv("TARGET_GROUP_ID", "PLACE_YOUR_GROUP_ID_HERE")
VERIFY_KEYWORD = os.getenv("VERIFICATION_KEYWORD", "105")
VERIFY_TIMEOUT = int(os.getenv("VERIFICATION_TIMEOUT", "300"))  # 5 minutes
WORKING_HOURS = (6, 18)  # 6 AM to 6 PM IST

# Bot username (will be fetched automatically)
BOT_USERNAME = None

# File to store verified users
VERIFIED_USERS_FILE = "verified_users.txt"

# Timezone for IST
IST = pytz.timezone('Asia/Kolkata')

# ============= FLASK WEB SERVER FOR WEBHOOK DEPLOYMENT ============
app = Flask(__name__)
application_global = None  # will hold the telegram Application instance


# ============================================
# Store pending verifications in private chat
# ============================================
pending_verifications = {}


def load_verified_users():
    """Load verified user IDs from file."""
    try:
        with open(VERIFIED_USERS_FILE, 'r') as f:
            return set(int(line.strip()) for line in f if line.strip())
    except FileNotFoundError:
        return set()


def save_verified_user(user_id):
    """Save a verified user ID to file."""
    with open(VERIFIED_USERS_FILE, 'a') as f:
        f.write(f"{user_id}\n")


# Load verified users at startup
verified_users = load_verified_users()


def is_working_hours():
    """Check if current time is within working hours (6 AM - 6 PM IST)."""
    now_ist = datetime.now(IST)
    current_hour = now_ist.hour
    return WORKING_HOURS[0] <= current_hour < WORKING_HOURS[1]


def escape_markdown_v2(text):
    """Escape special characters for MarkdownV2."""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle new members joining the group.
    During working hours: Send verification message.
    Outside working hours: Immediately kick them.
    """
    # Get the new member(s) from the update
    new_members = update.message.new_chat_members
    chat_id = update.message.chat_id
    
    for new_member in new_members:
        # Skip if the new member is a bot
        if new_member.is_bot:
            continue
        
        user_id = new_member.id
        username = new_member.username or new_member.first_name
        
        # Check if it's outside working hours - kick immediately
        if not is_working_hours():
            try:
                # Remove user from the group immediately
                await context.bot.ban_chat_member(chat_id, user_id)
                # Unban so they can rejoin during working hours
                await context.bot.unban_chat_member(chat_id, user_id)
                
                # Send message to group
                outside_hours_msg = (
                    f"🕕 `{escape_markdown_v2(username)}, the Helpdesk operates from 6 AM to 6 PM IST\\.`\n"
                    f"`Please join during college hours for verification\\.`"
                )
                try:
                    await update.message.reply_text(outside_hours_msg, parse_mode=ParseMode.MARKDOWN_V2)
                except Exception:
                    await update.message.reply_text(
                        f"🕕 {username}, the Helpdesk operates from 6 AM to 6 PM IST.\n"
                        f"Please join during college hours for verification."
                    )
                
                # Try to send DM to user
                try:
                    dm_msg = (
                        f"🕕 `Hello {escape_markdown_v2(username)}\\!`\n"
                        f"`The Barasat College Helpdesk operates from 6 AM to 6 PM IST\\.`\n"
                        f"`Please rejoin the group during working hours to verify\\.`"
                    )
                    await context.bot.send_message(chat_id=user_id, text=dm_msg, parse_mode=ParseMode.MARKDOWN_V2)
                except Exception:
                    try:
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=f"🕕 Hello {username}!\n"
                                 f"The Barasat College Helpdesk operates from 6 AM to 6 PM IST.\n"
                                 f"Please rejoin the group during working hours to verify."
                        )
                    except Exception:
                        pass
            except Exception as e:
                print(f"Error kicking user {user_id} outside working hours: {e}")
            continue
        
        # Check if user is already verified
        if user_id in verified_users:
            await update.message.reply_text(
                f"`✅ Welcome back, {escape_markdown_v2(username)}\\! You are already verified\\.`",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            continue
        
        # Create inline keyboard with verification button
        keyboard = [[
            InlineKeyboardButton(
                "✅ Verify Now",
                url=f"https://t.me/{BOT_USERNAME}?start=verify{VERIFY_KEYWORD}"
            )
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send welcome message with button in the group
        welcome_text = (
            f"👋 `Welcome, {escape_markdown_v2(username)}`\n"
            f"📜 `Please complete your registration for Barasat College Helpdesk Central\\.`\n"
            f"⏳ `Verification Timeout: 5 minutes`\n"
            f"🔐 `Tap below to verify in private\\.`"
        )
        
        try:
            await update.message.reply_text(
                welcome_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup
            )
        except Exception:
            # Fallback without markdown if formatting fails
            await update.message.reply_text(
                f"👋 Welcome, {username}\n"
                f"📜 Please complete your registration for Barasat College Helpdesk Central.\n"
                f"⏳ Verification Timeout: 5 minutes\n"
                f"🔐 Tap below to verify in private.",
                reply_markup=reply_markup
            )
        
        # Create a task to kick the user after timeout
        task = asyncio.create_task(
            kick_user_after_timeout(context, chat_id, user_id, username, VERIFY_TIMEOUT)
        )
        
        # Store the pending verification
        pending_verifications[user_id] = {
            'username': username,
            'group_id': chat_id,
            'task': task
        }


async def kick_user_after_timeout(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: int, username: str, timeout: int):
    """
    Wait for the specified timeout, then kick the user if they haven't verified.
    """
    await asyncio.sleep(timeout)
    
    # Check if user is still pending (hasn't been verified)
    if user_id in pending_verifications:
        try:
            # Remove user from the group
            await context.bot.ban_chat_member(chat_id, user_id)
            # Unban immediately so they can rejoin later
            await context.bot.unban_chat_member(chat_id, user_id)
            
            # Send private message to the user
            try:
                kicked_text = f"❌ `{escape_markdown_v2(username)} K I C K E D _O U T`"
                await context.bot.send_message(
                    chat_id=user_id,
                    text=kicked_text,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            except Exception:
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"❌ {username} K I C K E D _O U T"
                    )
                except Exception:
                    pass
            
            # Announce in group
            try:
                group_kicked = f"❌ `{escape_markdown_v2(username)} K I C K E D _O U T`"
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=group_kicked,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            except Exception:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"❌ {username} K I C K E D _O U T"
                )
            
            # Remove from pending verifications
            del pending_verifications[user_id]
            
        except Exception as e:
            print(f"Error kicking user {user_id}: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command.
    If the command contains 'verify105', show the verification panel.
    """
    # Check working hours
    if not is_working_hours():
        await update.message.reply_text(
            "🕕 `The Helpdesk operates from 6 AM to 6 PM IST\\.`\n"
            "`Please return during college hours for verification\\.`",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return
    
    user_id = update.message.from_user.id
    username = update.message.from_user.username or update.message.from_user.first_name
    
    # Check if this is a verification request
    if context.args and context.args[0].startswith('verify'):
        # Check if user is already verified
        if user_id in verified_users:
            success_text = f"`✅ {escape_markdown_v2(username)} V E R I F I E D`"
            try:
                await update.message.reply_text(success_text, parse_mode=ParseMode.MARKDOWN_V2)
            except Exception:
                await update.message.reply_text(f"✅ {username} V E R I F I E D")
            return
        
        # Show verification panel with proper formatting
        verification_text = (
            f"💬 `{escape_markdown_v2(username)},`\n"
            f"👉🏼 `Enter your`\n"
            f"```\nBarasat College Registration\n```"
            f"`To join —`\n"
            f"```\nThe Helpdesk Central.\n```"
            f"`Example :`\n"
            f"```\n1050231025000133\n```"
            f"`[ Verification Timeout in 5 mins ]`"
        )
        
        try:
            await update.message.reply_text(
                verification_text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as e:
            # Fallback to simpler formatting
            await update.message.reply_text(
                f"💬 {username},\n"
                f"👉🏼 Enter your\n"
                f"Barasat College Registration\n"
                f"To join —\n"
                f"The Helpdesk Central.\n"
                f"Example :\n"
                f"1050231025000133\n"
                f"[ Verification Timeout in 5 mins ]"
            )
        
        # Check if user is in pending verifications (joined a group)
        if user_id not in pending_verifications:
            # User clicked verify but hasn't joined the group yet
            pending_verifications[user_id] = {
                'username': username,
                'group_id': None,
                'task': None
            }
    else:
        # Regular start command
        await update.message.reply_text(
            "Hello! I'm the Barasat College Helpdesk verification bot.\n"
            "Add me to your group and make me an admin to start verifying new members."
        )


async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle messages in private chat.
    Check if the message is from a pending verification user and contains the keyword.
    """
    # Check working hours
    if not is_working_hours():
        await update.message.reply_text(
            "🕕 `The Helpdesk operates from 6 AM to 6 PM IST\\.`\n"
            "`Please return during college hours for verification\\.`",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return
    
    # Only process messages from private chats
    if update.message.chat.type != 'private':
        return
    
    user_id = update.message.from_user.id
    username = update.message.from_user.username or update.message.from_user.first_name
    
    # Check if this user is pending verification
    if user_id not in pending_verifications:
        return
    
    # Check if the message contains the verification keyword
    message_text = update.message.text or ""
    
    if VERIFY_KEYWORD in message_text:
        # Verification successful!
        verification_data = pending_verifications[user_id]
        
        # Cancel the timeout task if it exists
        if verification_data['task']:
            verification_data['task'].cancel()
        
        # Add to verified users
        verified_users.add(user_id)
        save_verified_user(user_id)
        
        # Remove from pending verifications
        del pending_verifications[user_id]
        
        # Send success message to user
        success_text = f"✅ `{escape_markdown_v2(username)} V E R I F I E D`"
        
        try:
            await update.message.reply_text(success_text, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception:
            await update.message.reply_text(f"✅ {username} V E R I F I E D")
        
        # Announce in the group if group_id is known
        if verification_data['group_id']:
            try:
                group_message = f"✅ `{escape_markdown_v2(username)} V E R I F I E D`"
                await context.bot.send_message(
                    chat_id=verification_data['group_id'],
                    text=group_message,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            except Exception:
                try:
                    await context.bot.send_message(
                        chat_id=verification_data['group_id'],
                        text=f"✅ {username} V E R I F I E D"
                    )
                except Exception as e:
                    print(f"Could not send verification message to group: {e}")
    else:
        # Wrong keyword - give them a hint
        hint_text = (
            f"`❌ Registration number must contain '{VERIFY_KEYWORD}'\\.`\n"
            f"`Please try again\\.`"
        )
        try:
            await update.message.reply_text(hint_text, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception:
            await update.message.reply_text(
                f"❌ Registration number must contain '{VERIFY_KEYWORD}'.\n"
                f"Please try again."
            )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    print(f"Exception while handling an update: {context.error}")


async def post_init(application: Application):
    """Get bot username after initialization."""
    global BOT_USERNAME
    bot = await application.bot.get_me()
    BOT_USERNAME = bot.username
    print(f"Bot username: @{BOT_USERNAME}")
    
@app.post("/webhook")
def webhook_handler():
    if application_global is None:
        return "App not ready", 503

    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, application_global.bot)
    application_global.update_queue.put_nowait(update)
    return "OK", 200
    
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    print(f"Flask server running on port {port}")
    app.run(host="0.0.0.0", port=port)

def main():
    """
    Main function to start the bot.
    """
    # Check if configuration is set
    if BOT_TOKEN == "PLACE_YOUR_TOKEN_HERE":
        print("ERROR: Please set your BOT_TOKEN!")
        print("Either:")
        print("  1. Add BOT_TOKEN to Replit Secrets (lock icon on left sidebar)")
        print("  2. Or edit line 16 in main.py")
        print("\nGet your bot token from @BotFather on Telegram")
        return
    
    if GROUP_ID == "PLACE_YOUR_GROUP_ID_HERE":
        print("WARNING: TARGET_GROUP_ID is not set.")
        print("The bot will work in any group, but you should set it for security.")
    
    print("Starting Barasat College Helpdesk Verification Bot...")
    print(f"Verification keyword: {VERIFY_KEYWORD}")
    print(f"Timeout: {VERIFY_TIMEOUT} seconds ({VERIFY_TIMEOUT // 60} minutes)")
    print(f"Working hours: {WORKING_HOURS[0]} AM to {WORKING_HOURS[1]} PM IST")
    print(f"Verified users loaded: {len(verified_users)}")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, handle_private_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    print("Bot is running! Press Ctrl+C to stop.")
    print("Operating hours: 6 AM to 6 PM IST")
    
    # Start the bot
    global application_global
    application_global = application

    if os.getenv("USE_WEBHOOK", "false").lower() == "true":
        # -------- RUNNING ON CLOUD HOST THAT REQUIRES PORT --------
        webhook_url = os.getenv("WEBHOOK_URL")
        if not webhook_url:
            raise ValueError("WEBHOOK_URL not set in environment!")

        print("Setting webhook to:", webhook_url + "/webhook")
        application.bot.set_webhook(webhook_url + "/webhook")

        # Start Flask in another thread
        threading.Thread(target=run_flask).start()

        print("Bot running via webhook mode.")
        application.run_async()
        asyncio.get_event_loop().run_forever()

    else:
        # -------- LOCAL DEVELOPMENT --------
        print("Running bot locally using polling…")
        application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
