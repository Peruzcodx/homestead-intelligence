import sqlite3


DB_PATH = "database/estatepulse.db"


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


# ============================================================
# 1. TOTAL RECORDS
# ============================================================

cursor.execute("SELECT COUNT(*) FROM properties")

total_properties = cursor.fetchone()[0]

print("\n========== DATABASE CHECK ==========")
print(f"Total properties: {total_properties}")


# ============================================================
# 2. DUPLICATE URL CHECK
# ============================================================

cursor.execute("""
    SELECT url, COUNT(*)
    FROM properties
    GROUP BY url
    HAVING COUNT(*) > 1
""")

duplicates = cursor.fetchall()

print(f"Duplicate URLs: {len(duplicates)}")


# ============================================================
# 3. NULL / MISSING DATA CHECK
# ============================================================

fields = [
    "url",
    "title",
    "price",
    "street",
    "city",
    "state",
    "zip",
    "neighborhood",
    "bedrooms",
    "bathrooms",
    "sqft",
    "property_type",
    "availability"
]

print("\n========== MISSING DATA ==========")

for field in fields:

    cursor.execute(
        f"SELECT COUNT(*) FROM properties WHERE {field} IS NULL"
    )

    missing = cursor.fetchone()[0]

    print(f"{field}: {missing}")


# ============================================================
# 4. SAMPLE RECORDS
# ============================================================

print("\n========== SAMPLE RECORDS ==========")

cursor.execute("""
    SELECT
        title,
        price,
        bedrooms,
        bathrooms,
        sqft,
        property_type,
        availability
    FROM properties
    LIMIT 5
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================================
# 5. CHECK FRACTIONAL BATHROOMS
# ============================================================

print("\n========== BATHROOM CHECK ==========")

cursor.execute("""
    SELECT DISTINCT bathrooms
    FROM properties
    WHERE bathrooms IS NOT NULL
    ORDER BY bathrooms
""")

bathrooms = cursor.fetchall()

for bathroom in bathrooms:
    print(bathroom[0])


# ============================================================
# 6. CHECK PRICE RANGE
# ============================================================

print("\n========== PRICE CHECK ==========")

cursor.execute("""
    SELECT
        MIN(price),
        MAX(price),
        AVG(price)
    FROM properties
    WHERE price IS NOT NULL
""")

minimum, maximum, average = cursor.fetchone()

print(f"Lowest price:  {minimum}")
print(f"Highest price: {maximum}")
print(f"Average price: {average}")


# ============================================================
# 7. CHECK SQFT RANGE
# ============================================================
# ============================================================
# 8. CHECK MISSING BEDROOMS
# ============================================================

cursor.execute("""
    SELECT
        title,
        url,
        bedrooms
    FROM properties
    WHERE bedrooms IS NULL
""")

missing_bedrooms = cursor.fetchall()

print("\n========== PROPERTIES MISSING BEDROOMS ==========")

for row in missing_bedrooms:
    print(row)

print(f"\nTotal missing bedrooms: {len(missing_bedrooms)}")


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

print("\n========== CHECK COMPLETE ==========")