# AI Data Analyst Agent

An AI-powered data analysis agent that allows users to ask questions about sales data in natural language.

## Project Overview

This project combines Python, Pandas, SQLite, SQL, and a local Llama 3.2 LLM through Ollama.

The agent can:

- Load sales data from CSV
- Validate the dataset
- Calculate sales
- Store and query data using SQLite
- Convert natural-language questions into SQL
- Validate SQL for safety
- Execute SELECT queries
- Validate query results
- Generate natural-language answers using Llama 3.2

## Architecture

User Question
      ↓
Local Llama 3.2
      ↓
Natural Language → SQL
      ↓
SQL Safety Validation
      ↓
SQLite Database
      ↓
Query Result Validation
      ↓
Local Llama 3.2
      ↓
Final Natural Language Answer

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Ollama
- Llama 3.2
- Git & GitHub

## Key Features

### 1. Data Ingestion
Loads sales data from CSV using Pandas.

### 2. Data Validation
Checks for missing values and duplicate records.

### 3. Sales Calculation
Sales are calculated using:

Quantity × Price

### 4. SQL Analysis
Sales data is stored in SQLite and queried using SQL.

### 5. Natural Language to SQL
Users can ask questions in normal English.  
The local Llama 3.2 model converts the question into SQL.

### 6. SQL Security
Only SELECT queries are allowed.

Dangerous operations such as:

- DROP
- DELETE
- UPDATE
- INSERT
- ALTER

are blocked.

### 7. Result Validation
The generated SQL result is validated before producing the final answer.

### 8. Local LLM
The project uses Llama 3.2 through Ollama, so no paid cloud LLM API is required.

## Example Questions

- Which product has the highest sales?
- Which product has the lowest sales?
- What is the total sales?
- How many unique products are there?
- What were the sales in January?

## Project Structure

```text
ai-data-analyst-agent/
│
├── data/
│   └── sales.csv
│
├── src/
├── tests/
├── data_analysis.py
├── generate.dataset.py
├── requirements.txt
├── .gitignore
└── README.md