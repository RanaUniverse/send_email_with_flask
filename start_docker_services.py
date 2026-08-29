"""
I need to start this first to start with my application
"""

import subprocess

command = [
    "ls",
    "-a",
]
result = subprocess.run(command)
# print(result)


command = [
    "docker",
    "start",
    "redis8",
    "mailpit",
]
print("Starting the Docker services.")
result = subprocess.run(command)
# print(result)
