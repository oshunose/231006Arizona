import sqlite3

conn = sqlite3.connect("account.db")
c = conn.cursor()

# Create accounts table if it doesn't already exist
c.execute(
    """CREATE TABLE IF NOT EXISTS accounts (

          user text,
          pass text

          )"""
)


def create_user(username, password):
    """Returns True if the user was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username and password into database
            c.execute(
                "INSERT INTO accounts VALUES (:user, :pass)",
                {"user": username, "pass": password},
            )
        return True
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return False


def does_username_exist(username):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE user=:user", {"user": username})
    user_entry = c.fetchone()
    return user_entry is not None


def check_login(username, password):
    """Returns True if the username and password match a user in the database, False otherwise"""
    c.execute(
        "SELECT * FROM accounts WHERE user=:user AND pass=:pass",
        {"user": username, "pass": password},
    )
    accEntry = c.fetchone()
    return accEntry is not None


def get_num_of_users():
    """Returns the number of users in the database"""
    c.execute("SELECT COUNT(*) FROM accounts")
    result = c.fetchone()
    if result:
        return result[0]  # Extract the count from the result
    else:
        return 0  # Return 0 if there are no users in the database
