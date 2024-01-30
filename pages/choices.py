PLEASE_CHOOSE_CATEGORY = ""
KITCHEN = "kitchen"
LIVING_ROOM = "living room"
GARAGE = "garage"
BATHROOM = "bathroom"
BEDROOM = "bedroom"
OFFICE = "office"
OUTDOOR = "outdoor"
TOYS = "toys"
GAMES = "games"
CLOTHING = "clothing"
ELECTRONICS = "electronics"

PLEASE_CHOOSE_CONDITION = ""
NEW = "new"
OPEN_BOX = "open box"
PREOWNED = "preowned"
USED_LIKE_NEW = "used (like new)"
USED_MODERATELY = "used (moderately)"
USED_HEAVILY = "used (heavily)"
BROKEN_UNUSABLE = "broken (unusable)"

class Choices:
    CHOICES_CATEGORY = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_CATEGORY, "Choose a category"),
        (KITCHEN, "kitchen"),
        (LIVING_ROOM, "living room"),
        (GARAGE, "garage"),
        (BATHROOM, "bathroom"),
        (BEDROOM, "bedroom"),
        (OFFICE, "office"),
        (OUTDOOR, "outdoor"),
        (TOYS, "toys"),
        (GAMES, "games"),
        (CLOTHING, "clothing"),
        (ELECTRONICS, "electronics")
    ]

    CHOICES_CONDITION = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_CONDITION, "Choose a condition"),
        (NEW, "new"),
        (OPEN_BOX, "open box"),
        (PREOWNED, "preowned"),
        (USED_LIKE_NEW, "used (like new)"),
        (USED_MODERATELY, "used (moderately)"),
        (USED_HEAVILY, "used (heavily)"),
        (BROKEN_UNUSABLE, "broken (unusable)")
    ]