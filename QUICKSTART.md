# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 2: Configure Bot (2 minutes)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

**Required configuration:**
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz  # Get from @BotFather
DASHBOARD_USERNAME=your_actual_username
DASHBOARD_PASSWORD=your_actual_password
```

### Step 3: Verify Setup (30 seconds)

```bash
python test_setup.py
```

Expected output:
```
✅ All checks passed! You can start the bot with:
   python bot.py
```

### Step 4: Start the Bot (30 seconds)

```bash
python bot.py
```

You should see:
```
Bot is running... Press Ctrl+C to stop.
```

### Step 5: Test It! 🎉

1. Open Telegram
2. Search for your bot (username from BotFather)
3. Send: `/start`
4. Send: `/create 791234567 testuser pass123`

---

## Getting Your Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow the prompts:
   - Choose a name (e.g., "My Account Creator")
   - Choose a username (must end in 'bot', e.g., "myaccountcreator_bot")
4. Copy the token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Paste it in your `.env` file

---

## Common Issues

### "TELEGRAM_BOT_TOKEN not found"
- Make sure you created the `.env` file (copy from `.env.example`)
- Make sure the token doesn't have quotes around it
- Make sure there are no spaces before or after the `=`

### "Failed to login to dashboard"
- Verify your username and password in `.env`
- Try visiting the dashboard URL in a browser manually
- Check if you need VPN or special access

### "Chrome driver not found"
- The first run downloads Chrome driver automatically
- If it fails, ensure you have Chrome installed
- Try running with `HEADLESS=false` to see what happens

---

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check the logs if something goes wrong
- Adjust `TIMEOUT` in `.env` if operations are slow

---

## Support

If you encounter issues:
1. Run `python test_setup.py` to diagnose problems
2. Check the console logs for error messages
3. Try with `HEADLESS=false` in `.env` to watch the browser
4. Open an issue on GitHub with logs and error messages
