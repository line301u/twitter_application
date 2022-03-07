from bottle import put, request
import x
import time
from datetime import datetime

##############################
@put("/items/<item_id>")
@put("/<language>/items/<item_id>")
def _(language="en", item_id=""):

  # VALIDATE
  try:
    # Maybe the user enters a language that is not supported, then default to english
    # Use any key to see if the language is in the errors dictionary
    if f"{language}_server_error" not in x._errors : language = "en"
    item_id, error = x._is_uuid4(item_id, language)
    if error : return x._send(400, error)      

    allowed_keys = ["item_name", "item_price", "item_description"]
    for key in request.forms.keys():
      if not key in allowed_keys:
        print(key)
        return x._send(400, f"Forbidded key {key}")

  except Exception as ex:
    print(ex)
    return x._send(500, x._errors[f"{language}_server_error"])


  try:
    # Get the item to overwrite it with new data
    db = x._db_connect("database.sqlite")
    item = db.execute("SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()
    if not item: return x._send(204, "")
    # The item has been fetched from the db, now overwrite the fields with the new values
    for key in item.keys():
      if key in request.forms.keys():
        item[key] = request.forms.get(key)
    # Validate the newly updated item
    item_text, error = x._is_item_name(item["item_name"], language)
    if error : return x._send(400, error)
    item_price, error = x._is_item_price(item["item_price"], language)
    if error : return x._send(400, error)
    item_description, error = x._is_item_description(item["item_description"], language)
    if error : return x._send(400, error)
    # Update the field
    item["item_price"] = item_price
    item["item_updated_at"] = str(int(time.time()))
    now = datetime.now()
    item["item_updated_at_date"] = now.strftime("%Y-%B-%d-%A %H:%M:%S")
    # Save the item with its updated values
    counter = db.execute("""UPDATE items 
                  SET item_name=:item_name, 
                  item_price=:item_price,
                  item_description=:item_description,
                  item_updated_at =:item_updated_at,
                  item_updated_at_date = :item_updated_at_date 
                  WHERE item_id = :item_id""", item).rowcount
    db.commit()
    if not counter : return x._send(204, "")
    return item
  except Exception as ex:
    print(ex)
    return x._send(500, x._errors[f"{language}_server_error"])
  finally:
    db.close()