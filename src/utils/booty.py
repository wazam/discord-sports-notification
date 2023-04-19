import requests


def lookup(user_search):
    msg = f'{user_search}'
    return msg


# Used for executing directly when testing
if __name__ == "__main__":
    msg = lookup('booty')
    print(msg, flush=True)
