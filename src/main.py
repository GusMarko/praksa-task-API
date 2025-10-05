from fastapi import FastAPI
from filelock import FileLock
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import variables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= variables.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(variables.COUNTER_FILE_PATH):
    os.makedirs(os.path.dirname(variables.COUNTER_FILE_PATH), exist_ok=True)
    with open(variables.COUNTER_FILE_PATH, "w") as f:
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
    lock = FileLock(variables.LOCK_FILE_PATH)
    with lock:
        return {"counter": read_counter(variables.COUNTER_FILE_PATH)}

@app.post("/increment")
def increment_counter():
    lock = FileLock(variables.LOCK_FILE_PATH)
    with lock:
        current_value = read_counter(variables.COUNTER_FILE_PATH)
        new_value = current_value + 1
        write_counter(variables.COUNTER_FILE_PATH, new_value)
        return {"counter": new_value}

@app.post("/reset")
def reset_counter_value():
    lock = FileLock(variables.LOCK_FILE_PATH)
    with lock:
        reset_counter(variables.COUNTER_FILE_PATH)
        return {"counter" : 0}