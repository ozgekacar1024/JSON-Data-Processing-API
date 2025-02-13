from fastapi import FastAPI, HTTPException, Request
from pymongo import MongoClient
from client import Client
from UpdateItem import UpdateItem
import mysql.connector

app = FastAPI()



# Veritabanı bağlantısı
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="appointment"
)


@app.on_event("startup")
async def collection_sequence_starter():
    counter = counter_data_collection.find_one({"_id": "data_id"})

    if not counter:
        counter_data_collection.insert_one({"_id": "data_id", "seq": 0})


def generate_seq_id(name):
    return counter_data_collection.find_one_and_update({"_id": name}, {"$inc": {"seq": 1}}, return_document=True)['seq']


@app.put("/update-json")
async def update_item(update_item: UpdateItem):

    document = collection.find_one({"_id": str(update_item.data_id)})

    document["data"][update_item.key] = update_item.value

    collection.replace_one({"_id": str(update_item.data_id)}, document)

    return {"mesaj": "JSON data güncellendi : " + str(update_item.data_id)}


@app.post("/process-json")
async def process_json(request: Request):
    try:
        json_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    # Artan bir ID oluşturma

    generated_id = int(generate_seq_id("data_id"))

    # Veriyi MongoDB'ye kaydetme
    try:
        collection.insert_one({"_id": generated_id, "data": json_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return {"message": "JSON data processed and saved successfully with ID: " + str(generated_id)}


@app.get("/send-json")
async def send_json():
    # MyApiClient sınıfını kullanarak JSON verisini gönderme
    client_instance = Client()
    response_data = await client_instance.post_json_data()
    return response_data
