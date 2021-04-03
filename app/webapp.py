import flask


app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def root_view():
    root_endpoint_txt = "FlaskExploring - root endpoint"
    return flask.jsonify(root_endpoint_txt)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    client = app.test_client()
    response = client.get("/")
    #print("-------------------------------")
    #print(dict(response.headers))
