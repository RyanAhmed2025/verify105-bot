# Quick Start Guide - Telegram Verification Bot

## ✅ YOUR BOT IS RUNNING IN REPLIT!

Your bot is currently active and will work as long as this Replit tab stays open.

---

## 📋 STEP-BY-STEP INSTRUCTIONS

### PART 1: TESTING YOUR BOT (5 minutes)

#### Step 1: Test the Bot Directly
1. Open Telegram on your phone or computer
2. Search for your bot (use the username @BotFather gave you)
3. Send the command: `/start`
4. You should get a welcome message back ✅

#### Step 2: Test in Your Group
1. Make sure your bot is added to your Telegram group
2. Make the bot an **admin** in the group:
   - Go to Group Settings → Administrators
   - Add your bot as admin
   - Enable "Delete Messages" and "Ban Users" permissions
3. Have someone leave and rejoin the group (or add a test account)
4. The bot should immediately send: "Enter Barasat College Registration Number to join the Helpdesk Central."
5. Type any message containing "105"
6. You should see: "Verification successful! Welcome to the Helpdesk Central! 🎉"

⚠️ **Problem?** Check the Console tab in Replit for any error messages.

---

### PART 2: DEPLOY TO RENDER FOR 24/7 RUNNING (15 minutes)

Your bot only runs while Replit is open. To keep it running 24/7 for free, follow these steps:

#### Step 1: Install Dependencies (Already Done!)
The required package `python-telegram-bot==22.5` is already installed.

If you ever need to reinstall, run in the Shell:
```bash
pip install python-telegram-bot==22.5
```

#### Step 2: Push to GitHub
1. Go to https://github.com/new
2. Create a repository called `telegram-verification-bot`
3. Make it **Private**
4. In Replit, click the **Version Control** icon (branch icon on left)
5. Click "Create a Git Repo"
6. Connect to GitHub and push your code

#### Step 3: Sign Up for Render
1. Go to https://render.com
2. Click "Sign Up"
3. Use your GitHub account to sign up (makes it easier!)

#### Step 4: Create a Background Worker
1. In Render dashboard, click **"New +"**
2. Select **"Background Worker"** (this is important - NOT Web Service!)
3. Connect your `telegram-verification-bot` repository

#### Step 5: Configure the Deployment

Fill in these exact settings:

| Setting | Value |
|---------|-------|
| **Name** | `telegram-verification-bot` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |
| **Instance Type** | Free |

#### Step 6: Add Environment Variables

Click "Add Environment Variable" and add these:

1. **BOT_TOKEN**
   - Value: Your bot token from @BotFather

2. **TARGET_GROUP_ID**
   - Value: Your group ID (the number)

3. **VERIFICATION_KEYWORD** (optional)
   - Value: `105`

4. **VERIFICATION_TIMEOUT** (optional)
   - Value: `60`

#### Step 7: Deploy!
1. Click **"Create Background Worker"**
2. Wait 2-3 minutes for deployment
3. Look for "Bot is running!" in the logs
4. Test in your Telegram group! 🎉

---

### PART 3: MONITORING

#### Check if Bot is Running:
1. Render Dashboard: Should show "Live" with green dot
2. Send `/start` to your bot in Telegram - if it responds, it's working

#### View Logs:
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. You'll see all bot activity here

#### Restart the Bot:
If it stops working:
1. Go to Render dashboard
2. Click your service
3. Click "Manual Deploy" → "Deploy latest commit"

---

### PART 4: MAKING CHANGES

#### Change the Verification Keyword (e.g., from "105" to "106"):

**Method 1: In Render (No code changes needed)**
1. Render dashboard → Your service
2. Click "Environment" tab
3. Find `VERIFICATION_KEYWORD`
4. Change to `106`
5. Click "Save Changes"
6. Bot restarts automatically ✅

**Method 2: In Code**
1. Edit `main.py` line 15
2. Push to GitHub
3. Render auto-deploys

#### Use Bot in Multiple Groups:

**Option 1: Remove Group Restriction**
- Delete the `TARGET_GROUP_ID` environment variable
- Bot will work in ANY group it's added to

**Option 2: Create Second Bot Instance**
1. Create new bot with @BotFather
2. Get new group ID
3. In Render, create another Background Worker
4. Use same code, different environment variables

#### Change Timeout Period:
1. Render → Environment tab
2. Change `VERIFICATION_TIMEOUT` to `120` (for 2 minutes)
3. Save

---

## 🆘 TROUBLESHOOTING

### Bot doesn't respond to /start:
- Check BOT_TOKEN is correct
- Make sure bot isn't blocked by Telegram

### Bot doesn't ask for verification:
- Make sure bot is an admin in the group
- Check that "Delete Messages" permission is enabled

### Bot doesn't kick users:
- Bot must be admin with "Ban Users" permission

### "Chat not found" error:
- Check GROUP_ID is correct
- Make sure GROUP_ID includes minus sign if it has one (e.g., `-1001234567890`)

### Bot was working, now stopped:
- Check Render logs for errors
- Click "Restart" in Render dashboard
- Verify environment variables are still set

---

## 📝 IMPORTANT FILES

- **main.py** - The bot code
- **requirements.txt** - Dependencies for deployment
- **DEPLOYMENT_GUIDE.md** - Full detailed guide
- **README.md** - Project documentation

---

## ✨ WHAT YOUR BOT DOES

1. **New member joins** → Bot asks for "Barasat College Registration Number"
2. **User types message with "105"** → Bot welcomes them: "Verification successful! Welcome to the Helpdesk Central! 🎉"
3. **60 seconds pass without correct keyword** → Bot kicks the user and sends them a private message

---

## 💰 COST

- **Replit**: Free tier is fine for testing
- **Render Free Tier**: 
  - 750 hours/month (enough for one bot 24/7)
  - 100 GB bandwidth/month
  - Perfect for one bot!

For multiple bots, you'll need multiple Render accounts or upgrade to paid plan.

---

## 🎉 YOU'RE ALL SET!

Your bot is ready to protect your Telegram group! If you have any questions, check the detailed DEPLOYMENT_GUIDE.md or the logs in Render.
