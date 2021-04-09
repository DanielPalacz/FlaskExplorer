import flask
from flask_basicauth import BasicAuth
from requests.auth import _basic_auth_str

import uuid


app = flask.Flask(__name__)

app.secret_key = "secret123"
app.config['BASIC_AUTH_USERNAME'] = "daniel"
app.config['BASIC_AUTH_PASSWORD'] = "1234"
basic_auth = BasicAuth(app)


local_db = dict(
    sessions={},
    users={},
    documents={}
)


@app.route("/", methods=["GET"])
def root_view():
    root_endpoint_txt = "FlaskExploring - root endpoint"
    return flask.jsonify(root_endpoint_txt)


@app.route("/session", methods=["POST"])
def create_session():
    # here we are forcing cookie creation by Flask app
    flask.session["a_value"] = uuid.uuid4()
    return flask.jsonify("Session_created")


@app.route("/session", methods=["GET"])
def get_session():
    flask.session["session_id"] = str(uuid.uuid4())
    if not flask.session:
        return flask.abort(404)
    return flask.jsonify("get session")


if __name__ == "__main__":
    #
    # curl -u daniel:1234 -i -X POST http://127.0.0.1:5000/session -vv
    #
    app.run(debug=True, use_reloader=True)
    #
    # client = app.test_client()
    # print(app.config)
    # r_root = client.get("/")

    # username = "daniel"
    # password = "1234"
    # r_session = client.post("/session", headers={"Authorization": _basic_auth_str(username, password)})

    # r_generic = client.open("/session", method="POST", headers={"Authorization": _basic_auth_str(username, password)})
    # print(r_generic.status_code)

    # print(r_session.status_code)
    # print(r_session.headers)
