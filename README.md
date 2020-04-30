***Description of the project***

**Target**

* Builds a test bed for selfless traffic routing based on SUMO: STR-SUMO.
* Tests existing selfish traffic routing algorithms on STR-SUMO.
* Develops and tests heuristic selfless traffic routing algorithms on STR-SUMO.
* (Optional) Use model-based reinforcement learning to generate selfless traffic routing algorithms with STR-SUMO.

**Route Map**

Phase 1:

* Randomly generate start points and end points.
* Use TraCI to connect scheduling algorithms and SUMO.
* Combine both parts for tests.

Phase 2:

* Choose and implement existing selfish traffic scheduling algorithms.
* Design and implement heuristic selfless traffic scheduling algorithms.



***Contribution Guidance***

**Codes**
Please add comments for each function using the style pydoc can recognize: https://stackoverflow.com/questions/13040646/how-do-i-create-documentation-with-pydoc

You are also recommended to add brief comments to state the function of each block of codes. Naming variables using convention lowercae_with_underscores is suggested.

**Tests**
For important functions, please write a simple test case naming as test_function_name.py. After the test is passed, archive it in the test directory. When reviewing codes, this would be helpful for code reviewers to understand the usage of functions and to expand the tests with some border cases.
