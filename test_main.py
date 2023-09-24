from unittest.mock import Mock

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
    if "Choose one of ['a', 'b', 'c']: " in prompt:
        return "a"


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
