import RPi.GPIO as GPIO
import requests
import time

BUTTON_PIN = 15 # The pin that works for you

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Button watcher started. Press Ctrl+C to exit.")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed! Sending request to server...")
            try:
                # Send a web request to our Flask app
                requests.get('http://127.0.0.1:5000/button_press', timeout=2)
            except requests.exceptions.RequestException as e:
                print(f"Could not connect to server: {e}")

            # Wait for button to be released
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.1)
        
        time.sleep(0.1)
finally:
    GPIO.cleanup()
