from automated_testing import AutomatedTesting, TestResult

def test_run_tests():
    automated_testing = AutomatedTesting()
    code_changes = ["change1", "change2 with bug"]
    test_results = automated_testing.run_tests(code_changes)
    assert len(test_results) == 2
    assert test_results[0].passed
    assert not test_results[1].passed

def test_display_test_results():
    automated_testing = AutomatedTesting()
    code_changes = ["change1", "change2 with bug"]
    test_results = automated_testing.run_tests(code_changes)
    test_results_str = automated_testing.display_test_results()
    assert "Test test_bug: Failed" in test_results_str
    assert "Test test_success: Passed" in test_results_str

def test_block_commit():
    automated_testing = AutomatedTesting()
    code_changes = ["change1", "change2 with bug"]
    test_results = automated_testing.run_tests(code_changes)
    assert automated_testing.block_commit(test_results)

def test_block_commit_all_passed():
    automated_testing = AutomatedTesting()
    code_changes = ["change1", "change2"]
    test_results = automated_testing.run_tests(code_changes)
    assert not automated_testing.block_commit(test_results)
