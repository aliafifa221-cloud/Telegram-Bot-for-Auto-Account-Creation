# 🚀 Deployment Guide

This guide covers different deployment methods for the Telegram Bot.

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Linux Service (systemd)](#linux-service-systemd)
4. [Cloud Deployment](#cloud-deployment)

---

## Local Deployment

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Add your credentials

# Run
python bot.py
```

### Running in Background (Linux/Mac)
```bash
# Using nohup
nohup python bot.py > bot.log 2>&1 &

# Or using screen
screen -S telegram-bot
python bot.py
# Press Ctrl+A then D to detach
# screen -r telegram-bot to reattach
```

---

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed (optional but recommended)

### Method 1: Using Docker Compose (Recommended)

```bash
# 1. Configure environment
cp .env.example .env
nano .env  # Add your credentials

# 2. Build and run
docker-compose up -d

# 3. Check logs
docker-compose logs -f

# 4. Stop
docker-compose down
```

### Method 2: Using Docker Directly

```bash
# 1. Build image
docker build -t telegram-account-bot .

# 2. Run container
docker run -d \
  --name telegram-bot \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e DASHBOARD_USERNAME="your_username" \
  -e DASHBOARD_PASSWORD="your_password" \
  -e HEADLESS=true \
  telegram-account-bot

# 3. Check logs
docker logs -f telegram-bot

# 4. Stop
docker stop telegram-bot
docker rm telegram-bot
```

### Docker Useful Commands

```bash
# View logs
docker-compose logs -f telegram-bot

# Restart bot
docker-compose restart telegram-bot

# Rebuild after code changes
docker-compose up -d --build

# Stop and remove everything
docker-compose down -v

# Enter container for debugging
docker exec -it telegram-account-creator-bot bash
```

---

## Linux Service (systemd)

### Setup as System Service

```bash
# 1. Edit service file
cp telegram-bot.service.example telegram-bot.service
nano telegram-bot.service

# Update these lines:
# User=your_username
# WorkingDirectory=/path/to/bot
# ExecStart=/usr/bin/python3 /path/to/bot/bot.py

# 2. Install service
sudo cp telegram-bot.service /etc/systemd/system/
sudo systemctl daemon-reload

# 3. Enable service (start on boot)
sudo systemctl enable telegram-bot

# 4. Start service
sudo systemctl start telegram-bot

# 5. Check status
sudo systemctl status telegram-bot
```

### Service Management Commands

```bash
# Start
sudo systemctl start telegram-bot

# Stop
sudo systemctl stop telegram-bot

# Restart
sudo systemctl restart telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f

# Disable (don't start on boot)
sudo systemctl disable telegram-bot
```

---

## Cloud Deployment

### AWS EC2

```bash
# 1. Launch Ubuntu EC2 instance
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip git

# 4. Clone repository
git clone https://github.com/aliafifa221-cloud/Telegram-Bot-for-Auto-Account-Creation.git
cd Telegram-Bot-for-Auto-Account-Creation

# 5. Setup
pip3 install -r requirements.txt
cp .env.example .env
nano .env  # Configure

# 6. Run as service (see systemd section above)
```

### Google Cloud Platform (GCP)

```bash
# 1. Create Compute Engine VM
# 2. SSH into VM
# 3. Follow same steps as AWS EC2
```

### DigitalOcean Droplet

```bash
# 1. Create Ubuntu Droplet
# 2. SSH into Droplet
# 3. Follow same steps as AWS EC2
```

### Heroku

```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create your-bot-name

# 4. Add buildpacks
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-chromedriver

# 5. Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set DASHBOARD_USERNAME=your_username
heroku config:set DASHBOARD_PASSWORD=your_password

# 6. Create Procfile
echo "worker: python bot.py" > Procfile

# 7. Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 8. Scale worker
heroku ps:scale worker=1

# 9. View logs
heroku logs --tail
```

### Railway.app

```bash
# 1. Go to railway.app
# 2. Click "New Project" → "Deploy from GitHub repo"
# 3. Select your repository
# 4. Add environment variables in Railway dashboard
# 5. Deploy automatically happens
```

---

## Production Best Practices

### 1. Security

```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use secrets management in production
# - AWS Secrets Manager
# - Google Secret Manager
# - HashiCorp Vault
```

### 2. Monitoring

```bash
# Add logging to file
python bot.py >> bot.log 2>&1

# Use monitoring tools
# - Sentry for error tracking
# - Prometheus + Grafana for metrics
# - ELK Stack for log aggregation
```

### 3. Backups

```bash
# Backup configuration
cp .env .env.backup

# Schedule automatic backups
# Add to crontab:
0 0 * * * cp /path/to/.env /path/to/backups/.env.$(date +\%Y\%m\%d)
```

### 4. Auto-restart on Failure

**Using systemd:**
```ini
# In service file
Restart=always
RestartSec=10
```

**Using Docker:**
```yaml
# In docker-compose.yml
restart: unless-stopped
```

### 5. Resource Limits

**Docker:**
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

**Systemd:**
```ini
[Service]
MemoryLimit=2G
CPUQuota=200%
```

---

## Scaling

### Running Multiple Instances

```bash
# Using different bot tokens
docker-compose -f docker-compose.yml up -d bot1
docker-compose -f docker-compose.bot2.yml up -d bot2
```

### Load Balancing
- Use multiple bot instances with different tokens
- Distribute across multiple servers
- Use queue system for processing requests

---

## Troubleshooting Deployment

### Check if bot is running
```bash
# Local
ps aux | grep bot.py

# Docker
docker ps

# Systemd
sudo systemctl status telegram-bot
```

### View logs
```bash
# Local
tail -f bot.log

# Docker
docker logs -f telegram-bot

# Systemd
sudo journalctl -u telegram-bot -f
```

### Test connection
```python
# test_connection.py
from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    me = await bot.get_me()
    print(f"Bot connected: @{me.username}")

asyncio.run(test())
```

---

## Updates and Maintenance

### Updating the Bot

**Local:**
```bash
git pull
pip install -r requirements.txt --upgrade
# Restart bot
```

**Docker:**
```bash
git pull
docker-compose down
docker-compose up -d --build
```

**Systemd:**
```bash
git pull
pip install -r requirements.txt --upgrade
sudo systemctl restart telegram-bot
```

---

## Rollback

### Docker
```bash
# List images
docker images

# Use previous image
docker-compose down
docker tag telegram-account-bot:previous telegram-account-bot:latest
docker-compose up -d
```

### Git
```bash
# Revert to previous commit
git log --oneline
git checkout <previous-commit-hash>
# Restart bot
```

---

## Support

For deployment issues:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review logs for errors
3. Open GitHub issue with:
   - Deployment method used
   - Error logs
   - Environment details
