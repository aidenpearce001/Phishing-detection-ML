from utils.feature_extraction import Extractor
import numpy as np
import joblib


class RandomForest():
    def __init__(self, ckpt_path="./model/ckpt/rf_final.pkl"):
        self.ckpt_path = ckpt_path
        self.extractor = Extractor()
        self.classifier = joblib.load(ckpt_path)

    def predict(self, url):
        url_feature_vector = self.extractor(url)
        
        if url_feature_vector is not None:
            vector = np.array(url_feature_vector[:-3])
            #vector = np.concatenate((vector, np.array([1]))) # This line is for testing only. Erase it
            prediction = self.classifier.predict(vector.reshape(1, -1))
            
            return prediction
        else:
            return None


# classifier = joblib.load("./model/ckpt/rf_final.pkl")
# ext = Extractor()
# url = "https://stackoverflow.com/questions/27344641/python-importing-from-parents-child-folder"
# # import IPython
# # IPython.embed()
# print(ext(url)[:-3])
# Vector = np.concatenate((np.array(ext(url)[:-3]), np.array([1])))
# print(Vector)
# prediction = classifier.predict(Vector.reshape(1, -1))

# print(prediction)
