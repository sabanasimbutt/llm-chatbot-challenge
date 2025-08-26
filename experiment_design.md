## Experiment Design: Evaluating the Generative Chatbot

### 1. Objective

The primary objective of this experiment is to rigorously evaluate the performance of the generative chatbot agent. The evaluation will focus on two key areas:

1.  **Decision-Making Accuracy (Tool Use):** How accurately does the agent choose the correct tool and extract the right parameters based on the user's intent?
2.  **Response Quality (Generation):** How helpful, accurate, and natural is the final response generated for the user after the tool has been executed?

### 2. Evaluation Metrics

We will use a combination of quantitative and qualitative metrics to get a holistic view of the chatbot's performance.

#### Quantitative Metrics:

* **Tool Selection Accuracy:** (Correct Tool Selections / Total Queries) \* 100%. A selection is "correct" if the agent chooses the right API to call (or correctly chooses "none").
* **Parameter Extraction F1-Score:** A score that balances the precision and recall of extracting parameters (like `orderId`). This is more robust than simple accuracy, especially if some queries have no parameters.
* **Policy Adherence Rate:** (Queries where policy was correctly handled / Total policy-related queries) \* 100%. This specifically measures if the agent correctly defers the 10-day cancellation rule to the API.

#### Qualitative Metrics:

* **Response Helpfulness Score (RHS):** A human-rated score from 1 to 5.
    * 1: Incorrect and unhelpful.
    * 2: Incorrect but related to the query.
    * 3: Correct but incomplete or unnatural.
    * 4: Correct and helpful.
    * 5: Correct, helpful, and sounds natural and empathetic.
* **Error Analysis Categories:** For any failed test case, we will categorize the failure type (e.g., `WrongTool`, `MissingParameter`, `HallucinatedResponse`, `PolicyViolation`).

### 3. Test Dataset

To ensure a thorough evaluation, we will create a small but diverse test set of user queries. This set will cover various intents, edge cases, and linguistic styles.

| Test Case ID | User Query                                       | Expected Tool      | Expected Parameters   | Key Challenge Tested          |
| :----------- | :----------------------------------------------- | :----------------- | :-------------------- | :---------------------------- |
| **TC-01** | "Cancel my order ORD12345"                       | `OrderCancellation`| `{'orderId': 'ORD12345'}` | **Baseline - Success** |
| **TC-02** | "I need to cancel ORD67890"                      | `OrderCancellation`| `{'orderId': 'ORD67890'}` | **Baseline - Policy Failure** |
| **TC-03** | "Where's my package ORDABCDE?"                   | `OrderTracking`    | `{'orderId': 'ORDABCDE'}` | **Baseline - Tracking** |
| **TC-04** | "I want to cancel my recent order."              | `none`             | `{}`                  | **Missing Information** |
| **TC-05** | "What's the status of order ord12345?"           | `OrderTracking`    | `{'orderId': 'ORD12345'}` | **Case Insensitivity** |
| **TC-06** | "Can you track ORD99999 for me?"                 | `OrderTracking`    | `{'orderId': 'ORD99999'}` | **Handling API Errors** |
| **TC-07** | "Thanks, that's all I needed."                   | `none`             | `{}`                  | **Irrelevant/Chit-chat** |
| **TC-08** | "Scrap my order, number is ORDABCDE"             | `OrderCancellation`| `{'orderId': 'ORDABCDE'}` | **Slang/Informal Language** |
| **TC-09** | "What's your cancellation policy?"               | `none`             | `{}`                  | **General Question** |
| **TC-10** | "Track ORDABCDE and cancel ORD12345"             | `OrderTracking`    | `{'orderId': 'ORDABCDE'}` | **Complex/Multi-intent** |

*(Note: For TC-10, we expect the model to only pick one action, which is a limitation we aim to identify).*

### 4. Execution & Reporting

**Procedure:**

1.  Set up the project according to the instructions in `README.md` (install dependencies, set `.env` file).
2.  Run the interactive session using `python chatbot_agent.py`.
3.  For each "User Query" in the test dataset, input the query into the running application.
4.  For each run, log the LLM's "thought," the selected tool, the extracted parameters, and the final response from the terminal output.
5.  Compare the actual output against the "Expected" columns in the test dataset to calculate the quantitative metrics.
6.  A human evaluator will review the final response for each test case and assign a **Response Helpfulness Score (RHS)**.
7.  Aggregate the results into a final report.

The complete, raw output and analysis for each test case are available in the `results.csv` file in this repository.

**Reporting Key Insights:**

This final section summarizes the quantitative scores and provide key qualitative insights, such as:

* "The agent demonstrated a **90% accuracy** in selecting the correct tool, struggling only with multi-intent queries (TC-10)."
* "Parameter extraction was highly effective, with an **F1-Score of 0.95**, indicating robustness to variations in user phrasing."
* "The agent achieved a **100% Policy Adherence Rate**, successfully deferring all cancellation eligibility checks to the designated API, which confirms the safety of the system architecture."
* "The average **Response Helpfulness Score was 4.2/5.0**, with lower scores typically associated with the agent's handling of API errors, suggesting an area for prompt improvement."