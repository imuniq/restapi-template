from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from time import time
import os
import json


class Database:
    def __init__(self, db_files: list = []) -> None:
        self.db_files = db_files
        self.query = Query()

    def create_file_if_not_exists(self):
        for db_file in self.db_files:
            file_path = os.path.join(os.path.dirname(__file__), "db", db_file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    json.dump({}, file)

    def set_config(self):
        self.create_file_if_not_exists()
        required_files = []
        for db_file in self.db_files:
            file_path = os.path.join(os.path.dirname(__file__), "db", db_file)
            required_files.append(file_path)

        return [TinyDB(file) for file in required_files]


REQUIRED_DB_FILES = [
    "api.json",
    "logs.json"
]

database = Database(REQUIRED_DB_FILES)
apidb, logsdb = database.set_config()


class APIHandler(Flask):
    def __init__(self, *args, **kwargs):
        super(APIHandler, self).__init__(*args, **kwargs)
        self.query = Query()
        self.db_endpoints = apidb.table("routes")
        self.db_visitors = logsdb.table("visitors")
        self.get_all_routes = self.db_endpoints.all()

    def clear_all_routes(self):
     for i in self.db_endpoints.all():
      return self.db_endpoints.remove(database.query.name == i['name'])
     return True
    
    def register_route(self, name, info, methods=["GET"], anti_spam=0, params=[], route_private: bool = False):
        def decorator(func):
            route_data = {"name": name,
                          "info": info,
                          "anti_spam": anti_spam,
                          "is_private": route_private,
                          "methods": methods,
                          "params": params
                          }
            if not self.db_endpoints.get(self.query.name == name):
                self.db_endpoints.insert(route_data)
            else:
                self.db_endpoints.upsert(route_data, self.query.name == name)

            endpoint_name = f"{name}_endpoint"  # Generate a unique endpoint name based on the route name

            @self.route("/" + name, methods=methods, endpoint=endpoint_name)
            def route_handler(*args, **kwargs):  # Use the generated unique endpoint name
                client_ip = request.remote_addr
                if anti_spam > 0:
                    anti_spam_data = self.db_visitors.get(
                        self.query.ip == client_ip)
                    current_timestamp = time()

                    if anti_spam_data:
                        time_passed = current_timestamp - \
                            anti_spam_data["last_used_timestamp"]
                        
                        time_left = int(anti_spam - time_passed)

                        if time_passed < anti_spam and time_left != 0:
                            return {"error": f"API rate-limited. Please wait {time_left}s to make another request."}

                    self.db_visitors.upsert(
                        {"ip": client_ip, "last_used_timestamp": current_timestamp}, self.query.ip == client_ip)

                return func(*args, **kwargs)

            return route_handler  # Return the generated route_handler function
        return decorator





app = APIHandler(__name__)
