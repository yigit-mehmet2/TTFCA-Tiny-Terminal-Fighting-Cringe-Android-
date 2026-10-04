# Imports
import subprocess
import os

# banner
BANNER = """
TTFCA v1.0 (Tiny Terminal Fighting with Cringe Android)
Type 'exit' to quit.
"""
print(BANNER)

def main():
    # Main Loop
     while True:
        # Input (PS1) & Split
        try:
            cmd = input(f"{os.getcwd()} $ ")
            token = cmd.split()
        
        # Conditionals
            if cmd == "exit":
                break
            if len(token) > 1 and token[1] == "~":
                # JUST, Cringe Android..
                home_path = os.environ.get("HOME", "/data/data/com.termux/files/home")
                os.chdir(home_path)
            elif cmd.startswith("cd"):
                os.chdir(token[1])
            else:
                subprocess.run(cmd, shell=True)
        except IndexError:
            print("​Error: Missing required argument.")
        except FileNotFoundError:
            print("Error: No such file or directory.")
        except KeyboardInterrupt:
            pass
                   
main()

# Writing code is very difficult in PyramIDE...
