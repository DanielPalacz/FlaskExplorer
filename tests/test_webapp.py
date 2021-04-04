from app.webapp import app

import unittest
from requests.auth import _basic_auth_str


class TestWebApp(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        # what is going on here? why I dont need to run app (app.run) and still... be able to send http reqs
        #
        # step by step:
        # 1. response.status_code ---> from app.webapp import app
        # --- then from global namespace in webapp we are really running "app = flask.Flask(__name__)"
        #
        # ... but when we triggered http server?? we dont run app.run
        # we did not...
        # but app.test_client()

    def test_db_users(self):
        from app.webapp import db_users
        self.assertIsInstance(db_users, dict, "db_users is not dict object type")
        self.assertFalse(db_users, "db_users is not empty")

    def test_root_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), '"FlaskExploring - root endpoint"'"\n")
        response_headers = dict(response.headers)
        self.assertEqual(response_headers["Content-Type"], "application/json")
        self.assertEqual(response_headers["Content-Length"], "33")
        #
        #
        # looks like something hidden in the Flask Client?
        #
        # Only the following two headers are visible in response.headers object
        # Content-Type:     application / json
        # Content-Length:   33
        #
        #
        # when Firefox shows bit more Response headers:
        #   Content-Type:    application / json
        #   Content-Length:  33
        #   Date:            Sat, 03 Apr 2021 19:33:35 GMT
        #   Server:          Werkzeug/1.0.1 Python/3.8.5
        #
        #
        # curl?
        # ------------------> the same as Firefox

    def test_root_post(self):
        response = self.client.post("/")
        #
        # Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_incorrect_endpoint(self):
        response = self.client.get("/unknown/notdefined/endpoint")
        self.assertEqual(response.status_code, 404)

    def test_session_authorized_user(self):
        username = "daniel"
        password = "1234"
        r_session = self.client.post("/session", headers={"Authorization": _basic_auth_str(username, password)})
        self.assertEqual(r_session.status_code, 200)
        self.assertEqual(r_session.data.decode(), '"Session_created"'"\n")
        r_session_headers = dict(r_session.headers)
        self.assertEqual(r_session_headers["Content-Type"], "application/json")
        self.assertEqual(r_session_headers["Vary"], "Cookie")
        self.assertEqual(r_session_headers["Content-Length"], "18")
        self.assertTrue("Set-Cookie" in r_session_headers, "Cookie was not sent by app")

    def test_session_notauthorized_user(self):
        username = "0_daniel"
        password = "0_1234"
        r_session = self.client.post("/session", headers={"Authorization": _basic_auth_str(username, password)})
        self.assertEqual(r_session.status_code, 401)
