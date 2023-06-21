import cv2
import typing
import numpy as np

from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder, get_cer


class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shape[:2][::-1])

        image_pred = np.expand_dims(image, axis=0).astype(np.float32)

        preds = self.model.run(None, {self.input_name: image_pred})[0]

        text = ctc_decoder(preds, self.char_list)[0]

        return text


def predict(image_path: str):
    from mltu.configs import BaseModelConfigs

    prediction_text = ""
    image = cv2.imread(image_path)
    configs = BaseModelConfigs.load("Models/configs.yaml")
    model = ImageToWordModel(model_path=configs.model_path, char_list=configs.vocab)

    try:
        prediction_text = model.predict(image)
        print(f"Image: {image_path}, Prediction: {prediction_text}")

        # resize image by 3 times for visualization
        # image = cv2.resize(image, (image.shape[1] * 3, image.shape[0] * 3))
        # cv2.imshow(prediction_text, image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    except Exception as err:
        raise err

    return prediction_text
