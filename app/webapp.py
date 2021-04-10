import flask
from flask_basicauth import BasicAuth

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
@basic_auth.required
def create_session():
    # here we are forcing cookie creation by Flask app
    flask.session["a_value"] = uuid.uuid4()
    # print("The body of the given http POST requests:")
    # print(flask.request.get_data())
    return flask.jsonify("Session_created")


@app.route("/session", methods=["GET"])
@basic_auth.required
def get_session():
    flask.session["session_id"] = str(uuid.uuid4())
    if not flask.session:
        return flask.abort(404)
    return flask.jsonify("Get session endpoint")


if __name__ == "__main__":
    run_app_mode = True

    if run_app_mode:
        app.run(debug=True, use_reloader=True, port=7777)
        # print(app.config)
    else:
        import base64

        def enc_auth(u, p):
            return "Basic %s" % base64.b64encode(":".join([u, p]).encode()).decode()

        username = "daniel"
        password = "1234"
        # telnet 127.0.0.1 7777
        # curl -u daniel:1234 -i -X POST http://127.0.0.1:7777/session -vv
        # curl -i -X GET -H "Cookie: session=........" http://127.0.0.1:7777/session -vv
        # curl -u daniel:1234 -i -X POST --data title=Hello http://127.0.0.1:7777/session -vv

        client = app.test_client()
        encoded = enc_auth(username, password)
        r_session = client.post("/session", headers={"Authorization": encoded})
        r_generic = client.open("/session", method="POST", headers={"Authorization": encoded})

