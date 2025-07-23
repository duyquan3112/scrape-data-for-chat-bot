from datetime import datetime
import os

from openai.types.vector_stores.vector_store_file_batch import VectorStoreFileBatch

def saveUploadLog(fileBatch: VectorStoreFileBatch):
    outDir = f"logs/local_log/local_log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    os.makedirs(os.path.dirname(outDir), exist_ok=True)
    with open(outDir, 'w') as f:
        f.write(f"Log time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Upload ID: {fileBatch.id}\n")
        f.write(f"Upload created at: {fileBatch.created_at}\n")
        f.write(f"Upload status: {fileBatch.status}\n")
        f.write(f"----- Upload file counts: -----\n")
        f.write(f"Upload success: {fileBatch.file_counts.completed} files\n")
        f.write(f"Upload failed: {fileBatch.file_counts.failed} files\n")
        f.write(f"Upload cancelled: {fileBatch.file_counts.cancelled} files\n")
        f.write(f"Upload in progress: {fileBatch.file_counts.in_progress} files\n")
        f.write(f"Upload total: {fileBatch.file_counts.total} files\n")