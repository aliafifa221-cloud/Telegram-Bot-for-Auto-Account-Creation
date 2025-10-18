# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Bot Won't Start

#### Error: "TELEGRAM_BOT_TOKEN not found"
**Solution:**
```bash
# Make sure .env file exists
cp .env.example .env

# Edit .env and add your token
nano .env
```

Make sure your `.env` looks like:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```
No quotes, no spaces around `=`.

#### Error: "Module 'telegram' not found"
**Solution:**
```bash
pip install -r requirements.txt
```

If you still get errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### 2. Login Issues

#### "Failed to login to dashboard"
**Possible causes and solutions:**

1. **Wrong credentials**
   - Double-check `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD` in `.env`
   - Try logging in manually in a browser
   - Make sure there are no extra spaces

2. **Website structure changed**
   - Run with `HEADLESS=false` in `.env` to see what's happening
   - Check logs for specific errors
   - May need to update selectors in `automation.py`

3. **Cloudflare blocking**
   - Increase `TIMEOUT` to 60 in `.env`
   - Try different browser engine: `BROWSER_ENGINE=playwright`
   - Website may have detected automation

---

### 3. Cloudflare Issues

#### "Cloudflare wait timeout"
**Solution:**
```env
# In .env, increase timeout
TIMEOUT=60

# Try Playwright instead of Selenium
BROWSER_ENGINE=playwright

# Run in visible mode to see what's happening
HEADLESS=false
```

#### Persistent Cloudflare blocking
**Possible solutions:**
1. Use a VPN
2. Use residential proxy (not implemented yet)
3. Try from different IP address
4. Contact website administrator for bot access

---

### 4. Form Submission Issues

#### "Failed to navigate to player creation page"
**Solution:**
1. Check if you have permission to create players
2. Verify the URL structure hasn't changed
3. Look for navigation links in visible browser mode:
   ```env
   HEADLESS=false
   ```

#### "Failed to fill and submit form"
**Common causes:**
1. **Form fields have different names**
   - Check `/tmp/before_submit.png` screenshot
   - Update field names in `automation.py` or `automation_playwright.py`

2. **JavaScript validation preventing submission**
   - May need to add delays
   - Check browser console in visible mode

3. **CAPTCHA appeared**
   - Website may have added CAPTCHA
   - May need manual intervention or CAPTCHA solving service

---

### 5. Browser/Driver Issues

#### "Chrome driver not found" or "Chromium not found"
**Selenium:**
```bash
# Driver is auto-downloaded, but if it fails:
pip install webdriver-manager --upgrade
```

**Playwright:**
```bash
# Install browser binaries
playwright install chromium
```

#### Browser crashes or hangs
**Solution:**
```env
# Increase timeout
TIMEOUT=60

# Add more delay between operations
# (requires code modification in automation.py)
```

---

### 6. Performance Issues

#### Bot is very slow
**Solutions:**
1. Keep `HEADLESS=true` (faster)
2. Increase `TIMEOUT` if operations time out
3. Check your internet connection
4. Website might be slow - nothing we can do

#### Multiple requests failing
**Solutions:**
1. Add rate limiting (wait between requests)
2. Website might be blocking your IP
3. Check website status

---

### 7. Debugging Steps

#### Step 1: Run setup validation
```bash
python test_setup.py
```

#### Step 2: Check logs
Bot logs everything to console. Look for:
- `ERROR` messages
- `WARNING` messages
- Last successful step before failure

#### Step 3: Run in visible mode
```env
# In .env
HEADLESS=false
```
Watch what the browser does.

#### Step 4: Check screenshots
Look in `/tmp/` directory for:
- `before_submit.png` (Selenium)
- `playwright_before_submit.png` (Playwright)

#### Step 5: Test individual components
```python
# Test login only
from automation import AccountCreator
import os
from dotenv import load_dotenv

load_dotenv()
creator = AccountCreator(
    dashboard_url=os.getenv('DASHBOARD_URL'),
    dashboard_username=os.getenv('DASHBOARD_USERNAME'),
    dashboard_password=os.getenv('DASHBOARD_PASSWORD'),
    parent_value=os.getenv('PARENT_VALUE'),
    headless=False,
    timeout=30
)
creator.driver = creator._setup_driver()
creator._login()
input("Press Enter to close browser...")
creator.driver.quit()
```

---

### 8. Advanced Solutions

#### Switch between Selenium and Playwright
```env
# Try Selenium
BROWSER_ENGINE=selenium

# Or try Playwright
BROWSER_ENGINE=playwright
```

#### Update selectors
If website structure changed, you may need to:
1. Inspect website HTML
2. Find correct selectors
3. Update in `automation.py` or `automation_playwright.py`

#### Add custom delays
Edit automation files to add `time.sleep()` between operations.

---

### 9. Error Messages Reference

| Error Message | Likely Cause | Solution |
|--------------|--------------|----------|
| "Invalid command format" | Wrong number of arguments | Use: `/create mobile username password` |
| "Mobile number must contain only digits" | Non-numeric mobile | Use only digits: `791234567` |
| "Username must be at least 3 characters" | Too short | Use longer username |
| "Password must be at least 6 characters" | Too short | Use longer password |
| "Could not find username field" | Website structure changed | Update selectors |
| "TimeoutError" | Page didn't load | Increase `TIMEOUT` |

---

### 10. Getting Help

If none of these solutions work:

1. **Gather information:**
   - Error message from console
   - Screenshot from `/tmp/`
   - Your `.env` settings (hide credentials!)
   - Steps to reproduce

2. **Open GitHub issue:**
   - Go to repository
   - Click "Issues" → "New Issue"
   - Provide all gathered information

3. **Include:**
   ```bash
   # Python version
   python --version
   
   # OS information
   uname -a  # Linux/Mac
   # or
   systeminfo  # Windows
   
   # Package versions
   pip freeze
   ```

---

## Prevention Tips

1. **Regular testing:** Test bot regularly to catch website changes early
2. **Monitor logs:** Check for warnings that might indicate upcoming issues
3. **Keep updated:** Update dependencies regularly
4. **Backup credentials:** Keep credentials in a secure place
5. **Document changes:** If you modify code, document what and why

---

## Still Having Issues?

Check these resources:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Setup guide
- GitHub Issues - Search for similar problems
- Telegram Bot API docs - For bot-specific issues
- Selenium/Playwright docs - For automation issues
