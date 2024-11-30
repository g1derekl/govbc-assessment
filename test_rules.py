import pytest
from rule import conditions
from rule_engine import Rule, Condition, InputData, OutputData

rule = Rule(conditions=conditions)

# ====== Testing defining conditions and creating ruleset ======
def test_add_condition():
    condition = Condition(
        name="Test condition 1",
        evaluation=lambda x: x["numberOfChildren"] == 5,
        result=lambda x: OutputData({
            "id": x["id"],
            "isEligible": True,
            "baseAmount": 60,
            "childrenAmount": 100,
            "supplementAmount": 160
        })
    )

    rule = Rule(conditions=[condition])

    inputs: list[InputData] = [
        {
            "id": "foo",
            "numberOfChildren": 5,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        },
        {
            "id": "foo",
            "numberOfChildren": 5,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": False
        }
    ]

    outputs: list[OutputData] = [
        {
            "id": "foo",
            "isEligible": True,
            "baseAmount": 60,
            "childrenAmount": 100,
            "supplementAmount": 160
        },
        {
            "id": "foo",
            "isEligible": True,
            "baseAmount": 60,
            "childrenAmount": 100,
            "supplementAmount": 160
        }
    ]

    for i, x in enumerate(inputs):
        result = rule.evaluate(x)

        assert result == outputs[i]

def test_no_condition_met():
    condition = Condition(
        name="Test condition 1",
        evaluation=lambda x: x["numberOfChildren"] == 5,
        result=lambda x: OutputData({
            "id": x["id"],
            "isEligible": True,
            "baseAmount": 60,
            "childrenAmount": 100,
            "supplementAmount": 160
        })
    )

    rule = Rule(conditions=[condition])

    input_: InputData = {
        "id": "foo",
        "numberOfChildren": 4,
        "familyComposition": "couple",
        "familyUnitInPayForDecember": True
    }

    with pytest.raises(Exception):
        rule.evaluate(input_)

# ====== Testing existing ruleset taken from rule.py ======
def test_childless_single():
    rule = Rule(conditions=conditions)

    input_: InputData = {
        "id": "foo",
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
    }

    result = rule.evaluate(input_)

    assert result == {
        "id": "foo",
        "isEligible": True,
        "baseAmount": 60,
        "childrenAmount": 0,
        "supplementAmount": 60
    }

def test_childless_couple():
    rule = Rule(conditions=conditions)

    input_: InputData = {
        "id": "foo",
        "numberOfChildren": 0,
        "familyComposition": "couple",
        "familyUnitInPayForDecember": True
    }

    result = rule.evaluate(input_)

    assert result == {
        "id": "foo",
        "isEligible": True,
        "baseAmount": 120,
        "childrenAmount": 0,
        "supplementAmount": 120
    }

def test_with_child():
    rule = Rule(conditions=conditions)

    inputs: list[InputData] = [
        {
            "id": "foo",
            "numberOfChildren": 2,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        },
        {
            "id": "foo",
            "numberOfChildren": 1,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
    ]

    outputs: list[OutputData] = [
        {
            "id": "foo",
            "isEligible": True,
            "baseAmount": 120,
            "childrenAmount": 40,
            "supplementAmount": 160
        },
        {
            "id": "foo",
            "isEligible": True,
            "baseAmount": 120,
            "childrenAmount": 20,
            "supplementAmount": 140
        }
    ]

    for i, x in enumerate(inputs):
        result = rule.evaluate(x)

        assert result == outputs[i]

def test_ineligible_input():
    rule = Rule(conditions=conditions)

    inputs: list[InputData] = [
        {
            "id": "foo",
            "numberOfChildren": 2,
            "familyComposition": "single",
            "familyUnitInPayForDecember": False
        },
        {
            "id": "foo",
            "numberOfChildren": 1,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": False
        }
    ]

    outputs: list[OutputData] = [
        {
            "id": "foo",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        },
        {
            "id": "foo",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }
    ]

    for i, x in enumerate(inputs):
        result = rule.evaluate(x)

        assert result == outputs[i]