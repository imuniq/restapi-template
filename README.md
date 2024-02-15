# restapi-template
Rest API Template, made with Flask
# To create a route 
Must import required modules when creating a new route in a new file
```python
from Api import app
```
Register a route with options
- You can set antispam time for each route `anti_spam=5`
- You can blacklist a route from public by using `route_private=True`

Here is the example code:
```python
@app.register_route(name="test", info="Testing plugin route...", anti_spam=4)
def test_plugin():
    # rest of your codes
    return jsonify(message="example plugin route created...")
```
