from bs4 import BeautifulSoup
from getopt import getopt, GetoptError
import pickle
from random import randint
from re import compile as re_compile
import sqlite3
from sys import argv, stderr

WORD = re_compile(r"(?:[a-zA-Z][-'a-zA-Z]*[0-9]*|[0-9][0-9,]*(?:'?s|th|nd|st|rd)?|[0-9](?:\.[0-9])+)")

def parse():
    conn = sqlite3.connect("vienna.db")
    c = conn.cursor()

    chain = {}

    for row in c.execute("SELECT text FROM messages WHERE folder_id=14"):
        text = row[0]
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()

        parts = WORD.findall(text)
        last = (None, None)

        for p in parts:
            if not p:
                continue

            selection = chain.get(last)
            if selection is None:
                selection = []
                chain[last] = selection
            
            selection.append(p)
            last = (last[1], p)

    with open("chain.pickle", "wb") as fd:
        pickle.dump(chain, fd)

def babble():
    with open("chain.pickle", "rb") as fd:
        chain = pickle.load(fd)
    
    length = 100
    last = (None, None)
    for i in range(length):
        selection = chain.get(last)
        if len(selection) == 0:
            break
        word = selection[randint(0, len(selection)-1)]
        print(word, end=' ')
        last = (last[1], word)

    print("")

def main(args):
    cmd = babble
    try:
        opts, args = getopt(args, "bp", ["babble", "parse"])
        for opt, arg in opts:
            if opt in ["-b", "--babble"]:
                cmd = babble
            elif opt in ["-p", "--parse"]:
                cmd = parse
    except GetoptError as e:
        print(str(e), file=stderr)
        return 1

    if args:
        print(f"Unknown argument {args[0]!r}", file=stderr)
        usage()
        return 1

    cmd()
    return 0

def usage():
    stderr.write("Usage: awsbabbler [--babble|--parse]\nDefaults to --babble\n")

if __name__ == "__main__":
    exit(main(argv[1:]))
