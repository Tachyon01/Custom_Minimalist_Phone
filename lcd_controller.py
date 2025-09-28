import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import time

# --- Configuration ---
# This part runs only once when the module is imported
GPIO.setwarnings(False)

# Define pin numbers (BOARD mode)
RS_PIN = 3
E_PIN = 5
DATA_PINS = [7, 8, 10, 11]

# Initialize the LCD object
lcd = CharLCD(pin_rs=RS_PIN,
              pin_e=E_PIN,
              pins_data=DATA_PINS,
              numbering_mode=GPIO.BOARD,
              cols=16,
              rows=2,
              dotsize=8,
              compat_mode=True)

# --- Public Functions ---
'''
def display_lcd(line1, line2):
    """
    Displays two lines of text on the LCD.
    """
    lcd.clear()
    lcd.write_string(str(line1))
    lcd.cursor_pos = (1, 0)
    lcd.write_string(str(line2))
'''

# Replace the old display_lcd function in lcd_controller.py with this one
'''
def display_lcd(line1, line2):
    """
    Displays two lines of text. This version uses a manual clear
    by writing blank spaces, which is more reliable than lcd.clear().
    """
    # Step 1: Manually clear the display by writing 16 spaces to each line
    lcd.cursor_pos = (0, 0)
    lcd.write_string("                ")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("                ")

    # Step 2: Return to the start and write the fresh text
    lcd.cursor_pos = (0, 0)
    lcd.write_string(str(line1))
    lcd.cursor_pos = (1, 0)
    lcd.write_string(str(line2))
'''
# Replace the old display_lcd function in your lcd_controller.py with this one.
'''''''''''''''''''''''''''''''''''''''''''''''''''''
def display_lcd(line1, line2):
    """
    A "super robust" display function designed to be more resilient
    in multi-threaded applications. It manually clears the screen and
    writes character by character with delays.
    """
    try:
        # Step 1: Manually clear the display by writing 16 spaces to each line
        lcd.cursor_pos = (0, 0)
        lcd.write_string("                ")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("                ")

        # Step 2: Add a small delay to let the display controller "settle"
        time.sleep(0.05)

        # Step 3: Return to the start and write the fresh text, char by char
        lcd.cursor_pos = (0, 0)
        for char in str(line1):
            lcd.write_string(char)
            time.sleep(0.001) # Tiny delay between characters

        lcd.cursor_pos = (1, 0)
        for char in str(line2):
            lcd.write_string(char)
            time.sleep(0.001) # Tiny delay between characters
            
    except Exception as e:
        # If any part of the LCD communication fails, print the error
        print(f"An error occurred in display_lcd: {e}")
'''
# --- Your LCD Initialization code is here ---
# (e.g., lcd = CharLCD(...) )
# ...

def display_lcd(line1, line2):
    """
    A final, simplified function. Manually clears the screen by writing
    spaces, then writes each new line as a single string.
    """
    try:
        # Step 1: Manually clear the display. This is more reliable.
        lcd.cursor_pos = (0, 0)
        lcd.write_string("                ") # 16 spaces
        lcd.cursor_pos = (1, 0)
        lcd.write_string("                ") # 16 spaces

        # Step 2: Write the new text as whole strings.
        lcd.cursor_pos = (0, 0)
        lcd.write_string(str(line1))
        
        lcd.cursor_pos = (1, 0)
        lcd.write_string(str(line2))
            
    except Exception as e:
        print(f"An error occurred during the final display update: {e}")

# ... your other functions like cleanup() are here ...


def cleanup():
    """
    Clears the display and releases GPIO pins.
    """
    lcd.clear()
    lcd.close()
    GPIO.cleanup()

# --- Self-Test Code ---
# This block runs only when you execute this file directly (e.g., python3 lcd_controller.py)
# It's useful for testing the module itself.
if __name__ == '__main__':
    print("Testing LCD Controller...")
    try:
        display_lcd("LCD Controller", "Test successful!")
        time.sleep(3)
    finally:
        cleanup()
        print("Test finished and GPIO cleaned up.")
