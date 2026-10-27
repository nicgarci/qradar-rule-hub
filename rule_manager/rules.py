import json
import pathlib
import csv
import logging
from typing import List

import pydantic

import rule_manager.utils as utils

LOGGER = logging.getLogger()

ROOT_DIR = pathlib.Path(__file__).parent.parent
RULES_DIR = ROOT_DIR / "rules"

class Rule(pydantic.BaseModel):
    """Data class for a JSON rule."""

    name: str | None
    notes: str | None
    enabled: bool | None
    group: List[str] | None
    log_source: List[str] | None
    creation_date: str | None
    modification_date: str | None
    rule_logic: str | None
    uuid: str | None

class Rules:
    """Class used to manage rules."""

    def __init__(self, rules: List[Rule]):
        self.rules = rules

    @classmethod
    def parse_rules(cls, csv_file_path: pathlib.Path) -> "Rules":
        parsed_rules = []
        with open(csv_file_path, "r", encoding="utf-8") as rule_file:
            LOGGER.info("Processing rules from file: %s.", csv_file_path)
            rules_report = csv.DictReader(rule_file)
            for rule_line in rules_report:
                parsed_rules.append(Rules.parse_rule(rule_line))
        rule_file.close()
        LOGGER.info("%s rules parsed successfully.", len(parsed_rules))
        return Rules(rules=parsed_rules)

    @classmethod
    def parse_rule(cls, raw_rule: List[str]) -> Rule:
        utils.sanitize_raw_rule(raw_rule)
        try:
            parsed_rule = Rule(
                name=raw_rule['Rule name'],
                notes=raw_rule['Notes'],
                enabled=raw_rule['Rule enabled'],
                group=utils.get_group_list(raw_rule['Group']),
                log_source=utils.get_sanitized_list(raw_rule['Log source type']),
                creation_date=raw_rule['Creation date'],
                modification_date=raw_rule['Modification date'],
                rule_logic=raw_rule['Test definition'],
                uuid=raw_rule['uuid']
            )
        except pydantic.ValidationError as e:
            LOGGER.error(
                """ValidationError occurred for rule %s"
                %s""",
                raw_rule,
                json.dumps(e.errors(), indent=2),
            )
            raise
        return parsed_rule

    def dump_rules(self, rules_dir: pathlib.Path = RULES_DIR):
        for rule in self.rules:
            rule_name_path = utils.sanitize_rule_name(rule.name)
            rule_file_path = f"{rules_dir}/{rule_name_path}.json"
            if pathlib.Path(rule_file_path).is_file():
                with open(rule_file_path, "r", encoding="utf-8") as rule_file:
                    rule_model = rule_file.read()
                    old_rule = Rule.model_validate_json(rule_model)
                    old_rule.log_source.append(rule.log_source[0])
                    rule = old_rule
                rule_file.close()
            with open(rule_file_path, "w", encoding="utf-8") as rule_file:
                rule_file.write(rule.model_dump_json(indent=2))
            rule_file.close()
        LOGGER.info("All rules were dumped successfully.")