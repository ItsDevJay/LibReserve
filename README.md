# 📚 Rutgers Study Room Booking Automation

A Python + Selenium automation tool that helps Rutgers–Newark students book study rooms at Dana Library (and soon other campuses). This was built to streamline the sluggish reservation process and save time for students juggling coursework, exams, and life.

## 🚀 Why I Built This

As a Rutgers–Newark student, I realized how slow the library reservation system can be—especially when you're trying to grab a room during busy exam weeks. One night, while prepping for a Calculus 2 study session, I thought:  
**“Why not automate this?”**  
Two days later, this bot was born. 🧠⚡

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

```bash
git clone https://github.com/ItsDevJay/LibReserve.git
cd rutgers-library-bot
