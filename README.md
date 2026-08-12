## Why This Project?
This project will help me to know and use email services.



## How i will run this in locally.
For local i will run mailpit and redis via docker so that i can see and check in local.

1. Redis Setup

For First time in my local machine:
```
docker run --name redis8 -d -p 6379:6379 redis:8.10.0
```

Next Time How i will run after i make one docker container wth name of redis8
```
docker start redis8
docker exec -it redis8 redis-cli
```
Then i will need to use anohter user in my redis so that it will do only what access this has given to this user:
```
ACL SETUSER admin on >admin@123 ~* +@all

ACL SETUSER rana on >rana@123 ~* +@read +@write +@connection

ACL SETUSER default off
```

2. Mailpit
I will use mailpit for local mail sending and see that in my local machine.
```
docker run -d --name mailpit -p 1025:1025 -p 8025:8025 axllent/mailpit
```



## What this website will do?
I will make a form where user will enter a email id and get a notification from my email services.
To use this user must to login using `flask_login`, then i will also use `flask_wtf` to protect against csrf token.

Later i will use Docker compose with to make it hostable website using Caddy, Redis, Postgres.
I will use bootstrap5, htmx4.

I will mainly use celery to do the task in background.

## Email Sending Logic:
For Nornmal user the email will send through my own `email` and `password`, and then when a login user login and give there own `email` and `password` to my service my backend will store this id password and for this user sending email page it will take the same to_email, subject, body but send the email based on his own email config.
i want to do this.
