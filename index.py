import os
from flask import Flask, request
from flask_restful import Api, Resource
from inferenceModel import predict
from werkzeug.utils import secure_filename
from utils import allowed_file, convert, get_extension
import requests

app = Flask(__name__)
api = Api(app)

DEBUG = True


class ImageRecognizer(Resource):
    def post(self):
        file = request.json.get("url")

        if not file or not allowed_file(file):
            return {"error": "Invalid content"}, 400

        owned_file = requests.get(file)
        new_name = f"./temp/temporary.{get_extension(file)}"

        with open(new_name, "wb") as f:
            f.write(owned_file.content)

            isExist = os.path.exists("./temp/")
            if not isExist:
                os.makedirs("./temp/")

            paths = [new_name]

            if new_name.rsplit(".", 1)[1].lower() == "gif":
                paths.append(convert(f))

            print(paths[-1])
            prediction = predict(paths[-1])

            [os.remove(one) for one in paths]

        return prediction


api.add_resource(ImageRecognizer, "/predict")

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port="4001")
