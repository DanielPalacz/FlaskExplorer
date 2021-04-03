from app.webapp import app

import unittest


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

    def test_root_get(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.data.decode() == '"FlaskExploring - root endpoint"'"\n"
        response_headers = dict(response.headers)
        assert response_headers["Content-Type"] == "application/json"
        assert response_headers["Content-Length"] == "33"
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
        assert response.status_code == 405

    def test_incorrect_endpoint(self):
        response = self.client.get("/unknownendpoint")
        assert response.status_code == 404
