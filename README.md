Husky Hunter API
================

The api component of the husky hunter app. It's a simple store of teams and those teams' clues.

A team is created by posting a name to `/teams/`, which returns a json object containing that same
name and an assigned id. A typical use would look something like:

    curl -d name=foo "http://husky-hunter-app/teams/"
    =>
    {"name": "foo", "id": 42535749}

With the given id, you can then query the new team's clues, or create new clues with the
`/teams/<id>/clues/` and `/teams/<id>/clues/<number>` endpoints respectively. GETing the
first returns the team with the given id's clues as a json array. PUTing to the second with a valid
clue json (description to come) as the body creates a clue with the given number for the team with
the given id.


Deployment
----------

This is deployable to Heroku in a similar process to what's described
[here](http://devcenter.heroku.com/articles/python).

Running Locally
---------------

The instructions for deployment to Heroku can be translated into running locally.

### Requirements

- Python 2.7
- pip
- PostgreSQL

It is necessary to have PostgreSQL installed and running locally. On a Mac, you can follow the first section of [these instructions](http://blog.willj.net/2011/05/31/setting-up-postgresql-for-ruby-on-rails-development-on-os-x/).

`virtualenv` is helpful to isolate this project from others. Set it up in the project directory:

    virtualenv --no-site-packages env
    source env/bin/activate

Then install Python modules:

    pip install -r requirements.txt

Make sure that PostgreSQL is running:

    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

You'll need to create a user and database:

    createuser username
    createdb -Ousername -Eutf8 dbname

The URL of this database will be of the format `postgres://username@localhost/dbname` which you need to set as the `DATABASE_URL` value:

    export DATABASE_URL=postgres://username:password@localhost/dbname

Create tables:

    python db_initer.py

To run the API server, you need to also set a `PORT` environment variable:

    export PORT=8001

Finally, you can run the API server:

    python huskyhunter.py