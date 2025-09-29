import sqlite3

# Connect to your database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all users with their details
cursor.execute("SELECT id, username, age, weight, height FROM users")
users = cursor.fetchall()

print("Users in database:")
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Age: {user[2]}, Weight: {user[3]}, Height: {user[4]}")

conn.close()
