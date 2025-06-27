from pydantic import BaseModel

class TestCase(BaseModel):
    language: str
    code: str
    expected_bug_type: str
    expected_description: str
    expected_suggestion: str

sample_cases = [
    TestCase(
        language="python",
        code="for i in range(1, len(arr)):\n    print(arr[i])",
        expected_bug_type="off-by-one",
        expected_description="The loop skips the first element (arr[0]).",
        expected_suggestion="Use range(len(arr)) or range(0, len(arr)) to include all elements."
    ),
    TestCase(
        language="python",
        code="def divide(x, y):\n    return x / y",
        expected_bug_type="runtime",
        expected_description="Will raise ZeroDivisionError if y is 0.",
        expected_suggestion="Add a check to ensure y is not zero before dividing."
    ),
    TestCase(
        language="python",
        code="if x = 5:\n    print('x is 5')",
        expected_bug_type="syntax",
        expected_description="Assignment (=) used instead of comparison (==).",
        expected_suggestion="Use '==' for comparison in conditionals."
    ),
    TestCase(
        language="javascript",
        code="let arr = [1, 2, 3];\nfor(let i = 0; i <= arr.length; i++) {\n  console.log(arr[i]);\n}",
        expected_bug_type="off-by-one",
        expected_description="Loop runs one step too far, logging 'undefined' at the end.",
        expected_suggestion="Use i < arr.length as the loop condition."
    ),
    TestCase(
        language="c",
        code="int main() { int x = 5; if(x = 10) { return 1; } return 0; }",
        expected_bug_type="logic",
        expected_description="Assignment (=) used in 'if' instead of comparison (==).",
        expected_suggestion="Use '==' for comparison in the if statement."
    )
]