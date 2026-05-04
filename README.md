# 🐱 Pawlytics

**AI-Driven Cat Nutrition & Health Tracking System**

Pawlytics empowers cat owners to make data-driven nutrition decisions using AI-powered label scanning, comprehensive health tracking, and intelligent analytics. 

---

## Key Features

### AI Kibble & Wetfood Scanner
- **Smart Label Recognition** - Upload kibble package photos for instant analysis
- **95%+ Accuracy** - Google Gemini AI extracts nutrition data automatically
- **Guaranteed Analysis** - Auto-detects protein, fat, fiber, moisture, and ash
- **AAFCO Grading** - Automatic A-F quality scoring based on nutritional standards
- **Database Storage** - Save and compare unlimited products

### Smart Dashboard
- **Real-Time Analytics** - Nutrition quality distribution and brand comparisons
- **Visual Insights** - Interactive pie charts and bar graphs
- **Health Alerts** - Automatic warnings for overweight cats
- **Multi-User Support** - Individual profiles plus guest mode for exploration

###  Cat Profile Management
- **Unlimited Cats** - Track health metrics for multiple pets
- **Smart Calculations** - Automatic RER/DER calorie recommendations
- **BCS Scoring** - Body Condition Score tracking (1-9 scale)
- **Activity-Based** - Portions adjusted for sedentary to very active cats
- **Health Monitoring** - Age, weight, and condition tracking over time

### Advanced Analytics
- **Value Analysis** - Cost vs protein scatter plots to find best deals
- **Brand Rankings** - Sortable comparisons with quality metrics
- **Carb Tracking** - NFE (carbohydrate) analysis with threshold warnings
- **Data Export** - Download complete nutrition database to Excel
- **Custom Insights** - Filter and sort by any nutritional parameter

### AI Nutrition Consultant
- **Gemini-Powered** - Real-time chat for nutrition questions
- **Evidence-Based** - Recommendations backed by feline nutrition science
- **Chat History** - Review past conversations and advice
- **Personalized** - Answers tailored to your cats' specific needs

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (copy template and add your keys)
cp .env.example .env

# Run the application
streamlit run Welcome.py
```

**For detailed setup instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

---

## Tech Stack

**Frontend**: Streamlit - Rapid Python-based UI development 
**Database**: MariaDB 11.0 - Relational data storage with connection pooling 
**AI/ML**: Google Gemini 2.0 Flash - Vision API for label scanning, text generation for chat 
**Visualization**: Plotly - Interactive charts and graphs 
**Data Processing**: Pandas, NumPy - Analytics calculations and data manipulation 
**Image Processing**: Pillow (PIL) - Image handling for label uploads 

---

## Database Schema (MariaDB)

Pawlytics uses **MariaDB 11.0** with a normalized schema for efficient data management:

### Core Tables

#### 1. cats
Pet profiles and health tracking
- **Fields:** id, name, breed, age (years/months), weight, gender, activity level, BCS (1-9), health conditions, user info
- **Purpose:** Store cat profiles with automatic calorie calculations (RER/DER)
- **Key Features:** Body condition scoring, activity-based recommendations

#### 2. kibbles
Nutrition database for cat food products
- **Fields:** id, brand name, product name, protein %, fat %, fiber %, moisture %, ash %, NFE %, rating (A-F), price per kg, user info
- **Purpose:** Store nutrition data from AI scans and manual entries
- **Key Features:** AAFCO-based grading, price tracking for value analysis

#### 3. feeding_logs
Meal tracking history
- **Fields:** id, cat_id (FK), kibble_id (FK), amount (grams), calories consumed, fed at timestamp, notes, user_id
- **Purpose:** Track daily feeding with portion and calorie logging
- **Key Features:** Foreign keys to cats & kibbles, automatic calorie calculations

#### 4. health_alerts
Automated health warnings
- **Fields:** id, cat_id (FK), alert type, severity (low/medium/high), message, created at
- **Purpose:** Generate alerts for overweight cats and nutrition concerns
- **Key Features:** Cascade delete with cat profiles

#### 5. scan_history
AI label scan audit trail
- **Fields:** id, user_id, user name, brand name, product name, nutrition percentages, rating, scanned at
- **Purpose:** Track all AI scans for usage analytics
- **Key Features:** Complete scan metadata with timestamps

#### 6. chat_history
AI conversation logs
- **Fields:** id, user_id, user name, user message, AI response, created at
- **Purpose:** Store chat interactions with Gemini AI
- **Key Features:** Full conversation history per user

#### 7. nutrition_standards
AAFCO reference data
- **Fields:** id, nutrient name, min %, max %, category (adult/kitten), source
- **Purpose:** Validate nutrition against official AAFCO standards
- **Key Features:** Reference table for grading algorithm

### Analytical Views

#### v_cat_health
Real-time health dashboard combining cat profiles, feeding logs, and alerts

#### v_dashboard_stats
Aggregate statistics for user overview (total cats, scans, avg quality)

#### v_feeding_trends
Time-series feeding patterns and calorie consumption analysis

#### v_kibble_analytics
Advanced product comparisons with value ratings and quality distributions

## Getting Started

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **XAMPP (MariaDB)** - [Download XAMPP](https://www.apachefriends.org/)
- **Google Gemini API Key** - [Get API Key](https://ai.google.dev/)

### Installation

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Database Setup

**Via phpMyAdmin (Recommended):**

1. Start XAMPP and run **Apache** + **MySQL**
2. Open http://localhost/phpmyadmin
3. Click **"New"** → Database name: `kibble_db`
4. Click **"Import"** → Select `database/kibble_db.sql`
5. Click **"Go"**

**Via Command Line:**

```bash
# Navigate to XAMPP MySQL bin
cd C:\xampp\mysql\bin

# Import schema
mysql -u root -p kibble_db < path/to/database/kibble_db.sql
```

#### 3. Environment Configuration

```bash
# Copy template
cp .env.example .env
```

**Edit `.env` file:**

```env
# Database (XAMPP defaults)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=          # Leave empty for default XAMPP
DB_NAME=kibble_db

# Google Gemini AI
GEMINI_API_KEY=your_actual_api_key_here

# App Settings
APP_NAME=Pawlytics
DEBUG_MODE=False
LOG_LEVEL=INFO
```

#### 4. Run Application

```bash
streamlit run Welcome.py
```

**Access at:** http://localhost:8501

---

## Project Highlights

- **95%+ AI Accuracy** - Gemini-powered nutrition extraction
- **Multi-User Ready** - Guest mode + individual profiles
- **Production Ready** - Complete deployment documentation
- **Secure** - Environment-based configuration, SQL injection protection

---

## Acknowledgments

- **MariaDB Foundation** - For organizing this amazing hackathon
- **Google Gemini** - For powerful AI vision and chat capabilities
- **Streamlit Community** - For the fantastic Python framework
- **Cat Lovers Worldwide** - For inspiring this project

---

## Support

**Having trouble setting up?**

- Check the detailed [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [Open an Issue](https://github.com/MariaDB-Hackathon-MY-2026/pawlytics-cat-health-tracker/issues)

---

<div align="center">

**Made with ❤️ for cats and their humans**

🐾 **Pawlytics** - Because every cat deserves optimal nutrition 🐾

⭐ Star this repo if you found it helpful!

</div>
