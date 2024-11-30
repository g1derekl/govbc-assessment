from rule import conditions
from rule_engine import Rule, InputData

rule = Rule(conditions=conditions)

input_: InputData = {
    "id": "foo",
    "numberOfChildren": 2,
    "familyComposition": "couple",
    "familyUnitInPayForDecember": True
}

print(rule.evaluate(input_))