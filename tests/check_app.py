# check_app.py
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app


def main():
    os.environ["FLASK_DEBUG"] = "1"
    app = create_app()
    try:
        app.test_client().get("/")
        print("App started successfully in debug mode.")
    except Exception as e:
        print(f"Failed to start app: {e}")
        exit(1)


if __name__ == "__main__":
    main()
