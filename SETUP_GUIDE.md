# Complete Setup Guide - Private Verification System

## 🎯 NEW VERIFICATION SYSTEM

Your bot now uses a **private verification system**:

1. **New member joins** → Bot sends welcome message with "✅ Verify Now" button
2. **User clicks button** → Opens private chat with the bot
3. **User sends registration number** → Bot checks if it contains "105"
4. **Verification complete** → User can stay in the group
5. **Verified users are saved** → They don't need to verify again

All messages use **monospace formatting** for a professional look!

---

## 📦 PART 1: INSTALLATION

### Dependencies Already Installed ✅

The bot requires:
```bash
python-telegram-bot==22.5
```

**Already installed!** But if you ever need to reinstall:
```bash
pip install python-telegram-bot==22.5
```

---

## 🔧 PART 2: CONFIGURATION

### Your Current Settings:

The bot is configured with these values (from environment variables):

- **BOT_TOKEN**: Set in Replit Secrets ✅
- **TARGET_GROUP_ID**: Set in Replit Secrets ✅
- **VERIFICATION_KEYWORD**: `105` (default)
- **VERIFICATION_TIMEOUT**: `300` seconds (5 minutes)

### To Modify Settings:

**Option 1: Using Replit Secrets (Recommended)**
1. Click the **lock icon (🔒)** on the left sidebar
2. Edit or add these secrets:
   - `BOT_TOKEN` - Your bot token from @BotFather
   - `TARGET_GROUP_ID` - Your group ID (optional)
   - `VERIFICATION_KEYWORD` - Change from "105" to something else
   - `VERIFICATION_TIMEOUT` - Change from 300 to another value

**Option 2: Edit main.py Directly**
Lines 16-19 in main.py:
```python
BOT_TOKEN = os.getenv("BOT_TOKEN", "PLACE_YOUR_TOKEN_HERE")
GROUP_ID = os.getenv("TARGET_GROUP_ID", "PLACE_YOUR_GROUP_ID_HERE")
VERIFY_KEYWORD = os.getenv("VERIFICATION_KEYWORD", "105")
VERIFY_TIMEOUT = int(os.getenv("VERIFICATION_TIMEOUT", "300"))
```

---

## 🧪 PART 3: TESTING THE BOT

### Step 1: Make Sure Bot is an Admin

1. Open your Telegram group
2. Go to **Group Settings** → **Administrators**
3. Add your bot as admin
4. Enable these permissions:
   - ✅ Delete Messages
   - ✅ Ban Users
   - ✅ Invite Users via Link

### Step 2: Test the Verification Flow

1. **Leave the group** (or have a friend join)
2. **Rejoin the group**
3. You should see a message like this:
   ```
   👋 Welcome, YourName
   📜 To complete your registration for the Barasat College Helpdesk Central:
   ⏳ You have 5 minutes to verify your registration.
   🔐 Tap the button below to open the verification panel.
   
   [✅ Verify Now] ← Button
   ```

4. **Click the "✅ Verify Now" button**
   - It will open a private chat with the bot
   
5. You should see:
   ```
   🏷️ Verification Panel
   Please enter your Barasat College Registration Number.
   Include the code '105' within it.
   Example: barasat1050001
   ```

6. **Send any message containing "105"**
   - Example: `barasat1050001` or `my reg is 105abc`

7. You should get:
   ```
   ✅ Verification successful!
   You are now approved to stay in the Helpdesk Central.
   ```

8. The group should also show:
   ```
   ✅ YourName has been verified successfully.
   ```

9. **You're verified!** If you leave and rejoin, you won't need to verify again.

### Step 3: Test the Timeout

1. Have someone join the group
2. Don't click the verify button or don't send the correct code
3. After 5 minutes, they should be automatically kicked
4. They'll receive a message: "❌ Verification failed or timed out. You may rejoin and try again."

---

## 🚀 PART 4: RUNNING IN REPLIT

### Current Status: ✅ RUNNING

Your bot is currently running in Replit! You can see the status in the Console tab.

**To stop the bot:**
- Click the Stop button in Replit

**To restart the bot:**
- Click the Run button (green play button)
- Or type in Shell: `python main.py`

**To view logs:**
- Check the Console tab for output
- Look for: "Bot is running! Press Ctrl+C to stop."

⚠️ **Important:** The bot only runs while Replit is open. For 24/7 running, continue to Part 5.

---

## 🌐 PART 5: DEPLOY TO RENDER (24/7 CONTINUOUS)

### Why Render?
- ✅ Free tier available
- ✅ Runs 24/7 even when you close Replit
- ✅ Automatic restarts if bot crashes
- ✅ Easy to manage environment variables

### Step-by-Step Deployment:

#### 1. Push Code to GitHub

**Create a GitHub Repository:**
1. Go to https://github.com/new
2. Name: `telegram-verification-bot`
3. Make it **Private** (to protect your code)
4. Click **Create repository**

**Push from Replit:**
1. Click **Version Control** icon (branch icon) on left sidebar
2. Click **"Create a Git Repo"**
3. Click **"Connect to GitHub"**
4. Authorize Replit
5. Select your repository and push

#### 2. Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. **Sign up with GitHub** (easiest option)
4. Authorize Render to access your repositories

#### 3. Create a Background Worker

1. From Render dashboard, click **"New +"**
2. Select **"Background Worker"**
   - ⚠️ **Important:** Choose "Background Worker" NOT "Web Service"
   - Background Workers are perfect for bots that don't serve web pages

3. Select your `telegram-verification-bot` repository

#### 4. Configure the Service

Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `telegram-verification-bot` |
| **Region** | Choose closest to you |
| **Branch** | `main` (or `master`) |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |
| **Instance Type** | **Free** |

#### 5. Add Environment Variables

Scroll to **"Environment Variables"** section and add:

**Required:**
1. Key: `BOT_TOKEN`
   - Value: Your bot token from @BotFather

**Optional:**
2. Key: `TARGET_GROUP_ID`
   - Value: Your group ID (e.g., `-1001234567890`)

3. Key: `VERIFICATION_KEYWORD`
   - Value: `105` (or any other keyword)

4. Key: `VERIFICATION_TIMEOUT`
   - Value: `300` (5 minutes in seconds)

#### 6. Deploy!

1. Click **"Create Background Worker"**
2. Wait 2-3 minutes while Render:
   - Downloads your code
   - Installs dependencies
   - Starts your bot

3. **Check the logs** for:
   ```
   Starting Telegram Verification Bot...
   Verification keyword: 105
   Timeout: 300 seconds (5 minutes)
   Bot is running! Press Ctrl+C to stop.
   Bot username: @YourBotUsername
   ```

4. **Test it!** Have someone join your Telegram group.

---

## 📊 PART 6: MONITORING & TROUBLESHOOTING

### Check Bot Status

**In Render:**
- Dashboard should show **"Live"** with a green dot
- If it says "Failed", check the logs

**In Telegram:**
- Send `/start` to your bot
- If it responds, it's working!

### View Logs

1. Go to Render dashboard
2. Click your service name
3. Click **"Logs"** tab
4. Look for errors (shown in red)

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Bot doesn't respond to /start** | Check BOT_TOKEN is correct |
| **Button doesn't appear** | Make sure bot is admin in group |
| **Bot doesn't kick users** | Enable "Ban Users" permission for bot |
| **"Chat not found" error** | GROUP_ID might be wrong (include minus sign) |
| **Conflict error** | Bot is running in multiple places - stop one instance |
| **Messages not formatted** | MarkdownV2 failed - bot falls back to plain text |

### Restart the Bot

If bot stops working:

**In Render:**
1. Go to dashboard
2. Click your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**
4. Or use the **"Restart"** button

**In Replit:**
- Just click the Run button again

---

## 🔄 PART 7: MAKING CHANGES LATER

### Change the Verification Keyword

**Example: Change from "105" to "106"**

**Method 1: Environment Variable (No code change)**
1. Render → Your service → **"Environment"** tab
2. Find `VERIFICATION_KEYWORD`
3. Change value to `106`
4. Click **"Save Changes"**
5. Bot restarts automatically ✅

**Method 2: Edit Code**
1. In Replit, edit line 18 in main.py
2. Change: `VERIFY_KEYWORD = os.getenv("VERIFICATION_KEYWORD", "106")`
3. Push to GitHub
4. Render auto-deploys

### Change Timeout Period

**Example: Change from 5 minutes to 10 minutes**

1. Render → Environment tab
2. Change `VERIFICATION_TIMEOUT` to `600` (seconds)
3. Save

Or multiply minutes × 60:
- 5 minutes = 300 seconds
- 10 minutes = 600 seconds
- 15 minutes = 900 seconds

### Use Bot in Multiple Groups

**Option 1: Remove Group Restriction**
- Delete `TARGET_GROUP_ID` environment variable
- Bot works in ANY group it's added to

**Option 2: Deploy Multiple Instances**
1. Create a second bot with @BotFather
2. Create another Background Worker in Render
3. Use same code repository
4. Different environment variables:
   - Different `BOT_TOKEN`
   - Different `TARGET_GROUP_ID`

### Reset Verified Users

The bot stores verified users in `verified_users.txt`.

**To clear all verified users:**
1. Stop the bot
2. Delete or empty `verified_users.txt`
3. Restart the bot
4. Everyone will need to verify again

---

## 💾 PART 8: VERIFIED USERS MANAGEMENT

### How It Works

- When a user verifies, their ID is saved to `verified_users.txt`
- If they leave and rejoin, they see: "✅ Welcome back! You are already verified."
- No need to verify again!

### File Location

- **In Replit:** `verified_users.txt` in the root folder
- **In Render:** Created automatically when first user verifies

### View Verified Users

**In Replit:**
```bash
cat verified_users.txt
```

Each line is a user ID:
```
123456789
987654321
555555555
```

---

## ✨ PART 9: CUSTOMIZATION IDEAS

### Change Welcome Message

Edit the `handle_new_member` function (around line 88):
```python
welcome_text = (
    f"`👋 Welcome, {escape_markdown_v2(first_name)}`\n"
    f"`📜 Custom message here:`\n"
    f"`⏳ You have 5 minutes to verify\\.`\n"
    f"`🔐 Tap the button below\\.`"
)
```

### Change Verification Panel Message

Edit the `start_command` function (around line 195):
```python
verification_text = (
    "`🏷️ Custom Panel Title`\n"
    "`Your custom instructions here\\.`\n"
    ...
)
```

### Change Success Message

Edit the `handle_private_message` function (around line 255):
```python
success_text = (
    "`✅ Custom success message\\!`\n"
    "`Welcome to our community\\.`"
)
```

---

## 📋 DEPLOYMENT CHECKLIST

Before going live, make sure:

- [ ] Bot token added to Replit Secrets or Render environment variables
- [ ] Bot is admin in your Telegram group
- [ ] Bot has "Ban Users" and "Delete Messages" permissions
- [ ] Tested verification flow works (join → click button → verify)
- [ ] Tested timeout kicks users after 5 minutes
- [ ] Tested that verified users can rejoin without verifying again
- [ ] Code pushed to GitHub
- [ ] Render Background Worker created and running
- [ ] Logs show "Bot is running!" and bot username

---

## 💰 COSTS

### Replit
- Free tier is sufficient for development and testing

### Render Free Tier
- **750 hours/month** (enough for one bot 24/7)
- **100 GB bandwidth/month**
- Perfect for one bot instance!

For multiple bots:
- Use multiple free Render accounts, OR
- Upgrade to Render paid plan ($7/month per service)

---

## 🆘 GETTING HELP

### If Bot Doesn't Work:

1. **Check Render logs** for error messages
2. **Verify bot is admin** in Telegram group
3. **Test /start command** in private chat
4. **Check environment variables** are set correctly
5. **Try restarting** the bot in Render

### If Verification Doesn't Work:

1. **Click the button** - make sure it opens private chat
2. **Send message with "105"** - check spelling/numbers
3. **Check timeout** - verify within 5 minutes
4. **Look at logs** for any errors

---

## 🎉 YOU'RE ALL SET!

Your new private verification system is ready! Users will:
1. See a professional welcome message with a button
2. Click to verify in private (keeps the group chat clean)
3. Send their registration number
4. Get verified and stay in the group
5. Never need to verify again (saved in verified_users.txt)

All messages are formatted in monospace for a clean, professional look! 

For detailed technical documentation, see the code comments in `main.py`.
