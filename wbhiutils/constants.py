DATE_FORMAT_FW = "%Y%m%d"
DATETIME_FORMAT_FW = "%Y%m%d %H%M%S.%f"
DATE_FORMAT_RC = "%Y-%m-%d"
REDCAP_API_URL = "https://redcap.stanford.edu/api/"
WBHI_ID_SUFFIX_LENGTH = 5 # An additional character corresponding to site will be prepended
SITE_KEY = {
    "ucsb": "A",
    "ucb": "B",
    "ucsf": "C",
    "uci": "D",
    "ucd": "E",
    "stanford": "F"
    }
SITE_KEY_REVERSE = {v: k for k, v in SITE_KEY.items()}
REDCAP_KEY = {
    "am_pm": {
        "1": "am",
        "2": "pm",
        "":""
    }
}
SITE_LIST = ["ucsb", "uci", "ucb"]
EMAIL_DICT = {
    "admin": [
        "jbwexler@stanford.edu",
        "cmtaylor@ucsb.edu",
        "buckholtz@stanford.edu",
        "markiewicz@stanford.edu"
    ],
    "ucsb": ["kianasabugo@ucsb.edu"],
    "uci": ["lazer@uci.edu"],
    "ucb": ["binglis@berkeley.edu"]
}
ADMIN_EMAIL = 'jbwexler@stanford.edu'
