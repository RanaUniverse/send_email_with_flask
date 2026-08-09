"""
main.py

This is the entrypoint of my application, so i did run this

i keep the dont write bytecode first so that in local development
i will not need to see the pycache folders there in my repo
"""

import sys

sys.dont_write_bytecode = True

# This upper is for safety and just to keep in the repo for testing purpose only


from flask import Flask


from app.config import settings

from app.features.identity.routes import auth_bp
from app.features.general.routes import general_bp
# from app.features.mail.routes import mail_bp

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

    app.register_blueprint(blueprint=auth_bp)
    app.register_blueprint(blueprint=general_bp)
    # app.register_blueprint(blueprint=mail_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    print(settings)
    app.run(
        host=settings.app.host,
        port=settings.app.port,
        debug=settings.app.debug,
    )
