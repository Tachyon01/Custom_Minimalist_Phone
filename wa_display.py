from flask import Flask, request
import RPi.GPIO as GPIO
import lcd_controller
import time

# --- Globals for State Management ---
pending_message = None

# --- GPIO Pin Definitions (BOARD numbering) ---
LED_PIN = 24

app = Flask(__name__)

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

@app.route('/whatsapp', methods=['POST'])
def receive_whatsapp():
    """Receives a message, saves it, and turns on the LED."""
    global pending_message
    
    message_body = request.values.get('Body', 'No Message')
    
    line1 = message_body[:16]
    line2 = message_body[16:32]
    pending_message = (line1, line2)
    
    print(f"SERVER LOG: Message Stored -> {pending_message}")
    
    GPIO.output(LED_PIN, GPIO.HIGH)
    return ('', 204)

@app.route('/button_press', methods=['GET'])
def button_press_handler():
    """This route is triggered by the button watcher. It updates the display."""
    global pending_message
    
    print("SERVER LOG: Button press route triggered.")
    print(f"SERVER LOG: Checking for message. Content is currently: {pending_message}")
    
    if pending_message:
        print("SERVER LOG: Message found! Updating display.")
        lcd_controller.display_lcd("Success", "")
        time.sleep(1)
        lcd_controller.display_lcd(pending_message[0], pending_message[1])
        GPIO.output(LED_PIN, GPIO.LOW)
        pending_message = None # Clear the message after displaying
    else:
        # --- MODIFIED SECTION ---
        # If no message is pending, update the display to show "Null".
        print("SERVER LOG: No pending message found. Displaying 'Null'.")
        lcd_controller.display_lcd("Null", "")
        
    return ('OK', 200)

if __name__ == '__main__':
    try:
        setup_gpio()
        lcd_controller.display_lcd("System Online", "Server is running")
        app.run(host='0.0.0.0', port=5000)
    finally:
        lcd_controller.cleanup()
