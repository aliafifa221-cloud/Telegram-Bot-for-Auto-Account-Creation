#!/usr/bin/env python3
"""
Telegram Bot for Auto Account Creation
Handles /create command to automatically create accounts on ichancy.com
"""

import os
import logging
import asyncio
from typing import Optional
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

from automation import AccountCreator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Welcome to Auto Account Creation Bot!\n\n'
        'Usage: /create <mobile> <username> <password>\n'
        'Example: /create 791234567 username123 pass123\n\n'
        'The bot will automatically:\n'
        '- Login to the dashboard\n'
        '- Create a new player account\n'
        '- Send you a success/failure message'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        'Command: /create <mobile> <username> <password>\n\n'
        'Parameters:\n'
        '- mobile: Phone number (e.g., 791234567)\n'
        '- username: Desired username (e.g., username123)\n'
        '- password: Account password (e.g., pass123)\n\n'
        'Email will be auto-generated\n'
        'Parent will be set to: 2565525-quick-ad1@ichancy.nsp'
    )


async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /create command."""
    # Check if correct number of arguments
    if len(context.args) != 3:
        await update.message.reply_text(
            '❌ Invalid command format!\n\n'
            'Usage: /create <mobile> <username> <password>\n'
            'Example: /create 791234567 username123 pass123'
        )
        return

    mobile, username, password = context.args
    
    # Validate inputs
    if not mobile.isdigit():
        await update.message.reply_text('❌ Mobile number must contain only digits!')
        return
    
    if len(mobile) < 7:
        await update.message.reply_text('❌ Mobile number is too short!')
        return
    
    if len(username) < 3:
        await update.message.reply_text('❌ Username must be at least 3 characters!')
        return
    
    if len(password) < 6:
        await update.message.reply_text('❌ Password must be at least 6 characters!')
        return

    # Send initial message
    status_message = await update.message.reply_text(
        f'⏳ Creating account...\n'
        f'Mobile: {mobile}\n'
        f'Username: {username}\n'
        f'Please wait...'
    )

    try:
        # Create account creator instance
        creator = AccountCreator(
            dashboard_url=os.getenv('DASHBOARD_URL', 'https://agents.ichancy.com/dashboard'),
            dashboard_username=os.getenv('DASHBOARD_USERNAME'),
            dashboard_password=os.getenv('DASHBOARD_PASSWORD'),
            parent_value=os.getenv('PARENT_VALUE', '2565525-quick-ad1@ichancy.nsp'),
            headless=os.getenv('HEADLESS', 'true').lower() == 'true',
            timeout=int(os.getenv('TIMEOUT', '30'))
        )

        # Create the account
        result = await asyncio.to_thread(
            creator.create_account,
            mobile=mobile,
            username=username,
            password=password
        )

        if result['success']:
            await status_message.edit_text(
                f'✅ Account created successfully!\n\n'
                f'Mobile: {mobile}\n'
                f'Username: {username}\n'
                f'Email: {result.get("email", "N/A")}\n'
                f'Password: {password}\n'
                f'Parent: {result.get("parent", "N/A")}\n\n'
                f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            )
            logger.info(f'Account created successfully for user {username}')
        else:
            error_msg = result.get('error', 'Unknown error')
            await status_message.edit_text(
                f'❌ Failed to create account!\n\n'
                f'Error: {error_msg}\n'
                f'Mobile: {mobile}\n'
                f'Username: {username}\n\n'
                f'Please try again or contact support.'
            )
            logger.error(f'Failed to create account: {error_msg}')

    except Exception as e:
        error_message = str(e)
        await status_message.edit_text(
            f'❌ An error occurred!\n\n'
            f'Error: {error_message}\n\n'
            f'Please try again later or contact support.'
        )
        logger.error(f'Exception in create_account: {error_message}', exc_info=True)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    """Start the bot."""
    # Get bot token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error('TELEGRAM_BOT_TOKEN not found in environment variables!')
        print('Error: Please set TELEGRAM_BOT_TOKEN in your .env file')
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('create', create_account))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start the Bot
    logger.info('Bot started successfully!')
    print('Bot is running... Press Ctrl+C to stop.')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
