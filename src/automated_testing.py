import json
from dataclasses import dataclass
from typing import List

@dataclass
class TestResult:
    test_name: str
    passed: bool
    message: str

class AutomatedTesting:
    def __init__(self):
        self.test_results = []

    def run_tests(self, code_changes: List[str]) -> List[TestResult]:
        # Simulate running tests
        test_results = []
        for change in code_changes:
            if "bug" in change:
                test_results.append(TestResult("test_bug", False, "Bug found in code"))
            else:
                test_results.append(TestResult("test_success", True, "Code change successful"))
        self.test_results = test_results
        return test_results

    def display_test_results(self) -> str:
        # Simulate displaying test results
        test_results_str = ""
        for result in self.test_results:
            test_results_str += f"Test {result.test_name}: {'Passed' if result.passed else 'Failed'} - {result.message}\n"
        return test_results_str

    def block_commit(self, test_results: List[TestResult]) -> bool:
        # Simulate blocking commit if any test fails
        for result in test_results:
            if not result.passed:
                return True
        return False
