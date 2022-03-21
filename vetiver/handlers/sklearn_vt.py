from ..ptype import vetiver_create_ptype


class SKLearnHandler:
    def __init__(self, model):
        self.model = model

    def create_description(self):
        desc = f"Scikit-learn model of type {type(self.model)}"
        return desc

    def create_meta():
        ...

    def prepare_model():
        ...

    def ptype(self, ptype_data, save_ptype):
        ptype = vetiver_create_ptype(ptype_data, save_ptype)
        return ptype

    def handler_startup():
        # add in required package
        ...

    def handler_predict(self, input_data, predict_proba: bool = False):

        if predict_proba:
            prediction = self.model.predict_proba([input_data])

        prediction = self.model.predict([input_data])

        return prediction
