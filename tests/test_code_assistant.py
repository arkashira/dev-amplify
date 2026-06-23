from code_assistant import CodeAssistant

def test_suggest_code():
    assistant = CodeAssistant()
    code = "# generate hello"
    suggested_code = assistant.suggest_code(code)
    assert suggested_code == "print('Hello World!')"

def test_suggest_code_no_match():
    assistant = CodeAssistant()
    code = "# generate foo"
    suggested_code = assistant.suggest_code(code)
    assert suggested_code is None

def test_validate_code():
    assistant = CodeAssistant()
    code = "print('Hello World!')"
    assert assistant.validate_code(code) is True

def test_validate_code_invalid():
    assistant = CodeAssistant()
    code = "print('Hello World!'"
    assert assistant.validate_code(code) is False

def test_suggest_and_validate_code():
    assistant = CodeAssistant()
    code = "# generate hello"
    suggested_code = assistant.suggest_code(code)
    assert suggested_code == "print('Hello World!')"
    assert assistant.validate_code(suggested_code) is True
