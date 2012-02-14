import codecs
import json

utf8_decoder = codecs.getdecoder("utf_8")

def encode(clue):
  return json.dumps(clue)

def decode(clue_json):
  # TODO: field validation.
  clue = json.loads(utf8_decoder(clue_json)[0])
  clue["id"] = clue["number"]
  return clue

def get(cursor, team, clue_number):
  maybe_json = get_json(cursor, team, clue_number)
  return (decode(maybe_json) if not maybe_json is None else maybe_json)

def get_json(cursor, team, clue_number):
  cursor.execute("select body from clues where team = %s and clue_number = %s ", (team, clue_number))
  maybe_row = cursor.fetchone()
  return (maybe_row[0] if not maybe_row is None else maybe_row)

def get_all(cursor, team):
  cursor.execute("select body from clues where team = %s", (team,))
  return [decode(row[0]) for row in cursor]

def create(cursor, team, clue_number, clue):
  cursor.execute("insert into clues (team, clue_number, body) values (%s, %s, %s)", (team, clue_number, encode(clue)))

def update(cursor, team, clue_number, clue):
  current_clue = get(cursor, team, clue_number)
  for field in clue.keys():
    current_clue[field] = clue[field]
  cursor.execute("update clues set body = %s where team = %s and clue_number = %s", (encode(current_clue), team, clue_number))
  return current_clue

def delete(db, team, clue_number):
  cursor.execute("delete from clues where team = %s and clue_number = %s", (team, clue_number))
