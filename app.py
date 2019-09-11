from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

path = os.getcwd() + "/cloud-drive"

@app.route("/")
def hello_world():
    for layer in os.walk(path):
        print(layer)

    print("/nbreak/n")
    print(os.listdir(path))
    print(path_to_dict(path))
    return jsonify(path_to_dict(path))

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir\
                        (path)]
    else:
        d['type'] = "file"
    return d


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
