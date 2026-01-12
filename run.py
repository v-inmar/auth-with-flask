import os
from app import create_app

port=os.getenv("PORT")
host=os.getenv("HOST")

app = create_app()

if __name__ == "__main__":
    app.run(host=host, port=port)