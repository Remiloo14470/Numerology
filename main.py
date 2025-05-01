import uvicorn
from preload import root_app


if __name__ == "__main__":
    uvicorn.run(app=root_app, host='0.0.0.0', port=5000)