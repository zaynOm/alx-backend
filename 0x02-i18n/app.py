#!/usr/bin/env python3
"""Display the current time"""

from datetime import datetime
from flask import Flask, g, render_template, request
from flask_babel import Babel, format_datetime
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError


class Config:
    """Configuration class"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Find user by ID"""
    login_as = request.args.get("login_as")
    if not login_as or int(login_as) not in users:
        return None
    return users.get(int(login_as))


@app.before_request
def before_request():
    """Check login user and set it as a global"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Use specified locale in the url or findes the best match language"""
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user["locale"]
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """Use appropriate time zone"""
    try:
        if request.args.get("timezone"):
            return timezone(request.args.get("timezone"))
        if g.user:
            return timezone(g.user.get("timezone"))
    except UnknownTimeZoneError:
        pass
    return "UTC"


@app.route("/")
def index():
    """Entry point route"""
    time = format_datetime(datetime.now())
    return render_template("index.html", current_time=time)


if __name__ == "__main__":
    app.run()
