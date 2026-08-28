"""
app/features/identity/exceptions.py

Here i will try to generat my own errors exceptions
"""


class InvalidEmailError(Exception):
    """
    Emails violates domain rules in that case i will call this
    """
    pass