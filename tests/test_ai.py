import importlib
import inspect

import pytest
import tests.test_helper_functions as thf

testReport = thf.TestReport("test_report.txt")

@pytest.mark.depends()
def test_ai_module_exists():
    """
    Test if the battleships ai module exists.
    """
    try:
        importlib.import_module('battleships_ai')
    except ImportError:
        testReport.add_message("battleships_ai not found.")
        pytest.fail("battleships_ai not found")

@pytest.mark.depends(on='test_ai_module_exists')
def test_proccess_attack_works():
    """
    Test if the battleships ai module exists.
    """
    battleships_ai = importlib.import_module('battleships_ai')
    try:
        player = battleships_ai.AIPlayer()
        player.proccessattack(0,0,1)
    except ImportError:
        testReport.add_message("Proccess attack failed")
        pytest.fail("Proccess attack failed")

@pytest.mark.depends(on='test_proccess_attack_works')
def test_attack_successfully_generates():
    """
    Test if the battleships ai module exists.
    """
    battleships_ai = importlib.import_module('battleships_ai')
    try:
        player = battleships_ai.AIPlayer()
        player.proccessattack(4,4,-1)
        player.attack()
        
    except ImportError:
        testReport.add_message("Generate attack failed")
        pytest.fail("Generate attack failed")
