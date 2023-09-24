import sqlite3

conn = sqlite3.connect("account.db")
c = conn.cursor()

# Create accounts table if it doesn't already exist
c.execute(
    """CREATE TABLE IF NOT EXISTS accounts (

          user text,
          pass text,
          first text,
          last text

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS jobs (

          title text,
          description text,
          employer text,
          location text,
          salary text,
          first text,
          last text

          )"""
)


def create_user(username, password, first, last):
    """Returns True if the user was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO accounts VALUES (:user, :pass, :first, :last)",
                {"user": username, "pass": password, "first": first, "last": last},
            )
        return True
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return False


def delete_user(username):
    """Returns True if the user was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the user with the provided username
            c.execute(
                "DELETE FROM accounts WHERE user = ?", (username,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete user from the sqlite table:", error)
        return False


def does_username_exist(username):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE user=:user", {"user": username})
    user_entry = c.fetchone()
    return user_entry is not None


def create_job(title, description, employer, location, salary, first, last):
    """Returns True if the user was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO jobs VALUES (:title, :description, :employer, :location,:salary, :first, :last)",
                {"title": title, "description": description, "employer": employer,
                    "location": location, "salary": salary, "first": first, "last": last},
            )
        return True
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return False


def delete_job(title):
    """Returns True if the job was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the job with the provided title
            c.execute("DELETE FROM jobs WHERE title = ?", (title,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete job from the sqlite table:", error)
        return False


def search_name(firstname, lastname):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE first=:first AND last=:last",
              {"first": firstname, "last": lastname})
    user_entry = c.fetchone()
    return user_entry is not None


def get_first_name(username):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE user=:user", {"user": username})
    user_entry = c.fetchone()
    return user_entry[2]


def get_last_name(username):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE user=:user", {"user": username})
    user_entry = c.fetchone()
    return user_entry[3]


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


def get_num_of_jobs():
    """Returns the number of users in the database"""
    c.execute("SELECT COUNT(*) FROM jobs")
    result = c.fetchone()
    if result:
        return result[0]  # Extract the count from the result
    else:
        return 0  # Return 0 if there are no users in the database
