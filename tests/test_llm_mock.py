from starforge.modules.llm.base import Message
from starforge.modules.llm.mock import MockLLMProvider


def test_complete_deterministic():
    p = MockLLMProvider()
    a = p.complete("你好世界")
    b = p.complete("你好世界")
    assert a == b
    assert "MOCK" in a


def test_chat_returns_string():
    p = MockLLMProvider()
    out = p.chat([Message(role="user", content="hi")])
    assert isinstance(out, str) and out
