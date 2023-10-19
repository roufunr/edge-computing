# your_script.py

import sys
import time

# Redirect stdout and stderr to nohup.out
sys.stdout = open('nohup.out', 'a')
sys.stderr = sys.stdout

print("This is a message to nohup.out")

# Your main script logic here
for i in range(5):
    print(f"Processing iteration {i}")
    time.sleep(1)

print("Script completed")

# Close the file to flush the buffer and release resources
sys.stdout.close()
