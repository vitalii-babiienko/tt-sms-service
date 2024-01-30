import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)


logging.basicConfig(filename="logs", level=logging.INFO)


@app.route("/home/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/send-sms/", methods=["POST"])
def send_sms():
    phone_number = request.form.get("phone")
    message = request.form.get("message")

    try:
        twilio_client.messages.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message,
        )

        logging.info(
            f"The SMS has been sent successfully to "
            f"{phone_number} at {datetime.now()}"
        )

        return "The SMS has been sent successfully!"

    except Exception as e:
        logging.error(f"Failed to send SMS to {phone_number}: {str(e)}")

        return "Failed to send SMS!"


@app.route("/api/v1/send-sms/", methods=["POST"])
def send_sms_api():
    data = request.get_json()
    phone_number = data.get("phone")
    message = data.get("message")

    try:
        twilio_client.messages.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message,
        )

        logging.info(
            f"API: The SMS has been sent successfully to "
            f"{phone_number} at {datetime.now()}"
        )

        return jsonify({
            "status": "success",
            "message": "The SMS has been sent successfully!",
        })

    except Exception as e:
        logging.error(f"API: Failed to send SMS to {phone_number}: {str(e)}")

        return jsonify({
            "status": "error",
            "message": "Failed to send SMS!",
        })


if __name__ == '__main__':
    app.run(debug=True)
