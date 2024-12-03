from typing import Callable, TypedDict

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
        """Run the condition's evaluation function"""
        return self.evaluation(input_)

    def get_result(self, input_: InputData) -> OutputData:
        """Determine the supplement amount if the condition is met"""
        if callable(self.result):
            return self.result(input_)
        return self.result
    
class Rule:
    def __init__(self, conditions: list[Condition]) -> None:
        self.conditions = conditions

    def evaluate(self, input_: InputData) -> OutputData:
        """
            Evaluate the input data, checking which condition it meets.
            Then, calculate and return the supplement amount if eligible.
        """
        for condition in self.conditions:
            print(f"Checking condition {condition.name}")
            if condition.evaluate(input_):
                print(f"Condition {condition.name} met")
                return condition.get_result(input_)

        # If none of the conditions are met, raise an error.
        # This should never be reached as the last condition in the list
        # should be a default condition.
        print("No condition met. Raising exception.")
        raise Exception("Condition not found")