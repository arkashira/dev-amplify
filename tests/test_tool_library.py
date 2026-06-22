from tool_library import Tool, ToolLibrary
import pytest

def test_add_tool():
    library = ToolLibrary()
    tool = Tool("Test Tool", "This is a test tool", "1.0")
    library.add_tool(tool)
    assert len(library.get_tools()) == 1

def test_get_tools():
    library = ToolLibrary()
    tool1 = Tool("Test Tool 1", "This is a test tool 1", "1.0")
    tool2 = Tool("Test Tool 2", "This is a test tool 2", "2.0")
    library.add_tool(tool1)
    library.add_tool(tool2)
    tools = library.get_tools()
    assert len(tools) == 2
    assert tools[0].name == "Test Tool 1"
    assert tools[1].name == "Test Tool 2"

def test_integrate_tool():
    library = ToolLibrary()
    tool = Tool("Test Tool", "This is a test tool", "1.0")
    library.add_tool(tool)
    project_workflow = {}
    updated_workflow = library.integrate_tool("Test Tool", project_workflow)
    assert updated_workflow["Test Tool"] == "1.0"

def test_integrate_tool_not_found():
    library = ToolLibrary()
    with pytest.raises(ValueError):
        library.integrate_tool("Test Tool", {})

def test_get_support():
    library = ToolLibrary()
    tool = Tool("Test Tool", "This is a test tool", "1.0")
    library.add_tool(tool)
    support = library.get_support("Test Tool")
    assert support == "Support for Test Tool is available"

def test_get_support_not_found():
    library = ToolLibrary()
    with pytest.raises(ValueError):
        library.get_support("Test Tool")

def test_update_tool():
    library = ToolLibrary()
    tool = Tool("Test Tool", "This is a test tool", "1.0")
    library.add_tool(tool)
    library.update_tool("Test Tool", "2.0")
    tools = library.get_tools()
    assert tools[0].version == "2.0"

def test_update_tool_not_found():
    library = ToolLibrary()
    with pytest.raises(ValueError):
        library.update_tool("Test Tool", "2.0")
