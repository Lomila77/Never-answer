import logging
from fastapi import FastAPI
import uvicorn
app = FastAPI()


@app.post("/")
def main() -> dict[str, str]:
    try:
        pass
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
