import re

def sanitize_rule_name(rule_name: str) -> str:
    rule_name = rule_name.lower()
    rule_name = re.sub(r"[\ |\/|\:|\|]", "_", rule_name)
    return rule_name

def sanitize_raw_rule(raw_rule: dict):
    for key in raw_rule:
        if raw_rule[key] == "" or raw_rule[key] == "None":
            raw_rule[key] = ""

def get_sanitized_list(rule_field: str):
    if rule_field == None:
        return [""]
    return [rule_field]

def get_group_list(rule_group: str):
    if (rule_group == None):
        return [""]
    rule_group_list = rule_group.split(sep=", ")
    for i in range(len(rule_group_list)):
        group = rule_group_list[i]
        rule_group_list[i] = group.replace(" ", "_").lower()
    return rule_group_list