from fighters import select_fighters, Fighter, MoreThanOneFighterException, FighterNonFoundException

def test_select_fighters():
    # Test case 1: Single fighter found
    fighters = [
        Fighter("John"),
        Fighter("Jane"),
        Fighter("Bob")
    ]
    message = "I want to select John as my fighter"
    assert select_fighters(message, fighters) == Fighter("John")

    # Test case 2: Multiple fighters found
    fighters = [
        Fighter("John"),
        Fighter("Jane"),
        Fighter("Bob")
    ]
    message = "I want to select John or Jane as my fighter"
    try:
        select_fighters(message, fighters)
    except MoreThanOneFighterException as e:
        assert str(e) == "john, jane"
    else:
        assert False, "Expected MoreThanOneFighterException"

    # Test case 3: No fighter found
    fighters = [
        Fighter("John"),
        Fighter("Jane"),
        Fighter("Bob")
    ]
    message = "I want to select Alex as my fighter"
    try:
        select_fighters(message, fighters)
    except FighterNonFoundException:
        assert True
    else:
        assert False, "Expected FighterNonFoundException"

test_select_fighters()