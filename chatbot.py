"""TF-IDF retrieval and deterministic follow-up handling for the Python FAQ."""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import FeatureUnion

from knowledge_base import KNOWLEDGE_BASE, format_code_block, format_teaching_answer


DEFAULT_THRESHOLD = 0.24
AMBIGUITY_MARGIN = 0.025

FOLLOW_UP_TARGETS = {
    ("python", "usage"): "Where is Python used?",
    ("python", "example"): "What is a Python example?",
    ("list", "add"): "How do I add an item to a list?",
    ("list", "example"): "How do I create a list in Python?",
    ("function", "example"): "What is a function in Python?",
    ("dictionary", "values"): "How do I access dictionary values?",
    ("dictionary", "add"): "How do I add or update a dictionary value?",
}

FOLLOW_UP_REFERENCES = re.compile(r"\b(it|its|them|their|this|that|these|those)\b")
EXPLANATION_INTENTS = {
    "detail": re.compile(
        r"\b(explain in more detail|explain more|more detail|did not understand|do not understand|help me understand|i am confused)\b"
    ),
    "code": re.compile(
        r"\b(what does (this|that|the) code mean|explain line by line|explain this code|break (this|that) code down|what does this do)\b"
    ),
    "another_example": re.compile(
        r"\b(show another example|another example|one more example|different example|give me another example)\b"
    ),
}
TOPIC_PATTERNS = {
    "python": r"\bpython\b",
    "list": r"\blists?\b",
    "dictionary": r"\b(dict|dictionaries|dictionary)\b",
    "function": r"\bfunctions?\b",
    "string": r"\bstrings?\b",
    "tuple": r"\btuples?\b",
    "set": r"\bsets?\b",
    "numpy": r"\bnumpy\b",
    "pandas": r"\bpandas\b",
    "machine_learning": r"\b(machine learning|model|training data)\b",
}

TOPIC_DETAILS = {
    "function": "A function is a named, reusable block: `def` defines it, parameters receive inputs, and `return` sends a result back. Defining a function does not run its body; calling it does.",
    "pandas": "A CSV stores tabular data as text. `pd.read_csv(...)` parses its rows and columns into a pandas DataFrame, which you can inspect, filter, and summarize.",
    "list": "A list keeps items in order and can be changed. Its indexes start at zero; methods such as `append()` add values to the existing list.",
    "dictionary": "A dictionary maps unique keys to values. Use a key for one value, `get()` for a lookup with a missing-key default, and `values()` to view all values.",
    "python": "Python is a general-purpose programming language. The prior answer is the source for this explanation; this follow-up expands that same topic rather than selecting a different FAQ.",
    "python_basics": "The previous answer explains a Python fundamental. Keep the exact names and values from that answer in mind; its code example shows how the concept is used.",
    "file_handling": "A file context manager opens a resource for a short block and closes it automatically afterward, including when an error occurs.",
    "control_flow": "Control-flow statements decide which indented statements run and how often. The condition or iterable determines the path through the code.",
    "machine_learning": "A machine-learning model learns patterns from training data. Keep training examples separate from held-out test examples when evaluating it.",
}

ANOTHER_EXAMPLES = {
    "function": (
        "def square(number):\n    return number ** 2\n\nprint(square(5))",
        "25",
    ),
    "pandas": (
        'import pandas as pd\ndata = pd.read_csv("scores.csv", usecols=["name", "score"])\nprint(data.head(2))',
        "The first two rows of the name and score columns.",
    ),
    "list": (
        'tasks = ["read", "practice"]\ntasks.insert(1, "review")\nprint(tasks)',
        "['read', 'review', 'practice']",
    ),
    "dictionary": (
        'profile = {"name": "Ada"}\nprofile["role"] = "developer"\nprint(profile.get("role"))',
        "developer",
    ),
    "python": ('message = "Hello again"\nprint(message)', "Hello again"),
}

CODE_LINE_EXPLANATIONS = (
    ("import pandas as pd", "Imports pandas and gives it the conventional short name `pd`."),
    ("data = pd.read_csv", "Reads the CSV file and stores its rows and columns in the `data` DataFrame."),
    ("print(data.head", "Displays the first rows so you can preview the loaded table."),
    ("def ", "Defines a function; the indented lines that follow are its body."),
    ("return ", "Sends this value back to the code that called the function."),
    ("for ", "Starts a loop; the indented body runs for each item."),
    ("while ", "Repeats the indented body while its condition remains true."),
    ("with open", "Opens a file for this block and arranges to close it when the block ends."),
    (".append(", "Adds one item to the end of the list."),
    (".extend(", "Adds each item from the given iterable to the list."),
    (".values(", "Gets a view of the dictionary's values."),
    (" = ", "Assigns the expression on the right to the name on the left."),
    ("print(", "Displays the value inside the parentheses."),
)


def normalize_question(question):
    """Normalize case, punctuation, and whitespace for matching and intent checks."""
    normalized = question.casefold().replace("didn't", "did not").replace("didn’t", "did not")
    normalized = normalized.replace("don't", "do not").replace("don’t", "do not")
    normalized = normalized.replace("i'm", "i am").replace("i’m", "i am")
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    return " ".join(normalized.split())


def _context_topic(entry):
    if entry.get("context_topic"):
        return entry["context_topic"]
    if entry["category"] == "Python basics" and normalize_question(entry["question"]) != "what is python":
        return "python_basics"
    return {
        "Lists": "list",
        "Dictionaries": "dictionary",
        "Functions": "function",
        "Strings": "string",
        "Tuples": "tuple",
        "Sets": "set",
        "Control flow": "control_flow",
        "Object-oriented programming": "oop",
        "File handling": "file_handling",
        "Modules": "modules",
        "NumPy": "numpy",
        "pandas": "pandas",
        "Machine learning": "machine_learning",
    }.get(entry["category"], normalize_question(entry["category"]).replace(" ", "_"))


def _follow_up_intent(question):
    explicit_topic = any(re.search(pattern, question) for pattern in TOPIC_PATTERNS.values())
    if not explicit_topic and re.search(
        r"\b(example|example code|show me|give me an example)\b", question
    ):
        return "example"
    if FOLLOW_UP_REFERENCES.search(question):
        if re.search(r"\b(how|where|what|applications?)\b.*\b(use|used|good for)\b", question):
            return "usage"
        if re.search(r"\b(add|append|insert)\b", question):
            return "add"
        if re.search(r"\b(access|get|read|retrieve|loop through)\b", question) and re.search(
            r"\b(value|values|key|keys|item|items)\b", question
        ):
            return "values"
        if len(question.split()) <= 6 and re.match(
            r"^(so|then|and|what about|how about)\b", question
        ):
            return "clarify"
    return None


def _explanation_intent(question):
    for intent, pattern in EXPLANATION_INTENTS.items():
        if pattern.search(question):
            return intent
    return None


def _code_from_answer(answer):
    example_match = re.search(
        r"\*\*Example\*\*\s*```python\s*(.*?)```", answer, re.DOTALL
    )
    if example_match:
        return example_match.group(1).strip()
    match = re.search(r"```python\s*(.*?)```", answer, re.DOTALL)
    return match.group(1).strip() if match else None


def _explain_code_lines(code):
    explanations = []
    for line in code.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        explanation = next(
            (text for prefix, text in CODE_LINE_EXPLANATIONS if stripped.startswith(prefix)),
            "This line provides a value or step used by the surrounding example.",
        )
        explanations.append(f"`{stripped}`: {explanation}")
    return tuple(explanations)


def _contextual_explanation(question, context, intent):
    if not isinstance(context, dict) or not context.get("matched_question"):
        return {
            "answer": "Which Python topic should I explain? Ask a question first, or name a topic such as functions, lists, or pandas.",
            "needs_clarification": True,
            "context": None,
        }

    topic = context.get("topic", "")
    matched_question = context["matched_question"]
    previous_answer = context.get("answer", "")
    code = _code_from_answer(previous_answer)
    category = context.get("category", "Python")

    if intent == "another_example":
        alternate = ANOTHER_EXAMPLES.get(topic)
        if not alternate:
            return {
                "answer": f"I can explain **{matched_question}** further, but I need a narrower example request for {category}.",
                "needs_clarification": True,
                "context": context,
            }
        example, output = alternate
        detail = TOPIC_DETAILS.get(topic, f"This example applies the idea from **{matched_question}**.")
        answer = format_teaching_answer(
            f"Another example for **{matched_question}**: {detail}",
            example=example,
            expected_output=output,
        )
    elif intent == "code":
        if not code:
            return {
                "answer": f"The previous answer about **{matched_question}** did not include a code block. Which part would you like me to unpack?",
                "needs_clarification": True,
                "context": context,
            }
        detail = TOPIC_DETAILS.get(topic, f"This code is an example for **{matched_question}**.")
        answer = format_teaching_answer(
            f"This code belongs to your previous question, **{matched_question}**. {detail}",
            example=code,
            line_by_line=_explain_code_lines(code),
        )
    else:
        detail = TOPIC_DETAILS.get(topic)
        if not detail:
            detail = (
                f"Your previous question was **{matched_question}**. "
                f"The curated answer says: {previous_answer}"
            )
        answer = format_teaching_answer(
            f"More detail on **{matched_question}**: {detail}",
            example=code,
            line_by_line=_explain_code_lines(code) if code else (),
        )

    return {
        "answer": answer,
        "category": category,
        "matched_question": matched_question,
        "score": None,
        "retrieval_type": "contextual_explanation",
        "context": context,
    }


class PythonQuestionBot:
    """Retrieve curated FAQ answers and resolve a narrow set of follow-ups."""

    def __init__(self, threshold=DEFAULT_THRESHOLD, ambiguity_margin=AMBIGUITY_MARGIN):
        if not KNOWLEDGE_BASE:
            raise ValueError("The knowledge base must contain at least one entry.")
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1.")

        self.threshold = threshold
        self.ambiguity_margin = ambiguity_margin
        self.vectorizer = FeatureUnion(
            [
                (
                    "word",
                    TfidfVectorizer(
                        lowercase=True,
                        stop_words="english",
                        ngram_range=(1, 2),
                        sublinear_tf=True,
                    ),
                ),
                (
                    "character",
                    TfidfVectorizer(
                        analyzer="char_wb",
                        lowercase=True,
                        ngram_range=(3, 5),
                        sublinear_tf=True,
                    ),
                ),
            ],
            transformer_weights={"word": 1.0, "character": 0.45},
        )
        documents = [
            normalize_question(
                " ".join(
                    (
                        entry["question"],
                        " ".join(entry.get("aliases", ())),
                        entry["keywords"],
                        entry["category"],
                    )
                )
            )
            for entry in KNOWLEDGE_BASE
        ]
        self.knowledge_vectors = self.vectorizer.fit_transform(documents)
        self.entry_by_question = {
            normalize_question(entry["question"]): entry for entry in KNOWLEDGE_BASE
        }
        self.entry_by_phrase = {}
        for entry in KNOWLEDGE_BASE:
            for phrase in (entry["question"], *entry.get("aliases", ())):
                self.entry_by_phrase[normalize_question(phrase)] = entry

    def _make_result(self, entry, score, context_topic=None, retrieval_type="similarity"):
        return {
            "answer": entry["answer"],
            "category": entry["category"],
            "matched_question": entry["question"],
            "score": score,
            "retrieval_type": retrieval_type,
            "context": {
                "topic": context_topic or _context_topic(entry),
                "last_question": entry["question"],
                "matched_question": entry["question"],
                "answer": entry["answer"],
                "category": entry["category"],
            },
        }

    def _resolve_follow_up(self, question, context):
        normalized = normalize_question(question)
        topic = context.get("topic") if isinstance(context, dict) else None
        for other_topic, pattern in TOPIC_PATTERNS.items():
            if topic != other_topic and re.search(pattern, normalized):
                return None

        explanation_intent = _explanation_intent(normalized)
        if explanation_intent:
            return _contextual_explanation(question, context, explanation_intent)

        intent = _follow_up_intent(normalized)
        if not intent:
            return None

        target_question = FOLLOW_UP_TARGETS.get((topic, intent))
        if target_question:
            entry = self.entry_by_question[normalize_question(target_question)]
            return self._make_result(entry, None, context_topic=topic, retrieval_type="contextual")

        label = topic.replace("_", " ") if topic else "the previous topic"
        if intent == "clarify" or intent == "example":
            prompt = f"Do you mean an example or more detail about {label}?"
        elif intent == "usage":
            prompt = f"Which topic do you mean by 'it'? I can answer about {label}, or you can name another Python topic."
        else:
            prompt = f"What would you like to do with {label}? Please name the value or operation."
        return {"answer": prompt, "needs_clarification": True, "context": context}

    def answer(self, question, context=None):
        """Return a matching answer or None when input is empty or below confidence."""
        if not isinstance(question, str) or not question.strip():
            return None

        follow_up = self._resolve_follow_up(question, context)
        if follow_up is not None:
            return follow_up

        normalized = normalize_question(question)
        if not normalized:
            return None
        exact_entry = self.entry_by_phrase.get(normalized)
        if exact_entry is not None:
            return self._make_result(exact_entry, None, retrieval_type="exact")

        question_vector = self.vectorizer.transform([normalized])
        scores = cosine_similarity(question_vector, self.knowledge_vectors).ravel()
        ranked_indices = scores.argsort()[::-1]
        best_index = int(ranked_indices[0])
        best_score = float(scores[best_index])

        if best_score < self.threshold:
            return None

        if len(ranked_indices) > 1:
            second_index = int(ranked_indices[1])
            score_gap = best_score - float(scores[second_index])
            best_topic = _context_topic(KNOWLEDGE_BASE[best_index])
            second_topic = _context_topic(KNOWLEDGE_BASE[second_index])
            if score_gap < self.ambiguity_margin and best_topic != second_topic:
                return None

        entry = KNOWLEDGE_BASE[best_index]
        return self._make_result(entry, best_score)


def context_after_answer(result):
    """Keep context for answers/clarifications and clear it after unsupported input."""
    if result is None:
        return None
    return result.get("context")


def clear_conversation_state(state):
    """Reset the chat state mapping without depending on Streamlit in tests."""
    state["messages"] = []
    state["conversation_context"] = None
    state.pop("pending_question", None)


_default_bot = PythonQuestionBot()


def get_answer(question, context=None):
    """Answer with the default bot; return None for unsupported questions."""
    return _default_bot.answer(question, context=context)