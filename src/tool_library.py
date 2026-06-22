import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Tool:
    name: str
    description: str
    version: str

class ToolLibrary:
    def __init__(self):
        self.tools = []

    def add_tool(self, tool: Tool):
        self.tools.append(tool)

    def get_tools(self) -> List[Tool]:
        return self.tools

    def integrate_tool(self, tool_name: str, project_workflow: Dict):
        for tool in self.tools:
            if tool.name == tool_name:
                project_workflow[tool_name] = tool.version
                return project_workflow
        raise ValueError("Tool not found")

    def get_support(self, tool_name: str) -> str:
        for tool in self.tools:
            if tool.name == tool_name:
                return f"Support for {tool_name} is available"
        raise ValueError("Tool not found")

    def update_tool(self, tool_name: str, new_version: str):
        for tool in self.tools:
            if tool.name == tool_name:
                tool.version = new_version
                return
        raise ValueError("Tool not found")
