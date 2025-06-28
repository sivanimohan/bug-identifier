from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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
        language="javascript",
        code="let arr = [1, 2, 3];\nfor(let i = 0; i <= arr.length; i++) {\n  console.log(arr[i]);\n}",
        bug_type="off-by-one",
        description="Loop runs one step too far, logging 'undefined' at the end.",
        suggestion="Use i < arr.length as the loop condition."
    ),
    SampleCase(
        language="c",
        code="int main() { int x = 5; if(x = 10) { return 1; } return 0; }",
        bug_type="logic",
        description="Assignment (=) used in 'if' instead of comparison (==).",
        suggestion="Use '==' for comparison in the if statement."
    )
]

