CREATE TABLE IF NOT EXISTS teams (
  id char(8) NOT NULL,
  name varchar(100) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clues (
  team char(8) NOT NULL,
  clue_number int NOT NULL,
  body bytea NOT NULL,
  PRIMARY KEY (team, clue_number)
);
