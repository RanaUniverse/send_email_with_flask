"""
app/features/general/routes.py

Here i will make normal routes of what my general
and some common things
"""

from flask import flash, Blueprint, render_template, session

general_bp = Blueprint(
    name="general_bp",
    import_name=__name__,
    template_folder="templates",
)


@general_bp.route(rule="/")
def home_page():
    all_data = dict(session)
    flash(
        "Development Things",
        "success",
    )
    flash(
        str(all_data),
        category="success",
    )
    return render_template(
        template_name_or_list="general/index.html",
    )
