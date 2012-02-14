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

This is deployable to Heroku in a similar process to what's described
[here](http://devcenter.heroku.com/articles/python). Run db_initer.py (with `DATABASE_URL` set to
the correct url) to create the necessary tables.
