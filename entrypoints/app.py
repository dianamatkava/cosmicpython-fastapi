import uvicorn

from src.app import create_app

app = create_app()


def start_app():
    try:
        uvicorn.run("entrypoints.app:app", host="127.0.0.1", port=8000, reload=True)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start_app()
