from app.server import app, set_logger
import dotenv
import logging



def main():
    print("Hello from curate-mcp!")
    app.run()


if __name__ == "__main__":
    main()
