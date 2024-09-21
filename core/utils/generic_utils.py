
from accounts.models import AccountsLoggingModel


def is_filter_required(input_key : str, data : dict):
    """checking if filter is required for the given key"""
    return data.get(input_key) not in [None, "", "undefined"]

def create_log(msg : str, user : object)->None:
    AccountsLoggingModel.objects.create(
        message = msg,
        created_by = user
    )
