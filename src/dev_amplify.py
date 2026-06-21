import json
from dataclasses import dataclass
from typing import List

@dataclass
class Step:
    explanation: str
    code_snippet: str
    test_suite: str

class DevAmplify:
    def __init__(self):
        self.technologies = {
            "python": [
                Step("Introduction to Python", "print('Hello World')", "assert True"),
                Step("Python data structures", "my_list = [1, 2, 3]", "assert len(my_list) == 3"),
                Step("Python functions", "def greet(name): print(f'Hello {name}')", "greet('John')"),
                Step("Python classes", "class Person: pass", "person = Person()")
            ],
            "java": [
                Step("Introduction to Java", "System.out.println('Hello World');", "assert True"),
                Step("Java data structures", "int[] myArray = {1, 2, 3};", "assert myArray.length == 3"),
                Step("Java functions", "public static void greet(String name) { System.out.println('Hello ' + name); }", "greet('John')"),
                Step("Java classes", "public class Person {}", "Person person = new Person()")
            ]
        }

    def generate_learning_path(self, technology: str) -> List[Step]:
        if technology in self.technologies:
            return self.technologies[technology]
        else:
            raise ValueError("Technology not found")

    def export_as_zip(self, learning_path: List[Step]):
        # Simulate exporting as zip
        print("Exporting as zip")

    def push_to_github(self, learning_path: List[Step]):
        # Simulate pushing to GitHub
        print("Pushing to GitHub")
