# 🎓 College AI Assistant Chatbot

A simple **Django based chatbot** that answers student questions using **college data stored in the database**.

The chatbot checks the database and returns the matching answer.

Example:

User: *What courses are offered?*
Bot: *Agra College offers BCA, BBA, BA, BSc programs.*

---

# 🚀 Features

* 📚 College information stored in database
* 💬 Chat interface for asking questions
* 🎤 Voice input (speech to text)
* 🔊 Voice reply (text to speech)
* 🧾 Chat history sidebar
* 🎨 Modern UI using TailwindCSS

---

# 🛠 Tech Stack

Backend

* Python
* Django

Frontend

* HTML
* TailwindCSS
* JavaScript

Database

* SQLite

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the project

```bash
# download project from GitHub
git clone https://github.com/yourusername/college-ai-chatbot.git

# go inside project folder
cd college-ai-chatbot
```

---

## 2️⃣ Create Virtual Environment

```bash
# create virtual environment
python -m venv .venv

# activate virtual environment (Windows)
.venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
# install required python packages
pip install -r requirements.txt
```

---

## 4️⃣ Run Database Migrations

```bash
# create database tables
python manage.py migrate
```

---

## 5️⃣ Import College Data

```bash
# this command imports all questions and answers
# from college_data.json into the database
python manage.py import_college_data
```

---

## 6️⃣ Start the Server

```bash
# run django development server
python manage.py runserver
```

Open browser:

```
http://127.0.0.1:8000
```

---

# 💬 How Chatbot Works

```
User Question
      ↓
Search Question in Database
      ↓
If Match Found → Return Stored Answer
Else → Show "No information available"
```

---

# 👨‍💻 Author

Rajkumar
BCA Student | Python & Django Developer
