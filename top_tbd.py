import time
from functions import function_call, function_message, function_IoT, display_rpi
from keypad import get_key


def main_menu():
    """The main navigation menu loop."""
    # Map keypad inputs '1', '2', '3' to their respective functions
    options = {
        '1': function_call,
        '2': function_message,
        '3': function_IoT,
    }
    
    # Define the display lines. Using spacing to align them.
    line1 = "Call Text Sens"
    line2 = "1    2    3"

    while True:
        # Display the static menu
        display_rpi(line1, line2)
        
        # Wait for user input from the keypad
        choice = get_key()
        
        if choice in options:
            # Call the selected function based on the key press
            options[choice]()
        elif choice == 'q': # Assuming 'q' is a dedicated quit button
            display_rpi("Exiting...", "")
            print("Exiting program.")
            break
        else:
            display_rpi("Invalid Key", "Press 1, 2, or 3")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        # Clean up GPIO if you are using it
        # This is where you would call GPIO.cleanup()
        print("Cleanup complete.")
