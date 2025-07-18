# 📚 GATE Study Tracker Dashboard

[![Render App](https://img.shields.io/badge/Render-Live%20App-3f7cff?logo=render&logoColor=white)](https://study-tracker-2zhd.onrender.com/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-ff4b4b?logo=streamlit)](https://study-tracker-2zhd.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-purple.svg)](https://github.com/your-repo-url/issues)
[![Last Commit](https://img.shields.io/github/last-commit/MohitGupta0123/Study_Tracker?color=purple)](https://github.com/MohitGupta0123/Study_Tracker/commits/main/)
[![Issues](https://img.shields.io/github/issues/MohitGupta0123/Study_Tracker)](https://github.com/MohitGupta0123/Study_Tracker/issues)


<!-- [![Visitors](https://visitor-badge.laobi.icu/badge?page_id=MohitGupta0123.Study_Tracker)](https://github.com/MohitGupta0123/Study_Tracker) -->
<!-- [![Forks](https://img.shields.io/github/forks/MohitGupta0123/Study_Tracker?style=social)](https://github.com/MohitGupta0123/Study_Tracker/fork)
[![Stars](https://img.shields.io/github/stars/MohitGupta0123/Study_Tracker?style=social)](https://github.com/MohitGupta0123/Study_Tracker/stargazers) -->





---

A beautiful and personalized 📈 **Study Progress Dashboard** built using **Streamlit** with secure authentication. Designed for students preparing for GATE or any exam — to track daily goals, visualize subject-wise progress, and maintain consistency using real data, session-wise scheduling, and performance metrics.

---

## 🚀 Live Demo

👉 **[Click here to try the app!](https://study-tracker-2zhd.onrender.com/)**

---

## 🖼️ Screenshot

> _Insert a screenshot here when hosted or from GitHub image upload_

---

## 🔑 Features

- 🔐 **Login & Registration** using SQLite (`users.db`) with `streamlit_authenticator`
- 📅 **Auto-Traced Study Sessions** with date-driven scheduling
- ✅ **Checkbox Grid** to mark each session as done
- 📊 **Subject-Wise Progress** with donut & bar charts
- ⏳ **Backlog Tracker** for missed subjects
- 🔁 **Auto-Rerun Logic** before session starts
- 🧠 **Per-user JSON Save State** for progress
- 🧾 **Daily Completion Table** with tick marks
- 📌 **Reset Button** to start over anytime

---

## 🗂️ Directory Structure

```

📁 gate-study-tracker/

    ├── gate\_study\_tracker\_final.py          # Streamlit main app

    ├── auth\_db.py                           # SQLite-based authentication

    ├── users.db                             # Registered users stored here

    ├── \*.json                               # User progress files (per user)

    ├── credentials.yaml                     # (Optional) legacy credentials

    ├── Study\_Plan\_Schedule.csv              # Timetable (days × session slots)

    ├── Subject\_Study\_Time\_Table.csv         # Subjects with video hours

    ├── requirements.txt                     # Python dependencies

    └── README.md                            # You're reading it 🙂

```

---

## 🛠️ Installation

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/MohitGupta0123/Study_Tracker.git
cd Study_Tracker
````

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App

```bash
streamlit run gate_study_tracker_final.py --server.port 8501
```

---

## 🧠 Tech Stack

* **Frontend:** Streamlit
* **Auth:** `streamlit_authenticator` + SQLite (`users.db`)
* **Charts:** Matplotlib
* **Data Processing:** Pandas, JSON
* **Storage:** CSV files for study data, JSON for user progress

---

## 📁 Data Files

| File                           | Description                       |
| ------------------------------ | --------------------------------- |
| `Study_Plan_Schedule.csv`      | Weekly plan (Day-wise × Sessions) |
| `Subject_Study_Time_Table.csv` | Subjects with total video hours   |
| `<username>_progress.json`     | Per-user saved checkbox state     |

---

## 📈 Dashboard Features in Action

### 📅 Today's Work

* Auto-detects what you need to study today based on the real calendar

### 🔁 Auto Rerun

* Reruns app 5 mins before session start to alert you

### 🧾 Progress Tracker Grid

* Tick off what you’ve studied; persists even after reload

### 🍩 Donut Charts

* See your completion % for each subject

### 🟥 Backlogs

* Automatically shows what you've missed in previous days

### 📊 Time Slot Analytics

* Frequency of time slots used across your plan

---

## 📸 Visual Elements

* ✅ **Checkbox table** for sessions per day
* 📊 **Bar chart** for session frequency
* 🟡 **Today's plan**
* 🔴 **Backlogs**
* 📅 **Dynamic live clock**
* 📈 **Donut & pie charts** showing progress distribution

---

## 🔐 Authentication System

* Uses SQLite-based DB (`users.db`) for login/signup
* Passwords are hashed using `streamlit_authenticator`
* Each user has their own progress file (`<username>_progress.json`)

---

## 🙌 Acknowledgements

* Thanks to `streamlit_authenticator` for easy auth integration
* Inspired by real preparation needs of students
* Created with 💙 using Python and Streamlit

---

## 👤 Author

* **Mohit Gupta**

  🔗 [LinkedIn](https://www.linkedin.com/in/mohitgupta012/)

  📧 [Email](mailto:mgmohit1111@gmail.com)

---

## 🌟 Support

If this helped you stay productive and consistent, please ⭐️ this repo and share it with your peers!

---

```
```
