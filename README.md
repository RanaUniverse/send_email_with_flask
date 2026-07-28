## Why This Project?
This project will help me to know and use email services.

## What this website will do?
I will make a form where user will enter a email id and get a notification from my email services.
To use this user must to login using `flask_login`, then i will also use `flask_wtf` to protect against csrf token.

Later i will use Docker compose with to make it hostable website using Caddy, Redis, Postgres.
I will use bootstrap5, htmx4.

I will mainly use celery to do the task in background.

## Email Sending Logic:
For Nornmal user the email will send through my own `email` and `password`, and then when a login user login and give there own `email` and `password` to my service my backend will store this id password and for this user sending email page it will take the same to_email, subject, body but send the email based on his own email config.
i want to do this.