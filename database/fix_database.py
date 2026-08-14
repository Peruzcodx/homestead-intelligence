import sqlite3


DB_PATH = "database/estatepulse.db"


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


# Fix Markdown-formatted URLs
cursor.execute("""
    UPDATE properties
    SET url = substr(
        url,
        2,
        instr(url, "](") - 2
    )
    WHERE url LIKE '[%](%)'
""")


# Convert Studio properties to 0 bedrooms
cursor.execute("""
    UPDATE properties
    SET bedrooms = 0
    WHERE bedrooms IS NULL
      AND LOWER(title) LIKE 'studio%'
""")


connection.commit()


print("Database fixes applied.")
print(f"Rows updated: {cursor.rowcount}")


# Verify URLs
print("\n========== URL CHECK ==========")

cursor.execute("""
    SELECT url
    FROM properties
    LIMIT 3
""")

for row in cursor.fetchall():
    print(row[0])


# Verify bedrooms
cursor.execute("""
    SELECT COUNT(*)
    FROM properties
    WHERE bedrooms IS NULL
""")

missing_bedrooms = cursor.fetchone()[0]

print("\n========== BEDROOM CHECK ==========")
print(f"Missing bedrooms: {missing_bedrooms}")


connection.close()