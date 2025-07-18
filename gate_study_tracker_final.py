from streamlit_authenticator.utilities.hasher import Hasher
# hashed = Hasher().hash_list(['newpass123'])
# print(hashed)

# ✅ Full Streamlit App with Authentication, Registration, and Study Tracker Dashboard

# import streamlit as st
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
# import pandas as pd
# import matplotlib.pyplot as plt
# import json
# import os
# from datetime import datetime

# st.set_page_config(layout="wide")

# CREDENTIALS_FILE = "credentials.yaml"

# # ---- Load or initialize YAML credentials ----
# if os.path.exists(CREDENTIALS_FILE):
#     with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as file:
#         config = yaml.load(file, Loader=SafeLoader)
# else:
#     config = {
#         "credentials": {"usernames": {}},
#         "cookie": {"name": "study_app_cookie", "key": "abcdef", "expiry_days": 30}
#     }

# # ---- Set up authenticator ----
# authenticator = stauth.Authenticate(
#     credentials=config['credentials'],
#     cookie_name=config['cookie']['name'],
#     key=config['cookie']['key'],
#     cookie_expiry_days=config['cookie']['expiry_days']
# )

# # ---- Login ----
# try:
#     authenticator.login(location='main', key='login')
# except Exception as e:
#     st.error(f"Authentication error: {e}")

# # ---- Registration Section (open to all) ----
# if st.session_state.get('authentication_status') is None:
#     with st.expander("📥 New user? Register here"):
#         with st.form("register_form"):
#             full_name = st.text_input("Full Name")
#             new_username = st.text_input("Username")
#             new_email = st.text_input("Email")
#             new_password = st.text_input("Password", type="password")
#             submit = st.form_submit_button("Register")

#         if submit:
#             if new_username in config["credentials"]["usernames"]:
#                 st.warning("⚠️ Username already exists.")
#             else:
#                 print(new_password)
#                 print(new_username)
#                 hashed_pw = Hasher().hash_list([new_password])[0]
#                 print(hashed_pw)
#                 config["credentials"]["usernames"][new_username] = {
#                     "email": new_email,
#                     "name": full_name,
#                     "password": hashed_pw
#                 }

#                 # Save to YAML
#                 with open(CREDENTIALS_FILE, 'w') as file:
#                     yaml.dump(config, file, default_flow_style=False)

#                 st.success(f"✅ Registered successfully! Please log in as `{new_username}`.")

# # ---- Authentication Flow ----
# auth_status = st.session_state.get('authentication_status')
# username = st.session_state.get('username')
# name = st.session_state.get('name')

# if auth_status is False:
#     st.error("❌ Incorrect username or password")
# elif auth_status is None:
#     st.warning("🔐 Please enter your username and password")
# elif auth_status:
#     authenticator.logout("Logout", location="main")
#     st.success(f"👋 Welcome, {name}!")


import streamlit as st
import streamlit_authenticator as stauth
from auth_db import init_db, get_all_users, user_exists, register_user
from streamlit_authenticator.utilities.hasher import Hasher
import os
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

# Initialize DB
init_db()

st.set_page_config(layout="wide")

# ---- Set up authenticator with DB users ----
credentials = {
    "credentials": get_all_users(),
    "cookie": {"name": "study_app_cookie", "key": "abcdef", "expiry_days": 30}
}

authenticator = stauth.Authenticate(
    credentials=credentials["credentials"],
    cookie_name=credentials["cookie"]["name"],
    key=credentials["cookie"]["key"],
    cookie_expiry_days=credentials["cookie"]["expiry_days"]
)

# ---- Login ----
try:
    authenticator.login(location='main', key='login')
except Exception as e:
    st.error(f"Authentication error: {e}")

# ---- Registration ----
if st.session_state.get('authentication_status') is None:
    with st.expander("📥 New user? Register here"):
        with st.form("register_form"):
            full_name = st.text_input("Full Name")
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")

        if submit:
            if user_exists(new_username):
                st.warning("⚠️ Username already exists.")
            else:
                register_user(new_username, full_name, new_email, new_password)
                st.success(f"✅ Registered successfully! Please log in as `{new_username}`.")

# ---- Authenticated Section ----
auth_status = st.session_state.get('authentication_status')
username = st.session_state.get('username')
name = st.session_state.get('name')

if auth_status is False:
    st.error("❌ Incorrect username or password")
elif auth_status is None:
    st.warning("🔐 Please enter your username and password")
elif auth_status:
    authenticator.logout("Logout", location="main")
    st.success(f"👋 Welcome, {name}!")

    # ---------- Your Dashboard Code Below ----------
    PROGRESS_FILE = f"{username}_progress.json"
    SESSION_HOURS = 2

    @st.cache_data
    def load_schedule():
        return pd.read_csv("Study_Plan_Schedule.csv")

    @st.cache_data
    def load_subject_hours():
        df = pd.read_csv("Subject_Study_Time_Table.csv")
        df.columns = df.columns.str.strip()
        return df.set_index("Subject")

    schedule_df = load_schedule()
    subject_df = load_subject_hours()
    session_cols = [col for col in schedule_df.columns if col != "Day"]
    subjects_list = subject_df.index.tolist()

    # ---- Persistent Progress State ----
    def load_progress():
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_progress(progress_dict):
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress_dict, f)

    stored_progress = load_progress()

    # Initialize session state
    if 'checkboxes' not in st.session_state:
        st.session_state.checkboxes = [[stored_progress.get(f"{i}-{j}", False)
                                        for j in range(len(session_cols))]
                                        for i in range(len(schedule_df))]

    # ---- Layout ----
    # st.title("📘 GATE Study Tracker")
    st.markdown("<h1 style='text-align: center; font-size: 52px;'> 📚 Study Tracker 📘</h1>", unsafe_allow_html=True)
    left_col, right_col = st.columns([2.3, 1.7])

    # ---- LEFT: Timetable View ----
    with left_col:
        # -------- AUTO-RERUN LOGIC: 5 MINS BEFORE SESSION STARTS --------
        now = datetime.now()

        # Define session start times
        session_times = [
            "09:00",  # 9:00 AM
            "11:15",
            "14:00",
            "16:15",
            "18:15"
        ]

        # Convert to datetime for comparison
        for time_str in session_times:
            session_start = datetime.strptime(time_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            rerun_trigger_time = session_start - pd.Timedelta(minutes=5)

            # If we are within the rerun window (±10 seconds to avoid jitter)
            if abs((now - rerun_trigger_time).total_seconds()) <= 10:
                st.rerun()
        
        # # --------- DYNAMIC CLOCK & DAILY TASKS ---------
        # st.subheader("📅 What To Do Today")

        # # Show current time
        # current_time = datetime.now().strftime("%A, %d %B %Y — %I:%M:%S %p")
        # st.markdown(f"**🕒 Current Time:** `{current_time}`")

        # # Find first uncompleted day based on checkboxes
        # today_index = None
        # for i in range(len(schedule_df)):
        #     if not all(st.session_state.checkboxes[i]):
        #         today_index = i
        #         break

        # if today_index is None:
        #     st.success("🎉 All scheduled days are completed!")
        # else:
        #     today_row = schedule_df.iloc[today_index]
        #     unchecked_subjects = []

        #     for j, session in enumerate(session_cols):
        #         subject = today_row[session]
        #         is_checked = st.session_state.checkboxes[today_index][j]
        #         if subject in subjects_list and not is_checked:
        #             unchecked_subjects.append((session, subject))

        #     st.markdown(f"### 📆 **Today: {today_row['Day']}**")
        #     if unchecked_subjects:
        #         st.markdown("### 🧠 **Subjects Remaining Today:**")
        #         for time_slot, subject in unchecked_subjects:
        #             st.markdown(f"- ⏰ **{time_slot}** → 📘 `{subject}`")
        #     else:
        #         st.success("🎉 All sessions for today are completed!")


        # --------- DYNAMIC CLOCK & DAILY TASKS (DATE DRIVEN) ---------
        st.subheader("📅 What To Do Today")

        # Set your Day 0 starting point
        START_DATE = datetime(2025, 7, 15)  # Customize as needed
        current_day_index = (datetime.now().date() - START_DATE.date()).days

        # Show real-time clock
        now = datetime.now().strftime("%A, %d %B %Y — %I:%M:%S %p")
        st.markdown(f"**🕒 Current Time:** `{now}`")

        # ---- BACKLOG TASKS ----
        backlogs = []
        for i in range(min(current_day_index, len(schedule_df))):
            for j, session in enumerate(session_cols):
                subject = schedule_df.loc[i, session]
                if subject in subjects_list and not st.session_state.checkboxes[i][j]:
                    backlogs.append((schedule_df.loc[i, 'Day'], session, subject))

        if backlogs:
            st.markdown("### 🔴 **Backlog Subjects**")
            for day_label, session, subject in backlogs:
                st.markdown(f"- ❌ `{day_label}` — ⏰ **{session}** → 📘 `{subject}`")

        # ---- TODAY'S WORK ----
        st.markdown("### 🟡 **Today's Work**")

        if 0 <= current_day_index < len(schedule_df):
            today_row = schedule_df.iloc[current_day_index]
            unchecked_today = []

            for j, session in enumerate(session_cols):
                subject = today_row[session]
                if subject in subjects_list and not st.session_state.checkboxes[current_day_index][j]:
                    unchecked_today.append((session, subject))

            st.markdown(f"**📆 Today: {today_row['Day']}**")
            if unchecked_today:
                for time_slot, subject in unchecked_today:
                    st.markdown(f"- ⏰ **{time_slot}** → 📘 `{subject}`")
            else:
                st.success("🎉 All sessions for today are completed!")
        else:
            st.warning("📅 You're beyond the scheduled plan!")

        st.header("📅 Study Tracker Grid View")
        subject_hours = {}

        # Header Row
        col_headers = st.columns([0.9] + [1]*len(session_cols))
        col_headers[0].markdown("**Day**")
        for i, session in enumerate(session_cols):
            col_headers[i+1].markdown(f"**{session}**")

        # Table Rows
        for i, row in schedule_df.iterrows():
            cols = st.columns([0.9] + [1]*len(session_cols))
            day_label = row['Day']
            all_checked = all(st.session_state.checkboxes[i])
            new_master = cols[0].checkbox(f"{day_label}", value=all_checked, key=f"master-{i}")

            if new_master != all_checked:
                for j in range(len(session_cols)):
                    st.session_state.checkboxes[i][j] = new_master
                st.toast(f"{day_label} {'selected' if new_master else 'cleared'} ✅", icon="🎯")


            for j, session in enumerate(session_cols):
                key = f"{i}-{j}"
                subject = row[session]
                current_value = st.session_state.checkboxes[i][j]
                new_value = cols[j+1].checkbox(subject, value=current_value, key=key)
                st.session_state.checkboxes[i][j] = new_value
                if new_value and subject in subjects_list:
                    subject_hours[subject] = subject_hours.get(subject, 0) + SESSION_HOURS

    # ---- Save checkbox progress ----
    progress_dict = {}
    for i in range(len(schedule_df)):
        for j in range(len(session_cols)):
            progress_dict[f"{i}-{j}"] = st.session_state.checkboxes[i][j]
    save_progress(progress_dict)

    # ---- RIGHT: Analytics ----
    with right_col:
        st.header("📊 Analysis & Insights")
        progress_data = []

        for subject, row in subject_df.iterrows():
            effective_total = row["Effective Study Hours (2x + Notes)"]
            original_total = row["Original Video Hours"]
            done_eff = subject_hours.get(subject, 0)
            done_eff = min(done_eff, effective_total)
            percent = round((done_eff / effective_total) * 100, 2) if effective_total > 0 else 0
            done_original = round((done_eff / effective_total) * original_total, 1) if effective_total > 0 else 0

            progress_data.append({
                'Subject': subject,
                'Done Hours': done_original,
                'Total Hours': original_total,
                'Percent Complete': f"{percent}%"
            })

        st.dataframe(pd.DataFrame(progress_data))

        # ---- Donut Charts ----
        st.markdown("### 🍩 Completion Charts")
        rows = [progress_data[i:i+3] for i in range(0, len(progress_data), 3)]
        for row in rows:
            chart_cols = st.columns(3)
            for i, entry in enumerate(row):
                subject = entry['Subject']
                done = float(entry['Done Hours'])
                total = float(entry['Total Hours'])
                percent = float(entry['Percent Complete'].strip('%'))
                remaining = max(total - done, 0)

                fig, ax = plt.subplots(figsize=(3, 3))
                ax.pie(
                    [done, remaining],
                    labels=["Done", "Remaining"],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=["#00c853", "#eeeeee"],
                    wedgeprops=dict(width=0.4),
                    textprops={'fontsize': 10}
                )
                ax.set(aspect="equal")
                ax.set_title(f"{subject}\n{done:.1f}h / {total:.1f}h ({percent:.1f}%)", fontsize=10)
                chart_cols[i].pyplot(fig)

        # ---- Daily Completion Table ----
        st.subheader("✅ Daily Completion Table")
        daily_data = []
        for i, row in schedule_df.iterrows():
            completed = [st.session_state.checkboxes[i][j] for j in range(len(session_cols))]
            daily_data.append({
                "Day": row['Day'],
                **{session_cols[j]: ("✔️" if completed[j] else "") for j in range(len(session_cols))}
            })
        st.dataframe(pd.DataFrame(daily_data))

        # ---- Time Slot Frequency ----
        st.subheader("⏰ Time Slot Usage Frequency")
        time_freq = {slot: 0 for slot in session_cols}
        for i in range(len(schedule_df)):
            for j, slot in enumerate(session_cols):
                if st.session_state.checkboxes[i][j]:
                    time_freq[slot] += 1
        time_freq_df = pd.DataFrame({
            "Time Slot": list(time_freq.keys()),
            "Times Used": list(time_freq.values())
        })
        time_freq_df["Time Slot"] = pd.Categorical(time_freq_df["Time Slot"], categories=session_cols, ordered=True)
        time_freq_df = time_freq_df.sort_values("Time Slot")
        st.bar_chart(time_freq_df.set_index("Time Slot"))


    st.subheader("📌 Overall Progress Summary")
    total_done = sum([float(entry['Done Hours']) for entry in progress_data])
    total_all = sum([float(entry['Total Hours']) for entry in progress_data])
    overall_percent = (total_done / total_all) * 100 if total_all > 0 else 0

    st.metric("Total Completed", f"{total_done:.1f}h")
    st.metric("Remaining", f"{total_all - total_done:.1f}h")
    st.metric("Overall Completion", f"{overall_percent:.2f}%")


    st.subheader("📊 Time Allocation Per Subject")

    alloc_df = subject_df.copy()
    alloc_df["Percent Share"] = (alloc_df["Original Video Hours"] / alloc_df["Original Video Hours"].sum()) * 100

    # Create a smaller figure
    fig2, ax2 = plt.subplots(figsize=(3, 3))  # Smaller physical figure size
    ax2.pie(alloc_df["Original Video Hours"], labels=alloc_df.index, autopct='%1.1f%%', textprops={'fontsize': 8})
    ax2.set_title("Time Allocation (Original Hours)", fontsize=10)

    # Render with tighter layout
    st.pyplot(fig2, clear_figure=True, bbox_inches='tight')


    if st.button("🔁 Reset All Progress"):
        for i in range(len(schedule_df)):
            for j in range(len(session_cols)):
                st.session_state.checkboxes[i][j] = False
        save_progress({})
        st.rerun()

else:
    # Optional: Allow registration if not authenticated
    with st.expander("\ud83d\udcc5 New user? Register here"):
        try:
            email, username, registered_name = authenticator.register_user(
                location='main',
                pre_authorized=config.get('preauthorized', {}).get('emails', [])
            )
            if email:
                st.success(f"✅ Registered successfully for: {registered_name} ({email})")
        except Exception as e:
            st.error(e)
