DEBUG = 1


def debug(*args):
    if DEBUG:
        print("[DEBUG]", *args)
