from flask import Flask
from app.config import settings

from app.features.general.routes import general_bp


def create_app() -> Flask:
    app = Flask(
        import_name=__name__,
    )

    app.register_blueprint(blueprint=general_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    print(settings)
    app.run(
        host=settings.app.host,
        port=settings.app.port,
        debug=settings.app.debug,
    )
