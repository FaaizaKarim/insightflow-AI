"""
Tests for the SQL tool validation layer.
"""
import pytest
from app.tools.sql_tool import validate_sql


def test_valid_select():
    sql = "SELECT id, name FROM customers WHERE region = 'Europe' LIMIT 10"
    valid, reason = validate_sql(sql)
    assert valid is True


def test_blocks_insert():
    sql = "INSERT INTO customers (name) VALUES ('hacker')"
    valid, reason = validate_sql(sql)
    assert valid is False
    assert "SELECT" in reason


def test_blocks_drop():
    sql = "SELECT * FROM customers; DROP TABLE customers;"
    valid, reason = validate_sql(sql)
    assert valid is False


def test_blocks_unknown_table():
    sql = "SELECT * FROM secret_table"
    valid, reason = validate_sql(sql)
    assert valid is False
    assert "secret_table" in reason


def test_allows_join():
    sql = "SELECT c.name, o.amount FROM customers c JOIN orders o ON c.id = o.customer_id"
    valid, reason = validate_sql(sql)
    assert valid is True


def test_blocks_update():
    sql = "UPDATE customers SET is_churned = true WHERE id = 1"
    valid, reason = validate_sql(sql)
    assert valid is False
