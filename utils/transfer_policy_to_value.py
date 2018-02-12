from chainer import serializers

from pydlshogi.network.policy import *
from pydlshogi.network.value import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('model_policy', type=str)
parser.add_argument('model_value', type=str)
args = parser.parse_args()

model_policy = PolicyNetwork()
model_value = ValueNetwork()

print('Load policy model from', args.model_policy)
serializers.load_npz(args.model_policy, model_policy)

print('value model params')
dict_value = {}
for path, param in model_value.namedparams():
    print(path, param.data.shape)
    dict_value[path] = param

print('policy model params')
for path, param in model_policy.namedparams():
    print(path, param.data.shape)
    if path in dict_value:
        dict_value[path].data = param.data

print('save the model')
serializers.save_npz(args.model_value, model_value)
