try:
    import hello.messages
except:
    # We include an except clause to catch indentation errors
    # e.g. a second line being emitted with no indentation.
    raise


def print_hello():
    print(hello.messages.message)
