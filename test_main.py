from main import *
from unittest.mock import Mock


# will connect to database, use these values for testing
# username: testuser
# password: ValidPass1!


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


# test 2: Support five unique student accounts
# if get_num_of_user = 5 Test is will pass if function returns 1 which will exit the program
def test_five_acc_made_fail():
    assert check_five_users(5) is 1


# if get_num_of_user < 5 Test is will pass if function returns 2 which will continue the program
def test_five_acc_made_success():
    num_users = get_num_of_users()
    for i in range(0, 5):
        assert check_five_users(i) is 2


# test 3: Error message when 6th account is created
def test_error_message_for_sixth_acc_success(capsys):
    check_five_users(5)
    captured = capsys.readouterr()
    assert (
        "All permitted accounts have been created, please come back later"
        in captured.out
    )


def test_error_message_for_sixth_acc_fail(capsys):
    for i in range(0, 5):
        check_five_users(i)
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
    assert try_again() == False


def test_unlimited_logins(monkeypatch):
    # Mock user input for try_again function
    monkeypatch.setattr("builtins.input", mock_try_again_input)

    # Call the try_again function and assert the expected output
    assert try_again() == True


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


def test_job_search(monkeypatch, capsys):
    # Mock user input for go_back function
    monkeypatch.setattr("builtins.input", mock_go_back_input)

    # Call the job_search function
    job_search("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "under construction" in captured.out


def test_friend_search(monkeypatch, capsys):
    # Mock user input for friend_search function
    monkeypatch.setattr("builtins.input", mock_go_back_input)

    # Call the friend_search function
    friend_search("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "under construction" in captured.out


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
    assert "under construction" in captured.out


def test_no_selected_skill(monkeypatch, capsys):
    # Mock user input for no selected skill
    monkeypatch.setattr("builtins.input", mock_no_selected_skill_input)

    # Call the learn_skill function
    learn_skill("testuser")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected message is printed
    assert "Not picking to learn a new skill?" in captured.out
