# 🤖 Telegram Bot for Auto Account Creation

Automated Telegram bot that creates player accounts on https://agents.ichancy.com/dashboard with Cloudflare bypass support.

## ✨ Features

- 📱 Simple Telegram command interface: `/create <mobile> <username> <password>`
- 🔐 Automatic login to dashboard with credential management
- 🛡️ Cloudflare protection bypass using Selenium
- 📧 Auto-generated email addresses
- 🔄 Robust error handling and retry logic
- 📊 Real-time status updates in Telegram
- 🚀 Asynchronous operation for better performance

## 🔧 Requirements

- Python 3.8 or higher
- Chrome/Chromium browser (automatically managed by webdriver-manager)
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Dashboard login credentials

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aliafifa221-cloud/Telegram-Bot-for-Auto-Account-Creation.git
   cd Telegram-Bot-for-Auto-Account-Creation
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   DASHBOARD_USERNAME=your_dashboard_username
   DASHBOARD_PASSWORD=your_dashboard_password
   DASHBOARD_URL=https://agents.ichancy.com/dashboard
   PARENT_VALUE=2565525-quick-ad1@ichancy.nsp
   HEADLESS=true
   TIMEOUT=30
   ```

## 🚀 Usage

### Starting the Bot

**Standard:**
```bash
python bot.py
```

**Docker:**
```bash
docker-compose up -d
```

**Linux Service:**
```bash
sudo systemctl start telegram-bot
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment options.

### Telegram Commands

1. **Start the bot:**
   ```
   /start
   ```
   Shows welcome message and usage instructions.

2. **Get help:**
   ```
   /help
   ```
   Displays detailed command information.

3. **Create an account:**
   ```
   /create 791234567 username123 pass123
   ```
   
   Parameters:
   - `mobile`: Phone number (digits only, minimum 7 digits)
   - `username`: Desired username (minimum 3 characters)
   - `password`: Account password (minimum 6 characters)

### Example Workflow

1. Send command:
   ```
   /create 791234567 testuser pass123456
   ```

2. Bot responds with:
   ```
   ⏳ Creating account...
   Mobile: 791234567
   Username: testuser
   Please wait...
   ```

3. After processing (usually 20-40 seconds), you'll receive:
   ```
   ✅ Account created successfully!
   
   Mobile: 791234567
   Username: testuser
   Email: testuser_20231215120530_ab3d@temp.mail
   Password: pass123456
   Parent: 2565525-quick-ad1@ichancy.nsp
   
   Time: 2023-12-15 12:05:42
   ```

## 🔍 How It Works

1. **Command Reception**: Bot receives `/create` command with parameters
2. **Validation**: Validates mobile, username, and password format
3. **Browser Automation**:
   - Launches Chrome with anti-detection settings
   - Navigates to dashboard login page
   - Handles Cloudflare protection
   - Logs in with provided credentials
   - Navigates to player creation page
   - Fills form with provided and auto-generated data
   - Submits the form
4. **Response**: Sends success or failure message to Telegram

## 🛡️ Cloudflare Bypass

The bot implements several techniques to bypass Cloudflare protection:

- Anti-detection browser options
- User agent spoofing
- CDP commands to hide automation
- Intelligent wait mechanism for Cloudflare challenges
- Realistic human-like delays

## 📝 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Required |
| `DASHBOARD_USERNAME` | Dashboard login username | Required |
| `DASHBOARD_PASSWORD` | Dashboard login password | Required |
| `DASHBOARD_URL` | Dashboard URL | `https://agents.ichancy.com/dashboard` |
| `PARENT_VALUE` | Fixed parent value | `2565525-quick-ad1@ichancy.nsp` |
| `HEADLESS` | Run browser in headless mode | `true` |
| `TIMEOUT` | Default timeout in seconds | `30` |

## 🐛 Troubleshooting

### Bot doesn't start
- Check if `TELEGRAM_BOT_TOKEN` is correctly set in `.env`
- Verify internet connection
- Check logs for error messages

### Login fails
- Verify `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD` in `.env`
- Check if dashboard is accessible
- Try with `HEADLESS=false` to see what's happening

### Cloudflare blocking
- Increase `TIMEOUT` value
- Try running with `HEADLESS=false`
- Check if IP is blocked by the website

### Form submission fails
- Website structure may have changed
- Check logs for specific error messages
- Update selectors in `automation.py` if needed

## 📊 Logging

The bot logs all operations to console with timestamps:
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Failed operations

To increase verbosity, modify the logging level in `bot.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your bot token and credentials secure
- Use environment variables for sensitive data
- The `.gitignore` file is configured to exclude `.env` automatically

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is provided as-is for educational and automation purposes.

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions to common issues
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide

## 📧 Support

For issues, questions, or suggestions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first
2. Open an issue on GitHub
3. Provide detailed logs and error messages
4. Include steps to reproduce the problem

## ⚠️ Disclaimer

This bot is intended for legitimate automation purposes. Ensure you have proper authorization to automate account creation on the target website. Misuse of this tool may violate the website's terms of service.
