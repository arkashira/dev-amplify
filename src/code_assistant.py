import re
import json
from dataclasses import dataclass

@dataclass
class CodeSnippet:
    pattern: str
    snippet: str

class CodeAssistant:
    def __init__(self):
        self.snippets = [
            CodeSnippet(pattern=r"#\s*generate\s*hello", snippet="print('Hello World!')"),
            CodeSnippet(pattern=r"#\s*generate\s*goodbye", snippet="print('Goodbye World!')"),
        ]

    def suggest_code(self, code):
        for snippet in self.snippets:
            if re.search(snippet.pattern, code):
                return snippet.snippet
        return None

    def validate_code(self, code):
        try:
            compile(code, "", "exec")
            return True
        except SyntaxError:
            return False
