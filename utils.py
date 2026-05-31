import json

file = "users.json"
log_file = "logs.txt"

#6new
def load_users():
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(file, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

def save_users(users):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False)

#10
def logs(message: str):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")