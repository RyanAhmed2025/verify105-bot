# Complete Bot Setup & Deployment Guide

This guide will walk you through setting up your Telegram bot in Replit, testing it, and deploying it to run continuously on Render.

---

## PART 1: SETUP IN REPLIT (Testing)

### Step 1: Install Dependencies
The dependencies are already installed, but if you ever need to reinstall them:

1. Click on the **Shell** tab in Replit (bottom right)
2. Run this command:
   ```bash
   pip install python-telegram-bot==22.5
   ```

### Step 2: Set Up Your Bot Token (Replit Secrets)

Instead of putting your token directly in the code, we'll use Replit Secrets:

1. On the left sidebar in Replit, click the **lock icon (🔒 Secrets)**
2. Click **"+ New Secret"**
3. Add these secrets one by one:

   **Secret 1:**
   - Key: `BOT_TOKEN`
   - Value: `8490557956:AAHX5O3MLHUOvaFY2EflNBdi0JTLkHEYJps`

   **Secret 2:**
   - Key: `TARGET_GROUP_ID`
   - Value: `1003391351685`

   **Secret 3 (Optional):**
   - Key: `VERIFICATION_KEYWORD`
   - Value: `105`

   **Secret 4 (Optional):**
   - Key: `VERIFICATION_TIMEOUT`
   - Value: `60`

4. Click **Save** for each secret

### Step 3: Test the Bot in Replit

1. Click the green **"Run"** button at the top of Replit
2. You should see in the console:
   ```
   Starting Telegram Verification Bot...
   Verification keyword: 105
   Timeout: 60 seconds
   Bot is running! Press Ctrl+C to stop.
   ```

3. **To test the bot:**
   - Open Telegram on your phone or computer
   - Find your bot by searching for its username
   - Send `/start` to the bot (you should get a welcome message)
   - Go to your group and add a test member
   - The bot should automatically ask them for the registration number

⚠️ **Important:** The bot will only work while Replit is open. To keep it running 24/7, continue to Part 2.

---

## PART 2: DEPLOY TO RENDER (24/7 Continuous Running)

Render is a free platform that will keep your bot running continuously, even when you close Replit.

### Step 1: Prepare Your Code for Render

Your code is already prepared! We've created a `requirements.txt` file that Render needs.

### Step 2: Push Code to GitHub

1. **Create a GitHub account** if you don't have one: https://github.com
2. **Create a new repository:**
   - Go to https://github.com/new
   - Name it: `telegram-verification-bot`
   - Keep it **Private** (to protect your code)
   - Click **"Create repository"**

3. **Connect Replit to GitHub:**
   - In Replit, click on the **Version Control** icon (looks like a branch)
   - Click **"Create a Git Repo"**
   - Click **"Connect to GitHub"**
   - Authorize Replit to access your GitHub
   - Push your code to the repository you just created

### Step 3: Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up using your **GitHub account** (this makes deployment easier)
4. Authorize Render to access your GitHub

### Step 4: Create a New Service on Render

1. From your Render dashboard, click **"New +"** button
2. Select **"Background Worker"** (NOT Web Service)
   - Background Workers are perfect for bots that don't serve web pages
   - They run continuously without needing a web server

### Step 5: Configure the Service

Fill in the form with these exact settings:

1. **Name:** `telegram-verification-bot` (or any name you like)

2. **Region:** Select the one closest to you (e.g., Oregon, Frankfurt, Singapore)

3. **Repository:** Select your `telegram-verification-bot` repository

4. **Branch:** `main` (or `master`)

5. **Runtime:** `Python 3`

6. **Build Command:**
   ```
   pip install -r requirements.txt
   ```

7. **Start Command:**
   ```
   python main.py
   ```

8. **Instance Type:** Select **"Free"**
   - This gives you 750 hours/month free (that's 24/7 for one bot)

### Step 6: Add Environment Variables (Secrets)

Scroll down to the **"Environment Variables"** section:

Click **"Add Environment Variable"** and add these one by one:

1. **BOT_TOKEN**
   - Key: `BOT_TOKEN`
   - Value: `8490557956:AAHX5O3MLHUOvaFY2EflNBdi0JTLkHEYJps`

2. **TARGET_GROUP_ID**
   - Key: `TARGET_GROUP_ID`
   - Value: `1003391351685`

3. **VERIFICATION_KEYWORD** (Optional, defaults to "105")
   - Key: `VERIFICATION_KEYWORD`
   - Value: `105`

4. **VERIFICATION_TIMEOUT** (Optional, defaults to 60)
   - Key: `VERIFICATION_TIMEOUT`
   - Value: `60`

### Step 7: Deploy!

1. Click **"Create Background Worker"** at the bottom
2. Render will now:
   - Download your code from GitHub
   - Install dependencies
   - Start your bot

3. **Watch the deployment:**
   - You'll see the logs in real-time
   - Look for: "Bot is running! Press Ctrl+C to stop."
   - If you see this, your bot is live! 🎉

### Step 8: Verify It's Working

1. Go to your Telegram group
2. Have someone join (or leave and rejoin yourself)
3. The bot should immediately ask for the registration number
4. Type a message with "105" in it
5. You should get the welcome message!

---

## PART 3: MONITORING & TROUBLESHOOTING

### How to Check Logs

If your bot stops responding:

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your `telegram-verification-bot` service
3. Click on the **"Logs"** tab
4. Look for any error messages (they'll be in red)

Common issues:
- **"Invalid token"**: Check that BOT_TOKEN is correct
- **"Chat not found"**: Check that TARGET_GROUP_ID is correct and includes the minus sign if it's negative
- **Bot doesn't kick users**: Make sure the bot is an admin in your group

### How to Restart the Bot

If the bot stops working:

1. Go to your Render dashboard
2. Click on your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**
4. Or click the **"Restart"** button

### How to Check Bot Status

- **In Render:** The status should show as "Live" with a green dot
- **In Telegram:** Send `/start` to your bot - if it replies, it's working

---

## PART 4: MODIFYING SETTINGS LATER

### To Change the Verification Keyword (e.g., from "105" to "106"):

**Option 1: Using Environment Variables (Recommended)**
1. Go to Render dashboard
2. Click your service
3. Go to **"Environment"** tab
4. Find `VERIFICATION_KEYWORD`
5. Change it to `106`
6. Click **"Save Changes"**
7. The bot will automatically restart with the new keyword

**Option 2: Editing the Code**
1. In Replit, change line 15:
   ```python
   VERIFICATION_KEYWORD = os.getenv("VERIFICATION_KEYWORD", "106")
   ```
2. Push to GitHub using Version Control
3. Render will automatically redeploy

### To Change the Group ID (Use Bot in Different Group):

**Option 1: Using Environment Variables**
1. Get the new group ID following the instructions in README.md
2. Go to Render → Environment tab
3. Update `TARGET_GROUP_ID` with the new group ID
4. Save changes

**Option 2: Create a New Bot for Another Group**
1. Create a new bot with @BotFather
2. In Render, create a new Background Worker
3. Use the same repository
4. Add different environment variables:
   - `BOT_TOKEN`: (new bot token)
   - `TARGET_GROUP_ID`: (new group ID)

### To Change the Timeout (e.g., from 60 to 120 seconds):

1. Go to Render → Environment tab
2. Find `VERIFICATION_TIMEOUT`
3. Change it to `120`
4. Save changes

---

## PART 5: COST & FREE TIER LIMITS

### Render Free Tier:
- **750 hours/month** of runtime (enough for one bot 24/7)
- **100 GB bandwidth/month**
- If you need multiple bots, you'll need to upgrade or use multiple accounts

### Alternative: Replit Deployments

If you prefer to deploy directly from Replit instead of using Render:

1. Replit offers deployments that can keep your bot running 24/7
2. Click the **"Deploy"** button in Replit
3. Choose **"Reserved VM"** deployment type (designed for bots)
4. Follow the prompts to set up
5. This costs money on Replit, but it's simpler to manage

---

## SUMMARY CHECKLIST

- [ ] Bot token and secrets added to Replit
- [ ] Bot tested in Replit and responds to `/start`
- [ ] Bot tested in group with new member
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Background Worker created on Render
- [ ] Environment variables added on Render
- [ ] Bot deployed and logs show "Bot is running"
- [ ] Tested in Telegram group - bot welcomes verified users
- [ ] Bot kicks unverified users after 60 seconds

---

## GETTING HELP

If something doesn't work:

1. Check the Render logs for error messages
2. Verify the bot is an admin in your Telegram group
3. Make sure all environment variables are set correctly
4. Test if the bot responds to `/start` in a direct message
5. Check that your bot token hasn't expired

Your bot is now ready to run 24/7! 🎉
