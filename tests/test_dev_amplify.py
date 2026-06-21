from dev_amplify import DevAmplify, Step
import pytest

def test_generate_learning_path():
    dev_amplify = DevAmplify()
    learning_path = dev_amplify.generate_learning_path("python")
    assert len(learning_path) == 4
    assert learning_path[0].explanation == "Introduction to Python"

def test_generate_learning_path_invalid_technology():
    dev_amplify = DevAmplify()
    with pytest.raises(ValueError):
        dev_amplify.generate_learning_path("invalid")

def test_export_as_zip():
    dev_amplify = DevAmplify()
    learning_path = dev_amplify.generate_learning_path("python")
    dev_amplify.export_as_zip(learning_path)
    # No assertion, just checking it runs without error

def test_push_to_github():
    dev_amplify = DevAmplify()
    learning_path = dev_amplify.generate_learning_path("python")
    dev_amplify.push_to_github(learning_path)
    # No assertion, just checking it runs without error
