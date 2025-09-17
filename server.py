import os
import uvicorn
from fastapi import FastAPI

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

app = FastAPI()

@app.get("/")
def read_root():
    print("Request received at root endpoint.")
    return {"status": "ok", "message": f"Hello from the server running on port {PORT}!"}

if __name__ == "__main__":
    print(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)

