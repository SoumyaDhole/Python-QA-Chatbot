"""Curated answers for common Python programming questions."""


def _entry(category, question, answer, *keywords, aliases=(), context_topic=None):
    return {
        "category": category,
        "question": question,
        "answer": answer,
        "keywords": " ".join(keywords),
        "aliases": tuple(aliases),
        "context_topic": context_topic,
    }


def format_code_block(code, language="python"):
    """Wrap multiline source without collapsing its line breaks."""
    source = code.strip("\n")
    if not source:
        return ""
    return f"```{language}\n{source}\n```"


def format_teaching_answer(
    explanation,
    syntax=None,
    example=None,
    expected_output=None,
    line_by_line=(),
):
    """Build consistent beginner-friendly Markdown with fenced code examples."""
    sections = [explanation.strip()]
    if syntax:
        sections.append(f"**Syntax**\n\n{format_code_block(syntax)}")
    if example:
        sections.append(f"**Example**\n\n{format_code_block(example)}")
    if expected_output:
        sections.append(
            f"**Expected output**\n\n{format_code_block(expected_output, language='text')}"
        )
    if line_by_line:
        details = "\n".join(f"- {line}" for line in line_by_line)
        sections.append(f"**Line by line**\n\n{details}")
    return "\n\n".join(section for section in sections if section)


KNOWLEDGE_BASE = [
    _entry("Python basics", "What is Python?", "Python is a high-level, general-purpose programming language known for readable syntax. It is commonly used for automation, web development, data analysis, and machine learning.", "language introduction overview", aliases=("Tell me about Python", "Explain the Python programming language", "What does Python mean"), context_topic="python"),
    _entry("Python basics", "Where is Python used?", "Python is used for web backends, automation and scripting, data analysis, scientific computing, machine learning, testing, and education. For example, a short Python script can rename many files or summarize a CSV dataset.", "applications use cases industry backend scripting science AI", aliases=("What can I do with Python", "What is Python good for", "What are Python applications"), context_topic="python"),
    _entry("Python basics", "What is a Python example?", "Here is a minimal Python program.\n\n```python\nmessage = \"Hello, Python!\"\nprint(message)\n```", "example code syntax hello world", aliases=("Show me a Python example", "Give me an example of Python"), context_topic="python"),
    _entry(
        "Python basics",
        "How do I create a variable in Python?",
        format_teaching_answer(
            "A variable is a name that refers to a value. Assign with `=`; Python determines the value's type.",
            syntax="name = value",
            example='name = "Ada"\nage = 36\nprint(f"{name} is {age}")',
            expected_output="Ada is 36",
            line_by_line=(
                '`name = "Ada"` stores text under the name `name`.',
                "`age = 36` stores an integer under `age`.",
                "The f-string inserts both values into the printed message.",
            ),
        ),
        "variable assignment declare",
        aliases=("How do variables work", "How can I assign a variable"),
    ),
    _entry("Python basics", "Why does indentation matter in Python?", "Indentation defines code blocks in Python, such as the body of a function or loop. Use consistent indentation; four spaces per level is the common convention.", "indent block whitespace spaces syntax"),
    _entry("Python basics", "How do I write a comment in Python?", "Start a single-line comment with `#`. For example: `# calculate the total`. Python has no dedicated multiline-comment syntax; use consecutive `#` lines or a docstring for documentation.", "comments hash documentation"),
    _entry("Python basics", "What are Python's built-in data types?", "Common built-in types include `int`, `float`, `bool`, `str`, `list`, `tuple`, `dict`, `set`, and `NoneType` (the type of `None`). Use `type(value)` to inspect a value's type.", "types integer number boolean string collection"),
    _entry("Python basics", "How do I convert a value to another type?", "Use a constructor such as `int()`, `float()`, `str()`, or `list()`. Conversion can fail when the value is not valid for the target type, such as `int(\"hello\")`.", "cast type conversion int float str"),
    _entry("Python basics", "What does None mean in Python?", "`None` represents the absence of a value. Compare it with `is None` rather than `== None`. A function that reaches its end without a `return` statement returns `None`.", "null nothing empty none return"),
    _entry("Strings", "How do I format a string in Python?", "For readable interpolation, use an f-string by prefixing the string with `f` and placing expressions in braces.\n\n```python\nname = \"Ada\"\nmessage = f\"Hello, {name}!\"\n```", "string formatting interpolation"),
    _entry("Strings", "How do I get part of a string?", "Use slicing with `text[start:stop:step]`; the stop index is excluded. For example, `text[:3]` returns the first three characters and `text[::-1]` returns a reversed copy.", "substring slice slicing index"),
    _entry("Strings", "Are Python strings mutable?", "No. Strings are immutable, so operations such as `replace()` return a new string instead of changing the original. Assign the result if you want to keep it.", "immutable modify replace"),
    _entry("Strings", "How do I remove whitespace from a string?", "Use `strip()` to remove whitespace from both ends, `lstrip()` for the left, or `rstrip()` for the right. These methods return new strings.", "trim spaces"),
    _entry(
        "Lists",
        "How do I create a list in Python?",
        format_teaching_answer(
            "A list is an ordered, changeable collection. Square brackets hold its items.",
            syntax="items = [value1, value2]",
            example='colors = ["red", "green", "blue"]\nprint(colors[0])',
            expected_output="red",
            line_by_line=(
                "The three strings are stored in order in `colors`.",
                "Index `0` selects the first item; Python indexes start at zero.",
            ),
        ),
        "array collection create",
        aliases=("Explain lists", "What is a list", "How can I make a list"),
        context_topic="list",
    ),
    _entry(
        "Lists",
        "How do I add an item to a list?",
        format_teaching_answer(
            "Use `append(item)` to add one item at the end, `extend(iterable)` to add items from another iterable, or `insert(index, item)` to choose a position.",
            example='fruits = ["apple", "pear"]\nfruits.append("plum")\nfruits.extend(["kiwi", "lime"])\nprint(fruits)',
            expected_output="['apple', 'pear', 'plum', 'kiwi', 'lime']",
            line_by_line=(
                "`append` adds `plum` as one new list item.",
                "`extend` adds each string from the second list.",
            ),
        ),
        "append insert add element value",
        aliases=("How can I add an element to a list", "Add an item to it", "How do I append to a list"),
        context_topic="list",
    ),
    _entry(
        "Lists",
        "What is the difference between append and extend?",
        format_teaching_answer(
            "`append(item)` adds its argument as one item. `extend(iterable)` adds every item from that iterable.",
            example='values = [1, 2]\nvalues.append([3, 4])\nprint(values)\nvalues = [1, 2]\nvalues.extend([3, 4])\nprint(values)',
            expected_output="[1, 2, [3, 4]]\n[1, 2, 3, 4]",
            line_by_line=(
                "The first `append` stores the whole `[3, 4]` list as one nested item.",
                "The second `extend` adds `3` and `4` as separate items.",
            ),
        ),
        "list add concatenate",
    ),
    _entry("Lists", "How do I use a list comprehension?", "A list comprehension builds a list from an iterable, optionally filtering its items.\n\n```python\nsquares = [number ** 2 for number in range(5)]\neven_squares = [number ** 2 for number in range(5) if number % 2 == 0]\n```", "comprehension map filter"),
    _entry("Lists", "How do I reverse a list?", "Use `items.reverse()` to reverse a list in place, or `items[::-1]` to create a reversed copy. The built-in `reversed(items)` returns an iterator.", "reverse order list backwards"),
    _entry("Lists", "How do I sort a list?", "Use `items.sort()` to sort the list in place, or `sorted(items)` to return a new sorted list. Pass `reverse=True` for descending order and `key=` to customize the sort key.", "order ascending descending"),
    _entry("Tuples", "What is a tuple and how do I create one?", "A tuple is an ordered, immutable collection. Use commas to create one; a one-item tuple needs a trailing comma: `single = (42,)`. Parentheses are often optional.", "tuple immutable collection"),
    _entry("Tuples", "When should I use a tuple instead of a list?", "Use a tuple for a fixed collection of values that should not be changed, such as coordinates. Use a list when you need to add, remove, or replace items.", "list comparison choose"),
    _entry(
        "Dictionaries",
        "How do I create a dictionary?",
        format_teaching_answer(
            "A dictionary stores values under unique keys. Use braces and separate each key and value with a colon.",
            syntax="mapping = {key: value}",
            example='user = {"name": "Ada", "active": True}\nprint(user["name"])',
            expected_output="Ada",
            line_by_line=(
                "`name` and `active` are keys; their associated values follow the colons.",
                "Square brackets look up the value for the `name` key.",
            ),
        ),
        "dict mapping key value create",
        aliases=("What is a dictionary", "Explain dictionaries", "How can I create a dict"),
        context_topic="dictionary",
    ),
    _entry(
        "Dictionaries",
        "How do I safely get a dictionary value?",
        format_teaching_answer(
            "Use `get(key)` to return a value without raising `KeyError` when the key is missing. `get(key, default)` lets you choose the missing-key result.",
            example='user = {"name": "Ada"}\nprint(user.get("name"))\nprint(user.get("role", "unknown"))',
            expected_output="Ada\nunknown",
            line_by_line=(
                "The first lookup finds the existing `name` key.",
                "The second lookup uses `unknown` because `role` is absent.",
            ),
        ),
        "lookup missing keyerror access value",
        aliases=("How do I access a dictionary value", "How can I get a value by key", "Read a value from a dict"),
        context_topic="dictionary",
    ),
    _entry(
        "Dictionaries",
        "How do I access dictionary values?",
        format_teaching_answer(
            "Use a key to retrieve one value, or call `values()` to view all values. `items()` gives key-value pairs.",
            example='user = {"name": "Ada", "role": "developer"}\nall_values = list(user.values())\nname = user["name"]\nprint(all_values)\nprint(name)',
            expected_output="['Ada', 'developer']\nAda",
            line_by_line=(
                "`values()` returns a view; `list()` makes its values easy to display.",
                "`user[\"name\"]` retrieves the value associated with the `name` key.",
            ),
        ),
        "dict values keys access retrieve items",
        aliases=("How do I access its values", "How can I get all values from a dictionary", "Get values from a dict"),
        context_topic="dictionary",
    ),
    _entry(
        "Dictionaries",
        "How do I add or update a dictionary value?",
        format_teaching_answer(
            "Assigning to a key adds it if missing or replaces its value if present. `update()` applies several assignments.",
            example='settings = {"theme": "light"}\nsettings["language"] = "en"\nsettings.update({"theme": "dark"})\nprint(settings)',
            expected_output="{'theme': 'dark', 'language': 'en'}",
            line_by_line=(
                "The assignment adds the `language` key.",
                "`update` changes the existing `theme` value.",
            ),
        ),
        "dict set insert change key",
        aliases=("Set a value in a dictionary", "How do I update a dict", "Add a key value pair"),
        context_topic="dictionary",
    ),
    _entry(
        "Dictionaries",
        "How do I loop through a dictionary?",
        format_teaching_answer(
            "Use `items()` to visit each key and value together, or `keys()`/`values()` when you need only one side.",
            example='user = {"name": "Ada", "role": "developer"}\nfor key, value in user.items():\n    print(f"{key}: {value}")',
            expected_output="name: Ada\nrole: developer",
            line_by_line=(
                "`items()` supplies one `(key, value)` pair per iteration.",
                "The indented `print` runs once for every pair.",
            ),
        ),
        "iterate loop keys values pairs",
    ),
    _entry("Sets", "What is a set in Python?", "A set is an unordered collection of distinct, hashable items. Create one with braces, such as `{1, 2, 3}`, or use `set()` for an empty set. `{}` creates an empty dictionary.", "unique duplicates collection"),
    _entry("Sets", "How do I find the union or intersection of sets?", "Use `a | b` or `a.union(b)` for the union, and `a & b` or `a.intersection(b)` for the intersection. The union contains items from either set; the intersection contains items in both.", "union intersection difference"),
    _entry(
        "Control flow",
        "How do I write an if statement in Python?",
        format_teaching_answer(
            "An `if` statement runs an indented block when its condition is true. Use `elif` for another condition and `else` for the remaining case.",
            syntax="if condition:\n    statements\nelse:\n    other_statements",
            example='score = 92\nif score >= 90:\n    grade = "A"\nelse:\n    grade = "Keep practicing"\nprint(grade)',
            expected_output="A",
            line_by_line=(
                "Python checks whether `score >= 90` is true.",
                "Only the matching indented branch runs.",
            ),
        ),
        "conditional condition branch",
    ),
    _entry(
        "Control flow",
        "How do I write a for loop?",
        format_teaching_answer(
            "A `for` loop runs once for each item in an iterable. Use `range()` to loop over numbers.",
            syntax="for item in iterable:\n    statements",
            example='for name in ["Ada", "Grace"]:\n    print(name)',
            expected_output="Ada\nGrace",
            line_by_line=(
                "The loop assigns each name to `name`, in order.",
                "The indented `print` runs once per name.",
            ),
        ),
        "iteration iterable repeat",
    ),
    _entry(
        "Control flow",
        "How do I write a while loop?",
        format_teaching_answer(
            "A `while` loop repeats as long as its condition is true. Update the condition in the body so the loop can finish.",
            syntax="while condition:\n    statements",
            example="count = 1\nwhile count <= 3:\n    print(count)\n    count += 1",
            expected_output="1\n2\n3",
            line_by_line=(
                "The condition is checked before each iteration.",
                "`count += 1` moves toward the stopping condition.",
            ),
        ),
        "repeat condition infinite",
    ),
    _entry("Control flow", "How do I get an index while looping?", "Use `enumerate(iterable)`, which yields an index and item on each iteration. You can set a different starting index with `start=`.\n\n```python\nfor index, item in enumerate(items, start=1):\n    print(index, item)\n```", "index counter loop"),
    _entry("Control flow", "What do break and continue do?", "`break` exits the nearest loop immediately. `continue` skips the rest of the current iteration and starts the next one.", "loop control stop skip"),
    _entry(
        "Functions",
        "How do I define a function in Python?",
        format_teaching_answer(
            "A function is a named, reusable block of code. `def` starts its definition; parameters receive inputs, and `return` gives a result back to the caller.",
            syntax="def function_name(parameter):\n    statements\n    return result",
            example="def add(left, right):\n    return left + right\n\nanswer = add(2, 3)\nprint(answer)",
            expected_output="5",
            line_by_line=(
                "`def add(left, right)` defines a function with two parameters.",
                "`return` sends their sum back to the caller.",
                "`add(2, 3)` calls the function; its result is stored and printed.",
            ),
        ),
        "function define def return",
        aliases=("What is a function", "Explain functions", "How do I make a function"),
        context_topic="function",
    ),
    _entry(
        "Functions",
        "What is a function in Python?",
        format_teaching_answer(
            "A function is a reusable block of code. It can accept inputs (parameters), perform work, and return a result.",
            syntax="def function_name(parameter):\n    statements\n    return result",
            example="def double(number):\n    return number * 2\n\nprint(double(4))",
            expected_output="8",
            line_by_line=(
                "`def double(number)` defines a function and its input parameter.",
                "`number * 2` is returned to whoever calls the function.",
                "`double(4)` passes `4` in, so the call returns `8`.",
            ),
        ),
        "function reusable block call example",
        aliases=("Explain what functions are", "Show me a function example"),
        context_topic="function",
    ),
    _entry(
        "Functions",
        "How do I set a default function argument?",
        format_teaching_answer(
            "Give a parameter a value in the function definition. The caller can omit that argument to use the default.",
            example='def greet(name="there"):\n    return f"Hello, {name}!"\n\nprint(greet())\nprint(greet("Ada"))',
            expected_output="Hello, there!\nHello, Ada!",
            line_by_line=(
                "`name` defaults to `there` when no argument is passed.",
                "Passing `Ada` overrides that default for the second call.",
            ),
        ),
        "parameter optional default argument",
    ),
    _entry("Functions", "What are *args and **kwargs?", "`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary. The names are conventional; the asterisks provide the behavior.", "variable arguments positional keyword"),
    _entry(
        "Functions",
        "What is a lambda function?",
        format_teaching_answer(
            "A `lambda` creates a small anonymous function with one expression. Use `def` for multi-step logic or code that needs a descriptive name.",
            syntax="lambda parameters: expression",
            example="double = lambda number: number * 2\nprint(double(4))",
            expected_output="8",
            line_by_line=(
                "The lambda takes one parameter, `number`.",
                "Its expression is evaluated and returned; `double(4)` passes in `4`.",
            ),
        ),
        "anonymous inline expression",
    ),
    _entry("Functions", "What is variable scope in Python?", "A name's scope is where it can be accessed. Python resolves names using the LEGB order: Local, Enclosing, Global, Built-in. Prefer passing values as arguments and returning results over changing globals.", "local global enclosing LEGB"),
    _entry("Object-oriented programming", "How do I define a class in Python?", "Use the `class` keyword. A class can define behavior with methods and store per-object data on instances.\n\n```python\nclass Dog:\n    def speak(self):\n        return \"Woof!\"\n```", "object class define OOP"),
    _entry("Object-oriented programming", "What are self and __init__?", "`__init__` is an initializer called when an instance is created. Its first parameter conventionally named `self` refers to that instance.\n\n```python\nclass User:\n    def __init__(self, name):\n        self.name = name\n```", "constructor instance initializer"),
    _entry("Object-oriented programming", "How does inheritance work in Python?", "A class can inherit from a base class by naming it in parentheses: `class Dog(Animal):`. The child class can reuse or override methods. Use `super()` to call the base implementation when appropriate.", "parent child subclass superclass extend"),
    _entry("Object-oriented programming", "What are dunder methods?", "Dunder (double-underscore) methods, such as `__init__`, `__str__`, and `__len__`, are special methods Python calls for built-in operations. Implement them to define how your objects behave with those operations.", "special magic methods"),
    _entry(
        "Exceptions",
        "How do I handle exceptions in Python?",
        format_teaching_answer(
            "Put risky code in `try` and handle expected errors with a specific `except` clause. This keeps a known input problem from crashing the example.",
            example='text = "42"\ntry:\n    number = int(text)\nexcept ValueError:\n    print("Please enter a whole number.")\nelse:\n    print(number + 1)',
            expected_output="43",
            line_by_line=(
                "`int(text)` converts the string to an integer and may raise `ValueError`.",
                "`except` runs only if that conversion fails.",
                "`else` runs when the `try` block succeeds.",
            ),
        ),
        "error try except finally catch",
    ),
    _entry("Exceptions", "How do I raise an exception?", "Use `raise` with an exception instance, such as `raise ValueError(\"age must be positive\")`. Choose a specific built-in exception that describes the problem.", "throw error valueerror"),
    _entry("Exceptions", "How do I create a custom exception?", "Define a class that inherits from `Exception` (or a more specific exception class).\n\n```python\nclass InvalidRecordError(Exception):\n    pass\n```", "user-defined custom error"),
    _entry(
        "File handling",
        "How do I open and read a text file?",
        format_teaching_answer(
            "Use `open()` inside `with`; Python closes the file when the block ends. Set `encoding=\"utf-8\"` for predictable text decoding.",
            example='with open("notes.txt", encoding="utf-8") as file:\n    contents = file.read()\nprint(contents)',
            line_by_line=(
                "`open` opens the path for reading text.",
                "`read()` returns the file contents as a string.",
                "The `with` block closes the file even if an error occurs.",
            ),
        ),
        "read file text context manager",
    ),
    _entry(
        "File handling",
        "How do I write to a file?",
        format_teaching_answer(
            "Open with mode `w` to create or replace a file. Use `a` to append instead. A `with` block closes it automatically.",
            example='with open("notes.txt", "w", encoding="utf-8") as file:\n    file.write("Hello, Python!\\n")',
            expected_output="Creates notes.txt containing: Hello, Python!",
            line_by_line=(
                "The `w` mode opens the path for writing and replaces existing content.",
                "`write` sends the text to the file; `\\n` adds a newline.",
            ),
        ),
        "save output write append",
    ),
    _entry("File handling", "What is the with statement used for?", "`with` manages a resource using its context-manager protocol, including cleanup when a block exits. It is commonly used with files and locks, ensuring cleanup even if an error occurs.", "context manager cleanup resource"),
    _entry("Modules", "What is a Python module?", "A module is a Python file that can define functions, classes, and variables for reuse. Import it with `import module_name` or import a specific name with `from module_name import name`.", "module file reusable"),
    _entry("Modules", "How do I import a module?", "Use `import math` and access names with `math.sqrt(9)`. You can also import a specific name with `from math import sqrt`. Prefer explicit imports and avoid wildcard imports in application code.", "import library package"),
    _entry("Modules", "What is a virtual environment?", "A virtual environment isolates a project's installed packages from other Python projects. Create one with `python -m venv .venv`, then activate it in your shell before installing project dependencies.", "venv isolate environment dependencies"),
    _entry("Modules", "How do I install a Python package with pip?", "Use `python -m pip install package_name` in the active environment. Using `python -m pip` helps ensure pip belongs to the Python interpreter you intend to use.\n\n```powershell\npython -m pip install requests\n```", "package manager install dependency pip", aliases=("How do I install a library", "Install Python dependencies", "How can I use pip")),
    _entry("Modules", "How do I create a virtual environment on Windows?", "From the project folder, create an environment with `py -m venv .venv`, then activate it in PowerShell with `.venv\\Scripts\\Activate.ps1`. If activation is restricted, run `.venv\\Scripts\\python.exe` directly.", "windows powershell venv activate environment setup", aliases=("Set up a Python venv on Windows", "How do I activate a virtual environment in PowerShell")),
    _entry("Strings", "How do I replace text in a string?", "Use `replace(old, new)` to create a new string with matching text replaced. Strings are immutable, so the original value does not change.\n\n```python\nmessage = \"hello world\"\nupdated = message.replace(\"world\", \"Python\")\n```", "string replace substitution change", aliases=("Replace a word in a string", "How can I change text in a string")),
    _entry("Tuples", "How do I unpack a tuple?", "Assign tuple items to the same number of variables to unpack them.\n\n```python\npoint = (3, 7)\nx, y = point\n```", "unpacking destructuring assign values", aliases=("How do I get tuple elements into variables", "Unpack tuple values")),
    _entry("Sets", "How do I add an item to a set?", "Use `add(item)` to add one item. Sets keep only unique values, so adding an item that is already present does not create a duplicate.\n\n```python\ntags = {\"python\"}\ntags.add(\"data\")\n```", "set add insert unique element", aliases=("Add an element to a set", "How can I put a value in a set")),
    _entry("Control flow", "How do I loop through a list?", "Use a `for` loop to visit each list item. Use `enumerate()` when you also need each item's index.\n\n```python\nfor fruit in [\"apple\", \"pear\"]:\n    print(fruit)\n```", "iterate list items elements traversal", aliases=("How can I go through a list", "Loop over list elements")),
    _entry("Python basics", "What is a Boolean in Python?", "A Boolean (`bool`) has one of two values: `True` or `False`. Comparisons such as `3 > 2` produce a Boolean and can be used in conditions.", "boolean bool true false logic condition", aliases=("What does bool mean", "How do true and false work in Python")),
    _entry("Modules", "What is the difference between a module and a package?", "A module is usually a single Python file that can be imported. A package groups related modules under a directory; modern Python packages can be regular packages with `__init__.py` or namespace packages.", "module package import folder directory", aliases=("Are Python modules and packages different", "Explain Python packages")),
    _entry("NumPy", "What is NumPy broadcasting?", "Broadcasting lets NumPy perform element-wise operations on arrays with compatible shapes without manually copying values. Dimensions are compatible when they are equal or one of them is 1.", "numpy shapes dimensions array arithmetic", aliases=("How does broadcasting work in NumPy", "Operate on arrays with different shapes")),
    _entry("pandas", "What is a pandas Series?", "A Series is a one-dimensional labeled array in pandas. It can hold values of one general data type and has an index. A DataFrame is made up of labeled columns, each commonly represented as a Series.", "pandas column one dimensional index dataframe", aliases=("Explain pandas Series", "What is the difference between Series and DataFrame")),
    _entry("NumPy", "How do I create a NumPy array?", "Import NumPy and call `np.array()` with a sequence. NumPy arrays are suited to numerical data and support vectorized operations.\n\n```python\nimport numpy as np\nvalues = np.array([1, 2, 3])\n```", "numpy ndarray create array"),
    _entry("NumPy", "How do arithmetic operations work on NumPy arrays?", "Many arithmetic operations are element-wise and vectorized, so you can operate on an array without writing a Python loop. Shapes must be compatible under NumPy broadcasting rules.\n\n```python\nvalues = np.array([1, 2, 3])\ndoubled = values * 2\n```", "vectorization elementwise calculation"),
    _entry(
        "pandas",
        "How do I create a pandas DataFrame?",
        format_teaching_answer(
            "A DataFrame is a labeled table with rows and columns. You can create one from a dictionary whose values are column lists.",
            example='import pandas as pd\ndata = pd.DataFrame({"name": ["Ada", "Grace"], "score": [98, 95]})\nprint(data)',
            expected_output="    name  score\n0    Ada     98\n1  Grace     95",
            line_by_line=(
                "`import pandas as pd` loads pandas using the common short name `pd`.",
                "Each dictionary key becomes a column; matching list positions form rows.",
            ),
        ),
        "pandas table rows columns",
        aliases=("Show me a pandas DataFrame example",),
    ),
    _entry(
        "pandas",
        "How do I read a CSV file with pandas?",
        format_teaching_answer(
            "`read_csv()` reads a comma-separated text file into a DataFrame, pandas' table structure. The path can be a filename or full path.",
            example='import pandas as pd\ndata = pd.read_csv("scores.csv")\nprint(data.head())',
            expected_output="The first five rows and their column names, for example:\n   name  score\n0   Ada     98",
            line_by_line=(
                "`pd` is the conventional alias for the pandas library.",
                "`read_csv` parses `scores.csv` and returns a DataFrame stored in `data`.",
                "`head()` displays the first five rows; it does not modify the file.",
            ),
        ),
        "csv load dataset",
        aliases=("How can I read a CSV with pandas", "Load CSV data into a DataFrame"),
        context_topic="pandas",
    ),
    _entry("pandas", "How do I filter rows in a pandas DataFrame?", "Use a boolean condition inside square brackets. Combine multiple conditions with `&` or `|` and wrap each condition in parentheses.\n\n```python\nhigh_scores = data[data[\"score\"] >= 90]\n```", "select subset condition rows"),
    _entry("pandas", "How do I find or handle missing values in pandas?", "Use `data.isna()` to locate missing values, `data.isna().sum()` to count them by column, `data.dropna()` to remove affected rows, or `data.fillna(value)` to replace them. Choose a strategy that fits the data.", "null NaN clean impute"),
    _entry("pandas", "How do I group data in pandas?", "Use `groupby()` to split rows by one or more columns, then aggregate with methods such as `mean()`, `sum()`, or `count()`.\n\n```python\nsummary = data.groupby(\"team\")[\"score\"].mean()\n```", "aggregate group aggregation"),
    _entry(
        "Machine learning",
        "What is the difference between supervised and unsupervised learning?",
        format_teaching_answer(
            "Supervised learning uses labeled examples to learn a target, such as classifying an email. Unsupervised learning looks for patterns without target labels, such as grouping similar observations.",
            example="# Supervised: rows have features and a known target label.\nfeatures = [[1.2], [3.4]]\nlabels = [0, 1]\n\n# Unsupervised: only features are supplied.\nobservations = [[1.2], [3.4]]",
            line_by_line=(
                "`features` are the input measurements in both settings.",
                "`labels` provide the known answers for supervised training.",
                "Clustering algorithms receive observations without a labels list.",
            ),
        ),
        "machine learning labeled classification clustering",
    ),
    _entry("Machine learning", "How do I split data into training and test sets?", "With scikit-learn, use `train_test_split` to hold out data for evaluation. Set `random_state` for reproducibility; for classification, `stratify=y` can preserve class proportions.\n\n```python\nfrom sklearn.model_selection import train_test_split\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42\n)\n```", "sklearn validation evaluate holdout"),
    _entry(
        "Machine learning",
        "What do fit and predict mean in scikit-learn?",
        format_teaching_answer(
            "`fit` learns model parameters from training examples. `predict` applies the trained model to new feature rows.",
            example="model.fit(X_train, y_train)\npredictions = model.predict(X_test)",
            line_by_line=(
                "`X_train` and `y_train` are the training features and target labels.",
                "`X_test` contains examples the model did not train on.",
                "`predictions` contains the model's estimated targets for those examples.",
            ),
        ),
        "train model inference estimator",
    ),
    _entry("Machine learning", "What is overfitting in machine learning?", "Overfitting occurs when a model learns training-set details, including noise, so it performs well on training data but poorly on new data. Evaluate on held-out data and consider simpler models, regularization, or more representative data.", "generalization variance memorization"),
    _entry("Machine learning", "What is data leakage in machine learning?", "Data leakage happens when training or model selection uses information that would not be available at prediction time, making evaluation misleadingly optimistic. Split data before fitting preprocessing steps; use a scikit-learn `Pipeline` to fit transformations only on training folds.", "target leakage preprocessing validation"),
]