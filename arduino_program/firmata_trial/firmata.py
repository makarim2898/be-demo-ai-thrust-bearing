from pyfirmata import Arduino, util
import time

# Replace with your Arduino's port (check with `ls /dev/ttyACM*` or `COM3` on Windows)
board = Arduino('/dev/ttyACM0')

# Start an iterator thread to avoid buffer overflow
it = util.Iterator(board)
it.start()

# Example: use pin 13 (built-in LED)
pin13 = board.get_pin('d:13:o')  # d=digital, 13=pin number, o=output

# Blink LED
for i in range(10):
    pin13.write(1)  # ON
    time.sleep(1)
    pin13.write(0)  # OFF
    time.sleep(1)

board.exit()
