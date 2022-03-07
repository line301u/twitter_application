DROP TABLE IF EXISTS items;
CREATE TABLE items(
  item_id                 TEXT UNIQUE NOT NULL,
  item_name               TEXT NOT NULL,
  item_price              TEXT NOT NULL,
  item_description        TEXT NOT NULL,
  item_created_at         TEXT NOT NULL,
  item_created_at_date    TEXT NOT NULL,
  item_updated_at         TEXT NOT NULL,
  item_updated_at_date    TEXT NOT NULL,
  PRIMARY KEY(item_id)
); WITHOUT ROWID
