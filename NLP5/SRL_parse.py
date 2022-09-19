from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

from allennlp.predictors.predictor import Predictor

text = 'Although my wise friends advised me, I still decided to not invest in cryptocurrency.'

predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz")
results = predictor.predict(
  sentence=text
)
results.keys()