# 🚜 Agri-Access  
**Precision Farming Equipment Rentals for Enhanced Crop Management Using KNN Algorithm**

Agri-Access is a smart agriculture rental platform built to connect farmers with vendors offering agricultural machinery on rent. Using KNN-based intelligent search, the platform helps small and marginal farmers find and book affordable equipment quickly and efficiently.

---

## 🌟 Features

- 🔑 Role-based login system (Admin, Vendor, Farmer)
- 🧠 KNN + Fuzzy Matching for smart equipment search
- 🗓️ Real-time equipment availability and booking system
- 💳 Secure payment system with SMS notifications
- ⭐ Reviews & Ratings for equipment and vendors
- 📊 Admin analytics dashboard
- 📱 Mobile-friendly responsive design

---

## ⚙️ Technologies Used

### Backend
- Python 3.7.4
- Flask 1.1.1
- MySQL 5.x
- MySQL Connector (Python)

### Frontend
- HTML5, CSS3, Bootstrap 4/5
- JavaScript

### Tools
- Visual Studio Code / PyCharm
- MySQL Workbench
- Postman

### AI & Search
- K-Nearest Neighbors (KNN)
- Fuzzy String Matching (fuzzywuzzy)
- Pandas, NumPy, Scikit-learn

---

## 🖥️ Installation Guide (Step-by-Step)

### 📌 Prerequisites
- Python 3.7.4 installed
- MySQL Server installed and running
- `pip` (Python package installer)
- WAMP/XAMPP (for local server simulation)

---

### 🚀 Step 1: Clone the Repository

```bash
git clone https://github.com/jeevitha28-g/agri-rental.git
cd agri-rental
```

### 🚀 Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate      # For Windows
# OR
source venv/bin/activate   # For Linux/Mac
```

### 🚀 Step 3: Install Required Python Packages

```bash
pip install -r requirements.txt
```

If requirements.txt is not available, install manually:

```bash
pip install flask mysql-connector-python scikit-learn pandas numpy matplotlib fuzzywuzzy python-Levenshtein
```

### 🚀 Step 4: Set Up MySQL Database

1. Open MySQL Workbench or phpMyAdmin.
   
2. Create a database:
   
   ```bash
   CREATE DATABASE agri_rental;
   ```
3. Import the SQL schema (if you have one), or run provided table creation scripts.

### 🚀 Step 5: Update Database Connection (if needed)

In app.py, find this section:
```bash
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="agri_rental"
)
```
🔁 Modify user, passwd, and database as per your local MySQL setup.

### 🚀 Step 6: Run the Application

```bash
python main.py
```

### 🚀 Step 7: Start the WAMP Server

1. Start WAMP Server
- Open the WAMP control panel.
- Wait until the WAMP icon in the taskbar turns green (this means Apache and MySQL are running).

2. Ensure MySQL Is Active
- Open phpMyAdmin via WAMP (usually at http://localhost/phpmyadmin) to verify MySQL is working.
- Confirm that your agri_rental database exists (or create/import it if needed).

### 🚀 Step 8: Final Step

Open your browser and go to:
```bash
http://localhost:5000
```

---

## License
This project is licensed under the MIT License - feel free to use and modify!

---

## Contact
Made with ❤️ by Jeevitha (https://github.com/jeevitha28-g)


