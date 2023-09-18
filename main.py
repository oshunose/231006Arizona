import shutil
import string
import sys

from database_helper import *

# IM ADDING CODE
# this will make the login attempts be unlimited and make it easier for testing for unlimited attempts right now
LOGIN_NUM_LIMIT = 1000000000
# END OF ADDITIONAL CODE
USER_NUM_LIMIT = 5
FEATURES = {
    "a": "Search for a job",
    "b": "Find someone you know",
    "c": "Learn a new skill",
}
SKILLS = ["Python", "Java", "C++", "JavaScript", "SQL"]

# IM ADDING CODE
limit_login = False
login_attempts = 0


# END OF ADDITIONAL CODE


def login():
    """Get username and password from user and check if they match a user in the database"""
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if check_login(username, password):
        print("You have successfully logged in")
        return username
    else:
        print("Incorrect username / password, please try again")
        # I'M ADDING CODE
        if try_again():
            return login()
        # END OF ADDITIONAL CODE


def signup():
    """Signup a new user if the username is not already taken and password meets requirements"""
    # ADDITIONAL CODE
    db_num_users = get_num_of_users()
    num_users = check_five_users(db_num_users)
    if num_users == 1:
        return None
    # ADDITIONAL CODE END

    username = input("Enter your username: ").strip()
    if does_username_exist(username):
        print("Username already exists, please try again")
        return signup()

    print(
        """Password must be 8-12 characters long and contain at least \
          one uppercase letter, one digit, and one special character"""
    )

    # ADDITIONAL CODE
    password_in = input("Enter your password: ").strip()

    password = validate_password(password_in)
    while password is None:
        password_in = input("Enter your password: ").strip()
        password = validate_password(password_in)
    # ADDITIONAL CODE END

    if create_user(username, password):
        print("Signup successful!")
        return username
    else:
        print("Username already exists, please try again")
        return signup()


# ADDITIONAL CODE
def check_five_users(num_users):
    if num_users == USER_NUM_LIMIT:
        print("All permitted accounts have been created, please come back later")
        return 1
    return 2


def validate_password(input_p):
    if not (
        8 <= len(input_p) <= 12
        and any(char.isupper() for char in input_p)
        and any(char.isdigit() for char in input_p)
        and any(char in string.punctuation for char in input_p)
    ):
        print("Password does not meet requirements, please try again")
        return None
    return input_p


# ADDITIONAL CODE END


def choose_features(username):
    """Display features and get user's choice"""
    draw_line(message="Features")
    print(f"Hi {username}! What would you like do?")
    for key, value in FEATURES.items():
        print(f"{key}. {value}")
    feature_choice = input(f"Choose one of {list(FEATURES.keys())}: ").strip().lower()

    if feature_choice in FEATURES:
        print(f"You selected {FEATURES[feature_choice]}")
        return feature_choice
    else:
        print("Feature ID not identied. Please try again")
        return choose_features(username)


def feature_direct(feature_choice, username):
    """Direct user to the feature they chose"""
    if feature_choice == "a":
        job_search(username)
    elif feature_choice == "b":
        friend_search(username)
    elif feature_choice == "c":
        learn_skill(username)


def job_search(username):
    """Job search page"""
    draw_line(message=FEATURES["a"])
    print("under construction")
    if go_back():
        feature_choice = choose_features(username)
        feature_direct(feature_choice, username)


def friend_search(username):
    """Friend search page"""
    draw_line(message=FEATURES["b"])
    print("under construction")
    if go_back():
        feature_choice = choose_features(username)
        feature_direct(feature_choice, username)


def learn_skill(username):
    """Learn skill page"""
    draw_line(message=FEATURES["c"])

    print("Here are some skills you can learn:")
    for i, skill in enumerate(SKILLS):
        print(f"{i + 1}. {skill}")

    # I'M ADDING CODE
    print("6. Go back")

    skill_choice = input(f"Enter integers from 1 to {len(SKILLS) + 1}: ").strip()
    if skill_choice.isdigit() and 1 <= int(skill_choice) <= len(SKILLS):
        single_skill(username, int(skill_choice))
    elif skill_choice.isdigit() and int(skill_choice) == 6:
        print("Not picking to learn a new skill?")
        if go_back():
            feature_choice = choose_features(username)
            feature_direct(feature_choice, username)
    # END OF ADDITIONAL CODE
    else:
        print("Invalid input, please try again")
        learn_skill(username)


def single_skill(username, skill_choice):
    """Learn skill page"""
    draw_line(message=SKILLS[skill_choice - 1])

    print("under construction")

    if go_back():
        learn_skill(username)


# ADDITIONAL CODE
def options(input_d):
    if input_d in ["S", "L"]:
        return input_d
    print("Invalid input, please try again")
    return None


# ADDITIONAL CODE END


def main_entry():
    """Welcome page and get the user into the system through login or signup"""
    draw_line(message="In College")
    print("Welcome to InCollege! Would you like to sign up or log in?")

    # ADDITIONAL CODE
    decision_in = input("Enter S to sign up or L to log in: ").strip().upper()
    decision = options(decision_in)
    while decision is None:
        decision_in = input("Enter S to sign up or L to log in: ").strip().upper()
        decision = options(decision_in)
    return decision
    # ADDITIONAL CODE END


def go_back():
    """Ask user if they want to go back to the previous page"""
    decision = input("Do you want to go back (Y / N)? ").strip().upper()
    if decision == "Y":
        return True
    elif decision == "N":
        return False
    else:
        print("Invalid input, please try again")
        go_back()


# I'M ADDING CODE
def change_limit_login():
    global limit_login
    global login_attempts
    if login_attempts > LOGIN_NUM_LIMIT:
        limit_login = True
    else:
        login_attempts += 1
    return limit_login


def try_again():
    """Ask user if they want to try to login again after failed attempt. Currently the user has unlimited attempts to try again"""
    decision = input("Do you want to try again (Y / N)? ").strip().upper()
    limit = change_limit_login()
    if decision == "Y" and limit == False:
        return True
    elif decision == "Y" and limit == True:
        print("Ran out of attempts! Try again later")
        return False
    elif decision == "N":
        return False
    else:
        print("Invalid input, please try again")
        try_again()


# END OF ADDIRIONAL CODE


# HELPERS
def draw_line(message):
    """Draw a line with the message in the middle. The line dynamically adjusts to the terminal width"""
    terminal_width, _ = shutil.get_terminal_size()
    print()
    print("-" * terminal_width)
    print(message.upper())
    print("-" * terminal_width)


def main():
    """Main function that controls the flow of the program"""
    decision = main_entry()

    username = None
    while decision is None:
        decision = main_entry()
    if decision == "S":
        username = signup()
    elif decision == "L":
        username = login()

    if username is None:
        sys.exit()

    feature_choice = choose_features(username)
    feature_direct(feature_choice, username)

    print("Thank you for using InCollege!")
    draw_line(message="End of Program")


if __name__ == "__main__":
    main()
