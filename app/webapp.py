import flask
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask_basicauth import BasicAuth
from markupsafe import escape


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
def index():
    if "username" in session:
        message = "Main page - logged in as: %s." % escape(session['username'])
        return "<p>" + message + "</p>" + """
        <a href="/logout">logout</a>
        <br>
        <br>
        <p>Magic application content:</p>
        <nav>
            <a href="/json">json</a>
            <a href="/str">str</a>
        </nav>
        """
    return """
    <p1>Hello on the main Page.</p1>
     <br><br>
     <a href="/login">login</a>
    """


@app.route("/json", methods=["GET"])
def root_view():
    root_endpoint_txt = "Root endpoint: (Content-Type: application/json)"
    return flask.jsonify(root_endpoint_txt)


@app.route("/str", methods=["GET"])
@basic_auth.required
def root_view_str():
    root_endpoint_txt = "Root endpoint - STR view: (Content-Type: text/html; charset=utf-8)"
    return root_endpoint_txt


@app.route("/none", methods=["GET"])
def root_view_none():
    # this will end with error
    return None


@app.route("/parametrized/<param>/")
def root_view_parametrized(param):
    root_endpoint_txt = "Parametrized endpoint: parametrized/%s" % param
    return flask.jsonify(root_endpoint_txt)


@app.route("/login", methods=["POST"])
def create_session():
    # here we are forcing cookie creation by Flask app
    # flask.session["a_value"] = uuid.uuid4()
    # print("The body of the given http POST requests:")
    name = request.form["username"]
    passw = request.form["password"]
    if name == app.config['BASIC_AUTH_USERNAME'] and passw == app.config['BASIC_AUTH_PASSWORD']:
        session['username'] = request.form['username']
        session.update(dict(request.headers))
        return redirect(url_for("index"))

    return """
     <p1>Something went wrong. Try to log in one more time.</p1>
     <br><br>
     <a href="/login">login</a>
    """


@app.route("/login", methods=["GET"])
def get_session():
    # flask.session["session_id"] = str(uuid.uuid4())
    if not flask.session:
        return """
        <h1>Login Page</h1>
        <form action="/login" method="post">
            <p>Name/Password:</p>
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    """
    name = session['username']
    message = "'" + "%s' you are already logged in." % escape(name)
    return "<p>" + message + "</p>" + """
    <a href="/logout">logout</a>
    <br>
    <a href="/">Main page.</a>
    """


@app.route("/logout/", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('index'))
    

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
        with app.test_request_context():
            print(flask.url_for('root_view_parametrized', param="Parametrized", x=1, y=2, z=3, next="/"))
        print("-" * 99)
        test_app_objs = [elem for elem in dir(app) if elem.startswith("test_")]
        print(test_app_objs)
