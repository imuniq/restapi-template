from Api import app, jsonify

@app.register_route(name="routes", info="To get all available methods", anti_spam=2)
def get_routes():
    return jsonify(message="running...", routes=app.db_endpoints.all())