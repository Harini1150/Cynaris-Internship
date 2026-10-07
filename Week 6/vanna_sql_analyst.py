import os
import asyncio

from dotenv import load_dotenv

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext

from vanna.integrations.ollama import OllamaLlmService
from vanna.integrations.mysql import MySQLRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory

from vanna.tools import RunSqlTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool,
    SaveTextMemoryTool
)


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv("Week 6/.env")

print("Environment variables loaded successfully!")


# --------------------------------------------------
# 2. Create Ollama LLM service
# --------------------------------------------------

llm = OllamaLlmService(
    model="qwen2.5:3b",
    host="http://localhost:11434",
    timeout=240,
    num_ctx=8192,
    temperature=0.2
)

print("Vanna + Qwen LLM service created successfully!")


# --------------------------------------------------
# 3. Connect Vanna to MySQL
# --------------------------------------------------

mysql_runner = MySQLRunner(
    host=os.getenv("MYSQL_HOST"),
    database=os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    port=int(os.getenv("MYSQL_PORT"))
)

print("Vanna MySQL runner created successfully!")


# --------------------------------------------------
# 4. Create SQL execution tool
# --------------------------------------------------

db_tool = RunSqlTool(
    sql_runner=mysql_runner
)

print("Vanna SQL tool created successfully!")


# --------------------------------------------------
# 5. Create Vanna agent memory
# --------------------------------------------------

agent_memory = DemoAgentMemory(
    max_items=1000
)

print("Vanna Agent memory created successfully!")


# --------------------------------------------------
# 6. Create tool registry
# --------------------------------------------------

tool_registry = ToolRegistry()


tool_registry.register_local_tool(
    db_tool,
    access_groups=["admin", "user"]
)


tool_registry.register_local_tool(
    SearchSavedCorrectToolUsesTool(),
    access_groups=["admin", "user"]
)


tool_registry.register_local_tool(
    SaveQuestionToolArgsTool(),
    access_groups=["admin"]
)


tool_registry.register_local_tool(
    SaveTextMemoryTool(),
    access_groups=["admin", "user"]
)


print("Vanna ToolRegistry created successfully!")


# --------------------------------------------------
# 7. Local user resolver
# --------------------------------------------------

class LocalUserResolver(UserResolver):

    async def resolve_user(
        self,
        request_context: RequestContext
    ) -> User:

        return User(
            id="harini",
            username="Harini",
            group_memberships=["admin", "user"]
        )


user_resolver = LocalUserResolver()

print("Local user resolver created successfully!")


# --------------------------------------------------
# 8. Create Vanna Agent
# --------------------------------------------------

agent = Agent(
    llm_service=llm,
    tool_registry=tool_registry,
    user_resolver=user_resolver,
    agent_memory=agent_memory
)

print("Vanna Agent created successfully!")


# --------------------------------------------------
# 9. Database schema context
# --------------------------------------------------

schema_context = """
You are working with a MySQL database called cynaris_sales.

TABLE: customers
COLUMNS:
- customer_id INT PRIMARY KEY
- customer_name VARCHAR(100)
- city VARCHAR(50)

TABLE: employees
COLUMNS:
- employee_id INT PRIMARY KEY
- employee_name VARCHAR(100)
- manager_id INT

TABLE: sales
COLUMNS:
- sale_id INT PRIMARY KEY
- customer_name VARCHAR(100)
- product VARCHAR(100)
- category VARCHAR(50)
- quantity INT
- price DECIMAL(10,2)
- city VARCHAR(50)
- sale_date DATE
- discount DECIMAL(5,2)

IMPORTANT:
For sales value, calculate:
quantity * price

Examples:

Question:
How many customers are there in each city?

SQL:
SELECT city, COUNT(*) AS customer_count
FROM customers
GROUP BY city;

Question:
What is the total sales value?

SQL:
SELECT SUM(quantity * price) AS total_sales
FROM sales;

Question:
What are the total sales for each category?

SQL:
SELECT category, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY category;

Question:
What are the top products by sales?

SQL:
SELECT product, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC;

Question:
What are the total sales for each city?

SQL:
SELECT city, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY city
ORDER BY total_sales DESC;
"""


# --------------------------------------------------
# 10. Test natural-language query
# --------------------------------------------------

async def test_agent():

    request_context = RequestContext()

    question = "How many customers are there in each city?"

    full_question = f"""
{schema_context}

Now answer this question:

{question}

Generate the correct SQL query and execute it using the SQL tool.
"""

    print("\n----------------------------------------")
    print("Natural Language Question:")
    print(question)
    print("----------------------------------------\n")

    async for response in agent.send_message(
        request_context,
        full_question
    ):
        print(response)


# --------------------------------------------------
# 11. Run
# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(test_agent())