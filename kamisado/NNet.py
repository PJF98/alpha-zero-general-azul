import sys
sys.path.append('../../')
from GenericNNetWrapper import GenericNNetWrapper
from .KamisadoNNet import KamisadoNNet as nn_model

class NNetWrapper(GenericNNetWrapper):
	def init_nnet(self, game, nn_args):
		self.nnet = nn_model(game, nn_args)
