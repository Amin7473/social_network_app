
from accounts.models import AccountsLoggingModel


def is_filter_required(input_key : str, data : dict):
    """checking if filter is required for the given key"""
    return data.get(input_key) not in [None, "", "undefined"]

def create_log(msg : str, user : object)->None:
    AccountsLoggingModel.objects.create(
        message = msg,
        created_by = user
    )

import re

def is_valid_password( password):
    """
    Check if password is strong
    """
    if not any(char in '!@#$%^&*()-=_+`~[]{}|;:"<>,./?' for char in password):
        return False        
    if len(password) <= 8 or len(password)> 16:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True