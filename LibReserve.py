import getpass
import time
import platform
import re
from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def launch_chrome_with_profile():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    system = platform.system()
    if system == "Windows":
        chrome_options.add_argument(r"user-data-dir=C:\\Users\\Jay\\AppData\\Local\\Google\\Chrome\\User Data")
        chrome_options.add_argument("profile-directory=Default")
    elif system == "Darwin":
        chrome_options.add_argument("user-data-dir=/Users/Jay/Library/Application Support/Google/Chrome")
        chrome_options.add_argument("profile-directory=Default")
    else:
        raise Exception("Unsupported OS")
    return webdriver.Chrome(options=chrome_options)

def wait_for_login(driver):
    if driver.current_url.startswith("https://rutgers.primo.exlibrisgroup.com/discovery/account"):
        print("✅ Already logged in. Skipping login.")
        return

    print("\n🔓 Opening Rutgers login page...")
    driver.get("https://quicksearch.libraries.rutgers.edu/account")

    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#tab-content-0 > div > md-content > md-list > md-list-item:nth-child(1) > div > div.md-list-item-inner > prm-login-item > div > div > span"))
        )
        login_button.click()
        print("🔁 Redirecting to NetID login page...")
    except:
        print("⚠️ Could not auto-click login button. Proceed manually.")
        return

    while True:
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))
            netid = input("🧑‍💻 Enter your NetID username: ").strip()
            password = getpass.getpass("🔒 Enter your NetID password (hidden): ").strip()

            driver.find_element(By.CSS_SELECTOR, "#username").send_keys(netid)
            driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
            driver.find_element(By.CSS_SELECTOR, "#fm1 > input.btn.btn-block.btn-submit").click()
            time.sleep(3)

            try:
                alert_box = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-danger span")
                if "Invalid credentials" in alert_box.get_attribute("outerHTML"):
                    print("❌ Invalid credentials. Please try again.\n")
                    continue
            except:
                pass

            WebDriverWait(driver, 10).until(lambda d: "duosecurity.com" in d.current_url or "account" in d.current_url)

            if "duosecurity.com" in driver.current_url:
                print("📲 Duo 2FA detected.")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,
                            "#auth-view-wrapper > div:nth-child(2) > div.row.display-flex.send-passcode-button > button"))
                    )
                    send_button = driver.find_element(By.CSS_SELECTOR,
                        "#auth-view-wrapper > div:nth-child(2) > div.row.display-flex.send-passcode-button > button")
                    send_button.click()
                    time.sleep(1)

                    try:
                        phone_info_text = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="auth-view-wrapper"]/div[2]/div[2]/span'))
                        ).text
                        match = re.search(r"ending in (\d{4})", phone_info_text)
                        if match:
                            last_digits = match.group(1)
                            print(f"📨 A verification code has been sent to the phone number ending in {last_digits}.")
                        else:
                            print("📨 A verification code has been sent to your phone.")
                    except Exception as e:
                        print("⚠️ Could not extract phone number info, continuing anyway.")

                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#passcode-input"))
                    )
                    otp = input("🔢 Enter the 7-digit passcode you received: ").strip()
                    driver.find_element(By.CSS_SELECTOR, "#passcode-input").send_keys(otp)
                    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

                    # ✅ Check for "Trust this browser?" prompt
                    try:
                        trust_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "#trust-browser-button"))
                        )
                        trust_button.click()
                        print("🔒 'Trust this browser' button clicked.")
                    except:
                        print("ℹ️ 'Trust this browser' prompt not shown or already trusted.")

                except Exception as e:
                    print("⚠️ Duo OTP flow not detected or failed:", e)
                    print("📲 Please approve push notification on your device.")

                WebDriverWait(driver, 300).until(
                    lambda d: d.current_url.startswith("https://rutgers.primo.exlibrisgroup.com/discovery/account")
                )

            print("✅ Login successful!")
            return

        except Exception as e:
            print(f"⚠️ Error during login: {e}")
            continue

def go_to_date(driver, date_input):
    try:
        dt = datetime.strptime(date_input, "%m/%d/%Y").replace(tzinfo=timezone.utc)
        target_timestamp = int(dt.timestamp()) * 1000

        print(f"\n📅 Attempting to select date: {date_input} (timestamp: {target_timestamp})")

        go_to_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#eq-time-grid > div.fc-header-toolbar.fc-toolbar.fc-toolbar-ltr > div:nth-child(1) > button.fc-goToDate-button.btn.btn-default.btn-sm"))
        )
        go_to_btn.click()
        time.sleep(1)

        calendar_cells = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.day"))
        )

        for cell in calendar_cells:
            if cell.get_attribute("data-date") == str(target_timestamp):
                cell.click()
                print("✅ Date selected successfully.")
                time.sleep(3)
                return

        print("❌ Could not find matching calendar cell — likely wrong month visible.")

    except Exception as e:
        print(f"❌ Failed to go to date: {e}")

def round_to_nearest_half_hour(dt):
    minutes = dt.minute
    if minutes < 15:
        dt = dt.replace(minute=0)
    elif minutes < 45:
        dt = dt.replace(minute=30)
    else:
        dt = dt.replace(minute=0) + timedelta(hours=1)
    return dt

def get_library_hours():
    return {
        "monday": (8, 22),
        "tuesday": (8, 22),
        "wednesday": (8, 22),
        "thursday": (8, 22),
        "friday": (8, 18),
        "saturday": (9, 17.5),
        "sunday": (None, None),
    }

def format_hour_min_display(hour_decimal):
    hour = int(hour_decimal)
    minute = int((hour_decimal - hour) * 60)
    return datetime.strptime(f"{hour}:{minute:02d}", "%H:%M").strftime("%-I:%M %p")

def prompt_for_valid_times(weekday, open_hour, close_hour):
    while True:
        print("🕒 Note: Times are in 30-minute intervals (e.g., 9:00 AM, 9:30 AM, 10:00 AM).")
        start_time = input("⏰ Enter start time (e.g., 8:00 AM): ").strip()
        end_time = input("⏰ Enter end time (e.g., 9:00 AM): ").strip()

        try:
            time_format = "%I:%M %p"
            start_dt = round_to_nearest_half_hour(datetime.strptime(start_time, time_format))
            end_dt = round_to_nearest_half_hour(datetime.strptime(end_time, time_format))

            open_dt = datetime.combine(start_dt.date(), datetime.min.time()) + timedelta(hours=open_hour)
            close_dt = datetime.combine(start_dt.date(), datetime.min.time()) + timedelta(hours=close_hour - 0.5)

            if start_dt < open_dt or end_dt > close_dt:
                print(f"❌ Reservation must be within {format_hour_min_display(open_hour)} and {format_hour_min_display(close_hour - 0.5)} on {weekday.title()}.")
                continue
            if end_dt <= start_dt:
                print("❌ End time must be after start time.")
                continue
            if end_dt - start_dt > timedelta(minutes=240):
                print("❌ Reservation too long. Maximum allowed per day is 240 minutes (4 hours).")
                continue
            return start_time, end_time
        except:
            print("❌ Invalid time format. Try again.")

def generate_slot_labels(start_time_str, end_time_str, full_date_str):
    time_format = "%I:%M %p"
    start_time = round_to_nearest_half_hour(datetime.strptime(start_time_str, time_format))
    end_time = round_to_nearest_half_hour(datetime.strptime(end_time_str, time_format))

    labels = []
    while start_time < end_time:
        time_str = start_time.strftime("%-I:%M%p").lower()
        label = f"{time_str} {full_date_str.lower().strip()}"
        print(f"🔑 Generated label: '{label}'")
        labels.append(label)
        start_time += timedelta(minutes=30)
    return labels

def click_available_slots(driver, full_date_str, start_time_str, end_time_str, group_size):
    desired_labels = generate_slot_labels(start_time_str, end_time_str, full_date_str)
    print(f"\n🔍 Looking for slots: {desired_labels}")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.fc-timeline-event"))
    )

    slots = driver.find_elements(By.CSS_SELECTOR, "a.fc-timeline-event")
    available_rooms = {}

    capacity_one_rooms = {
        "booth ferris a", "booth ferris b", "group study 203"
    }

    for slot in slots:
        label = slot.get_attribute("aria-label") or slot.get_attribute("title")
        slot_class = slot.get_attribute("class")

        if label and slot_class and "s-lc-eq-avail" in slot_class:
            label_lower = label.lower()
            time_part = label_lower.split(" - ")[0].strip()
            room = label_lower.split(" - ")[1].strip()

            if group_size > 1 and room in capacity_one_rooms:
                continue

            if room not in available_rooms:
                available_rooms[room] = {}

            available_rooms[room][time_part] = slot

    for room, times in available_rooms.items():
        match_all = all(any(label.startswith(time_part) for time_part in times) for label in desired_labels)
        if match_all:
            print(f"✅ Found all time slots in {room}")
            for label in desired_labels:
                for time_part, slot in times.items():
                    if label.startswith(time_part):
                        print(f"✅ Clicking: {slot.get_attribute('aria-label') or slot.get_attribute('title')}")
                        slot.click()
                        time.sleep(1)
                        break

            # ✅ Submit selected time slots
            try:
                submit_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit_times"))
                )
                submit_btn.click()
                print("📤 Submitted selected time slots.")
            except Exception as e:
                print(f"❌ Failed to submit time slots: {e}")
                return

            # ✅ Accept terms or finalize confirmation
            try:
                terms_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#terms_accept"))
                )
                terms_btn.click()
                print("✅ Reservation confirmed!")
            except Exception as e:
                print(f"❌ Failed to confirm reservation: {e}")

            # ✅ Final form submission
            try:
                final_submit = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn-form-submit"))
                )
                final_submit.click()
                print("📌 Final confirmation submitted — your room is now officially booked!")
            except Exception as e:
                print(f"❌ Final submission failed: {e}")

            print(f"\n🏠 Room booked: {room}")
            print("📧 A confirmation email has been sent to your account.")
            return

    print("❌ No single room has all requested time slots available.")
    while True:
        print("\n❓ What would you like to do next?")
        print("1. Try a different time")
        print("2. Exit")
        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            new_start = input("⏰ New start time (e.g., 8:00 AM): ").strip()
            new_end = input("⏰ New end time (e.g., 9:00 AM): ").strip()
            click_available_slots(driver, full_date_str, new_start, new_end, group_size)
            return
        elif choice == "2":
            print("👋 Exiting the program.")
            driver.quit()
            exit()
        else:
            print("❌ Invalid input. Please try again.")

def main(driver=None):
    if driver is None:
        driver = launch_chrome_with_profile()
        wait_for_login(driver)

    library_url = "https://libcal.rutgers.edu/reserve/spaces/dana_lib"

    while True:
        print("\n📅 What kind of reservation do you want?")
        print("1. One-time reservation")
        print("2. Recurring reservation")
        mode = input("Enter 1 or 2: ").strip()

        if mode == "1":
            print("🟢 One-time reservation selected.")
            break
        elif mode == "2":
            print("🔁 Recurring reservation selected. (Feature in development — not yet implemented)")
            continue
        else:
            print("❌ Invalid input. Please try again.")

    date_input = input("📆 What date do you want to reserve? (MM/DD/YYYY): ").strip()
    weekday = datetime.strptime(date_input, "%m/%d/%Y").strftime("%A").lower()
    open_hour, close_hour = get_library_hours().get(weekday, (None, None))

    if open_hour is None:
        print("❌ The library is closed on this day. Cannot make a reservation.")
        return

    start_time, end_time = prompt_for_valid_times(weekday, open_hour, close_hour)

    group_input = input("👥 How many people will use the room? (Enter a number): ").strip()
    try:
        group_size = int(group_input)
    except:
        group_size = 1

    full_date_str = datetime.strptime(date_input, "%m/%d/%Y").strftime("%A, %B %d, %Y")

    print(f"\n🚀 Opening: {library_url}")
    driver.get(library_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#eq-time-grid"))
    )

    go_to_date(driver, date_input)
    click_available_slots(driver, full_date_str, start_time, end_time, group_size)

    print("\n🧠 Finished processing. Press ENTER to close browser.")
    input()
    driver.quit()

if __name__ == "__main__":
    main()