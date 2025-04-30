import uvicorn
from app.api.v1.routes import *
from preload import *


if __name__ == "__main__":
    uvicorn.run(app=root_app, host='0.0.0.0', port=5000)