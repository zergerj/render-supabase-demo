import os

from fastapi import FastAPI
from supabase import create_client, Client
from pydantic import BaseModel

class Machine(BaseModel):
    name: str
    status: str

app = FastAPI()


supabase_url: str = os.environ["SUPABASE_URL"]
supabase_key: str = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(
    supabase_url,
    supabase_key
)


@app.get("/")
def root():
    return {
        "message": "API is running"
    }


@app.get("/machines")
def get_machines():

    response = (
        supabase
        .table("machines")
        .select("*")
        .execute()
    )

    return response.data

@app.post("/machines")
def create_machine(machine: Machine):
    response = (
        supabase
        .table("machines")
        .insert({
            "name": machine.name,
            "status": machine.status
        })
        .execute()
    )

    return response.data
