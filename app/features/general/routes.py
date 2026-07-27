"""
app/features/general/routes.py

Here i will make normal routes of what my general
and some common things
"""

from flask import (
    Blueprint,
    render_template,
)

general_bp = Blueprint(
    name="general_bp",
    import_name=__name__,
    template_folder="templates",
)


@general_bp.route(rule="/")
def home_page():
    return render_template(
        template_name_or_list="general/index.html",
    )
