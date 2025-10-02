from fastapi import FastAPI
from filelock import FileLock
from fastapi.middleware.cors import CORSMiddleware
import json
import os

COUNTER_FILE_PATH = "/data/counter.json"
LOCK_FILE_PATH = "/data/counter.lock"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(COUNTER_FILE_PATH):
    os.makedirs(os.path.dirname(COUNTER_FILE_PATH), exist_ok=True)
    with open(COUNTER_FILE_PATH, "w") as f:
        json.dump({"counter": 0}, f)

    
def reset_counter(file_path):
        write_counter(file_path, 0)

def read_counter(file_path):
    with open(file_path, "r") as f:
        return json.load(f)["counter"]


def write_counter(file_path, value):
    with open(file_path, "w") as f:
        json.dump({"counter": value}, f)


@app.get("/")
def get_counter():
    lock = FileLock(LOCK_FILE_PATH)
    with lock:
        return {"counter": read_counter(COUNTER_FILE_PATH)}

@app.post("/increment")
def increment_counter():
    lock = FileLock(LOCK_FILE_PATH)
    with lock:
        current_value = read_counter(COUNTER_FILE_PATH)
        new_value = current_value + 1
        write_counter(COUNTER_FILE_PATH, new_value)
        return {"content": new_value}

@app.post("/reset")
def reset_counter_value():
    lock = FileLock(LOCK_FILE_PATH)
    with lock:
        reset_counter(COUNTER_FILE_PATH)
        return {"counter" : 0}