#example from https://github.com/hktan125/CircuitPython-HuskyLens/blob/main/Examples/tag_recognition.py

import board
import time
import neopixel
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_TAG_RECOGNITION") # Redirect to Tag Recognition Function

pixel = neopixel.NeoPixel(board.GP28, 1)

# Colors (r,g,b)
OFF = (0,0,0)
ON = (30,30,30)

# Assign different color to different ID
color = {1:(30,0,0),
         2:(0,30,0),
         3:(0,0,30)}

while True:
    try:
        results = hl.learnedBlocks() # Only get learned results
        
        if results: # if result not empty
            all_id = list(set([result.ID for result in results])) # Get all ID
            all_id.sort()
            print(f"All Tag ID: {all_id}")
            
            first = all_id[0] # Only take first Tag ID
            pixel.fill(color[first])
            print(f"ID: {first}")
        else:
            pixel.fill(OFF)
            
    except KeyError: # Handle if there is no color to be assigned to an ID
        pixel.fill(ON)
    
    finally:
        pixel.show()
        time.sleep(0.5)