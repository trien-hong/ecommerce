# product status
PLEASE_CHOOSE_PRODUCT_STATUS = ""
ACTIVE = "active"
INACTIVE = "inactive"
SOLD_OUT = "sold out"

# category choices
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

# condition choices
PLEASE_CHOOSE_CONDITION = ""
NEW = "new"
OPEN_BOX = "open box"
PREOWNED = "preowned"
USED_LIKE_NEW = "used (like new)"
USED_MODERATELY = "used (moderately)"
USED_HEAVILY = "used (heavily)"
BROKEN_UNUSABLE = "broken (unusable)"

# overall rating
PLEASE_CHOOSE_OVERALL_RATING = ""
POSITIVE = "positive"
NEUTRAL = "neutral"
NEGATIVE = "negative"

class Choices:
    CHOICES_PRODUCT_STATUS = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_PRODUCT_STATUS, "Choose a status"),
        (ACTIVE, "active"),
        (INACTIVE, "inactive"),
        (SOLD_OUT, "sold out")
    ]

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

    CHOICES_OVERALL_RATING = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_OVERALL_RATING, "Choose an overall rating"),
        (POSITIVE, "positive"),
        (NEUTRAL, "neutral"),
        (NEGATIVE, "negative")
    ]