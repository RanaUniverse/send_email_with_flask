from flask import Flask
from app.config import settings


def create_app() -> Flask:
    app = Flask(
        import_name=__name__,
    )
    return app


if __name__ == "__main__":
    app = create_app()

    print(settings)
    app.run(
        host="0.0.0.0",
        port=9999,
        debug=True,
    )
