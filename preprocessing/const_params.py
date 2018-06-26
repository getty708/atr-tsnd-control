# -----------------------------------------------------------------------
# Name: make_frame.py
# Author: Yoshimura Naoya
# Created: 2018.06.26
# Copyright:   (c) yoshimura 2018
#
# Purpose: Constant Params
# -----------------------------------------------------------------------


# ============
#  Name List
# ============
#root_dir = "./dataStore/n{}/".format(f_shape[0])

def get_DIR_DATA_RAW(DIR_ROOT):
    return os.path.join(DIR_ROOT, "CSV")

def get_DIR(DIR_ROOT, N, cat=None, is_cleaned=False):
    # Configure Direcotry Name
    if not cat == None: dir_name = "n{}_{}".format(N, cat)
    elif not is_cleand: dir_name = "n{}s_{}".format(N, cat)
    else:               dir_name = "n{}".format(N)
    # Return a path of DIRECTORY 
    return os.path.join(DIR_ROOT, "n{}".format(N))


# ==================
#  Sequence Config
# ==================
SEQ_CONFIG = {
    "1000Hz": {"fs":1000, "step": 1},
    "500Hz" : {"fs": 500, "step": 2},
    "250Hz" : {"fs": 250, "step": 4},
    "200Hz" : {"fs": 200, "step": 5},
    "125Hz" : {"fs": 125, "step": 8},
    "100Hz" : {"fs": 100, "step":10},
    "50Hz"  : {"fs":  50, "step":20},
    "25Hz"  : {"fs":  25, "step":40},
}

# ============
#  Name List
# ============
# NAME_LIST = {
#     "01":"01_kawabe",    "02":"02_higashinaka", "03":"03_yasuda",     "04":"04_kamiya",
#     "05":"05_ishiyama",  "06":"06_yoshimura",   "07":"07_aiko",       "08":"08_higashide",
#     "09":"09_others",    "10":"10_others",      "11":"11_others",     "12":"12_others",
#     "13":"13_others",    "14":"14_others",      "15":"15_others",
#     "16":"16_others",    "17":"17_others",
#     "30":"30_hada",      "31":"31_teramae",     "32":"32_torisuke",   "33":"33_matsukawa",  "34":"34_sato", 
#     "35":"35_hamase",    "36":"36_yamasaki",    "37":"37_koguchi",    "38":"38_onuma",      "39":"39_kashiyama",
#     "40":"40_yamaguchi", "41":"41_watase",      "42":"42_oga",        "43":"43_shigeyoshi", "44":"44_hukuda",
#     "45":"45_maekawa",
# }

NAME_LIST = {
    "01": {"ID": "01", "NAME":"01_kawabe",      "NAME":"kawabe", },
    "02": {"ID": "02", "NAME":"02_yasuda",      "NAME":"yasuda", },
    "03": {"ID": "03", "NAME":"03_higashinaka", "NAME":"higashinaka", },
    "04": {"ID": "04", "NAME":"04_kamiya",      "NAME":"kamiya", },
    "05": {"ID": "05", "NAME":"05_ishiyama",    "NAME":"ishiyama", },
    "06": {"ID": "06", "NAME":"06_yoshimura",      "NAME":"yoshimura", },
    "07": {"ID": "07", "NAME":"07_aiko",        "NAME":"aiko", },
    "08": {"ID": "08", "NAME":"08_higashide",   "NAME":"higashide", },

    "10": {"ID": "10", "NAME":"10_others", "NAME":"others",},
    "11": {"ID": "11", "NAME":"11_others", "NAME":"others",},
    "12": {"ID": "12", "NAME":"12_others", "NAME":"others",},
    "13": {"ID": "13", "NAME":"13_others", "NAME":"others",},
    "14": {"ID": "14", "NAME":"14_others", "NAME":"others",},
    "15": {"ID": "15", "NAME":"15_others", "NAME":"others",},
    "16": {"ID": "16", "NAME":"16_others", "NAME":"others",},
    "17": {"ID": "17", "NAME":"17_others", "NAME":"others",},

    "30": {"ID": "30", "NAME":"30_hada",       "NAME":"hada",},
    "31": {"ID": "31", "NAME":"31_teramae",    "NAME":"hada",},
    "32": {"ID": "32", "NAME":"32_torisuke",   "NAME":"torisuke",},
    "33": {"ID": "33", "NAME":"33_matsukawa",  "NAME":"matsukawa",},
    "34": {"ID": "34", "NAME":"34_sato",       "NAME":"sato",},
    "35": {"ID": "35", "NAME":"35_hamase",     "NAME":"hamase",},
    "36": {"ID": "36", "NAME":"36_yamasaki",   "NAME":"yamasaki",},
    "37": {"ID": "37", "NAME":"37_koguchi",    "NAME":"koguchi",},
    "38": {"ID": "38", "NAME":"38_onuma",      "NAME":"onuma",},
    "39": {"ID": "39", "NAME":"39_kashiyama",  "NAME":"kashiyama",},
    "40": {"ID": "40", "NAME":"40_yamaguchi",  "NAME":"yamaguchi",},
    "41": {"ID": "41", "NAME":"41_watase",     "NAME":"watase",},
    "42": {"ID": "42", "NAME":"42_oga",        "NAME":"oga",},
    "43": {"ID": "43", "NAME":"43_shigeyoshi", "NAME":"shigeyoshi",},
    "44": {"ID": "44", "NAME":"44_hukuda",     "NAME":"hukuda",},
    "45": {"ID": "45", "NAME":"45_maekawa",    "NAME":"maekawa",},
}
