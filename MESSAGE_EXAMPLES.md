# Bot Message Examples - What Users Will See

This document shows exactly what messages the bot sends in different situations.

---

## 📱 SCENARIO 1: NEW MEMBER JOINS GROUP

### Message in Group Chat:

```
👋 Welcome, John
📜 To complete your registration for the Barasat College Helpdesk Central:
⏳ You have 5 minutes to verify your registration.
🔐 Tap the button below to open the verification panel.

[✅ Verify Now] ← Inline button (clickable)
```

**Notes:**
- Text appears in monospace (code-style) font
- "John" is replaced with the user's first name
- The button links to: `https://t.me/YourBotUsername?start=verify105`

---

## 💬 SCENARIO 2: USER CLICKS "VERIFY NOW" BUTTON

### Bot Opens in Private Chat:

### First Message (from /start verify105):

```
🏷️ Verification Panel
Please enter your Barasat College Registration Number.
Include the code '105' within it.
Example: barasat1050001
```

**Notes:**
- Appears in monospace font
- User needs to reply to this message
- Reply must contain "105" somewhere in the text

---

## ✅ SCENARIO 3: USER SENDS CORRECT REGISTRATION NUMBER

### User Sends (Example):
```
barasat1050001
```
or
```
My registration number is 105
```
or
```
105abc
```

### Bot Replies in Private Chat:

```
✅ Verification successful!
You are now approved to stay in the Helpdesk Central.
```

### Bot Also Sends to Group Chat:

```
✅ John has been verified successfully.
```

**Notes:**
- User is now verified and saved in `verified_users.txt`
- User can stay in the group
- If they leave and rejoin, no need to verify again

---

## ❌ SCENARIO 4: USER SENDS WRONG REGISTRATION NUMBER

### User Sends (Example):
```
barasat0001
```
(no "105" in it)

### Bot Replies in Private Chat:

```
❌ Registration number must contain '105'.
Please try again.
Example: barasat1050001
```

**Notes:**
- User can try again
- They still have time until the 5-minute timeout
- Each message is checked for "105"

---

## ⏰ SCENARIO 5: USER DOESN'T VERIFY WITHIN 5 MINUTES

### After 5 Minutes:

1. **User is kicked from the group**
2. **Bot sends to user in private chat:**

```
❌ Verification failed or timed out.
You may rejoin and try again.
```

**Notes:**
- User can rejoin the group and try again
- The timer starts when they join the group
- Clicking verify button doesn't reset the timer

---

## 🔄 SCENARIO 6: VERIFIED USER REJOINS GROUP

### User was verified before and rejoins:

### Message in Group Chat:

```
✅ Welcome back, John! You are already verified.
```

**Notes:**
- No need to verify again
- No timeout, no kick
- User can stay immediately

---

## 🤖 SCENARIO 7: USER SENDS /start WITHOUT VERIFY LINK

### User opens bot and sends `/start` directly:

### Bot Replies:

```
Hello! I'm the Helpdesk Central verification bot.
Add me to your group and make me an admin to start verifying new members.
```

**Notes:**
- This is for users who message the bot directly
- They should click the "✅ Verify Now" button from the group instead

---

## 📋 MESSAGE FORMATTING DETAILS

### Monospace Font:
All verification messages use monospace (code-style) formatting for a professional look.

**In MarkdownV2:**
```
`This text appears in monospace`
```

**How it looks in Telegram:**
```
This text appears in monospace
```

### Fallback:
If MarkdownV2 formatting fails, the bot automatically sends plain text instead:
```
✅ Verification successful!
You are now approved to stay in the Helpdesk Central.
```

---

## 🎨 CUSTOMIZATION

Want to change the messages? Edit these sections in `main.py`:

### Welcome Message (Group):
**Line ~88:**
```python
welcome_text = (
    f"`👋 Welcome, {escape_markdown_v2(first_name)}`\n"
    f"`📜 To complete your registration for the Barasat College Helpdesk Central:`\n"
    f"`⏳ You have 5 minutes to verify your registration\\.`\n"
    f"`🔐 Tap the button below to open the verification panel\\.`"
)
```

### Verification Panel (Private Chat):
**Line ~195:**
```python
verification_text = (
    "`🏷️ Verification Panel`\n"
    "`Please enter your Barasat College Registration Number\\.`\n"
    "`Include the code '105' within it\\.`\n"
    "`Example: barasat1050001`"
)
```

### Success Message (Private Chat):
**Line ~255:**
```python
success_text = (
    "`✅ Verification successful\\!`\n"
    "`You are now approved to stay in the Helpdesk Central\\.`"
)
```

### Timeout Message (Private Chat):
**Line ~149:**
```python
timeout_text = (
    "`❌ Verification failed or timed out\\.`\n"
    "`You may rejoin and try again\\.`"
)
```

### Wrong Keyword Message (Private Chat):
**Line ~285:**
```python
hint_text = (
    "`❌ Registration number must contain '105'\\.`\n"
    "`Please try again\\.`\n"
    "`Example: barasat1050001`"
)
```

### Group Verification Confirmation:
**Line ~271:**
```python
group_message = f"`✅ {escape_markdown_v2(first_name)} has been verified successfully\\.`"
```

---

## 🔤 SPECIAL CHARACTERS IN MARKDOWN

When customizing messages, escape these characters with `\\`:

```
_ * [ ] ( ) ~ > # + - = | { } . !
```

**Example:**
```python
# Wrong:
"`Welcome! You're verified.`"

# Correct:
"`Welcome\\! You're verified\\.`"
```

The `escape_markdown_v2()` function does this automatically for names.

---

## ✨ EMOJI REFERENCE

Current emojis used:
- 👋 Welcome
- 📜 Instructions
- ⏳ Timeout/Time limit
- 🔐 Security/Verification
- ✅ Success/Verified
- ❌ Failed/Error
- 🏷️ Panel/Form

Feel free to change these to match your style!

---

## 📸 VISUAL FLOW

```
┌─────────────────────────────────┐
│  New Member Joins Group         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Bot: Welcome message           │
│  with [✅ Verify Now] button    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  User Clicks Button             │
│  → Opens Private Chat           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Bot: Verification Panel        │
│  "Enter registration number"    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  User: Sends number with "105"  │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
 Contains        Doesn't
  "105"?         contain
      │             │
      │             ▼
      │      ┌──────────────────┐
      │      │  Bot: Try again  │
      │      └──────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Bot: ✅ Success! (Private)     │
│  Bot: ✅ Verified! (Group)      │
└─────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  User Saved to                  │
│  verified_users.txt             │
└─────────────────────────────────┘
```

---

## 🕐 TIMEOUT FLOW

```
User Joins Group
      │
      │ Timer starts (5 minutes)
      │
      ├─── Within 5 min + Verified ✅
      │         └─→ User stays in group
      │
      └─── After 5 min + Not verified ❌
                └─→ User kicked
                └─→ Can rejoin and try again
```

---

This gives you a complete picture of what users will see when they interact with your verification bot!
