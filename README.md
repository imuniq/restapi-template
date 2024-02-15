# restapi-template
A simple and easy to use Rest API Template, made with Flask with AntiSpam with system.

Here is the usage of this template:
 - Easy to use & lightweight
 - Antispam system
 - Blacklist endpoint
 - Documentation (Soon)
 - Easy handle get and post parameters

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
    return app._jsonify(message="example plugin route created...")
```

You can use `app._set_params()` to set required parameters
Here is the example code:
```python
@app.register_route(name="params", info="Testing plugin route...", anti_spam=4, params=["hello"])
def test_plugin_with_params():

    params, err = app._set_params(params=["hello"])
    if err:
        return app._jsonify(error=err), 400
    
    # rest of your codes
    return app._jsonify(message="example plugin route  with params...", hello=params.hello)
```
When you navigate to your endpoint you can access the parameter from `set_params`\n
You can get the value from parameter:

```python
params, err = app._set_params(method="GET", params=["hello"])

# example endpoint: http://127.0.0.1/params?hello=world
print(params.hello) # Output: world
```
