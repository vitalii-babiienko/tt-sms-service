import os
import unittest
from app import app

REAL_PHONE_NUMBER = os.getenv("REAL_PHONE_NUMBER")


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get("/home/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<form", response.data)
        self.assertIn(b"Phone Number:", response.data)
        self.assertIn(b"Message:", response.data)

    def test_send_sms_route(self):
        response = self.app.post(
            "/send-sms/",
            data={"phone": REAL_PHONE_NUMBER, "message": "Test message"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The SMS has been sent successfully!", response.data)

    def test_send_sms_invalid_phone(self):
        response = self.app.post(
            "/send-sms/", data={"phone": "invalid", "message": "Test message"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Failed to send SMS!", response.data)

    def test_send_sms_api_route(self):
        json_data = {"phone": REAL_PHONE_NUMBER, "message": "Test message"}
        response = self.app.post(
            "/api/v1/send-sms/",
            json=json_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertIn(b"The SMS has been sent successfully!", response.data)

    def test_send_sms_api_invalid_phone(self):
        json_data = {"phone": "invalid", "message": "Test message"}
        response = self.app.post(
            "/api/v1/send-sms/",
            json=json_data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "error")
        self.assertIn(b"Failed to send SMS!", response.data)


if __name__ == "__main__":
    unittest.main()
