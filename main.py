"""
Barasat College Helpdesk Verification Bot
Private verification system with working hours (6 AM - 6 PM IST)
"""

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

# Bot username (auto-fetched)
BOT_USERNAME = None

# File to store verified users
VERIFIED_USERS_FILE = "verified_users.txt"

# Timezone for IST
IST = pytz.timezone('Asia/Kolkata')

# Store pending verifications
pending_verifications = {}

# ============================================
# VERIFIED USERS STORAGE
# ============================================
def load_verified_users():
    try:
        with open(VERIFIED_USERS_FILE, 'r') as f:
            return set(int(line.strip()) for line in f if line.strip())
    except FileNotFoundError:
        return set()

def save_verified_user(user_id):
    with open(VERIFIED_USERS_FILE, 'a') as f:
        f.write(f"{user_id}\n")

verified_users = load_verified_users()

# ============================================
# TIME CHECK
# ============================================
def is_working_hours():
    now_ist = datetime.now(IST)
    return WORKING_HOURS[0] <= now_ist.hour < WORKING_HOURS[1]

def escape_markdown_v2(text):
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for c in special_chars:
        text = text.replace(c, f'\\{c}')
    return text


# ============================================
# HANDLERS
# ============================================
async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members
    chat_id = update.message.chat_id
    
    for new_member in new_members:
        if new_member.is_bot:
            continue
        
        user_id = new_member.id
        username = new_member.username or new_member.first_name

        # Outside working hours → auto-kick
        if not is_working_hours():
            try:
                await context.bot.ban_chat_member(chat_id, user_id)
                await context.bot.unban_chat_member(chat_id, user_id)
                await update.message.reply_text(
                    f"🕕 {username}, the Helpdesk operates 6 AM–6 PM IST.\nJoin during working hours."
                )

                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"🕕 Hello {username}! Please rejoin during 6 AM–6 PM IST for verification."
                    )
                except:
                    pass

            except Exception as e:
                print("Kick error:", e)
            continue

        # Already verified
        if user_id in verified_users:
            await update.message.reply_text(
                f"✅ `{escape_markdown_v2(username)}\\! Already verified.`",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            continue
        
        # Button
        keyboard = [[
            InlineKeyboardButton(
                "✅ Verify Now",
                url=f"https://t.me/{BOT_USERNAME}?start=verify{VERIFY_KEYWORD}"
            )
        ]]
        markup = InlineKeyboardMarkup(keyboard)

        welcome = (
            f"👋 `Welcome, {escape_markdown_v2(username)}`\n"
            f"📜 `Complete your registration.`\n"
            f"⏳ `Timeout: 5 minutes`\n"
            f"🔐 `Tap below to verify in private.`"
        )

        await update.message.reply_text(
            welcome,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=markup
        )

        # Kick timeout
        task = asyncio.create_task(kick_user_after_timeout(
            context, chat_id, user_id, username, VERIFY_TIMEOUT
        ))

        pending_verifications[user_id] = {
            'username': username,
            'group_id': chat_id,
            'task': task
        }


async def kick_user_after_timeout(context, chat_id, user_id, username, timeout):
    await asyncio.sleep(timeout)

    if user_id in pending_verifications:
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            await context.bot.unban_chat_member(chat_id, user_id)

            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"❌ {username} KICKED OUT"
                )
            except:
                pass

            await context.bot.send_message(
                chat_id=chat_id,
                text=f"❌ {username} KICKED OUT"
            )

            del pending_verifications[user_id]

        except Exception as e:
            print("Kick error:", e)


async def start_command(update, context):
    if not is_working_hours():
        await update.message.reply_text(
            "🕕 Helpdesk runs 6 AM–6 PM IST."
        )
        return

    user_id = update.message.from_user.id
    username = update.message.from_user.username or update.message.from_user.first_name

    if context.args and context.args[0].startswith("verify"):
        if user_id in verified_users:
            await update.message.reply_text(f"✅ {username} VERIFIED")
            return

        msg = (
            f"💬 {username},\n"
            f"👉🏼 Enter your\n"
            f"Barasat College Registration\n"
            f"To join —\n"
            f"The Helpdesk Central.\n"
            f"Example:\n"
            f"1050231025000133\n"
            f"[Timeout: 5 mins]"
        )

        await update.message.reply_text(msg)

        if user_id not in pending_verifications:
            pending_verifications[user_id] = {
                'username': username,
                'group_id': None,
                'task': None
            }
    else:
        await update.message.reply_text(
            "Hello! Add me to a group and make me admin to start verifying new members."
        )


async def handle_private_message(update, context):
    if not is_working_hours():
        await update.message.reply_text("🕕 Helpdesk runs 6 AM–6 PM IST.")
        return
    
    if update.message.chat.type != "private":
        return

    user_id = update.message.from_user.id
    username = update.message.from_user.username or update.message.from_user.first_name

    if user_id not in pending_verifications:
        return

    text = update.message.text or ""

    if VERIFY_KEYWORD in text:
        data = pending_verifications[user_id]

        if data['task']:
            data['task'].cancel()

        verified_users.add(user_id)
        save_verified_user(user_id)

        del pending_verifications[user_id]

        await update.message.reply_text(f"✅ {username} VERIFIED")

        if data['group_id']:
            await context.bot.send_message(
                chat_id=data['group_id'],
                text=f"✅ {username} VERIFIED"
            )
    else:
        await update.message.reply_text(f"❌ Registration must contain '{VERIFY_KEYWORD}'.")


async def error_handler(update, context):
    print("Error:", context.error)


async def post_init(app: Application):
    global BOT_USERNAME
    bot = await app.bot.get_me()
    BOT_USERNAME = bot.username
    print("Bot username:", BOT_USERNAME)


# ============================================
# MAIN (POLLING ONLY)
# ============================================
def main():
    if BOT_TOKEN == "PLACE_YOUR_TOKEN_HERE":
        print("ERROR: BOT_TOKEN missing!")
        return

    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, handle_private_message))
    application.add_error_handler(error_handler)

    print("Bot running (polling)… Working hours: 6 AM to 6 PM IST")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
