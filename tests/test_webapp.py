from app.webapp import app

import unittest
import base64


def encode_base_auth(u, p):
    joined = "".join([u, ":", p])
    return "Basic " + base64.b64encode(joined.encode()).decode()


class TestWebApp(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        # what is going on here? why I dont need to run app (app.run) and still... be able to send http reqs
        # Thread-Locals in Flask???

    def test_db_users(self):
        from app.webapp import local_db
        self.assertIsInstance(local_db.get("users"), dict, "db_users is not dict object type")
        self.assertFalse(local_db.get("users"), "db_users is not empty")

    def test_root_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), '"FlaskExploring - root endpoint"'"\n")
        response_headers = dict(response.headers)
        self.assertEqual(response_headers.get("Content-Type"), "application/json")
        self.assertEqual(response_headers.get("Content-Length"), "33")

    def test_session_authorized_user(self):
        username = "daniel"
        password = "1234"
        encoded = encode_base_auth(username, password)
        r_session = self.client.post("/session", headers={"Authorization": encoded})
        self.assertEqual(r_session.status_code, 200)
        self.assertEqual(r_session.data.decode(), '"Session_created"'"\n")
        r_session_headers = dict(r_session.headers)
        self.assertEqual(r_session_headers.get("Content-Type"), "application/json")
        self.assertEqual(r_session_headers.get("Vary"), "Cookie")
        self.assertEqual(r_session_headers.get("Content-Length"), "18")
        self.assertTrue("Set-Cookie" in r_session_headers, "Cookie was not sent by app")


class TestWebAppClientErrors400(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        # what is going on here? why I dont need to run app (app.run) and still... be able to send http reqs
        # Thread-Locals in Flask???

    def test_session_notauthorized_user(self):
        username = "0_daniel"
        password = "0_1234"
        encoded = encode_base_auth(username, password)
        r_session = self.client.post("/session", headers={"Authorization": encoded})
        self.assertEqual(r_session.status_code, 401)

    def test_incorrect_endpoint(self):
        response = self.client.get("/unknown/notdefined/endpoint")
        # Resource not found
        self.assertEqual(response.status_code, 404)

    def test_root_post(self):
        response = self.client.post("/")
        # Method Not Allowed
        self.assertEqual(response.status_code, 405)
