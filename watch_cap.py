#!/usr/bin/env python3

import hashlib
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://dowcio.war.gov/Cyber-Workforce/Cyber-Workforce-Development/Cyber-Apprenticeship-Program/"
TRIGGER_KEYWORDS = ["usajobs", "usajobs.gov", "apply now", "open now"]

from dotenv import load_dotenv
import os

load_dotenv(Path.home() / ".env_cap_watcher")
YOUR_EMAIL   = os.getenv("YOUR_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")

HASH_FILE = Path.home() / ".cap_watcher_hash"

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; job-watcher/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ").lower(), response.text

def page_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def load_last_hash():
    if HASH_FILE.exists():
        return HASH_FILE.read_text().strip()
    return None

def save_hash(h):
    HASH_FILE.write_text(h)

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"]    = YOUR_EMAIL
    msg["To"]      = NOTIFY_EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(YOUR_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
    print("Email sent!")

def check_for_trigger(text, html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=True)
    return any("usajobs.gov" in link["href"] for link in links)

def main():
    print(f"Checking: {TARGET_URL}")
    try:
        visible_text, raw_html = fetch_page(TARGET_URL)
    except Exception as e:
        print(f"Failed to fetch page: {e}")
        sys.exit(1)

    current_hash = page_hash(visible_text)
    last_hash    = load_last_hash()

    if last_hash is None:
        save_hash(current_hash)
        print("Baseline saved. Watcher is now active!")
        return

    if check_for_trigger(visible_text, raw_html):
        print("USAJOBS link detected!")
        send_email(
            subject="Cyber Apprenticeship Program - Applications Are Open!",
            body=f"The job posting is live!\n\nApply here:\n{TARGET_URL}\n\nGood luck!"
        )
        save_hash(current_hash)
        return

    if current_hash != last_hash:
        print("Page changed - no USAJOBS link yet, but worth checking.")
        send_email(
            subject="CAP Page Changed - Check It Out",
            body=f"The page changed but no USAJOBS link yet.\n\nCheck it:\n{TARGET_URL}"
        )
        save_hash(current_hash)
    else:
        print("No changes detected.")

if __name__ == "__main__":
    main()
