# Quick Instructions - Telegram Private Verification Bot

## ✅ WHAT'S CHANGED

Your bot now uses a **private verification system**:

1. New member joins → Gets welcome message with **"✅ Verify Now"** button
2. Clicks button → Opens private chat with bot
3. Sends registration number with "105" → Gets verified
4. Verified users are saved → No need to verify again!

All messages use **monospace formatting** (professional look).

---

## 📦 1. INSTALL DEPENDENCIES

### In Replit Console (Shell):

```bash
pip install python-telegram-bot==22.5
```

**Already installed!** ✅ But run this if you ever need to reinstall.

### What Gets Installed:
- `python-telegram-bot` version 22.5 (latest stable)
- All required dependencies (httpx, anyio, etc.)

---

## 🧪 2. TEST IF BOT IS WORKING

### Test 1: Check if Bot Responds

1. Open Telegram
2. Find your bot (search for username from @BotFather)
3. Send: `/start`
4. **Expected:** Bot replies with welcome message ✅

### Test 2: Test in Group (Full Flow)

**Setup:**
1. Add bot to your Telegram group
2. Make bot an **admin** with these permissions:
   - ✅ Delete Messages
   - ✅ Ban Users

**Testing:**
1. Leave the group and rejoin (or have a friend join)

2. **You should see:**
   ```
   👋 Welcome, YourName
   📜 To complete your registration for the Barasat College Helpdesk Central:
   ⏳ You have 5 minutes to verify your registration.
   🔐 Tap the button below to open the verification panel.
   
   [✅ Verify Now] ← Click this button
   ```

3. Click **"✅ Verify Now"** button
   - Opens private chat with bot

4. **Bot sends in private chat:**
   ```
   🏷️ Verification Panel
   Please enter your Barasat College Registration Number.
   Include the code '105' within it.
   Example: barasat1050001
   ```

5. Send any message containing "105"
   - Examples: `barasat1050001`, `105`, `my registration 105abc`

6. **Bot replies:**
   ```
   ✅ Verification successful!
   You are now approved to stay in the Helpdesk Central.
   ```

7. **Group also shows:**
   ```
   ✅ YourName has been verified successfully.
   ```

8. **Done!** You're verified and can stay in the group.

### Test 3: Test Timeout

1. Have someone join the group
2. Don't click the verify button (or don't send correct code)
3. **After 5 minutes:**
   - User gets kicked automatically
   - Receives: "❌ Verification failed or timed out. You may rejoin and try again."

### Test 4: Test Verified User

1. Leave the group
2. Rejoin
3. **You should see:**
   ```
   ✅ Welcome back, YourName! You are already verified.
   ```
   No need to verify again! ✅

---

## 🌐 3. DEPLOY TO RENDER (24/7 CONTINUOUS)

### Why Render Instead of Keeping Replit Open?

| Replit | Render |
|--------|--------|
| Only runs when tab is open | Runs 24/7 automatically |
| Stops when you close browser | Never stops (always running) |
| Good for testing | Good for production |
| Free | Also free! (750 hours/month) |

### Step-by-Step Render Deployment:

#### A. Choose Service Type

**Type to Choose:** **Background Worker**

⚠️ **IMPORTANT:** 
- ✅ Choose **"Background Worker"**
- ❌ NOT "Web Service"
- ❌ NOT "Static Site"
- ❌ NOT "Cron Job"

**Why Background Worker?**
- It runs continuously (like keeping a program running 24/7)
- Perfect for bots that need to be always online
- No web server needed

#### B. Build Command

**What to enter:**
```
pip install -r requirements.txt
```

**What this does:**
- Installs `python-telegram-bot` version 22.5
- Installs all required dependencies
- Runs automatically before starting your bot

#### C. Start Command

**What to enter:**
```
python main.py
```

**What this does:**
- Starts your bot
- Runs continuously until you stop it
- Automatically restarts if it crashes

#### D. Add Environment Variables (Secrets)

Click **"Add Environment Variable"** for each:

**Required Variables:**

1. **BOT_TOKEN**
   - Key: `BOT_TOKEN`
   - Value: Your bot token from @BotFather
   - Example: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

**Optional Variables:**

2. **TARGET_GROUP_ID**
   - Key: `TARGET_GROUP_ID`
   - Value: Your group ID (with minus sign if negative)
   - Example: `-1001234567890`
   - Leave blank to work in any group

3. **VERIFICATION_KEYWORD**
   - Key: `VERIFICATION_KEYWORD`
   - Value: `105` (or any other code)
   - Default: `105` if not set

4. **VERIFICATION_TIMEOUT**
   - Key: `VERIFICATION_TIMEOUT`
   - Value: `300` (seconds)
   - Default: 300 (5 minutes) if not set
   - To change: 10 minutes = 600, 15 minutes = 900

#### E. Deploy & Monitor

1. Click **"Create Background Worker"**
2. Wait 2-3 minutes
3. **Check logs** for:
   ```
   Starting Telegram Verification Bot...
   Verification keyword: 105
   Timeout: 300 seconds (5 minutes)
   Bot is running! Press Ctrl+C to stop.
   Bot username: @YourBotUsername
   ```

4. If you see that, your bot is **LIVE!** ✅

#### F. Check Logs If Bot Stops

**Where to find logs:**
1. Render dashboard
2. Click your service name
3. Click **"Logs"** tab

**What to look for:**
- ✅ Green text = good
- ❌ Red text = errors
- Common errors:
  - "Invalid token" → Check BOT_TOKEN
  - "Chat not found" → Check TARGET_GROUP_ID
  - "Conflict" → Bot running in multiple places (stop one)

---

## 🔄 4. MODIFY SETTINGS LATER

### Change Verification Keyword (from "105" to something else)

**Example: Change to "106"**

**Method 1: In Render (Recommended - No code change needed)**
1. Render dashboard → Your service
2. Click **"Environment"** tab
3. Find `VERIFICATION_KEYWORD`
4. Change value to `106`
5. Click **"Save Changes"**
6. Bot restarts automatically ✅

**Method 2: In Code**
1. Edit `main.py` line 18
2. Change default value: `VERIFY_KEYWORD = os.getenv("VERIFICATION_KEYWORD", "106")`
3. Push to GitHub
4. Render auto-deploys

### Change Group ID (Use in Different Group)

**Method 1: Update Environment Variable**
1. Get new group ID (see README.md for instructions)
2. Render → Environment tab
3. Update `TARGET_GROUP_ID`
4. Save

**Method 2: Multiple Groups = Multiple Bots**

To run the same bot in multiple groups:

**Option A: Remove Group Restriction**
- Delete `TARGET_GROUP_ID` from environment variables
- Bot works in ALL groups it's added to

**Option B: Create Separate Bot Instance**
1. Create new bot with @BotFather
2. Create new Background Worker in Render
3. Use same code repository
4. Different environment variables:
   - Different `BOT_TOKEN` (new bot token)
   - Different `TARGET_GROUP_ID` (new group ID)

**Result:** Two bots running independently!

### Change Timeout Period

**Example: Change from 5 minutes to 10 minutes**

1. Render → Environment tab
2. Find `VERIFICATION_TIMEOUT`
3. Change value to `600` (10 minutes in seconds)
4. Save

**Time conversions:**
- 3 minutes = 180 seconds
- 5 minutes = 300 seconds ← Current
- 10 minutes = 600 seconds
- 15 minutes = 900 seconds
- 30 minutes = 1800 seconds

### View or Clear Verified Users

**View verified users:**
```bash
cat verified_users.txt
```

**Clear all verified users (everyone must verify again):**
1. Stop the bot
2. Delete `verified_users.txt`
3. Restart bot
4. File recreates automatically

---

## 📋 COMPLETE DEPLOYMENT CHECKLIST

### Before Deploying:

- [ ] Installed `python-telegram-bot==22.5`
- [ ] Got bot token from @BotFather
- [ ] Got group ID (if restricting to one group)
- [ ] Added bot to Telegram group
- [ ] Made bot an admin with Ban Users + Delete Messages permissions
- [ ] Tested in Replit - bot responds to `/start`
- [ ] Tested verification flow works

### During Deployment:

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Created Render account
- [ ] Created **Background Worker** (not Web Service!)
- [ ] Set Build Command: `pip install -r requirements.txt`
- [ ] Set Start Command: `python main.py`
- [ ] Added `BOT_TOKEN` environment variable
- [ ] Added other optional environment variables
- [ ] Clicked "Create Background Worker"

### After Deployment:

- [ ] Checked logs show "Bot is running!"
- [ ] Tested `/start` command in private chat
- [ ] Tested new member join flow in group
- [ ] Tested verification in private chat works
- [ ] Tested timeout kicks unverified users
- [ ] Tested verified users can rejoin without verifying again

### All Green? 🎉 Your Bot is Live!

---

## 🆘 TROUBLESHOOTING

### Bot doesn't respond to `/start`
- **Check:** BOT_TOKEN is correct in environment variables
- **Test:** Copy token from @BotFather and paste in Render

### "Verify Now" button doesn't appear
- **Check:** Bot is admin in the group
- **Check:** Bot has "Delete Messages" permission

### Bot doesn't kick unverified users
- **Check:** Bot has "Ban Users" permission
- **Check:** VERIFICATION_TIMEOUT is set (default 300)

### Button opens bot but nothing happens
- **Check:** Send `/start verify105` manually in private chat
- **Check:** Bot logs for errors

### "Conflict: terminated by other getUpdates request"
- **Cause:** Bot running in multiple places
- **Fix:** Stop bot in Replit or close duplicate Render services

### Messages not in monospace format
- **Normal:** If MarkdownV2 fails, bot falls back to plain text
- **Fix:** Not needed, bot works either way

### Want to reset everything
1. Stop bot
2. Delete `verified_users.txt`
3. Restart bot
4. All users must verify again

---

## 💡 QUICK TIPS

1. **Save verified users:** The bot saves verified user IDs in `verified_users.txt` so they don't need to verify again
2. **Clean group chat:** Verification happens in private chat, keeping the group clean
3. **Professional look:** All messages use monospace formatting
4. **Flexible keyword:** Change verification keyword anytime in environment variables
5. **Multiple groups:** Deploy multiple instances with different BOT_TOKENs for different groups

---

## 📁 FILES IN YOUR PROJECT

- `main.py` - The bot code ⭐
- `requirements.txt` - Dependencies for deployment
- `verified_users.txt` - Stores verified user IDs (auto-created)
- `SETUP_GUIDE.md` - Detailed setup instructions
- `INSTRUCTIONS.md` - This file (quick reference)
- `README.md` - Project overview

---

## ✨ SUMMARY

**Your bot now:**
- ✅ Sends welcome message with inline button
- ✅ Verifies users in private chat (clean group)
- ✅ Uses monospace formatting (professional)
- ✅ Saves verified users (no repeat verification)
- ✅ Kicks unverified users after timeout
- ✅ Easy to customize (environment variables)
- ✅ Ready for 24/7 deployment on Render

**Deploy to Render using:**
- Service Type: **Background Worker**
- Build: `pip install -r requirements.txt`
- Start: `python main.py`
- Add environment variables for BOT_TOKEN, etc.

**You're ready to go! 🚀**
