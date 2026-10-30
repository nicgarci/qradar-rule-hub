# QRadar Rule Hub
As of now, this project only supports dumping QRadar Use Case Manager CSV report to local rules as code due to QRadar's API limitations. This is enough for version history, rule inventory, and could provide advantages for rule logic translation.
## Usage
The CSV file should meet the following columns:
- `{N,NO,EN,GR,LST,CD,MD,TD}` (QRadar notation)
- {Rule name, Notes, Rule enabled, Group, Log source type, Creation date, Modification date, Test definition}
## Rule Dumping
Install necessary modules:

`pip install -r requirements.txt`

Dumping all rules from CSV file:

`python -m rule_manager dump [CSV_FILE_PATH]`

The script will create a `rules` folder with each rule inside following the JSON format.
## Rule schema
```json
"name": "Rule name",
"notes": "Brief description of what the rule is supposed to detect.",
"enabled": "true|false. Boolean value that denotes if the rule is enabled or not in production.",
"group": [
    "foo",
    "bar"
],
"log_source": [
    "Microsoft Entra ID",
    "Azure AD"
],
"creation_date": "2024-12-12T07:12:03.693Z",
"modification_date": "2026-04-29T09:36:59.599Z",
"rule_logic": "AQL Rule logic",
"uuid": "b5db25bd-13ef-40b8-9327-f3a27ff759e8"
```