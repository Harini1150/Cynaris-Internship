import sys
sys.path.insert(0, "Week 7")

from w7d4_sql_safety import validate_read_only_sql, UnsafeSQLQuery

tests = [
    ("Safe SELECT", "SELECT COUNT(*) FROM customers", True),
    ("DELETE", "DELETE FROM customers", False),
    ("UPDATE", "UPDATE customers SET city = 'Delhi'", False),
    ("Multiple statements", "SELECT * FROM customers; DELETE FROM customers", False),
    ("WITH DELETE", "WITH x AS (SELECT 1) DELETE FROM customers", False),
]

for name, sql, should_pass in tests:
    try:
        validate_read_only_sql(sql)
        passed = True
    except UnsafeSQLQuery:
        passed = False

    status = "PASS" if passed == should_pass else "FAIL"
    print(f"{status}: {name}")
