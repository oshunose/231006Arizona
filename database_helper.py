import sqlite3

conn = sqlite3.connect("account.db")
c = conn.cursor()

# Create accounts table if it doesn't already exist
c.execute(
    """CREATE TABLE IF NOT EXISTS accounts (

          user text,
          pass text,
          first text,
          last text,
          university text,
          major text

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

c.execute(
    """CREATE TABLE IF NOT EXISTS friends (
    
          user text,
          friend_user text

          )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS friends_list (

          user text,
          friend_user text

          )"""
)


def create_user(username, password, first, last, university, major):
    """Returns True if the user was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO accounts VALUES (:user, :pass, :first, :last, :university, :major)",
                {"user": username, "pass": password, "first": first, "last": last, "university": university,
                 "major": major},
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add user into sqlite table:", error)
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
        print("Failed to add job into sqlite table:", error)
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


def add_friend(username, friend_username):
    """Returns True if the friend was successfully added into the database, False otherwise"""
    try:
        with conn:
            c.execute("INSERT INTO friends VALUES (:user, :friend_user)",
                      {"user": username, "friend_user": friend_username})
        return True
    except sqlite3.Error as error:
        print("Failed to add friend to the sqlite table:", error)
        return False


def search_name(firstname, lastname):
    """Returns True if the username already exists in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE first=:first AND last=:last",
              {"first": firstname, "last": lastname})
    user_entry = c.fetchone()
    return user_entry is not None


def get_username_from_last_name(lastname):
    """Returns the username is found with friend's last name in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE last=:last", {"last": lastname})
    user_entry = c.fetchone()
    if user_entry:
        return user_entry[0]
    else:
        return False


def get_username_from_university(university):
    """Returns the username is found with friend's university in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE university=:university", {"last": university})
    user_entry = c.fetchone()
    if user_entry:
        return user_entry[0]
    else:
        return False


def get_username_from_major(major):
    """Returns the username is found with friend's major in the database, False otherwise"""
    c.execute("SELECT * FROM accounts WHERE major=:major", {"major": major})
    user_entry = c.fetchone()
    if user_entry:
        return user_entry[0]
    else:
        return False


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


def does_friend_request_match(username, friend_username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute("SELECT * FROM friends WHERE user=:user AND friend_user=:friend_user",
              {"user": friend_username, "friend_user": username})
    user_entry = c.fetchone()
    if user_entry:
        return True
    else:
        return False


def pending_friend_request_list(username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute("SELECT * FROM friends WHERE friend_user=:friend_user", {"friend_user": username})
    user_entry = c.fetchall()

    if user_entry:
        return user_entry
    else:
        return False


def add_to_friend_list(username, friend_username):
    """Returns True if the friend was successfully added into the database, False otherwise"""
    try:
        with conn:
            c.execute("INSERT INTO friends_list VALUES (:user, :friend_user)",
                      {"user": username, "friend_user": friend_username})
            c.execute("INSERT INTO friends_list VALUES (:user, :friend_user)",
                      {"user": friend_username, "friend_user": username})
        return True
    except sqlite3.Error as error:
        print("Failed to add friend to the sqlite table:", error)
        return False


def delete_friend_request(username, friend_username):
    """Returns True if the friend was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the friend with the provided username
            c.execute(
                "DELETE FROM friends WHERE user = ? AND friend_user = ?", (friend_username, username,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete user from the sqlite table:", error)
        return False


def list_of_friends(username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute("SELECT * FROM friends_list WHERE user=:user", {"user": username});
    user_entry = c.fetchall()

    if user_entry:
        return user_entry
    else:
        return False


def does_friend_match(username, friend_username):
    """Returns friend username if the username already exists in the friends, False otherwise"""
    c.execute("SELECT * FROM friends_list WHERE user=:user AND friend_user=:friend_user",
              {"user": username, "friend_user": friend_username})
    user_entry = c.fetchone()
    if user_entry:
        return True
    else:
        return False


def delete_friend_from_list(username, friend_username):
    """Returns True if the friend was successfully deleted, False otherwise"""
    try:
        with conn:
            # Delete the friend with the provided username
            c.execute(
                "DELETE FROM friends_list WHERE user = ? AND friend_user = ?", (friend_username, username,))
            c.execute(
                "DELETE FROM friends_list WHERE user = ? AND friend_user = ?", (username, friend_username,))
        return True
    except sqlite3.Error as error:
        print("Failed to delete user from the sqlite table:", error)
        return False


