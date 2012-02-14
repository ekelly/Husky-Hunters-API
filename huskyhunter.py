import tornado.ioloop
import tornado.web
import psycopg2
import functools
import json
import os
import sys
import uuid
import urlparse
import clues
from contextlib import contextmanager

DATABASE_URL = urlparse.urlparse(os.environ['DATABASE_URL'])

@contextmanager
def commit(connection):
  yield
  connection.commit()

def jsonp(name, body):
  return "%s(%s)" % (name, body)

def generate_id():
  base_id = uuid.uuid4()
  return base_id.int % 100000000

def valid_team(fun):
  @functools.wraps(fun)
  def wrapped(self, team, *args, **kwargs):
    self.cursor.execute("select count(*) from teams where id = %s", (team,))
    team_count = self.cursor.fetchone()[0]

    if not team_count > 0:
      raise tornado.web.HTTPError(404)

    fun(self, team, *args, **kwargs)
  return wrapped

def existing_clue(fun):
  @functools.wraps(fun)
  def wrapped(self, team, clue, *args, **kwargs):
    if clues.get(self.cursor, team, clue) is None:
      raise tornado.web.HTTPError(404)

    fun(self, team, clue, *args, **kwargs)
  return wrapped

class BaseHandler(tornado.web.RequestHandler):
  def prepare(self):
    self.jsonp_callback = self.get_argument("callback", "")
    self.has_jsonp_callback = self.jsonp_callback != ""
    self.connection = psycopg2.connect(host=DATABASE_URL.hostname, database=DATABASE_URL.path[1:],
                                       user=DATABASE_URL.username, password=DATABASE_URL.password)
    self.cursor = self.connection.cursor()

  def on_finish(self):
    self.cursor.close()
    self.connection.close()

  def writeJsonp(self, body):
    self.write(jsonp(self.jsonp_callback, body) if self.has_jsonp_callback else body)

class CluesHandler(BaseHandler):
  @valid_team
  def get(self, team):
    self.writeJsonp(json.dumps(clues.get_all(self.cursor, team)))

class ClueHandler(BaseHandler):
  @valid_team
  @existing_clue
  def get(self, team, clue_number):
    self.writeJsonp(clues.get_json(self.cursor, team, clue_number))

  @valid_team
  def put(self, team, clue_number):
    clue = clues.decode(self.request.body)

    with commit(self.connection):
      if clues.get(self.cursor, team, clue_number) is None:
        clues.create(self.cursor, team, clue_number, clue)
      else:
        clue = clues.update(self.cursor, team, clue_number, clue)

    self.writeJsonp(json.dumps(clue))

  @valid_team
  @existing_clue
  def delete(self, team, clue_number):
    with commit(self.connection):
      clues.delete(self.cursor, team, clue_number)

class PhotosHandler(BaseHandler):
  @valid_team
  @existing_clue
  def get(self, team, clue):
    self.writeJsonp(json.dumps(clues.get(self.cursor, team, clue)["photos"]))

class TeamHandler(BaseHandler):
  @valid_team
  def get(self, team):
    self.cursor.execute("select name, id from teams where id = %s", (team,))
    team = self.cursor.fetchone()
    self.writeJsonp(json.dumps({"name": team[0], "id": team[1]}))

class TeamsHandler(BaseHandler):
  def post(self):
    name = self.get_argument("name")
    new_id = generate_id()

    with commit(self.connection):
      self.cursor.execute("insert into teams (id, name) values (%s, %s)", (new_id, name))

    self.writeJsonp(json.dumps({"name": name, "id": new_id}))

application = tornado.web.Application([
    (r"/teams/?", TeamsHandler),
    (r"/teams/([^/]+)/?", TeamHandler),
    (r"/teams/([^/]+)/clues/?", CluesHandler),
    (r"/teams/([^/]+)/clues/([^/]+)/?", ClueHandler),
    (r"/teams/([^/]+)/clues/([^/]+)/photos/?", PhotosHandler),
])

if __name__ == "__main__":
  port = os.environ.get("PORT")
  print "Listening on port %s" % port
  sys.stdout.flush()
  application.listen(port)
  tornado.ioloop.IOLoop.instance().start()
