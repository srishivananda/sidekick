#!env python3

# imports
import os
import sys
import inspect
import readline

# get current directory, and add parent directory to path
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

# source all skill modules
from skill.example import *
from skill.webextract import *

# the command line interface
def main():
    skills = {}

    # inspect all modules, retrieve the functions 
    functions = inspect.getmembers(sys.modules['__main__'])
    for (name, function) in functions:
        prefix = "skill_"
        offset = len(prefix)
        # filter to ones that start with skill_
        if name[0:offset] == prefix:
            skills[name[offset:]] = function

    # using skill text, create the auto-completer
    def complete(text, state):
        results = [skill for skill in skills if skill.startswith(text)] + [None]
        return results[state]

    # enable auto complete for skills
    readline.set_completer(complete)
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    
    # listen in cli mode, till you see a exit/bye/^D
    try:
        while True:
            command = input("sidekick> ")
            args = command.split()
            if args:
                skill = args[0]
                if skill in ['exit', 'bye']:
                    break
                elif skill in skills.keys():
                    skills[skill](args[1:])
                else:
                    print("Unknown command.")
    except EOFError:
        print()
        print("Bye!") 

if __name__ == '__main__':
    main()