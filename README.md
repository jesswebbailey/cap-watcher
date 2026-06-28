# CAP Job Posting Watcher

A Python script that automatically monitors the Department of the Army's
Cyber Apprenticeship Program page and sends an email notification when
the USAJOBS application link goes live.

## Why I Built This

I'm actively pursuing a career in cybersecurity and applied to the DoA
Cyber Apprenticeship Program. Rather than manually checking the page,
I built this tool to automate the monitoring process.

## How It Works

- Fetches the CAP page hourly via cron job
- Uses BeautifulSoup to parse HTML and detect a real usajobs.gov link
- Compares page hash to detect any other content changes
- Sends a Gmail notification when the link appears

## Setup

1. Clone the repo
2. Install dependencies: `pip install requests beautifulsoup4 python-dotenv`
3. Create a `.env_cap_watcher` file in your home directory:
# CAP Job Posting Watcher

A Python script that automatically monitors the Department of the Army's
Cyber Apprenticeship Program page and sends an email notification when
the USAJOBS application link goes live.

## Why I Built This

I'm actively pursuing a career in cybersecurity and applied to the DoA
Cyber Apprenticeship Program. Rather than manually checking the page,
I built this tool to automate the monitoring process.

## How It Works

- Fetches the CAP page hourly via cron job
- Uses BeautifulSoup to parse HTML and detect a real usajobs.gov link
- Compares page hash to detect any other content changes
- Sends a Gmail notification when the link appears

## Setup

1. Clone the repo
2. Install dependencies: `pip install requests beautifulsoup4 python-dotenv`
3. Create a `.env_cap_watcher` file in your home directory:
4. Run once to set baseline: `python3 watch_cap.py`
5. Schedule with cron: `0 * * * * /usr/bin/python3 /path/to/watch_cap.py`

## Tools Used

- Python 3
- requests
- BeautifulSoup4
- python-dotenv
- Ubuntu 24.04 LTS
- cron
