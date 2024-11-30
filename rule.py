from rule_engine import Condition, OutputData

def eval_children(number_of_children: int) -> int:
    return number_of_children * 20

conditions = [
    Condition(
        name="Single person",
        evaluation=lambda x: x["numberOfChildren"] == 0 and x["familyComposition"] == "single" and x["familyUnitInPayForDecember"],
        result=lambda x: OutputData({
            "id": x["id"],
            "isEligible": True,
            "baseAmount": 60,
            "childrenAmount": 0,
            "supplementAmount": 60
        })
    ),
    Condition(
        name="Couple",
        evaluation=lambda x: x["numberOfChildren"] == 0 and x["familyComposition"] == "couple" and x["familyUnitInPayForDecember"],
        result=lambda x: OutputData({
            "id": x["id"],
            "isEligible": True,
            "baseAmount": 120,
            "childrenAmount": 0,
            "supplementAmount": 120
        })
    ),
    Condition(
        name="Either single- or two-parent family with dependent children",
        evaluation=lambda x: x["numberOfChildren"] >= 1 and x["familyUnitInPayForDecember"],
        result=lambda x: OutputData({
            "id": x["id"],
            "isEligible": True,
            "baseAmount": 120,
            "childrenAmount": eval_children(x["numberOfChildren"]),
            "supplementAmount": 120 + eval_children(x["numberOfChildren"])
        })
    ),
    Condition(
        name="Other",
        evaluation=lambda x: True,
        result=lambda x: OutputData({
            "id": x["id"],
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        })
    )
]