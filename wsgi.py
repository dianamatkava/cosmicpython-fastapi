from app import app

if __name__ == '__main__':
    print(f"DEBAG {app.config.FLASK_DEBUG}")
    app.run()

