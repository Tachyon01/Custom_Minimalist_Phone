import time
import random
from twilio.rest import Client
import threading
from keypad import get_key

account_sid = "ACXXX"
auth_token = "e0XXX"


# Placeholder for a function to display text on the 16x2 LCD.
# You will need to replace this with your actual display driver code.
def display_rpi(line1, line2=""):
    """Displays two lines of text on the 16x2 LCD."""
    print("----- Display -----")
    print(line1)
    print(line2)
    print("-------------------")

# Pre-fed contact entries
CONTACTS = {
    
    "B": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
    "C": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
    "D": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
    "E": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
}

PRESET_MESSAGES = [
    "See you there",
    "Busy",
    "On my way",
    "Pls call",
    "Custom"
]

'''Fix to button input handling for menus'''
def get_menu_input():
    """Generic input for menus. Now uses the keypad."""
    return get_key()

# def get_call_input():
#     """Waits for and returns user input for the call menu. Now uses the keypad."""
#     return get_key()

def select_contact():
    """Allows user to scroll through and select a contact. Returns contact name or None."""
    contact_names = list(CONTACTS.keys())
    current_index = 0
    
    while True:
        contact_name = contact_names[current_index]
        display_rpi(f"To: {contact_name}", "s:select, n:next, b:back")
        
        choice = get_menu_input()
        
        if choice == 's': # Select
            return contact_name
        elif choice == 'n': # Next
            current_index = (current_index + 1) % len(contact_names)
        elif choice == 'b': # Back
            return None
        else:
            display_rpi("Invalid Option", "")
            time.sleep(2)

def get_custom_message():
    """Dummy function to get a custom message from the user."""
    display_rpi("Enter custom msg:", "")
    message = input("Type your message: ")
    return message

def function_call():
    """Allows the user to scroll through contacts and make a call."""
    contact_names = list(CONTACTS.keys())
    current_index = 0
    
    while True:
        contact_name = contact_names[current_index]
        display_rpi(f"Name: {contact_name}", "Call, next")
        
        # choice = get_call_input()
        choice = get_key()
        
        if choice == 'c': # Call
            phone_number = CONTACTS[contact_name]
            display_rpi(f"Calling {contact_name}", phone_number)
            print(f"Calling {contact_name} at {phone_number}...")
            time.sleep(3) # Simulate call duration
            display_rpi("Call Ended", "")
            time.sleep(2)
            # After the call, we go back to the main menu
            break
        elif choice == 'n': # Next
            current_index = (current_index + 1) % len(contact_names)
        elif choice == 'b': # Back to main menu
            break
        else:
            display_rpi("Invalid Option", "c:call, n:next")
            time.sleep(2)

def function_message():
    """Allows user to select a contact, a message, and send it."""
    # Step 1: Select a contact
    contact_name = select_contact()
    if not contact_name:
        return # User backed out

    # Step 2: Select a message
    message_index = 0
    final_message = ""
    while True:
        current_message = PRESET_MESSAGES[message_index]
        display_rpi("Select message:", f'"{current_message}"')
        
        choice = get_menu_input()

        if choice == 's': # Select
            if current_message == "Custom":
                final_message = get_custom_message()
            else:
                final_message = current_message
            break # Move to sending confirmation
        elif choice == 'n': # Next
            message_index = (message_index + 1) % len(PRESET_MESSAGES)
        elif choice == 'b': # Back
            return # Go back to main menu

    # Step 3: Confirm and send
    while True:
        display_rpi(f"Send to {contact_name}?", "s:send, b:cancel")
        choice = get_menu_input("s:send, b:cancel")
        if choice == 's':
            try:
                client = Client(account_sid, auth_token)
                # Note: Twilio requires 'whatsapp:' prefix for WhatsApp numbers
                # and E.164 format for phone numbers.
                recipient_number = CONTACTS[contact_name]
                # Assuming the number is for WhatsApp for this example
                # You might need to format this properly based on your contact data
                formatted_recipient = f"whatsapp:{recipient_number}"
                
                message = client.messages.create(
                    body=final_message,
                    from_="whatsapp:+1416",  # Your Twilio WhatsApp number
                    to=formatted_recipient
                )
                display_rpi("Message Sent!", f"SID: {message.sid[:10]}...")
                print(f"Message sent with SID: {message.sid}")
            except Exception as e:
                display_rpi("Send Failed", "Check logs")
                print(f"Error sending message: {e}")
            
            time.sleep(3)
            break
        elif choice == 'b':
            display_rpi("Cancelled", "")
            time.sleep(2)
            break
        else:
            display_rpi("Invalid Option", "")
            time.sleep(2)


# ... (existing code for Twilio, display_rpi, contacts, messages, etc.)
# NOTE: The top part of the file remains unchanged.
# To keep the response clean, I am omitting the existing code that is not directly
# related to the new IoT functionality. The edit will be applied to the real file.

# --- Start of New/Modified IoT Section ---

# Dummy functions to simulate reading from different hardware sensors
def read_temperature():
    """Simulates reading a temperature sensor."""
    return random.randint(15, 30) # Celsius

def read_moisture():
    """Simulates reading a soil moisture sensor."""
    return random.randint(20, 80) # Percentage

# Mapping of available sensor types to their read functions
SENSOR_TYPES = {
    "Temp": read_temperature,
    "Moisture": read_moisture,
}

# Global state for 3 sensors. Each sensor is a dictionary.
SENSORS = [
    {"type": "Temp", "value": -1, "read_function": read_temperature},
    {"type": None, "value": -1, "read_function": None},
    {"type": None, "value": -1, "read_function": None},
]

def poll_sensors(stop_event):
    """
    Function to be run in a background thread.
    Continuously updates values for active sensors.
    """
    while not stop_event.is_set():
        for sensor in SENSORS:
            if sensor["read_function"]:
                sensor["value"] = sensor["read_function"]()
        time.sleep(2) # Poll every 2 seconds

def view_sensor_values():
    """Displays the current values of the sensors from the global state."""
    names = []
    vals = []
    for i, sensor in enumerate(SENSORS):
        sensor_type = sensor["type"]
        if sensor_type:
            # Use the first 4 chars of the type, e.g., "Temp" or "Mois"
            names.append(sensor_type[:4])
            vals.append(str(sensor["value"]))
        else:
            names.append("NA")
            vals.append("-1")
    
    line1 = "{:<5}{:<5}{:<5}".format(*names)
    line2 = "{:<5}{:<5}{:<5}".format(*vals)
    
    display_rpi(line1, line2)
    input("Press Enter to return...")

def change_sensor_menu():
    """Menu to select a sensor slot and assign a new sensor type to it."""
    # Step 1: Select which sensor slot to change
    slot_index = -1
    while True:
        display_rpi("Change which sensor?", "1, 2, 3, or b:back")
        choice = get_menu_input("1, 2, 3, or b")
        if choice in ['1', '2', '3']:
            slot_index = int(choice) - 1
            break
        elif choice == 'b':
            return
        else:
            display_rpi("Invalid slot", "")
            time.sleep(2)

    # Step 2: Select the type of sensor to assign
    sensor_type_names = list(SENSOR_TYPES.keys()) + ["Disable"]
    type_index = 0
    while True:
        selected_type = sensor_type_names[type_index]
        display_rpi(f"Slot {slot_index+1}: {selected_type}", "s:select, n:next, b:back")
        
        choice = get_menu_input()
        if choice == 's':
            if selected_type == "Disable":
                SENSORS[slot_index]["type"] = None
                SENSORS[slot_index]["read_function"] = None
                SENSORS[slot_index]["value"] = -1
                display_rpi(f"Slot {slot_index+1} Disabled", "")
            else:
                SENSORS[slot_index]["type"] = selected_type
                SENSORS[slot_index]["read_function"] = SENSOR_TYPES[selected_type]
                display_rpi(f"Slot {slot_index+1} set to", selected_type)
            
            time.sleep(2)
            break
        elif choice == 'n':
            type_index = (type_index + 1) % len(sensor_type_names)
        elif choice == 'b':
            break
        else:
            display_rpi("Invalid Option", "")
            time.sleep(2)

def function_IoT():
    """
    Manages the IoT sensor menu and the background polling thread.
    """
    stop_event = threading.Event()
    polling_thread = threading.Thread(target=poll_sensors, args=(stop_event,))
    polling_thread.start()
    
    iot_options = {
        '1': view_sensor_values,
        '2': change_sensor_menu
    }
    
    try:
        while True:
            display_rpi("1:View Val", "2:Change Sensor")
            choice = get_menu_input("1, 2, or b for back")

            if choice in iot_options:
                iot_options[choice]()
            elif choice == 'b':
                break
            else:
                display_rpi("Invalid Option", "")
                time.sleep(2)
    finally:
        # Ensure the thread is stopped when we exit the menu
        print("Stopping sensor polling thread...")
        stop_event.set()
        polling_thread.join()
        print("Thread stopped.")
