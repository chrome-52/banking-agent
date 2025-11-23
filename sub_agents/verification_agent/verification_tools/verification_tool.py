import sqlite3
from google.adk.tools import ToolContext, FunctionTool

#from .db_setup import setup_db


verification_query = """
SELECT account_id FROM Accounts
WHERE full_name = '{name}'
AND zip_code = '{zip_code}'
AND date_of_birth = '{dob}';
"""

def execute_query(query: str, database: str = '/home/chinmay244625/banking_demo/banking_demo.db') -> list:
  """
  Connects to a SQL database and executes the given query.

  Args:
    query (str): The SQL query to execute.
    database (str, optional): The path to the SQL database in which the query is to be executed.
  """
  #setup_db()
  try:
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(query)
    return {"status":"success", "rows":cursor.fetchall()}
  except Exception as e:
    return {"status":"error", "message":str(e)}


def verify_user(name: str, zip_code: str, dob: str):
  """
  Uses the given details to verify a user.

  Args:
    name (str): The full name of the user.
    zip_code (str): The ZIP code for the user's permanent address.
    dob (str): The user's date of birth in YYYY-MM-DD format.
  """
  verification = execute_query(verification_query.format(name=name,
                                                         zip_code=zip_code,
                                                         dob=dob))
  if verification['status'] == "success":
    if len(verification['rows']) > 0:
      return {"status":"success", "message":f"Accounts found: {[k[0] for k in verification['rows']]}"}
    else:
      return {"status":"failure", "message":"Verification Failed! Please check your details."}
  else:
    return verification


def update_and_verify(tool_context: ToolContext, name: str = 'None', zip_code: str = 'None', dob: str = 'None'):
  """
  Uses the values provided to update a user's details.
  Once all three values are obtained, attempts to verify the user.

  Args:
    name (str): The full name of the user.
    zip_code (str): The ZIP code for the user's permanent address.
    dob (str): The user's date of birth in DD/MM/YYYY format.
  """
  if name != 'None':
    tool_context.state['Full Name'] = name
  if zip_code != 'None':
    tool_context.state['ZIP code'] = zip_code
  if dob != 'None':
    tool_context.state['Date of Birth'] = dob

  state = tool_context.state
  if state.get('Full Name', None) and state.get('ZIP code', None) and state.get('Date of Birth', None):
    verification = verify_user(name=state['Full Name'], zip_code=state['ZIP code'], dob=state['Date of Birth'])
  else:
    verification = {"status":"pending", "message":"Verification is pending. Please provide the nessary details."}

  tool_context.state['verification status'] = verification['status']
  if verification['status'] == 'success':
    tool_context.state['Accounts'] = eval(verification['message'].split(":")[1])
  return verification


update_verify_tool = FunctionTool(func=update_and_verify)
