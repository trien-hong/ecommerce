# states/territories
PLEASE_CHOOSE_STATE_TERRITORY = ""
OUTSIDE_USA = "Non US state/territory"
AL = "Alabama"
AK = "Alaska"
AS = "American Samoa"
AZ = "Arizona"
AR = "Arkansas"
CA = "California"
CO = "Colorado"
CT = "Connecticut"
DE = "Delaware"
DC = "Washington D.C."
FL = "Florida"
GA = "Georgia"
GU = "Guam"
HI = "Hawaii"
ID = "Idaho"
IL = "Illinois"
IN = "Indiana"
IA = "Iowa"
KS = "Kansas"
KY = "Kentucky"
LA = "Louisiana"
ME = "Maine"
MD = "Maryland"
MA = "Massachusetts"
MI = "Michigan"
MN = "Minnesota"
MS = "Mississippi"
MO = "Missouri"
MT = "Montana"
NE = "Nebraska"
NV = "Nevada"
NH = "New Hampshire"
NJ = "New Jersey"
NM = "New Mexico"
NY = "New York"
NC = "North Carolina"
ND = "North Dakota"
MP = "Northern Mariana Islands"
OH = "Ohio"
OK = "Oklahoma"
OR = "Oregon"
PA = "Pennsylvania"
PR = "Puerto Rico"
RI = "Rhode Island"
SC = "South Carolina"
SD = "South Dakota"
TN = "Tennessee"
TX = "Texas"
UT = "Utah"
VT = "Vermont"
VA = "Virginia"
VI = "Virgin Islands"
WA = "Washington"
WV = "West Virginia"
WI = "Wisconsin"
WY = "Wyoming"

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

# product status
PLEASE_CHOOSE_PRODUCT_STATUS = ""
ACTIVE = "active"
INACTIVE = "inactive"
SOLD_OUT = "sold out"

# overall rating
PLEASE_CHOOSE_OVERALL_RATING = ""
NEGATIVE = "negative"
NEUTRAL = "neutral"
POSITIVE = "positive"

# feedback ratings
PLEASE_CHOOSE_FEEDBACK_RATINGS = ""
APPALLING = 1
BAD = 2
AVERAGE = 3
GOOD = 4
GREAT = 5

class Choices:
    CHOICES_STATE_TERRITORY = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        (PLEASE_CHOOSE_STATE_TERRITORY, "Choose your state/territory"),
        (OUTSIDE_USA, "Non US state/territory"),
        (AL, "AL - Alabama"),
        (AK, "AK - Alaska"),
        (AS, "AS - American Samoa"),
        (AZ, "AZ - Arizona"),
        (AR, "AR - Arkansas"),
        (CA, "CA - California"),
        (CO, "CO - Colorado"),
        (CT, "CT - Connecticut"),
        (DE, "DE - Delaware"),
        (DC, "DC - Washington D.C."),
        (FL, "FL - Florida"),
        (GA, "GA - Georgia"),
        (GU, "GU - Guam"),
        (HI, "HI - Hawaii"),
        (ID, "ID - Idaho"),
        (IL, "IL - Illinois"),
        (IN, "IN - Indiana"),
        (IA, "IA - Iowa"),
        (KS, "KS - Kansas"),
        (KY, "KY - Kentucky"),
        (LA, "LA - Louisiana"),
        (ME, "ME - Maine"),
        (MD, "MD - Maryland"),
        (MA, "MA - Massachusetts"),
        (MI, "MI - Michigan"),
        (MN, "MN - Minnesota"),
        (MS, "MS - Mississippi"),
        (MO, "MO - Missouri"),
        (MT, "MT - Montana"),
        (NE, "NE - Nebraska"),
        (NV, "NV - Nevada"),
        (NH, "NH - New Hampshire"),
        (NJ, "NJ - New Jersey"),
        (NM, "NM - New Mexico"),
        (NY, "NY - New York"),
        (NC, "NC - North Carolina"),
        (ND, "ND - North Dakota"),
        (MP, "MP - Northern Mariana Islands"),
        (OH, "OH - Ohio"),
        (OK, "OK - Oklahoma"),
        (OR, "OR - Oregon"),
        (PA, "PA - Pennsylvania"),
        (PR, "PR - Puerto Rico"),
        (RI, "RI - Rhode Island"),
        (SC, "SC - South Carolina"),
        (SD, "SD - South Dakota"),
        (TN, "TN - Tennessee"),
        (TX, "TX - Texas"),
        (UT, "UT - Utah"),
        (VT, "VT - Vermont"),
        (VA, "VA - Virginia"),
        (VI, "VI - Virgin Islands"),
        (WA, "WA - Washington"),
        (WV, "WV - West Virginia"),
        (WI, "WI - Wisconsin"),
        (WY, "WY - Wyoming")
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

    CHOICES_PRODUCT_STATUS = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_PRODUCT_STATUS, "Choose a status"),
        (ACTIVE, "active"),
        (INACTIVE, "inactive"),
        (SOLD_OUT, "sold out")
    ]

    CHOICES_OVERALL_RATING = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_OVERALL_RATING, "Choose an overall rating"),
        (NEGATIVE, "negative"),
        (NEUTRAL, "neutral"),
        (POSITIVE, "positive")
    ]

    CHOICES_FEEDBACK_RATING = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        (PLEASE_CHOOSE_FEEDBACK_RATINGS, "Choose a rating (1-5)"),
        (APPALLING, "1 - Appaling"),
        (BAD, "2 - Bad"),
        (AVERAGE, "3 - Average"),
        (GOOD, "4 - Good"),
        (GREAT, "5 - Great")
    ]