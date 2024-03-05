import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from instructor import llm_validator

import os
os.environ['OPENAI_API_KEY'] = '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'

# Define user output
client = instructor.patch(OpenAI())

class TestCase(BaseModel):
    description: str = Field(description="Test case description")
    function_name: str = Field(description="Function name this test case is covering")
    input: str = Field(description="Input to the test case")
    output: str = Field(description="expected correct output to the testcase")
    number_of_lines_per_testcase: int = Field(description="Return number of lines covered with this testcase")
    

class TestCaseDetails(BaseModel):
    '''
    This class will define the output.
    Output will have No of Test cases needed to cover 90% test coverage
    And description for each testcase
    '''
    num_test_cases: int = Field(description="Return No of Test cases for all the methods in uploaded file")
    test_case: list[TestCase] = Field(description="Write description for each sceanrio with function name this test case is covering in scala file passed as prompt")
    code_coverage: Annotated[
        str,
        BeforeValidator(
            llm_validator("Code coverage should be greater then or equal to 90%", allow_override=True)
        ),
    ]
    #Field(description="Return code coverage for current file in percentage")
    list_function_names: str = Field(description="list of all function names to be tested. Make the list comma seperated")
    
    '''
    test_cases: str = Field(description="Generate testcases in the language of the uploaded file for 90% coverage")
    '''

with open("/Users/jayatinaik/Projects/gen-ai-oneoone/scala_test_generator/reosurces/Huffman.scala") as f:
    scala_code = f.read()


prompt = f"Take the input scala class and generate number of test cases required to cover 90% test cases and description of each test case. Parse the code and generate testcases from: {scala_code}"

# Initialize model
try:
    tester = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=TestCaseDetails,
        max_retries = 3,
        messages=[
            {"role": "system", "content": "You are a good test case generator with excellent understanding of Scala"},
            {"role": "user", "content": prompt},
        ],
    )

    print(tester.model_dump_json(indent=2))

except Exception as e:
    print(e)
