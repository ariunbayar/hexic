CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  email TEXT,
  phone TEXT UNIQUE NOT NULL,
  code TEXT NOT NULL,
  created DATETIME NOT NULL,
  last_seen DATETIME,
  is_admin BOOLEAN DEFAULT FALSE
);

INSERT INTO users VALUES (null, "Ариунбаяр", null, 99437911, 1234, DATETIME("now"), null, 1);
INSERT INTO users VALUES (null, "User1", null, 88776655, 1234, DATETIME("now"), null, 0);
INSERT INTO users VALUES (null, "User2", null, 99887766, 1234, DATETIME("now"), null, 0);

/* vim: set ts=2 sw=2 sts=2 fdn=4 : */
