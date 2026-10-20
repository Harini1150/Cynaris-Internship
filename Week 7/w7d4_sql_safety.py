import sqlparse
from sqlparse.tokens import DML, DDL, Keyword


class UnsafeSQLQuery(ValueError):
    """Raised when a query is not permitted by the read-only policy."""


def validate_read_only_sql(sql: str) -> str:
    """Allow one SELECT statement and reject non-read-only SQL."""
    if not isinstance(sql, str) or not sql.strip():
        raise UnsafeSQLQuery("SQL query cannot be empty.")

    cleaned = sqlparse.format(sql, strip_comments=True).strip()
    statements = [stmt for stmt in sqlparse.parse(cleaned) if str(stmt).strip()]

    if len(statements) != 1:
        raise UnsafeSQLQuery("Only one SQL statement is allowed.")

    statement = statements[0]
    first_token = next(
        (token for token in statement.tokens
         if not token.is_whitespace and not token.is_group
         and not str(token.ttype).startswith("Token.Comment")),
        None,
    )

    if first_token is None or first_token.value.upper() != "SELECT":
        raise UnsafeSQLQuery("Only SELECT queries are allowed.")

    blocked_keywords = {
        "INSERT", "UPDATE", "DELETE", "REPLACE", "DROP", "ALTER",
        "CREATE", "TRUNCATE", "GRANT", "REVOKE", "CALL", "EXEC",
        "EXECUTE", "SET", "USE", "INTO", "OUTFILE", "DUMPFILE",
        "LOCK", "UNLOCK",
    }

    for token in statement.flatten():
        if token.ttype in DML and token.value.upper() != "SELECT":
            raise UnsafeSQLQuery("Data-changing SQL is not allowed.")
        if token.ttype in DDL:
            raise UnsafeSQLQuery("Schema-changing SQL is not allowed.")
        if token.ttype in Keyword and token.value.upper() in blocked_keywords:
            raise UnsafeSQLQuery("This query contains a prohibited SQL operation.")

    if ";" in cleaned.rstrip().rstrip(";"):
        raise UnsafeSQLQuery("Multiple SQL statements are not allowed.")

    return cleaned
