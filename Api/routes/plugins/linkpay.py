from Api import jsonify, app 

@app.register_route(name="test", info="Testing plugin route...", anti_spam=4)
def test_plugin():
    # rest of your codes
    return jsonify(message="example plugin route created...")


