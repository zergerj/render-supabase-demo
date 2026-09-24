from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os

app = FastAPI()

supabase_url = os.environ["SUPABASE_URL"]
supabase_key = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(
    supabase_url,
    supabase_key
)


class MachineCreate(BaseModel):
    name: str
    status: str


class MachineUpdate(BaseModel):
    name: str | None = None
    status: str | None = None


@app.get("/machines")
def get_machines():
    response = (
        supabase
        .table("machines")
        .select("*")
        .execute()
    )

    return response.data


@app.get("/machines/{machine_id}")
def get_machine(machine_id: int):
    response = (
        supabase
        .table("machines")
        .select("*")
        .eq("id", machine_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    return response.data[0]


@app.post("/machines")
def create_machine(machine: MachineCreate):
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


@app.patch("/machines/{machine_id}")
def update_machine(machine_id: int, machine: MachineUpdate):

    update_data = machine.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields supplied to update"
        )

    response = (
        supabase
        .table("machines")
        .update(update_data)
        .eq("id", machine_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    return response.data[0]


@app.delete("/machines/{machine_id}")
def delete_machine(machine_id: int):

    response = (
        supabase
        .table("machines")
        .delete()
        .eq("id", machine_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    return {
        "message": "Machine deleted",
        "machine": response.data[0]
    }
