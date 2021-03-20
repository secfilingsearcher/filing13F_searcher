"""Generates Primary Key"""
import hashlib


def primary_key_generator(row):
    """Uses hash to generate Primary Key based on original row data"""
    full_str = ''.join(str(cell) for cell in row)
    result = hashlib.md5(full_str.encode())
    return result.hexdigest()
