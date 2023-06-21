import os
from flask import Flask, request
from flask_restful import Api, Resource
from inferenceModel import predict
from werkzeug.utils import secure_filename
from utils import allowed_file, convert

app = Flask(__name__)
api = Api(app)

DEBUG = True


class ImageRecognizer(Resource):
    def post(self):
        file = request.files.get("file")

        if not file or not allowed_file(file.filename):
            return {"error": "Invalid content"}, 400

        isExist = os.path.exists("./temp/")
        if not isExist:
            os.makedirs("./temp/")

        filename = secure_filename(file.filename)
        paths = [os.path.join("./temp/", filename)]

        file.save(paths[0])

        if file.filename.rsplit(".", 1)[1].lower() == "gif":
            paths.append(convert(filename))

        prediction = predict(paths[-1])

        [os.remove(one) for one in paths]
        file.close()
        return prediction


api.add_resource(ImageRecognizer, "/predict")

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port="4001")
