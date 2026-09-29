import pandas as pd
import sqlite3
import ollama

df = pd.read_csv("data/sales.csv")

print("COLUMN NAMES:")
print(df.columns.tolist())

df["Sales"] = df["Quantity"] * df["Unit_Price"]

conn = sqlite3.connect("sales.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

print("Sales data loaded into SQLite successfully!")
print(df["Sales"].head())
product_sales = df.groupby("Product")["Sales"].sum()
print(product_sales)
highest_product = product_sales.idxmax()
print("Highest sales product:", highest_product)
highest_value = product_sales.max()
print("Highest Sales Value:", highest_value)
# Result validation
validation_sales = product_sales.sort_values(ascending=False)
if validation_sales.index[0] == highest_product and validation_sales.iloc[0] == highest_value:
    print("VALIDATION: PASSED")
else:
    print("VALIDATION: FAILED")

analysis_result = {
    "highest_product": highest_product,
    "highest_sales": highest_value,
    "validation": "PASSED"
}

print("\nAnalysis Result:")
print(analysis_result)
llm_input = f"""
Analyze the following sales analysis result:

Highest Sales Product: {analysis_result["highest_product"]}
Highest Sales Value: {analysis_result["highest_sales"]}
Validation Status: {analysis_result["validation"]}
"""
from ollama import chat

response = chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": llm_input
        }
    ]
)

print("\nFINAL LLM ANSWER:")
print(response.message.content)

print("\nLLM INPUT:")
print(llm_input)

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
print("DATASET SHAPE:", df.shape)
cursor = conn.cursor()

cursor.execute("""
SELECT Product, SUM(Sales) AS total_sales
FROM sales
GROUP BY Product
ORDER BY total_sales DESC
LIMIT 1
""")

sql_result = cursor.fetchone()

print("\nHIGHEST SALES FROM SQL:")
print(sql_result)

if sql_result[0] == highest_product and sql_result[1] == highest_value:
    print("SQL VALIDATION: PASSED")
else:
    print("SQL VALIDATION: FAILED")

user_question = input("\nAsk your question: ")

sql_prompt = f"""
You are a SQL assistant.

Database table: sales

Columns:
Product
Quantity
Unit_Price
Sales
Order_Date

Your task:
Convert the user's question into a valid SQLite SELECT query.

Rules:
1. Use only the table: sales
2. Use only the columns listed above.
3. Generate SQL based ONLY on the user's actual question.
4. Do not assume that the user is asking about highest sales.
5. For total sales, use SUM(Sales).
6. For product-wise sales, use GROUP BY Product.
7. For highest sales by product, use SUM(Sales), GROUP BY Product, and ORDER BY total sales DESC.
8. For lowest sales by product, use SUM(Sales), GROUP BY Product, and ORDER BY total sales ASC.
9. For questions asking how many different or unique products there are, use COUNT(DISTINCT Product).
10. For month-based questions, use SQLite strftime('%m', Order_Date) to filter the month.
11. For January, use strftime('%m', Order_Date) = '01'. For February use '02', and so on.
12. Do not include explanations or markdown.
13. Only SELECT statements are allowed.
14. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or other modification commands.

User question:
{user_question}

Return only the SQL query.
"""

sql_response = chat(
    model="llama3.2:3b",
    messages=[
        {"role": "user", "content": sql_prompt}
    ]
)

generated_sql = sql_response.message.content.strip()

# Remove markdown code fences if the LLM returns them
if generated_sql.startswith("```"):
    lines = generated_sql.splitlines()
    lines = [line for line in lines if not line.strip().startswith("```")]
    generated_sql = "\n".join(lines).strip()

print("\nGENERATED SQL:")
print(generated_sql)


# SQL SAFETY VALIDATION
sql_upper = generated_sql.upper().strip()

# Remove one trailing semicolon
if sql_upper.endswith(";"):
    sql_upper = sql_upper[:-1].strip()
    generated_sql = generated_sql[:-1].strip()

# Only SELECT queries are allowed
if not sql_upper.startswith("SELECT "):
    print("\nSQL SECURITY ERROR: Only SELECT queries are allowed.")
    conn.close()
    exit()

# Block dangerous SQL commands
blocked_commands = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
    "PRAGMA"
]

if any(command in sql_upper.split() for command in blocked_commands):
    print("\nSQL SECURITY ERROR: Dangerous SQL command detected.")
    conn.close()
    exit()

print("SQL SECURITY VALIDATION: PASSED")

# Execute only after safety validation
try:
    cursor.execute(generated_sql)
    query_result = cursor.fetchone()

    print("\nLLM SQL RESULT:")
    print(query_result)

except sqlite3.Error as e:
    print("\nSQL EXECUTION ERROR:")
    print(e)
    conn.close()
    exit()


final_prompt = f"""
Answer the user's question using the SQL result.

User question:
{user_question}

SQL result:
{query_result}

Give a clear and concise answer in natural language.
Do not assume or add a currency symbol unless the user or dataset specifies the currency.
"""

final_response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": final_prompt
        }
    ]
)

final_answer = final_response["message"]["content"]

print("\nFINAL ANSWER:")
print(final_answer)