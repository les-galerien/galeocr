import os
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow.exceptions import ValidationError
from inferenceModel import predict
from werkzeug.utils import secure_filename
from utils import allowed_file

app = Flask(__name__)
api = Api(app)

DEBUG = True
UPLOAD_FOLDER = "./temp/"


class ImageRecognizer(Resource):
    def post(self):
        file = request.files.get("file")

        if not file or not allowed_file(file.filename):
            return {"error": "Invalid content"}, 400

        isExist = os.path.exists(UPLOAD_FOLDER)
        if not isExist:
            os.makedirs(UPLOAD_FOLDER)

        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(path)

        prediction = predict(path)

        file.close()
        os.remove(path)

        return prediction


api.add_resource(ImageRecognizer, "/predict")

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port="4001")
