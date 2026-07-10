import time
import random
import json

# Список возможных логов: успешные и критические ошибки
MESSAGES = [
    {"level": "INFO", "status": 200, "message": "User login successful, token generated."},
    {"level": "INFO", "status": 200, "message": "Product catalog viewed by user_id=412."},
    {"level": "WARN", "status": 404, "message": "Product image not found on S3 bucket: 'images-cache'."},
    {"level": "ERROR", "status": 500, "message": "Database connection timeout. Pool size exhausted."},
    {"level": "CRITICAL", "status": 500, "message": "Disk Full! Cannot write session logs to /var/log/app."}
]

print("--- AWS Fake Service Started. Generating logs... ---", flush=True)

while True:
    log_entry = random.choice(MESSAGES).copy()
    log_entry["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    log_entry["cloud"] = "AWS"
    log_entry["service"] = "payment-gateway"

    # flush=True важен, чтобы докер сразу выводил лог в консоль
    print(json.dumps(log_entry), flush=True)
    time.sleep(random.randint(1, 5))