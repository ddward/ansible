from flask import Flask, jsonify, request, abort
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

path = os.getcwd() + "/cloud-drive"

@app.route("/")
def hello_world():
    passed_key = request.headers.get('api_key')
    if(passed_key == 'test_key'):
        return file_tree(path)
    else:
        return abort(404)

def file_tree(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [file_tree(os.path.join(path,x)) for x in os.listdir\
                        (path)]
    else:
        d['type'] = "file"
    return d


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
