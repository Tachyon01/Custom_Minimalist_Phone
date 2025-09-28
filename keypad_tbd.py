import time

# This is a placeholder for the actual GPIO keypad decoding logic.
def decode_keypad():
    """
    This function will contain the logic to read GPIO pins
    and determine which button was pressed.
    For simulation, we read a single character from the command line.
    """
    # In a real scenario, you would have GPIO logic here, probably using
    # a library like RPi.GPIO to detect button presses.
    # This input simulates a single character press from your keypad.
    key = input("SIMULATED KEY PRESS (e.g., a,b,c,s,n,q,1,2,3): ")
    return key[0] if key else ""

def get_key():
    """
    Waits for a single key press from the keypad and returns it.
    This is the main function the rest of the application will use.
    """
    # print("(Waiting for keypad input...)")
    # This loop simulates waiting for a button press.
    # In a real GPIO implementation, this might be an event-driven callback
    # or a loop that polls GPIO pins.
    while True:
        key = decode_keypad()
        if key:
            # print(f"Key '{key}' detected.")
            # A short debounce delay is good practice for physical buttons
            time.sleep(0.2) 
            return key.lower()
