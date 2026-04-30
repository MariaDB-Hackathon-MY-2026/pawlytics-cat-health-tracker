# 🚀 Pawlytics Deployment Guide

## Prerequisites
- Python 3.11 or higher
- XAMPP (with MariaDB/MySQL)
- Google Gemini API key

---

## Step 1: Install Python Dependencies

Open Command Prompt and run:
```bash
pip install -r requirements.txt
```

---

## Step 2: Database Setup (Using XAMPP)

### 2.1 Start XAMPP Services

1. Open **XAMPP Control Panel**
2. Click **Start** on **Apache** (if you want phpMyAdmin)
3. Click **Start** on **MySQL** (MariaDB)

### 2.2 Create Database (Option A: phpMyAdmin - Easy!)

1. Open browser and go to: `http://localhost/phpmyadmin`
2. Click **"New"** in the left sidebar
3. Database name: `kibble_db`
4. Collation: `utf8mb4_general_ci`
5. Click **"Create"**

### 2.3 Import Schema

1. Click on **`kibble_db`** database in left sidebar
2. Click **"Import"** tab at the top
3. Click **"Choose File"**
4. Select: `database/kibble_db.sql` from project folder
5. Click **"Go"** at bottom
6. Wait for success message ✅

**Alternative (Command Line):**
```bash
# Navigate to XAMPP mysql bin folder
cd C:\xampp\mysql\bin

# Import schema
mysql -u root -p kibble_db < path\to\database\kibble_db.sql
```

---

## Step 3: Configure Environment Variables

### 3.1 Create .env File

1. Copy `.env.example` file
2. Rename copy to `.env`

### 3.2 Edit Configuration

Open `.env` with Notepad and update:

```env
# Database (XAMPP Default Settings)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=          #Leave empty if no password set
DB_NAME=kibble_db

# Google Gemini API
GEMINI_API_KEY=your_actual_api_key_here
```

**Get Gemini API Key:**
1. Go to: https://ai.google.dev/
2. Click **"Get API Key"**
3. Sign in with Google account
4. Click **"Create API Key"**
5. Copy key and paste into `.env`

---

## Step 4: Run Application

Open Command Prompt in project folder and run:

```bash
streamlit run Welcome.py
```

Application will open in browser at: `http://localhost:8501`

---

## Troubleshooting

### ❌ Database Connection Error

**Error:** `Can't connect to MySQL server on 'localhost'`

**Solution:**
1. Open **XAMPP Control Panel**
2. Make sure **MySQL** is running (green highlight)
3. If not, click **Start**

### ❌ Access Denied Error

**Error:** `Access denied for user 'root'@'localhost'`

**Solution:**
1. Check if XAMPP MySQL has password
2. If yes, add password to `.env` file:
```env
   DB_PASSWORD=your_xampp_mysql_password
```
3. To check/set password in phpMyAdmin:
   - Go to `http://localhost/phpmyadmin`
   - Click **"User accounts"**
   - Check root user settings

### ❌ Table Doesn't Exist

**Error:** `Table 'cats' doesn't exist`

**Solution:**
1. Database schema not imported properly
2. Go back to **Step 2.3** and import `kibble_db.sql` again

### ❌ API Key Invalid

**Error:** `Invalid API key`

**Solution:**
1. Verify Gemini API key in `.env` is correct
2. No extra spaces before/after key
3. API key starts with `AIza...`

### ❌ Module Not Found

**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install -r requirements.txt
```

---

## Default Access

**Login Options:**
1. **Enter your name** - Creates personal profile
2. **Guest Mode** - Browse features without account

**Features:**
- Dashboard - Nutrition statistics
- Cat Profiles - Manage your cats
- AI Scanner - Analyze kibble labels
- Analytics - Data insights
- AI Chat - Nutrition Q&A

---

## System Requirements

- **OS:** Windows 10/11, macOS, Linux
- **RAM:** 4GB minimum
- **Storage:** 500MB free space
- **Internet:** Required for AI features
- **Browser:** Chrome, Firefox, Edge (latest)

---

## Quick Verification Checklist

After setup, verify:
- [ ] XAMPP MySQL is running
- [ ] Database `kibble_db` exists
- [ ] All tables imported (cats, kibbles, etc.)
- [ ] `.env` file created with valid API key
- [ ] `streamlit run Welcome.py` starts without errors
- [ ] Can access app at `http://localhost:8501`

---

## Notes for Evaluators

- XAMPP used for local MariaDB/MySQL
- Default root user has no password (common XAMPP setup)
- All sensitive keys configured via `.env` file

---

## Support

For issues, please check:
- GitHub Issues: https://github.com/MariaDB-Hackathon-MY-2026/pawlytics-cat-health-tracker/issues

---