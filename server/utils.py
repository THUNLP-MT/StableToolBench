import re

categories = [
    "Sports",
    "Finance",
    "Data",
    "Entertainment",
    "Travel",
    "Location",
    "Science",
    "Food",
    "Transportation",
    "Music",
    "Business",
    "Visual Recognition",
    "Tools",
    "Text Analysis",
    "Weather",
    "Gaming",
    "SMS",
    "Events",
    "Health and Fitness",
    "Payments",
    "Financial",
    "Translation",
    "Storage",
    "Logistics",
    "Database",
    "Search",
    "Reward",
    "Mapping",
    "Artificial%20Intelligence%2FMachine%20Learning",
    "Email",
    "News, Media",
    "Video, Images",
    "eCommerce",
    "Medical",
    "Devices",
    "Business Software",
    "Advertising",
    "Education",
    "Media",
    "Social",
    "Commerce",
    "Communication",
    "Other",
    "Monitoring",
    "Energy",
    "Jobs",
    "Movies",
    "Cryptography",
    "Cybersecurity"
]

def standardize_category(category):
    save_category = category.replace(" ", "_").replace(",", "_").replace("/", "_")
    while " " in save_category or "," in save_category:
        save_category = save_category.replace(" ", "_").replace(",", "_")
    save_category = save_category.replace("__", "_")
    return save_category

def standardize(string):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9^_]")
    string = res.sub("_", string)
    string = re.sub(r"(_)\1+","_", string).lower()
    while True:
        if len(string) == 0:
            return string
        if string[0] == "_":
            string = string[1:]
        else:
            break
    while True:
        if len(string) == 0:
            return string
        if string[-1] == "_":
            string = string[:-1]
        else:
            break
    if string[0].isdigit():
        string = "get_" + string
    return string

def change_name(name):
    change_list = ["from", "class", "return", "false", "true", "id", "and"]
    if name in change_list:
        name = "is_" + name
    return name
