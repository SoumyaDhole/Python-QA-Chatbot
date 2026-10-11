from collections import defaultdict
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from chatbot import (
    PythonQuestionBot,
    clear_conversation_state,
    context_after_answer,
    normalize_question,
)
from knowledge_base import KNOWLEDGE_BASE, format_code_block, format_teaching_answer


@pytest.fixture
def bot():
    return PythonQuestionBot()


def test_retrieves_direct_python_question(bot):
    result = bot.answer("What is Python?")

    assert result is not None
    assert result["matched_question"] == "What is Python?"
    assert result["matched_question"] in {entry["question"] for entry in KNOWLEDGE_BASE}
    assert "programming language" in result["answer"]


def test_knowledge_base_has_at_least_sixty_entries():
    assert len(KNOWLEDGE_BASE) >= 60


def test_knowledge_base_has_no_duplicate_questions_or_alias_collisions():
    canonical = [normalize_question(entry["question"]) for entry in KNOWLEDGE_BASE]
    phrases = defaultdict(set)
    for entry in KNOWLEDGE_BASE:
        for phrase in (entry["question"], *entry.get("aliases", ())):
            phrases[normalize_question(phrase)].add(entry["question"])

    assert len(canonical) == len(set(canonical))
    assert all(len(questions) == 1 for questions in phrases.values())


@pytest.mark.parametrize(
    ("question", "expected_question"),
    [
        ("TELL me about Python!!!", "What is Python?"),
        ("Explain lists", "How do I create a list in Python?"),
        ("How can I add an element to a list", "How do I add an item to a list?"),
        ("How can I load a CSV into pandas?", "How do I read a CSV file with pandas?"),
    ],
)
def test_common_alternate_phrasings_retrieve_relevant_answers(
    bot, question, expected_question
):
    result = bot.answer(question)

    assert result is not None
    assert result["matched_question"] == expected_question


def test_list_answer_includes_a_code_example(bot):
    result = bot.answer("How can I make a list comprehension?")

    assert result is not None
    assert result["category"] == "Lists"
    assert "[number ** 2" in result["answer"]


def test_empty_and_non_string_questions_are_ignored(bot):
    assert bot.answer("") is None
    assert bot.answer("   \t\n") is None
    assert bot.answer("?!...") is None
    assert bot.answer(None) is None


@pytest.mark.parametrize(
    "question",
    ["What is the weather on Mars today?", "Explain quantum mechanics"],
)
def test_unrelated_questions_have_no_match(bot, question):
    assert bot.answer(question) is None


def test_python_follow_up_resolves_to_python_applications(bot):
    first_answer = bot.answer("What is Python?")

    result = bot.answer("So then where is this used?", first_answer["context"])

    assert result["matched_question"] == "Where is Python used?"
    assert "web backends" in result["answer"]


def test_list_follow_up_resolves_to_adding_an_item(bot):
    first_answer = bot.answer("Explain lists")

    result = bot.answer("How do I add an item to it?", first_answer["context"])

    assert result["matched_question"] == "How do I add an item to a list?"
    assert "append(item)" in result["answer"]


def test_function_example_follow_up_uses_function_context(bot):
    first_answer = bot.answer("What is a function?")

    result = bot.answer("Show me an example.", first_answer["context"])

    assert result["matched_question"] == "What is a function in Python?"
    assert "def double(number):" in result["answer"]


def test_function_detail_follow_up_explains_the_previous_function_answer(bot):
    initial = bot.answer("What is a function?")

    result = bot.answer(
        "I didn't understand, explain in more detail", initial["context"]
    )

    assert result["retrieval_type"] == "contextual_explanation"
    assert result["matched_question"] == initial["matched_question"]
    assert "function" in result["answer"].lower()
    assert "return" in result["answer"]
    assert "def add(left, right):" in result["answer"]
    assert "statements" not in result["answer"]


def test_pandas_code_follow_up_explains_previous_csv_example(bot):
    initial = bot.answer("How do I read a CSV file with pandas?")

    result = bot.answer("what does this code mean?", initial["context"])

    assert result["retrieval_type"] == "contextual_explanation"
    assert result["matched_question"] == initial["matched_question"]
    assert "DataFrame" in result["answer"]
    assert "pd.read_csv(\"scores.csv\")" in result["answer"]
    assert "**Line by line**" in result["answer"]


def test_line_by_line_follow_up_keeps_context_and_code(bot):
    initial = bot.answer("How do I read a CSV file with pandas?")

    result = bot.answer("explain line by line", initial["context"])

    assert result["matched_question"] == initial["matched_question"]
    assert "`import pandas as pd`" in result["answer"]
    assert "`print(data.head())`" in result["answer"]


def test_another_example_uses_the_previous_function_topic(bot):
    initial = bot.answer("What is a function?")

    result = bot.answer("show another example", initial["context"])

    assert result["matched_question"] == initial["matched_question"]
    assert "def square(number):" in result["answer"]
    assert "25" in result["answer"]


def test_explanation_follow_up_without_context_asks_for_a_topic(bot):
    result = bot.answer("Explain in more detail")

    assert result["needs_clarification"] is True
    assert "Which Python topic" in result["answer"]


def test_dictionary_follow_up_explains_accessing_values(bot):
    first_answer = bot.answer("What is a dictionary?")

    assert first_answer is not None
    result = bot.answer("How do I access its values?", first_answer["context"])

    assert result is not None
    assert result["matched_question"] == "How do I access dictionary values?"
    assert "values()" in result["answer"]


def test_new_question_replaces_old_context(bot):
    python_answer = bot.answer("What is Python?")
    pandas_answer = bot.answer(
        "How do I read a CSV file with pandas?", python_answer["context"]
    )

    assert pandas_answer["category"] == "pandas"
    assert pandas_answer["context"]["topic"] == "pandas"
    assert context_after_answer(None) is None


def test_explicit_new_topic_is_not_routed_as_old_topic_follow_up(bot):
    python_answer = bot.answer("What is Python?")

    result = bot.answer(
        "Show me a pandas DataFrame example.", python_answer["context"]
    )

    assert result is not None
    assert result["category"] == "pandas"
    assert result["matched_question"] == "How do I create a pandas DataFrame?"


def test_python_example_follow_up_has_a_curated_answer(bot):
    python_answer = bot.answer("What is Python?")

    result = bot.answer("Show me an example.", python_answer["context"])

    assert result["matched_question"] == "What is a Python example?"
    assert 'print(message)' in result["answer"]


def test_unsupported_question_does_not_reuse_old_context(bot):
    python_answer = bot.answer("What is Python?")

    result = bot.answer("Will it rain on Mars tomorrow?", python_answer["context"])

    assert result is None
    assert context_after_answer(result) is None


def test_unrelated_explicit_topic_does_not_inherit_explanation_context(bot):
    function_answer = bot.answer("What is a function?")

    result = bot.answer(
        "What is the weather on Mars today?", function_answer["context"]
    )

    assert result is None
    assert context_after_answer(result) is None


def test_clear_conversation_resets_messages_pending_question_and_context():
    state = {
        "messages": [{"role": "assistant", "content": "old answer"}],
        "conversation_context": {"topic": "python"},
        "pending_question": "stale prompt",
    }

    clear_conversation_state(state)

    assert state["messages"] == []
    assert state["conversation_context"] is None
    assert "pending_question" not in state


def test_similarity_threshold_accepts_known_and_rejects_weak_match(bot):
    known = bot.answer("How can I build a list comprehension?")
    strict_bot = PythonQuestionBot(threshold=1.0)

    assert known is not None
    assert known["matched_question"] == "How do I use a list comprehension?"
    assert strict_bot.answer("How can I build a list comprehension?") is None


def test_cross_topic_ambiguous_match_is_rejected():
    cautious_bot = PythonQuestionBot(threshold=0.0, ambiguity_margin=1.0)

    assert cautious_bot.answer("explain data") is None


def test_threshold_must_be_between_zero_and_one():
    with pytest.raises(ValueError, match="between 0 and 1"):
        PythonQuestionBot(threshold=1.1)


def test_code_formatting_helper_preserves_indentation_and_newlines():
    source = 'data = pd.read_csv("scores.csv")\nprint(data.head())'

    result = format_code_block(source)

    assert result == f"```python\n{source}\n```"
    assert "\nprint(data.head())\n" in result


def test_teaching_answer_helper_formats_syntax_example_output_and_steps():
    result = format_teaching_answer(
        "A function reuses code.",
        syntax="def run():\n    return 1",
        example="print(run())",
        expected_output="1",
        line_by_line=("`return` sends a value back.",),
    )

    assert "**Syntax**" in result
    assert "**Example**" in result
    assert "**Expected output**" in result
    assert "**Line by line**" in result
    assert "```python\ndef run():\n    return 1\n```" in result


def test_streamlit_app_starts_without_uncaught_exceptions():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path), default_timeout=30).run()

    assert not app.exception
    assert len(app.chat_input) == 1
    assert any(button.label == "What is Python?" for button in app.button)