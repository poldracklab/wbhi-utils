DATE_FORMAT_FW = "%Y%m%d"
DATETIME_FORMAT_FW = "%Y%m%d %H%M%S.%f"
DATE_FORMAT_RC = "%Y-%m-%d"
DATETIME_FORMAT_RC = "%Y-%m-%d %H:%M:%S"
REDCAP_API_URL = "https://redcap.stanford.edu/api/"
WBHI_ID_SUFFIX_LENGTH = 5 # An additional character corresponding to site will be prepended
SITE_KEY = {
    "ucsb": "A",
    "ucb": "B",
    "ucsf": "C",
    "uci": "D",
    "ucd": "E",
    "stanford": "F",
    "ucsd": "G",
    "ucr": "H"
    }
SITE_KEY_REVERSE = {v: k for k, v in SITE_KEY.items()}
REDCAP_KEY = {
    "am_pm": {
        "1": "am",
        "2": "pm",
        "":""
    }
}
SITE_LIST = ["ucsb", "uci", "ucb", "ucsd", "ucsf", "ucr"]
SOFTWARE_DICT = {
    "ucsb": "syngo MR E11",
    "uci": "syngo MR XA30",
    "ucb": "syngo MR XA30",
    "ucsd": "syngo MR E11",
    "ucsf": "syngo MR E11",
    "ucr": "syngo MR XA30"
}
EMAIL_DICT = {
    "admin": [
        "jbwexler@stanford.edu",
        "cmtaylor@ucsb.edu",
        "buckholtz@stanford.edu",
        "markiewicz@stanford.edu",
        "mathiasg@stanford.edu",
    ],
    "ucsb": ["kyliewoodman@ucsb.edu"],
    "uci": ["lazer@uci.edu", "avirovka@uci.edu"],
    "ucb": ["binglis@berkeley.edu", "sam.weiller@berkeley.edu"],
    "ucsd": ["ajacobson@health.ucsd.edu", "r2barnes@health.ucsd.edu"],
    "ucsf": ["joseph.chen3@ucsf.edu"],
    "ucr": ["xu.chen@ucr.edu"]
}
ADMIN_EMAIL = "jbwexler@stanford.edu"
