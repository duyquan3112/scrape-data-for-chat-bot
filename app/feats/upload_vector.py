from openai import OpenAI
from app.config.app_config import OPENAI_API_KEY, VECTOR_STORE_ID
import os
from app.utils.save_upload_log import saveUploadLog

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# Create file path for all markdown files in the folder
def createFilePaths(folder='data/markdown'):
    filePaths = []
    relativePath = os.path.relpath(folder)
    for filename in os.listdir(relativePath):
        if filename.endswith('.md'):
            filePaths.append(os.path.join(relativePath, filename))
    return filePaths

# Upload file to OpenAI
def uploadVector(filePaths):
    print(filePaths)
    print(f"Uploading {len(filePaths)} files to OpenAI")
    # Ready the files for upload to OpenAI
    fileStreams = [open(path, "rb") for path in filePaths]

    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    fileBatch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=VECTOR_STORE_ID, files=fileStreams
    )
    print(f"Upload status: {fileBatch.status}")
    print(f"File count: {fileBatch.file_counts}")
    saveUploadLog(fileBatch=fileBatch)

    return fileBatch
