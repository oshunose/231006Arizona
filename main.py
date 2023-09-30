import shutil
import string
import sys
import time

from database_helper import *

# this will make the login attempts be unlimited and make it easier for testing for unlimited attempts right now
LOGIN_NUM_LIMIT = 1000000000
USER_NUM_LIMIT = 5


FEATURES = {
    "a": "Search for a job",
    "b": "Find someone you know",
    "c": "Learn a new skill",
    "d": "Go to Navigation Links",
}

JOB_OPTIONS = {
    "a": "Post a job",
    "b": "Go back",
}

FRIEND_OPTIONS = {
    "a": "Find by first and last name",
    "b": "Go back",
}

NAVIGATION_LINKS_GROUP = {
    "a": "Useful Links",
    "b": "InCollege Important Links",
    "c": "Go back",
}

USEFUL_LINKS_GROUP = {
    "a": "General",
    "b": "Browse InCollege",
    "c": "Business Solutions",
    "d": "Directories",
    "e": "Go back",
}

INCOLLEGE_IMPORTANT_LINKS_GROUP = {
    "a": "A Copyright Notice",
    "b": "About",
    "c": "Accessibility",
    "d": "User Agreement",
    "e": "Privacy Policy",
    "f": "Cookie Policy",
    "g": "Copyright Policy",
    "h": "Brand Policy",
    "i": "Guest Controls",
    "j": "Languages",
    "k": "Go back",
}

NOT_SIGNED_IN_GENERAL_LINKS_GROUP = {
    "a": "Sign Up",
    "b": "Help Center",
    "c": "About",
    "d": "Press",
    "e": "Blog",
    "f": "Careers",
    "g": "Developers",
    "h": "Go back",
}

SIGNED_IN_GENERAL_LINKS_GROUP = {
    "a": "Help Center",
    "b": "About",
    "c": "Press",
    "d": "Blog",
    "e": "Careers",
    "f": "Developers",
    "g": "Go back",
}

SKILLS = ["Python", "Java", "C++", "JavaScript", "SQL"]


limit_login = False
login_attempts = 0
signed_in = False


def prompt_person_search():
    """Ask user if they want to search for someone before logging in"""
    decision = (
        input("Before logging in, Do you want to look for someone (Y / N)? ")
        .strip()
        .upper()
    )

    if decision == "Y":
        name_search()
    elif decision == "N":
        return False
    else:
        print("Invalid input, please try again")
        prompt_person_search()


def login():
    """Get username and password from user and check if they match a user in the database"""
    draw_line(message="Login")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if check_login(username, password):
        print("You have successfully logged in")
        global signed_in
        signed_in = True
        return username
    else:
        print("Incorrect username / password, please try again")
        if try_again():
            return login()


def signup():
    """Signup a new user if the username is not already taken and password meets requirements"""
    db_num_users = get_num_of_users()
    if reached_user_limit(db_num_users):
        return None
    draw_line(message="Sign Up")
    username = input("Enter your username: ").strip()
    if does_username_exist(username):
        print("Username already exists, please try again")
        return signup()

    print(
        """Password must be 8-12 characters long and contain at least \
          one uppercase letter, one digit, and one special character"""
    )

    password_in = input("Enter your password: ").strip()

    password = validate_password(password_in)
    while password is None:
        password_in = input("Enter your password: ").strip()
        password = validate_password(password_in)

    firstname = input("Please insert your first name: ")
    lastname = input("Please insert your last name: ")

    if create_user(username, password, firstname, lastname):
        print("Signup successful!")
        global signed_in 
        signed_in = True
        return username
    else:
        print("Username already exists, please try again")
        return signup()


def reached_job_limit(num_jobs):
    """Check if jobs are as many as users"""
    if num_jobs >= USER_NUM_LIMIT:
        print("All permitted jobs have been created, please come back later")
        return True
    return False


def reached_user_limit(num_users):
    """Check if users are as many as permitted"""
    if num_users == USER_NUM_LIMIT:
        print("All permitted accounts have been created, please come back later")
        return True
    return False


def validate_password(input_p):
    """Check if password meets requirements"""
    if not (
        8 <= len(input_p) <= 12
        and any(char.isupper() for char in input_p)
        and any(char.isdigit() for char in input_p)
        and any(char in string.punctuation for char in input_p)
    ):
        print("Password does not meet requirements, please try again")
        return None
    return input_p


def choose_features(username):
    """Display features and get user's choice"""
    draw_line(message="Features")
    print(f"Hi {username}! What would you like do?")
    for key, value in FEATURES.items():
        print(f"{key}. {value}")
    feature_choice = input(f"Choose one of {list(FEATURES.keys())}: ").strip().lower()

    if feature_choice in FEATURES:
        print(f"You selected {FEATURES[feature_choice]}")
        feature_direct(feature_choice, username)
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
    elif feature_choice == "d":
        choose_navigation_link()


def job_search(username):
    """Job search page"""
    draw_line(message="JOB_OPTIONS")
    print("What would you like to do with jobs?")
    for key, value in JOB_OPTIONS.items():
        print(f"{key}. {value}")
    feature_choice = input(f"Choose one of {list(JOB_OPTIONS.keys())}:").strip().lower()

    if feature_choice == "a":
        job_posting(username)
    elif feature_choice == "b":
        if go_back():
            choose_features(username)


def job_posting(username):
    """Post a job page"""
    db_num_jobs = get_num_of_jobs()
    if reached_job_limit(db_num_jobs):
        return None

    draw_line(message="JOB_POSTING")

    job_title = input("Please enter the job's title: ")
    job_description = input("Please enter the job's description: ")
    job_employer = input("Please enter the job's employer: ")
    job_location = input("Please enter the job's location: ")
    job_salary = input("Please enter the job's salary: ")

    create_job(
        job_title,
        job_description,
        job_employer,
        job_location,
        job_salary,
        get_first_name(username),
        get_last_name(username),
    )

    print(
        "\nJob created: Thank You for posting. We hope you'll find great employees!\n"
    )

    choose_features(username)


def friend_search(username):
    """Friend search page"""
    draw_line(message="FRIEND_SEARCH")
    print("How would you like to search for friends?")
    for key, value in FRIEND_OPTIONS.items():
        print(f"{key}. {value}")
    feature_choice = (
        input(f"Choose one of {list(FRIEND_OPTIONS.keys())}:").strip().lower()
    )

    if feature_choice == "a":
        name_search()
        choose_features(username)
    elif feature_choice == "b":
        if go_back():
            choose_features(username)


def name_search():
    """name search page"""
    draw_line(message="NAME_SEARCH")

    friend_firstname = input("Please enter your friend's first name: ")
    friend_lastname = input("Please enter your friend's last name: ")

    result = search_name(friend_firstname, friend_lastname)

    if result:
        print(
            f"\n{friend_firstname} {friend_lastname} is an existing user on inCollege."
        )
    else:
        print(
            f"\n{friend_firstname} {friend_lastname} is not yet an existing user on inCollege."
        )


def learn_skill(username):
    """Learn skill page"""
    draw_line(message=FEATURES["c"])

    print("Here are some skills you can learn:")
    for i, skill in enumerate(SKILLS):
        print(f"{i + 1}. {skill}")

    print("6. Go back")

    skill_choice = input(f"Enter integers from 1 to {len(SKILLS) + 1}: ").strip()
    if skill_choice.isdigit() and 1 <= int(skill_choice) <= len(SKILLS):
        single_skill(username, int(skill_choice))
    elif skill_choice.isdigit() and int(skill_choice) == 6:
        print("Not picking to learn a new skill?")
        if go_back():
            choose_features(username)
    else:
        print("Invalid input, please try again")
        learn_skill(username)


def single_skill(username, skill_choice):
    """Learn skill page"""
    draw_line(message=SKILLS[skill_choice - 1])

    print("under construction")

    if go_back():
        learn_skill(username)


def options(input_d):
    if input_d in ["S", "L"]:
        return input_d
    print("Invalid input, please try again")
    return None


def choose_navigation_link():
    """Display navigation links and get user's choice"""
    draw_line(message="Navigation Links")
    print("What link would you like to go to?")
    for key, value in NAVIGATION_LINKS_GROUP.items():
        print(f"{key}. {value}")
    navigation_link_choice = input(f"Choose one of {list(NAVIGATION_LINKS_GROUP.keys())}: ").strip().lower()

    if navigation_link_choice in NAVIGATION_LINKS_GROUP:
        print(f"You selected {NAVIGATION_LINKS_GROUP[navigation_link_choice]}")
        navigation_link_direct(navigation_link_choice)
    else:
        print("Link not identfied. Please try again")
        return choose_navigation_link()
    

def navigation_link_direct(navigation_link_choice, username="test"):
    """Direct user to the naviagation link they chose"""
    if navigation_link_choice == "a":
        choose_useful_links()
    elif navigation_link_choice == "b":
        choose_incollege_important_links()
    elif navigation_link_choice == "c":
        if go_back():
            if signed_in == True:
                choose_features(username)
            else:
                links_or_login()


def choose_useful_links():
    """Display useful links and get user's choice"""
    draw_line(message="Useful Links")
    print("What link would you like to go to?")
    for key, value in USEFUL_LINKS_GROUP.items():
        print(f"{key}. {value}")
    useful_link_choice = input(f"Choose one of {list(USEFUL_LINKS_GROUP.keys())}: ").strip().lower()

    if useful_link_choice in USEFUL_LINKS_GROUP:
        print(f"You selected {USEFUL_LINKS_GROUP[useful_link_choice]}")
        useful_link_direct(useful_link_choice)
    else:
        print("Link not identfied. Please try again")
        return choose_useful_links()


def useful_link_direct(useful_link_choice):
    """Direct user to the useful link they chose"""
    if useful_link_choice == "a":
        general()
    elif useful_link_choice == "b":
        browse_incollege()
    elif useful_link_choice == "c":
        business_solutions()
    elif useful_link_choice == "d":
        directories()
    elif useful_link_choice == "e":
        if go_back():
            choose_navigation_link()


def general():
    """Display general links and get user's choice"""
    draw_line(message="General")
    print("What link would you like to go to?")
    global signed_in
    if signed_in == False:
        for key, value in NOT_SIGNED_IN_GENERAL_LINKS_GROUP.items():
            print(f"{key}. {value}")
        general_link_choice = input(f"Choose one of {list(NOT_SIGNED_IN_GENERAL_LINKS_GROUP.keys())}: ").strip().lower()

        if general_link_choice in NOT_SIGNED_IN_GENERAL_LINKS_GROUP:
            print(f"You selected {NOT_SIGNED_IN_GENERAL_LINKS_GROUP[general_link_choice]}")
            return non_signed_in_general_direct(general_link_choice)
        else:
            print("Link not identfied. Please try again")
            return general()
    else:
        for key, value in SIGNED_IN_GENERAL_LINKS_GROUP.items():
            print(f"{key}. {value}")
        general_link_choice = input(f"Choose one of {list(SIGNED_IN_GENERAL_LINKS_GROUP.keys())}: ").strip().lower()

        if general_link_choice in SIGNED_IN_GENERAL_LINKS_GROUP:
            print(f"You selected {SIGNED_IN_GENERAL_LINKS_GROUP[general_link_choice]}")
            return signed_in_general_direct(general_link_choice)
        else:
            print("Link not identfied. Please try again")
            return general()



def non_signed_in_general_direct(general_link_choice):
    """Direct user to the general link they chose if not signed in"""
    if general_link_choice == "a":
        main_helper()
    elif general_link_choice == "b":
        help_center()
    elif general_link_choice == "c":
        about()
    elif general_link_choice == "d":
        press()
    elif general_link_choice == "e":
        blog()
    elif general_link_choice == "f":
        careers()
    elif general_link_choice == "g":
        developers()
    elif general_link_choice == "h":
        if go_back():
            choose_useful_links()


def signed_in_general_direct(general_link_choice):
    """Direct user to the general link they chose if signed in"""
    if general_link_choice == "a":
        help_center()
    elif general_link_choice == "b":
        about()
    elif general_link_choice == "c":
        press()
    elif general_link_choice == "d":
        blog()
    elif general_link_choice == "e":
        careers()
    elif general_link_choice == "f":
        developers()
    elif general_link_choice == "g":
        if go_back():
            choose_useful_links()


def help_center():
    """Browse Help Center page"""
    draw_line(message="Help Center")

    print("We're here to help")

    if go_back():
        general()


def about():
    """Browse About page"""
    draw_line(message="Press")

    print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")

    if go_back():
        general()


def press():
    """Browse Press page"""
    draw_line(message="Press")

    print("In College Pressroom: Stay on top of the latest news, updates, and reports")

    if go_back():
        general()


def blog():
    """Browse Blog page"""
    draw_line(message="Blog")

    print("Under construction")

    if go_back():
        general()


def careers():
    """Browse Careers page"""
    draw_line(message="Careers")

    print("Under construction")

    if go_back():
        general()


def developers():
    """Browse Developers page"""
    draw_line(message="Developers")

    print("Under construction")

    if go_back():
        general()


def browse_incollege():
    """Browse InCollege page"""
    draw_line(message="Browse InCollege")

    print("Under construction")

    if go_back():
        choose_useful_links()


def business_solutions():
    """Business Solutions page"""
    draw_line(message="Business Solutions")

    print("Under construction")

    if go_back():
        choose_useful_links()


def directories():
    """Directories page"""
    draw_line(message="Directories")

    print("Under construction")

    if go_back():
        choose_useful_links()
    

def choose_incollege_important_links():
    print("add code here")
    

def main_entry():
    """Welcome page and get the user into the system through login or signup"""
    draw_line(message="In College")
    print("Welcome to InCollege! Would you like to sign up or log in?")

    decision_in = input("Enter S to sign up or L to log in: ").strip().upper()
    decision = options(decision_in)
    while decision is None:
        decision_in = input("Enter S to sign up or L to log in: ").strip().upper()
        decision = options(decision_in)
    return decision


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


def change_limit_login():
    """Determine if the user has exceeded the number of login attempts"""
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


# HELPERS
def draw_line(message):
    """Draw a line with the message in the middle. The line dynamically adjusts to the terminal width"""
    terminal_width, _ = shutil.get_terminal_size()
    print()
    print("-" * terminal_width)
    print(message.upper())
    print("-" * terminal_width)


def web_opening():
    """Opening page for the web application"""
    print(
        '"I found making a career difficult, but thanks to inCollege: I was able to find the help that I needed!" - Hoff Reidman\n'
    )

    video_prompt = input("Would you like to watch their story (Y/N)? ")

    if video_prompt == "y" or video_prompt == "Y":
        print("Video is now playing...\n")
        time.sleep(5)
        print("Video is complete.\n")


def links_or_login():
    """Prompts user to either use the navigation links or to login page"""
    links_prompt = input("Do you want to navigate and explore InCollege while logged out (Y/N)? ")

    if links_prompt == "y" or links_prompt == "Y":
        choose_navigation_link()


def main_helper():
    decision = main_entry()

    username = None
    while decision is None:
        decision = main_entry()
    if decision == "S":
        username = signup()
    elif decision == "L":
        prompt_person_search()
        username = login()

    if username is None:
        sys.exit()

    choose_features(username)

    print("Thank you for using InCollege!")
    draw_line(message="End of Program")
    exit()


def main():
    """Main function that controls the flow of the program"""

    web_opening()
    links_or_login()
    main_helper()


if __name__ == "__main__":
    main()
