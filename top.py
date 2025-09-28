import RPi.GPIO as GPIO
import time

# Import functions from your other python files
from comm import to_call, to_txt
from lcd_controller import display_lcd # Assuming this is your function

# --- GPIO Pin Definitions ---
CALL_BUTTON_PIN = 12
TEXT_BUTTON_PIN = 15
# New pins based on your request
BUZZ_BUTTON_PIN = 13                 # The new button input
OUTPUT_PIN = 24                     # Physical pin 18 corresponds to GPIO 24

# --- Main Program Setup ---
try:
    # Set up GPIO using BOARD numbering (physical pin locations)
    GPIO.setmode(GPIO.BOARD)

    # Set up existing button pins as inputs with internal pull-up resistors.
    GPIO.setup(CALL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TEXT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # --- New Pin Setup ---
    # Set up the new button pin as an input
    GPIO.setup(BUZZ_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Set up the new output pin, defaulting to LOW
    GPIO.setup(OUTPUT_PIN, GPIO.OUT, initial=GPIO.LOW)
    # ---------------------

    print("Script started. Waiting for button press...")
    display_lcd("Call Light Text", "L   M    R") # Initial display

    # --- Main Polling Loop ---
    # This loop constantly checks the state of the buttons.
    while True:
        # Check if the CALL button is pressed (input is LOW)
        if GPIO.input(CALL_BUTTON_PIN) == GPIO.LOW:
            print(f"Button press detected on physical pin {CALL_BUTTON_PIN}.")
            display_lcd("Calling","")
            to_call()

            # Return to the default screen
            display_lcd("Call  Text", "Y       W")
            # Wait a moment to prevent multiple rapid triggers (debouncing)
            time.sleep(0.5)

        # Check if the TEXT button is pressed (input is LOW)
        if GPIO.input(TEXT_BUTTON_PIN) == GPIO.LOW:
            print(f"Button press detected on physical pin {TEXT_BUTTON_PIN}.")
            display_lcd("Messaging","")
            to_txt()

            # Return to the default screen
            display_lcd("Call  Text", "Y       W")
            # Wait a moment for debouncing
            time.sleep(0.5)

        # --- New Button Logic ---
        # This section makes the output pin HIGH only while the button is held down.
        if GPIO.input(BUZZ_BUTTON_PIN) == GPIO.LOW:
            # When button 13 is pressed, pull output pin 18 (GPIO 24) HIGH
            GPIO.output(OUTPUT_PIN, GPIO.HIGH)
            print(f"Pin {BUZZ_BUTTON_PIN} pressed, setting pin {OUTPUT_PIN} (GPIO 24) HIGH.")
        else:
            # When the button is not pressed, keep the output LOW
            GPIO.output(OUTPUT_PIN, GPIO.LOW)
        # ------------------------

        # Small delay to prevent the loop from using 100% CPU
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    # Clean up GPIO settings on exit
    GPIO.cleanup()
    print("GPIO cleanup complete. Exiting.")
