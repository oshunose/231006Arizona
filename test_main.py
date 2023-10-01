from unittest.mock import Mock, patch

from main import *

# will connect to database, use these values for testing
# username: testuser
# password: ValidPass1!
# first name: Test
# last name: User


# Test 1: Test whether main_entry() reads user's input correctly
# with test cases = ['g', 'G', 'ss', '1', '$', 's', 'l'] all should fail
# with test cases = ['S', 'L'] all should pass
def test_options_success():
    input_tests = ["S", "L"]
    for i in input_tests:
        entry = options(i)
        assert entry is not None


def test_options_fail():
    input_tests = ["g", "G", "ss", "1", "$", "s", "l"]
    for i in input_tests:
        entry = options(i)
        assert entry is None


def test_five_acc_made_fail():
    """check if the number of users reached the limit of 5"""
    assert reached_user_limit(5) is True


def test_five_acc_made_success():
    """check that the number of users is less than 5"""
    for i in range(0, 5):
        assert reached_user_limit(i) is False


# test 3: Error message when 6th account is created
def test_error_message_for_sixth_acc_success(capsys):
    reached_user_limit(5)
    captured = capsys.readouterr()
    assert (
        "All permitted accounts have been created, please come back later"
        in captured.out
    )


def test_error_message_for_sixth_acc_fail(capsys):
    for i in range(0, 5):
        reached_user_limit(i)
        captured = capsys.readouterr()
        assert (
            "All permitted accounts have been created, please come back later"
            not in captured.out
        )


# test 4: Secure password
# all cases should pass this test which means the passwords were invalid in main
def test_validate_password_fails():
    password_list = [
        "Games1$",  # less than 8 characters
        "Games&cats123",  # more than 12 characters
        "games&cats12",  # no capitalized character
        "Games&cats$#",  # no digits
        "Games3cats47",  # no special characters
    ]
    for i in password_list:
        password = validate_password(i)
        assert password is None


# all cases should pass this test which means the passwords were valid in main
def test_validate_password_success():
    password_list = [
        "Gamess&1",  # 8 character success
        "Gamess&12",  # 9 character success
        "Gamess&123",  # 10 character success
        "Gamess&1234",  # 11 character success
        "Gamess&12345",  # 12 character success
    ]
    for i in password_list:
        password = validate_password(i)
        assert password is not None


"---------------------------------------------------------------------------"


def mock_success_input(prompt):
    if "Enter your username: " in prompt:
        return "testuser"
    elif "Enter your password: " in prompt:
        return "ValidPass1!"


def mock_failed_input(prompt):
    if "Enter your username: " in prompt:
        return "usernotindb"
    elif "Enter your password: " in prompt:
        return "invalidpassword"
    elif "Do you want to try again (Y / N)? " in prompt:
        return "N"


def mock_try_again_input(prompt):
    if "Do you want to try again (Y / N)? " in prompt:
        return "Y"


def mock_features_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd']: " in prompt:
        return "a"
    if "Choose one of ['a', 'b']:" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_go_back_input(prompt):
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_learn_skill_input(prompt):
    if "Enter integers from 1 to 6: " in prompt:
        return "1"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def mock_no_selected_skill_input(prompt):
    if "Enter integers from 1 to 6: " in prompt:
        return "6"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_successful_login(monkeypatch, capsys):
    # Mock user input for successful login
    create_user("testuser", "ValidPass1!", "Test", "User")
    monkeypatch.setattr("builtins.input", mock_success_input)

    # Call the login function
    username = login()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output and username
    assert "You have successfully logged in" in captured.out
    assert username == "testuser"


def test_failed_login(monkeypatch, capsys):
    # Mock user input for failed login
    monkeypatch.setattr("builtins.input", mock_failed_input)

    # Call the login function
    login()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Incorrect username / password, please try again" in captured.out
    assert try_again() is False


def test_unlimited_logins(monkeypatch):
    # Mock user input for try_again function
    monkeypatch.setattr("builtins.input", mock_try_again_input)

    # Call the try_again function and assert the expected output
    assert try_again() is True


def test_features(monkeypatch, capsys):
    # Mock user input for choose_features function
    monkeypatch.setattr("builtins.input", mock_features_input)

    # Call the choose_features function
    choose_features("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Search for a job" in captured.out
    assert "b. Find someone you know" in captured.out
    assert "c. Learn a new skill" in captured.out
    assert "d. Go to Navigation Links" in captured.out


def test_learn_skill(monkeypatch, capsys):
    # Mock user input for learn_skill function
    monkeypatch.setattr("builtins.input", mock_learn_skill_input)

    # Call the learn_skill function
    learn_skill("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "1. Python" in captured.out
    assert "2. Java" in captured.out
    assert "3. C++" in captured.out
    assert "4. JavaScript" in captured.out
    assert "5. SQL" in captured.out
    assert "6. Go back" in captured.out


def test_no_selected_skill(monkeypatch, capsys):
    # Mock user input for no selected skill
    monkeypatch.setattr("builtins.input", mock_no_selected_skill_input)

    # Call the learn_skill function
    learn_skill("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Not picking to learn a new skill?" in captured.out


"-----------------------------EPIC 2 Tests------------------------------------------"


def mock_watch_video(prompt):
    if "Would you like to watch their story (Y/N)? " in prompt:
        return "Y"


def mock_not_watch_video(prompt):
    if "Would you like to watch their story (Y/N)? " in prompt:
        return "N"


def mock_name_search_success(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "Test"
    elif "Please enter your friend's last name: " in prompt:
        return "User"


def mock_name_search_fail(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "Test"
    elif "Please enter your friend's last name: " in prompt:
        return "NotUser"


def mock_signup(prompt):
    if "Enter your username: " in prompt:
        return "anothertestuser"
    elif "Enter your password: " in prompt:
        return "ValidPass1!"
    elif "Please insert your first name: " in prompt:
        return "anotherTest"
    elif "Please insert your last name: " in prompt:
        return "anotherUser"


def test_signup(monkeypatch, capsys):
    # Mock user input for successful signup
    monkeypatch.setattr("builtins.input", mock_signup)

    # Call the signup function
    signup()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Signup successful!" in captured.out
    assert delete_user("anothertestuser") is True


def test_name_search_success(monkeypatch, capsys):
    create_user("testuser", "ValidPass1!", "Test", "User")
    # Mock user input for successful name search
    monkeypatch.setattr("builtins.input", mock_name_search_success)

    # Call the name_search function
    name_search()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Test User is an existing user on inCollege." in captured.out


def test_name_search_fail(monkeypatch, capsys):
    # Mock user input for failed name search
    monkeypatch.setattr("builtins.input", mock_name_search_fail)

    # Call the name_search function
    name_search()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Test NotUser is not yet an existing user on inCollege." in captured.out


def test_watch_video(monkeypatch, capsys):
    # Mock user input for watching the video
    monkeypatch.setattr("builtins.input", mock_watch_video)

    # Call the web_opening function
    web_opening()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Video is now playing..." in captured.out


def test_not_watch_video(monkeypatch, capsys):
    # Mock user input for not watching the video
    monkeypatch.setattr("builtins.input", mock_not_watch_video)

    # Call the web_opening function
    web_opening()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Video is now playing..." not in captured.out


def friend_search_pass_input(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "Test"
    if "Please enter your friend's last name: " in prompt:
        return "User"


def friend_search_fail_input(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "test"
    if "Please enter your friend's last name: " in prompt:
        return "user"


def friend_search_fail_input_2(prompt):
    if "Please enter your friend's first name: " in prompt:
        return "jack"
    if "Please enter your friend's last name: " in prompt:
        return "mack"


def test_friend_search_pass(monkeypatch, capsys):
    create_user(username="testuser", password="ValidPass1!", first="Test", last="User")
    monkeypatch.setattr("builtins.input", friend_search_pass_input)
    name_search()
    captured = capsys.readouterr()
    assert "is an existing user on inCollege." in captured.out
    assert search_name("Test", "User") is True


def test_friend_search_fail_1(monkeypatch, capsys):
    create_user(username="testuser", password="ValidPass1!", first="Test", last="User")
    monkeypatch.setattr("builtins.input", friend_search_fail_input)
    name_search()
    captured = capsys.readouterr()

    assert "is not yet an existing user on inCollege." in captured.out
    assert search_name("test", "user") is False


def test_friend_search_fail_2(monkeypatch, capsys):
    create_user(username="testuser", password="ValidPass1!", first="Test", last="User")
    monkeypatch.setattr("builtins.input", friend_search_fail_input_2)
    name_search()
    captured = capsys.readouterr()

    assert "is not yet an existing user on inCollege." in captured.out
    assert search_name("test", "user") is False


def go_back_pass_input(prompt):
    if "Choose one of" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def go_back_learn_skill_pass_input(prompt):
    if "Enter integers from 1 to " in prompt:
        return "6"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_job_search_go_back(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", go_back_pass_input)
    job_search("testuser")
    captured = capsys.readouterr()
    assert "Go back" in captured.out


def test_friend_search_go_back(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", go_back_pass_input)
    friend_search("testuser")
    captured = capsys.readouterr()
    assert "Go back" in captured.out


def test_learn_skill_go_back(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", go_back_learn_skill_pass_input)
    learn_skill("testuser")
    captured = capsys.readouterr()
    assert "Go back" in captured.out


def test_check_five_jobs_pass(capsys):
    for i in range(0, 5):
        assert reached_job_limit(i) is False


def test_check_five_jobs_fail(capsys):
    assert reached_job_limit(5) is True
    captured = capsys.readouterr()
    assert (
        "All permitted jobs have been created, please come back later" in captured.out
    )


def create_job_pass_input(prompt):
    if "Please enter the job's title: " in prompt:
        return "Software Engineer"
    if "Please enter the job's description: " in prompt:
        return "Code accurate and fast software"
    if "Please enter the job's employer: " in prompt:
        return "Google"
    if "Please enter the job's location: " in prompt:
        return "Los Angeles, CA"
    if "Please enter the job's salary: " in prompt:
        return "$125,000"
    if "Choose one of" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


def test_create_job_pass(monkeypatch, capsys):
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    create_job(
        title="a",
        description="b",
        employer="c",
        location="d",
        salary="e",
        first="f",
        last="g",
    )
    monkeypatch.setattr("builtins.input", create_job_pass_input)
    job_posting("testuser")
    captured = capsys.readouterr()
    assert "JOB_POSTING" in captured.out
    assert (
        "title" or "description" or "employer" or "location" or "salary" in captured.out
    )
    assert "Failed to insert Python variable into sqlite table" not in captured.out
    assert (
        "\nJob created: Thank You for posting. We hope you'll find great employees!\n"
        in captured.out
    )
    assert delete_job("a") is True
    assert delete_job("Software Engineer") is True


"------------------ EPIC #3 ---------------------------------------------------"


def mock_choose_useful_links(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e']: " in prompt:
        return "a"


def test_choose_useful_links(monkeypatch, capsys):
    """Mock user input for useful_links function"""
    monkeypatch.setattr("builtins.input", mock_choose_useful_links)
    monkeypatch.setattr("main.useful_link_direct", Mock())

    # Call the useful_links function
    choose_useful_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. General" in captured.out
    assert "b. Browse InCollege" in captured.out
    assert "c. Business Solutions" in captured.out
    assert "d. Directories" in captured.out
    assert "e. Go back" in captured.out


def mock_general_signed_in(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g']: " in prompt:
        return "a"


@patch("main.signed_in", True)
def test_general_signed_in(monkeypatch, capsys):
    """Mock user input for general function"""
    monkeypatch.setattr("builtins.input", mock_general_signed_in)
    monkeypatch.setattr("main.signed_in_general_direct", Mock())

    # Call the general function
    general()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Help Center" in captured.out
    assert "b. About" in captured.out
    assert "c. Press" in captured.out
    assert "d. Blog" in captured.out
    assert "e. Careers" in captured.out
    assert "f. Developers" in captured.out
    assert "g. Go back" in captured.out


def mock_general_not_signed_in(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']: " in prompt:
        return "a"


@patch("main.signed_in", False)
def test_general_not_signed_in(monkeypatch, capsys):
    """Mock user input for general function"""
    monkeypatch.setattr("builtins.input", mock_general_not_signed_in)
    monkeypatch.setattr("main.non_signed_in_general_direct", Mock())

    # Call the general function
    general()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Sign Up" in captured.out
    assert "b. Help Center" in captured.out
    assert "c. About" in captured.out
    assert "d. Press" in captured.out
    assert "e. Blog" in captured.out
    assert "f. Careers" in captured.out
    assert "g. Developers" in captured.out
    assert "h. Go back" in captured.out


def test_help_center(monkeypatch, capsys):
    """Mock user input for help_center function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the help_center function
    help_center()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "We're here to help" in captured.out


def test_about(monkeypatch, capsys):
    """Mock user input for about function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the about function
    about()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
        in captured.out
    )


def test_press(monkeypatch, capsys):
    """Mock user input for press function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the press function
    press()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "In College Pressroom: Stay on top of the latest news, updates, and reports"
        in captured.out
    )


def test_blog(monkeypatch, capsys):
    """Mock user input for blog function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the blog function
    blog()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Under construction" in captured.out


def test_careers(monkeypatch, capsys):
    """Mock user input for careers function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the careers function
    careers()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Under construction" in captured.out


def test_developers(monkeypatch, capsys):
    """Mock user input for developers function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.general", Mock())
    # Call the developers function
    developers()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Under construction" in captured.out


def test_browse_incollege(monkeypatch, capsys):
    """Mock user input for browse_incollege function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.choose_useful_links", Mock())

    browse_incollege()

    captured = capsys.readouterr()

    assert "Under construction" in captured.out


def test_business_solutions(monkeypatch, capsys):
    """Mock user input for business_solutions function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.choose_useful_links", Mock())

    business_solutions()

    captured = capsys.readouterr()

    assert "Under construction" in captured.out


def test_directories(monkeypatch, capsys):
    """Mock user input for directories function"""
    monkeypatch.setattr("main.go_back", Mock())
    monkeypatch.setattr("main.choose_useful_links", Mock())

    directories()

    captured = capsys.readouterr()

    assert "Under construction" in captured.out


# Designed to mock the transition from navigation to imporant links
def mock_navi_to_important_input(prompt):
    if "Choose one of ['a', 'b', 'c']: " in prompt:
        return "b"
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "j"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the copyright notice option
def mock_copyright_notice_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "a"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the about option
def mock_about_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the accessibiltity option
def mock_accessibility_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "c"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the user agreement option
def mock_user_agreement_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "d"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the privacy policy option, and turning email off
def mock_privacy_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "e"
    if "Choose one of ['a', 'b', 'c']:" in prompt:
        return "a"
    if "Choose one of ['a', 'b']:" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the cookie policy option
def mock_cookie_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "f"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the copyright policy option
def mock_copyright_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "g"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the brand policy option
def mock_brand_policy_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "h"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock selecting the language option and changing it to spanish
def mock_language_input(prompt):
    if "Choose one of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']: " in prompt:
        return "i"
    if "Choose one of ['a', 'b']:" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock turning something on
def mock_turn_on_input(prompt):
    if "Choose one of ['a', 'b']:" in prompt:
        return "a"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Designed to mock turning something off
def mock_turn_off_input(prompt):
    if "Choose one of ['a', 'b']:" in prompt:
        return "b"
    if "Do you want to go back (Y / N)? " in prompt:
        return "N"


# Testing to see if navigation can move to important link, and print all the options
def test_navigation_to_important_link(monkeypatch, capsys):
    # Mock user input for choosing important link
    monkeypatch.setattr("builtins.input", mock_navi_to_important_input)

    # Call the choose navigation link function
    choose_navigation_link()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "a. Useful Links" in captured.out
    assert "b. InCollege Important Links" in captured.out
    assert "c. Go back" in captured.out

    assert "a. A Copyright Notice" in captured.out
    assert "b. About" in captured.out
    assert "c. Accessibility" in captured.out
    assert "d. User Agreement" in captured.out
    assert "e. Privacy Policy" in captured.out
    assert "f. Cookie Policy" in captured.out
    assert "g. Copyright Policy" in captured.out
    assert "h. Brand Policy" in captured.out
    assert "i. Languages" in captured.out
    assert "j. Go back" in captured.out


# Testing to see if the copyright notice text is printed
def test_copyright_notice(monkeypatch, capsys):
    # Mock user input for choosing copyright notice
    monkeypatch.setattr("builtins.input", mock_copyright_notice_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "© Team_Arizona_2023_forever" in captured.out
    assert "All rights reserved" in captured.out


# Testing to see if the about text is printed
def test_about(monkeypatch, capsys):
    # Mock user input for  choosing about
    monkeypatch.setattr("builtins.input", mock_about_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert (
        "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
        in captured.out
    )


# Testing to see if the accessibility text is printed
def test_accessibility(monkeypatch, capsys):
    # Mock user input for choosing accessibility
    monkeypatch.setattr("builtins.input", mock_accessibility_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected messages are printed
    assert (
        "We are committed to ensuring that our platform is accessible to all users,including those with disabilities. Here are some of the features we have implemented to enhance accessibility:"
        in captured.out
    )

    assert (
        "If you encounter any accessibility issues or have suggestions for improvement,please contact us at Team Arizona."
        in captured.out
    )


# Testing to see if the user agreement text is printed
def test_user_agreement(monkeypatch, capsys):
    # Mock user input for choosing user agreement
    monkeypatch.setattr("builtins.input", mock_user_agreement_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected messages are printed
    assert (
        "By using our platform, you agree to abide by the following terms and conditions: \n <Respect the rights of other users> \n <Do not engage in any unlawful activities on our platform.> \n <Abide by our community guidelines.> \n <Protect your account credentials and personal information.> \n <Report any suspicious or inappropriate content.> \n \n \n <Failure to comply with these terms may result in account suspension or termination.>"
        in captured.out
    )


# Testing to see if the privacy policy is printing the proper options
def test_privacy_policy(monkeypatch, capsys):
    # Mock user input for choosing privacy policy
    monkeypatch.setattr("builtins.input", mock_privacy_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Guest Controls" in captured.out
    assert "b. Go Back" in captured.out
    assert "a. Email" in captured.out
    assert "b. SMS" in captured.out
    assert "c. Target_Advertising" in captured.out
    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out


# Testing to see if the cookie policy text is printed
def test_cookie_policy(monkeypatch, capsys):
    # Mock user input for choosing cookie policy
    monkeypatch.setattr("builtins.input", mock_cookie_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert (
        "Our website uses cookies to improve your experience. By continuing to use our site, you accept our use of cookies."
        in captured.out
    )


# Testing to see if the copyright policy text is printed
def test_copyright_policy(monkeypatch, capsys):
    # Mock user input for choosing copyright policy
    monkeypatch.setattr("builtins.input", mock_copyright_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert (
        "All content on this platform is protected by copyright laws. The content includes but is not limited to text, images, logos, and graphics \n You may not reproduce, distribute, or modify our content without explicit written permission from us \n For copyright-related inquiries, please contact: legal@incollege.com."
        in captured.out
    )


# Testing to see if the brand policy text is printed
def test_brand_policy(monkeypatch, capsys):
    # Mock user input for choosing brand policy
    monkeypatch.setattr("builtins.input", mock_brand_policy_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert (
        "Our brand is a valuable asset, including our name, logo, and visual identity. To maintain consistency and integrity, we have established guidelines for the use of our brand elements. \n \n You may not use our brand elements without prior written permission. Any use must adhere to our brand guidelines \n \n If you require the use of our brand for any purpose, please contact us to request approval."
        in captured.out
    )


# Testing to see if the language options are presented and can change to spanish
def test_language_setting(monkeypatch, capsys):
    # Mock user input for choosing language options
    monkeypatch.setattr("builtins.input", mock_language_input)

    # Call the choose incollege important links function
    choose_incollege_important_links()

    # Capture the printed output
    captured = capsys.readouterr()

    assert "You selected Languages" in captured.out
    assert "a. English" in captured.out
    assert "b. Spanish" in captured.out
    assert (
        "Congratulations, the app language has been changed to Spanish" in captured.out
    )


# Testing to see if email is turned on
def test_turn_on_email(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_on_input)

    # Call the turn on and off function
    change = turn_on_off("a")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 1


# Testing to see if email is turned off
def test_turn_off_email(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_off_input)

    # Call the turn on and off function
    change = turn_on_off("a")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 0


# Testing to see if SMS is turned on
def test_turn_on_SMS(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_on_input)

    # Call the turn on and off function
    change = turn_on_off("b")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 1


# Testing to see if SMS is turned off
def test_turn_off_SMS(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_off_input)

    # Call the turn on and off function
    change = turn_on_off("b")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 0


# Testing to see if targeted Ads are turned on
def test_turn_on_ads(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_on_input)

    # Call the turn on and off function
    change = turn_on_off("c")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 1


# Testing to see if targeted Ads are turned off
def test_turn_off_ads(monkeypatch, capsys):
    # Mock user input for choosing guest policy
    monkeypatch.setattr("builtins.input", mock_turn_off_input)

    # Call the turn on and off function
    change = turn_on_off("c")

    # Capture the printed output
    captured = capsys.readouterr()

    assert "a. Turn On" in captured.out
    assert "b. Turn Off" in captured.out
    assert change == 0
