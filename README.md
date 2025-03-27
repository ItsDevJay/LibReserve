# 📚 Rutgers Study Room Booking Automation

A Python + Selenium automation tool that helps Rutgers–Newark students book study rooms at Dana Library (and soon other campuses). This was built to streamline the sluggish reservation process and save time for students juggling coursework, exams, and life.

## 🚀 Why I Built This

As a Rutgers–Newark student, I realized how slow the library reservation system can be—especially when you're trying to grab a room during busy exam weeks. One night, while prepping for a Calculus 2 study session, I thought:  
**“Why not automate this?”**  
Two days later, this bot was born.

## 🎥 [Watch the Tutorial](#) https://youtu.be/eRbLv3eoxtM

## ✅ Features

- Secure login using Rutgers NetID and password  
- Duo Security 2FA passcode detection & handling  
- Date selection and time input in 30-minute intervals  
- Auto-finds group-friendly rooms (skips solo-capacity rooms)  
- Auto-submits reservation and final confirmation

## 🛠️ Tech Stack

- Python 3
- Selenium WebDriver
- ChromeDriver (with user profile loading)
- Duo 2FA compatibility

## 📦 Installation

1. Clone this repo:
git clone https://github.com/ItsDevJay/LibReserve.git
cd rutgers-library-bot

2. Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Update the launch_chrome_with_profile() function in main.py with the correct path to your Chrome user profile.

🖥️ Running the Bot
python main.py
The bot will guide you step-by-step through:
- Logging in
- Picking a date
- Selecting a start and end time
- Reserving a room (if available)
- Finalizing the confirmation


🌐 Supported Libraries
✅ Dana Library (Rutgers–Newark)
🔜 Coming Soon: Rutgers – Camden, Rutgers - New Brunswick, and more!

🤝 Contributing
Pull requests are welcome! If you'd like to help add support for other campuses or recurring reservations, feel free to fork the repo and open a PR.

📬 Contact
Questions or suggestions? Hit me up on LinkedIn or open an issue here on GitHub.
