from pydantic import BaseModel

class SampleCase(BaseModel):
    language: str
    code: str
    bug_type: str
    description: str
    suggestion: str

sample_cases = [
    SampleCase(
        language="python",
        code="for i in range(1, len(arr)):\n    print(arr[i])",
        bug_type="off-by-one",
        description="The loop skips the first element (arr[0]).",
        suggestion="Use range(len(arr)) or range(0, len(arr)) to include all elements."
    ),
    SampleCase(
        language="python",
        code="def divide(x, y):\n    return x / y",
        bug_type="runtime",
        description="Will raise ZeroDivisionError if y is 0.",
        suggestion="Add a check to ensure y is not zero before dividing."
    ),
    SampleCase(
        language="python",
        code="if x = 5:\n    print('x is 5')",
        bug_type="syntax",
        description="Assignment (=) used instead of comparison (==).",
        suggestion="Use '==' for comparison in conditionals."
    ),
    SampleCase(
        language="python",
        code="if not arr:\n    process(arr)",
        bug_type="edge-case",
        description="If arr is an empty list, process(arr) is called, but the intent may have been to skip processing empty lists.",
        suggestion="Check if arr is not empty before calling process(arr)."
    ),
    SampleCase(
        language="python",
        code="def is_even(n):\n    return n % 2 == 1",
        bug_type="logic",
        description="Returns True for odd numbers instead of even numbers due to incorrect modulus check.",
        suggestion="Use 'n % 2 == 0' to check for even numbers."
    ),
]