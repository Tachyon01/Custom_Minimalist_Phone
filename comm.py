import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def to_txt():
    """
    Sends a WhatsApp message using the Twilio API.

    WARNING: This function contains hardcoded credentials (account_sid, auth_token).
    This is a security risk. It's highly recommended to use environment
    variables instead for production code.

    Returns:
        str: The Message SID (a unique ID) if the message is sent successfully.
        None: If there is an error.
    """
    # ?? Security Warning: Avoid hardcoding credentials. Use environment variables.
    account_sid = "ACXXXXXXXXXXXXXXXXXX"
    auth_token = "e0XXXXXXXXXXXXXXXXXXX"

    # --- Message Details ---
    message_body = "This is a test message from my custom phone!"
    from_whatsapp_number = "whatsapp:+1xxxxxxxx" # Twilio's Sandbox Number
    to_whatsapp_number = "whatsapp:+1xxxxxxxx"   # Your WhatsApp Number

    try:
        client = Client(account_sid, auth_token)
        print(f"?? Sending a message to {to_whatsapp_number}...")

        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )

        print(f"? Message sent successfully! SID: {message.sid}")
        return message.sid

    except TwilioRestException as e:
        print(f"?? Twilio Error: {e}")
        return None
    except Exception as e:
        print(f"?? An unexpected error occurred: {e}")
        return None


def to_call():
    """
    Initializes the Twilio client and places an automated phone call.
    
    This function reads credentials from environment variables and uses them
    to make a call to a specified number. The message spoken during the
    call is defined within the function.

    Returns:
        str: The Call SID if the call is initiated successfully.
        None: If there is an error or credentials are not set.
    """
    # --- Configuration ---
    # It's best practice to use environment variables for sensitive data.
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

    # Your Twilio phone number and the number you want to call.
    twilio_phone_number = "+1xxxxxxx"  # Replace with your Twilio number
    to_phone_number = "+1xxxxxxxx"      # Replace with the destination number

    # Message to be spoken when the call is answered.
    message_to_say = "Hello! This is a call from your custom-designed phone."

    # --- Main Logic ---
    if not all([account_sid, auth_token]):
        print("?? Error: TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables not set.")
        return None

    try:
        # Initialize the Twilio client
        client = Client(account_sid, auth_token)

        print(f"?? Placing a call to {to_phone_number}...")

        # Create the TwiML response to be read over the phone
        twiml_response = f'<Response><Say>{message_to_say}</Say><Hangup/></Response>'

        # Initiate the call
        call = client.calls.create(
            twiml=twiml_response,
            to=to_phone_number,
            from_=twilio_phone_number
        )

        print(f"? Call initiated successfully! SID: {call.sid}")
        return call.sid

    except TwilioRestException as e:
        print(f"?? Twilio Error: {e}")
        return None
    except Exception as e:
        print(f"?? An unexpected error occurred: {e}")
        return None

# --- Example of how to run the function ---
if __name__ == "__main__":
    print("Testing the to_call() function...")
    # To test, make sure you have set your environment variables:
    # export TWILIO_ACCOUNT_SID='Your_SID_Here'
    # export TWILIO_AUTH_TOKEN='Your_Token_Here'
    to_call()
