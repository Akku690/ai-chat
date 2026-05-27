# 🔑 Step-by-Step Guide: Getting All Required API Keys & Credentials

This guide explains each key in your `.env` file and exactly how to obtain or generate them.

---

## 📋 Table of Contents
1. [SECRET_KEY](#1-secret_key) - Application security key
2. [DB_USER & DB_PASSWORD](#2-db_user--db_password) - Database credentials
3. [REDIS_PASSWORD](#3-redis_password) - Cache password
4. [OPENAI_API_KEY](#4-openai_api_key) - AI integration key (Optional)

---

## 1. SECRET_KEY

### What is it?
A cryptographic key used by FastAPI to sign JWT tokens and secure sessions. Must be **random** and **unique**.

### Current Value in `.env`
```env
SECRET_KEY=FGPl3djEmtZVIstatX_6AetI-M6nr3ayMEC9Z1jKpzE
```

### ✅ Already Generated
You don't need to do anything! This was auto-generated when the project was created.

### 🔄 How to Regenerate (if needed)

#### Option 1: Windows PowerShell (Simple)
```powershell
# Run this command in PowerShell
[System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
```

#### Option 2: Python (Recommended)
```powershell
# Run in PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Option 3: Online Tool (Browser)
1. Go to: https://randomkeygen.com/
2. Look for "Fort Knox Passwords" section
3. Copy any one of the 64-character passwords
4. Paste into `.env` as `SECRET_KEY=<paste-here>`

### ⚠️ Important
- **Change this before deploying to production**
- Current dev key is fine for testing
- Each new deployment should have a different key
- **Never** commit SECRET_KEY to Git (add to .gitignore)

### How to Update in `.env`
```bash
# Edit .env
notepad .env

# Find this line:
SECRET_KEY=FGPl3djEmtZVIstatX_6AetI-M6nr3ayMEC9Z1jKpzE

# Replace with new value:
SECRET_KEY=<your-new-64-char-string>

# Save and close
```

---

## 2. DB_USER & DB_PASSWORD

### What are they?
Credentials to log into PostgreSQL database. Can be any username and password you choose.

### Current Values in `.env`
```env
DB_USER=chatuser
DB_PASSWORD=chatpass
```

### ✅ Already Set
These are safe for development. They work out of the box.

### 🔄 How to Change (Optional)

#### Step 1: Generate Strong Password
```powershell
# Use this in PowerShell to generate secure password
python -c "import secrets; print(secrets.token_urlsafe(16))"

# Example output: "rK7x_jPq2m9wL3vZ_8B"
```

#### Step 2: Update `.env`
```bash
# Edit .env
notepad .env

# Change these lines:
DB_USER=chatuser          # Change to any username (no spaces)
DB_PASSWORD=chatpass      # Change to generated password above

# Example:
DB_USER=admin
DB_PASSWORD=rK7x_jPq2m9wL3vZ_8B

# Save
```

#### Step 3: Update docker-compose.yml
```bash
# Edit docker-compose.yml
notepad docker-compose.yml

# Find this section and update it:
services:
  db:
    environment:
      POSTGRES_USER: chatuser         # Change to match DB_USER
      POSTGRES_PASSWORD: chatpass     # Change to match DB_PASSWORD
      POSTGRES_DB: chatdb

# Save
```

#### Step 4: Restart Services
```powershell
# Stop current services
docker-compose down

# Remove old database (to apply new credentials)
docker volume rm chat-postgres-data

# Start with new credentials
docker-compose up -d
```

### ✅ Production Note
- For production: Use strong passwords (16+ characters)
- Include uppercase, lowercase, numbers, special characters
- Example: `Prod_ChAt_P@ssw0rd_2024_Secure`

### 📝 Database Connection String
```
postgresql://DB_USER:DB_PASSWORD@localhost:5432/chatdb

Example:
postgresql://admin:rK7x_jPq2m9wL3vZ_8B@localhost:5432/chatdb
```

---

## 3. REDIS_PASSWORD

### What is it?
Password to secure your Redis cache instance.

### Current Value in `.env`
```env
REDIS_PASSWORD=redispass
```

### ✅ Already Set
Works fine for development. Can stay as-is for testing.

### 🔄 How to Change (Optional)

#### Step 1: Generate Password
```powershell
python -c "import secrets; print(secrets.token_urlsafe(16))"
# Output: something like "xY2q_mK8pL5vJ9nW_3B"
```

#### Step 2: Update `.env`
```bash
notepad .env

# Change this line:
REDIS_PASSWORD=redispass
# To:
REDIS_PASSWORD=xY2q_mK8pL5vJ9nW_3B

# Save
```

#### Step 3: Update docker-compose.yml
```bash
notepad docker-compose.yml

# Find the Redis service and update:
services:
  cache:
    command: redis-server --requirepass xY2q_mK8pL5vJ9nW_3B

# Save
```

#### Step 4: Restart Services
```powershell
docker-compose down
docker-compose up -d
```

### 📝 Redis Connection String
```
redis://:REDIS_PASSWORD@localhost:6379/0

Example:
redis://:xY2q_mK8pL5vJ9nW_3B@localhost:6379/0
```

---

## 4. OPENAI_API_KEY

### What is it?
API key from OpenAI that enables ChatGPT integration in your chat application. **OPTIONAL** - app works without it (uses mock responses).

### Current Value in `.env`
```env
OPENAI_API_KEY=sk-test-key-optional-for-development
```

### ⏳ Currently: Optional Mock Responses
The app provides AI responses without a real key. They're placeholder responses.

### 🔄 To Get Real AI Responses - Follow These Steps

---

## 🚀 STEP-BY-STEP: Get OpenAI API Key

### STEP 1: Create OpenAI Account

1. **Open browser** and go to: https://platform.openai.com/signup
2. **Sign up** using:
   - Google account, OR
   - Microsoft account, OR
   - Email + password
3. **Verify email** (check email inbox)
4. **Accept terms** of service

### STEP 2: Add Billing Information

⚠️ **Required to use API** (even with free trial credits)

1. **Log in** to https://platform.openai.com
2. **Click account icon** (top-right corner)
3. **Select "Billing"** from menu
4. **Click "Add payment method"**
5. **Enter credit/debit card details**:
   - Card number
   - Expiration date
   - CVC (3-digit code)
   - Billing address
6. **Save payment method**

### STEP 3: Set Spending Limits (Recommended)

To avoid unexpected charges:

1. **In Billing section**, find **"Usage limits"**
2. **Set "Hard limit"** to: `$10` (or your budget)
3. **Set "Soft limit"** to: `$5` (notification at this amount)
4. **Save**

This prevents overspending.

### STEP 4: Create API Key

1. **Go to**: https://platform.openai.com/api/keys
2. **Click "Create new secret key"** button
3. **Choose name** (optional): `Smart-Chat-AI-Dev`
4. **Click "Create secret key"**
5. **COPY the key immediately** - it won't be shown again!

**Your key will look like**: `sk-proj-1a2b3c4d5e6f7g8h9i0j...`

### ⚠️ CRITICAL: Save the Key Somewhere Safe

**Copy the entire key** and save it temporarily in:
- Notepad (locally)
- Password manager
- But NOT in a public place

**You cannot retrieve it again** from OpenAI!

---

## 📝 STEP 5: Add to `.env` File

### Option A: Manual Update

```bash
# Open .env file
notepad .env

# Find this line:
OPENAI_API_KEY=sk-test-key-optional-for-development

# Replace with your actual key:
OPENAI_API_KEY=sk-proj-1a2b3c4d5e6f7g8h9i0j...

# Save the file (Ctrl+S)
```

### Option B: PowerShell Update

```powershell
# Copy your key first

# Then run this (replace YOUR_KEY with your actual key):
$newKey = "sk-proj-1a2b3c4d5e6f7g8h9i0j..."
(Get-Content .env) -replace 'OPENAI_API_KEY=.*', "OPENAI_API_KEY=$newKey" | Set-Content .env

# Verify it was updated:
cat .env | findstr OPENAI_API_KEY
```

---

## ✅ STEP 6: Restart Application

```powershell
# Stop current services
docker-compose down

# Start with new API key
docker-compose up -d

# Wait 15 seconds for startup
```

---

## 🧪 STEP 7: Test AI Integration

### Option 1: Web UI (Easiest)

1. **Open**: http://localhost:8000/docs
2. **Click** on `POST /auth/register`
3. **Click "Try it out"**
4. **Enter**:
   ```json
   {
     "email": "test@example.com",
     "password": "Test123!"
   }
   ```
5. **Click "Execute"**
6. **Go to** `POST /auth/login` and get token
7. **Go to** `POST /conversations/{id}/chat`
8. **Send**: `{"message": "Hello, tell me a joke"}`
9. **See AI response** (will now be from ChatGPT!)

### Option 2: PowerShell Test

```powershell
# Test AI endpoint
$response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
$response

# Expected response with real API:
# ai_service: true (instead of false)
```

---

## 💰 OpenAI Pricing Info

### Free Trial
- New accounts get **$5 free credits**
- Valid for **3 months**
- Must add billing to use

### Current Pricing (gpt-3.5-turbo)
- **Input**: $0.0005 per 1K tokens
- **Output**: $0.0015 per 1K tokens

### Example Costs
- 100 conversations × 10 messages = ~$0.20
- 1000 conversations = ~$2.00
- Typical usage costs **under $1/month**

---

## 🔐 Security Best Practices

### ✅ DO
- [x] Keep SECRET_KEY private
- [x] Use strong DB_PASSWORD (16+ chars)
- [x] Rotate OPENAI_API_KEY annually
- [x] Add `.env` to `.gitignore` (don't commit)
- [x] Use different keys for dev/staging/production

### ❌ DON'T
- [ ] Share OPENAI_API_KEY in emails/messages
- [ ] Commit `.env` to GitHub
- [ ] Use simple passwords like "password123"
- [ ] Reuse keys across multiple environments
- [ ] Post keys in public forums

### 🔄 Rotate Keys Regularly
```powershell
# Delete old key from OpenAI dashboard
# Generate new key
# Update .env
# Restart services
# Delete old key from everywhere
```

---

## 📞 Troubleshooting

### Problem: API key not working
**Solution**:
1. Verify key is correct (copy-paste again)
2. Check key is not deleted in OpenAI dashboard
3. Restart services: `docker-compose restart app`
4. Check logs: `docker-compose logs app`

### Problem: Can't add billing
**Solution**:
1. Use valid credit/debit card
2. Check card is not declined
3. Ensure billing address matches
4. Contact OpenAI support

### Problem: Rate limited
**Solution**:
1. Check usage in OpenAI dashboard
2. Upgrade to paid tier if needed
3. Implement request queuing in app

### Problem: High charges
**Solution**:
1. Check usage logs in OpenAI dashboard
2. Set spending limits (hard limit: $10)
3. Review conversation patterns
4. Optimize prompts

---

## 📊 Complete `.env` Reference

```env
# Application
DEBUG=False
SECRET_KEY=FGPl3djEmtZVIstatX_6AetI-M6nr3ayMEC9Z1jKpzE

# Database
DB_USER=chatuser
DB_PASSWORD=chatpass
DB_NAME=chatdb

# Redis Cache
REDIS_PASSWORD=redispass

# OpenAI (Optional)
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
OPENAI_MODEL=gpt-3.5-turbo
```

---

## ✅ Verification Checklist

- [ ] SECRET_KEY is set (unique 32-64 char string)
- [ ] DB_USER set (any username, no spaces)
- [ ] DB_PASSWORD set (16+ chars recommended)
- [ ] REDIS_PASSWORD set (any password)
- [ ] OPENAI_API_KEY added (from OpenAI account)
- [ ] All values in `.env` file
- [ ] Services restarted after changes
- [ ] No keys committed to Git
- [ ] `.gitignore` includes `.env`

---

## 🚀 Ready!

Once all keys are configured:

```powershell
# Restart services to apply changes
docker-compose down
docker-compose up -d

# Test health check
curl http://localhost:8000/health

# Open API docs
Start-Process http://localhost:8000/docs
```

---

## 📞 Need Help?

| Issue | Resource |
|-------|----------|
| OpenAI Account | https://platform.openai.com |
| API Documentation | https://platform.openai.com/docs |
| Pricing Calculator | https://openai.com/pricing |
| Support | https://help.openai.com |

---

## 🚀 Ready for Production?

**For production deployment**, see **PRODUCTION_KEYS_GUIDE.md** for:
- Production-specific key requirements
- Secure key generation for production
- SSL/TLS certificate setup (Let's Encrypt)
- Database backup passwords
- Deployment checklist
- Security best practices
- Key rotation schedule

**Location**: `PRODUCTION_KEYS_GUIDE.md`

---

**You now have a complete guide to get all API keys! 🎉**

Start with OpenAI if you want real AI responses, or skip it for now and use mock responses.
