from google.adk.tools import FunctionTool
import sqlite3

from .db_setup import setup_db


def execute_query(query: str, database: str = '/home/chinmay244625/banking_demo/banking_demo.db') -> list:
  """
  Connects to a SQL database and executes the given query.

  Args:
    query (str): The SQL query to execute.
    database (str, optional): The database in which the query is to be executed.
  """
  setup_db()
  try:
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(query)
    return {"status":"success", "rows":cursor.fetchall()}
  except:
    return {"status":"error", "rows":None}

query_executor_tool = FunctionTool(func=execute_query)