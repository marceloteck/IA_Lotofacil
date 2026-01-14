from src.engine.nn_cerebro import CerebroNeural
from src.engine.motor_multicerebro import gerar_jogo
from src.utils.extrator_features import extrair_features

nn = CerebroNeural()

jogo = gerar_jogo()
features = extrair_features(jogo)

score = nn.avaliar_jogo(features)
print("Score NN:", score)
