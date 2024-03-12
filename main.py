import os
import uvicorn

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from embedchain import App

from mapping import mime_type_mapping, reverse_mime_type_mapping
from models import UserInput, DataSource

app = FastAPI(
    title="Embedchain REST API",
    description="This is the REST API for Embedchain.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedchain_app = App.from_config("config.yaml")


@app.get("/data-sources")
async def get_sources():
    try:
        raw_data_sources = embedchain_app.get_data_sources()
        data_sources = [DataSource(data_type=reverse_mime_type_mapping.get(src["data_type"], "unknown/unknown"),
                                   data_value=src["data_value"]) for src in raw_data_sources]
        return data_sources
    except Exception as e:
        return {"error": str(e)}


@app.post("/reset")
async def reset():
    try:
        embedchain_app.reset()
        return {"result": "success"}
    except Exception as e:
        return {"error": str(e)}


@app.delete("/delete")
async def delete_file(file_name):
    try:
        result = embedchain_app.db.get(where={'source': file_name})
        ids = [metadata['hash'] for metadata in result['metadatas']]
        if not ids:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        for doc_id in ids:
            embedchain_app.delete(doc_id)

        return {"result": "success"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content_type = file.content_type
    file_name = file.filename
    unknown_file_type = "unknown_type"
    file_type = mime_type_mapping.get(content_type, unknown_file_type)

    if file_type == unknown_file_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File format '{content_type}' is not supported."
        )

    existing_files = embedchain_app.db.get(where={'source': file_name})
    existing_files_ids = [metadata['hash'] for metadata in existing_files['metadatas']]
    if existing_files_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A file with this name already exists."
        )

    with open(file.filename, "wb+") as temp_file:
        temp_file.write(await file.read())

    try:
        embedchain_app.add(file.filename, data_type=file_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while uploading the file to Embedchain: {str(e)}"
        )
    finally:
        os.remove(file.filename)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully."
    }


@app.post("/query")
async def get_answer(user_input: UserInput):
    response = embedchain_app.query(user_input.question)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
