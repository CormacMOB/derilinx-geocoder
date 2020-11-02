import re

def validate_address(address_string):
    """
        Validate that a string is a comma seperated address.
    """
    valid = False
    if not address_string or (address_string.strip() == ""):
        return valid

    if ',' not in address_string:
        return valid

    whitelist = r'[a-zA-Z0-9()\'-,./ ]'
    result = re.sub(whitelist, '', address_string)
    if len(result) == 0:
        valid = True

    return valid
