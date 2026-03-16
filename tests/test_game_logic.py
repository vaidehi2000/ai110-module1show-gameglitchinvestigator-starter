from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_string_secret_does_not_break_comparison():
    # Regression: the old code cast secret to str on even attempts.
    # String comparison makes "9" > "10" (True), so check_guess(9, "10")
    # would wrongly return "Too High". It must return "Too Low".
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too Low"


def test_parse_negative_number():
    # Edge case: Negative numbers should be rejected
    ok, value, error = parse_guess("-10")
    assert ok == False
    assert value is None
    assert error == "Please enter a positive number."


def test_parse_decimal_number():
    # Edge case: Decimal numbers should be rejected
    ok, value, error = parse_guess("5.7")
    assert ok == False
    assert value is None
    assert error == "Please enter a whole number (no decimals)."


def test_parse_whitespace_input():
    # Edge case: Inputs with leading/trailing spaces are accepted after stripping
    ok, value, error = parse_guess(" 50 ")
    assert ok == True
    assert value == 50
    assert error is None
