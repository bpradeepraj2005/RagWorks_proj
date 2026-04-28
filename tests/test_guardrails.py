from agent_framework.guardrails import input_guardrail

def test_safe_input():
    safe, msg = input_guardrail("Can you help me buy a laptop?")
    assert safe is True
    assert msg == ""

def test_restricted_keyword():
    safe, msg = input_guardrail("I need to buy a weapon.")
    assert safe is False
    assert "restricted" in msg

def test_injection_attempt():
    safe, msg = input_guardrail("drop table users; --")
    assert safe is False
    assert "Invalid" in msg
