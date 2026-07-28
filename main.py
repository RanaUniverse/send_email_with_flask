from flask import Flask


from app.config import settings

from app.features.general.routes import general_bp
from app.features.identity.routes import auth_bp

from app.shared.extensions import login_manager, csrf


def create_app() -> Flask:
    app = Flask(
        import_name=__name__,
    )

    login_manager.init_app(  # type: ignore
        app=app,
    )
    csrf.init_app(  # type: ignore
        app=app,
    )

    app.secret_key = settings.app.secret_key.get_secret_value()

    app.register_blueprint(blueprint=general_bp)
    app.register_blueprint(blueprint=auth_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    print(settings)
    app.run(
        host=settings.app.host,
        port=settings.app.port,
        debug=settings.app.debug,
    )
