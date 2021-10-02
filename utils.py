from sys import stderr


def eprint(msg) -> None:
    print("[!] %s" % (msg), file=stderr)
