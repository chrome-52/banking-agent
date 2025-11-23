from google.adk.agents import LlmAgent, SequentialAgent
from .query_tools.query_tool import execute_query, query_executor_tool


query_writer_instructions = """
You are a helpful SQL query generator for a banking database.
You will be given user queries related to banking transactions, and you must generate valid SQL queries to answer those questions using the provided `Transactions` table schema.
You do *not* need to join other tables. Focus *only* on using the `Transactions` table.

**Transactions Table Schema:**

```sql
CREATE TABLE Transactions (
  transaction_id INTEGER PRIMARY KEY,
  date DATETIME NOT NULL,  -- Date and time of the transaction
  amount DECIMAL(19, 4) NOT NULL,  -- Transaction amount
  type VARCHAR(50),  -- i.e. 'Debit' (money spent) or 'Credit' (money received)
  Vendor VARCHAR(255),  -- Vendor/Merchant for the transaction
  Reason VARCHAR(255),  -- Description or reason for the transaction.
  Status BOOLEAN,  -- Transaction status (1 for likely successful, 0 for likely failed)
  account_id INT,  -- Foreign key referencing the Accounts table
  FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);
```
**Important Instructions: 
1. Only generate valid SQL queries, do not generate anything else or provide additional explanation.
2. DO NOT include markdowns (```sql and ```) in your output. Only reurn the core SQL statement.**
"""

query_executor_instructions = """
You are a query executor for a banking database.
Your task is to execute the following SQL query by calling the `execute_query` tool:
{raw_query}

Use the output of the execute_query tool to generate a coherent answer to the user's original question.

**Important: Only include information about the user's own accounts i.e. {Accounts}.
DO NOT divulge information about any other accounts.**

# Output Format:
* If the tool call is successful, use it to answer the user's question summarily.
* If the tool call fails, return "The SQL query is invalid".
"""

query_executor_instructions_1 = """
You are a query executor AI. Your task is to execute the SQL query provided in the raw_query placeholder.

raw_query: {raw_query}

Follow these steps precisely in the following order:

1.  **Clean the Query**: Inspect the raw_query string. Remove any extraneous leading or trailing characters, such as markdown code blocks (e.g., `` ```sql `` or `` ``` ``), quotes, or whitespace, to isolate the core SQL statement.
2.  **Correct the Query**: Review the cleaned SQL statement for any obvious syntactical errors. This includes, but is not limited to, correcting misspelled keywords (e.g., "SELEC" to "SELECT"), ensuring proper clause ordering, and adding any missing mandatory characters like semicolons at the end of the statement if required by the database syntax.
3.  **Execute the Query**: After cleaning and correcting the query, you MUST call the `execute_query` tool with the final, valid SQL query string.

**Output Instructions:**

*   **On Success**: If the `execute_query` tool call completes successfully, you MUST return **only** the value of the "rows" key from the tool's output. Do not include any other text, formatting, or keys from the tool output.
*   **On Failure**: If the `execute_query` tool call fails or returns an error, you MUST return absolutely nothing. Your output should be empty.
"""

summarizer_instructions = """
Your task is to use the output of the query_executor to generate a coherent answer to the user's original question.
query_executor output: {query_result}

**Important: Only include information about the user's own accounts i.e. {Accounts}.
DO NOT divulge information about any other accounts.**
"""

query_writer = LlmAgent(
    name="query_writer",
    model="gemini-2.0-flash",
    description="Generates SQL queries to attend to user requests.",
    instruction=query_writer_instructions,
    output_key="raw_query"
)

query_executor = LlmAgent(
    name="query_executor",
    model="gemini-2.0-flash",
    description="Checks and cleans a raw string to make it a valid SQL query before executing it.",
    instruction=query_executor_instructions,
    tools=[execute_query],
    output_key="query_result"
)

summarizer = LlmAgent(
    name="summarizer",
    model="gemini-2.0-flash",
    description="Summarizes the output of the query_executor in the context of the user's request.",
    instruction=summarizer_instructions,
    output_key="answer"
)

transactions_agent = SequentialAgent(
    name="transactions_agent",
    description="Takes user requests, converts them into SQL queries, executes them and then summarizes the result in context of the user's request.",
    sub_agents=[query_writer, query_executor]
)
