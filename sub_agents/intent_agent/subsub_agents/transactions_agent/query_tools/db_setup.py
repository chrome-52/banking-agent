import sqlite3

def setup_db():
  return
  # Create a SQLite database file
  conn = sqlite3.connect('banking_demo.db')
  cursor = conn.cursor()

  try:
    # Create the Accounts table
    cursor.execute("""
        CREATE TABLE Accounts (
          account_id INT PRIMARY KEY,
          full_name VARCHAR(100),
          zip_code VARCHAR(10),
          date_of_birth DATE
          );
      """)

    # Insert values into the Accounts table
    cursor.execute("""
        INSERT INTO Accounts (account_id, full_name, zip_code, date_of_birth) VALUES
          (12345, 'Chinmay Ratnaparkhi', '441614', '2001-08-29'),
          (67890, 'Gunjan Turkar', '560012', '2001-08-03'),
          (98765, 'Gunjan Turkar', '560012', '2001-08-03'),
          (43210, 'Zaki Seraj', '700001', '1998-10-6'),
          (11111, 'Chinmay Ratnaparkhi', '441614', '2001-08-29'),
          (99999, 'Gunjan Turkar', '560012', '2001-08-03');
    """)

    # Create the transactions table
    cursor.execute("""
        CREATE TABLE Transactions (
          transaction_id INTEGER PRIMARY KEY,  -- Auto-increments automatically in SQLite
          date DATETIME NOT NULL,
          amount DECIMAL(19, 4) NOT NULL,
          type VARCHAR(50),
          vendor VARCHAR(255),
          reason VARCHAR(255),
          status BOOLEAN,
          account_id INT,
          FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
      );
    """)

    # Insert values into the transactions table
    cursor.execute("""
        INSERT INTO Transactions (date, amount, type, vendor, reason, status, account_id) VALUES
          ('2025-08-01 10:30:00', 1500.00, 'Debit', 'Amazon', 'Electronics', 1, 12345),
          ('2025-08-03 14:20:00', 200.50, 'Debit', 'Flipkart', 'Groceries', 1, 12345),
          ('2025-08-05 09:00:00', 5000.00, 'Credit', 'Employer', 'Salary', 1, 12345),
          ('2025-08-07 18:45:00', 750.00, 'Debit', 'Zomato', 'Food', 1, 12345),
          ('2025-08-08 12:10:00', 120.00, 'Debit', 'Uber', 'Travel', 0, 12345),

          ('2025-08-02 08:30:00', 100.00, 'Debit', 'BigBasket', 'Groceries', 1, 67890),
          ('2025-08-04 16:00:00', 250.00, 'Debit', 'Myntra', 'Clothing', 1, 67890),
          ('2025-08-06 11:20:00', 2000.00, 'Credit', 'Freelance', 'Payment', 1, 67890),

          ('2025-08-03 19:30:00', 800.00, 'Debit', 'Amazon', 'Books', 1, 98765),
          ('2025-08-09 14:40:00', 150.00, 'Debit', 'Swiggy', 'Food', 1, 98765),
          ('2025-08-02 13:00:00', 1500.00, 'Credit', 'Scholarship', 'Education', 1, 98765),
          ('2025-08-04 10:10:00', 100.00, 'Debit', 'Amazon', 'Stationery', 1, 98765),
          ('2025-08-06 21:15:00', 650.00, 'Debit', 'Ajio', 'Clothing', 1, 98765),

          ('2025-08-01 10:00:00', 3000.00, 'Credit', 'Employer', 'Salary', 1, 43210),
          ('2025-08-03 15:00:00', 180.00, 'Debit', 'Reliance Fresh', 'Groceries', 1, 43210),
          ('2025-08-05 20:30:00', 220.00, 'Debit', 'Ola', 'Travel', 1, 43210),

          ('2025-08-07 08:30:00', 130.00, 'Debit', 'Dominos', 'Food', 0, 99999),
          ('2025-08-09 17:00:00', 75.00, 'Debit', 'BookMyShow', 'Entertainment', 1, 99999),

          ('2025-08-10 08:00:00', 2500.00, 'Credit', 'Client', 'Project Work', 1, 11111),
          ('2025-08-11 09:45:00', 950.00, 'Debit', 'MakeMyTrip', 'Travel', 1, 11111);
      """)

    # Commit the changes
    conn.commit()
  except:
    print("Database already exists.")
  # Close the connection
  conn.close()