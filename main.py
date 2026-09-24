from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "API is running"
    }


@app.get("/machines")
def get_machines():
    return [
        {
            "id": 1,
            "name": "Machine 001",
            "status": "online"
        },
        {
            "id": 2,
            "name": "Machine 002",
            "status": "offline"
        }
    ]
