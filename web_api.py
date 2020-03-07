from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}
app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/event/")
async def read_item(name: str, ts: float, event_type: str):
    return {
        "name": name, "ts": ts, "event_type": event_type,
        'status': 'sucess'
    }