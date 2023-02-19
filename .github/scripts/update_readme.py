#!/usr/bin/env python3
import re
import random

# Define the regex pattern to match HTML comments containing "attr-start" and "attr-end"
pattern = r'<!--\s*attr-start\s*-->(.*?)<!--\s*attr-end\s*-->'

# Define the function to generate random replacement text
def random_text(length=8):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=length))

# Open the file for reading and writing
with open('README.md', 'r+') as f:
    # Read the contents of the file
    contents = f.read()

    # Use regex to find all matches of the pattern
    matches = re.findall(pattern, contents, flags=re.DOTALL)

    # Loop over the matches and replace them with random text
    for match in matches:
        replacement = random_text()
        contents = contents.replace(match, replacement)

    # Reset the file pointer to the beginning of the file and truncate the file
    f.seek(0)
    f.truncate()

    # Write the modified contents back to the file
    f.write(contents)
