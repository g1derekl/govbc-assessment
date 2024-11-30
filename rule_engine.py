from typing import Callable, Any, TypedDict

class InputData(TypedDict):
    id: str
    numberOfChildren: int
    familyComposition: str
    familyUnitInPayForDecember: bool

class OutputData(TypedDict):
    id: str
    isEligible: bool
    baseAmount: float
    childrenAmount: float
    supplementAmount: float

class Condition:
    def __init__(self, name: str, evaluation: Callable, result: Callable) -> None:
        self.name = name
        self.evaluation = evaluation
        self.result = result
    
    def evaluate(self, input_: InputData) -> bool:
        return self.evaluation(input_)

    def get_result(self, input_: InputData) -> OutputData:
        if callable(self.result):
            return self.result(input_)
        return self.result
    
class Rule:
    def __init__(self, conditions: list[Condition]) -> None:
        self.conditions = conditions

    def evaluate(self, input_: InputData) -> OutputData:
        for condition in self.conditions:
            if condition.evaluate(input_):
                return condition.get_result(input_)

        # If none of the conditions are met, raise an error.
        # This should never be reached as the last condition in the list
        # should be a default condition.
        raise Exception("Condition not found")