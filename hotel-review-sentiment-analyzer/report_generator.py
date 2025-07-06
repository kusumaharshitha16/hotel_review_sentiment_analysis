import schedule
import time
import subprocess

def run_analysis():
    print("⏳ Running scheduled analysis...")
    subprocess.run(["python", "main.py"])
    print("✅ Daily report generated.")

# Schedule task at 10 AM daily
schedule.every().day.at("10:00").do(run_analysis)

print("🕒 Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)