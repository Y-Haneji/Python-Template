"""https://qiita.com/si1242/items/d2f9195c08826d87d6ad"""
import random

import numpy as np
import torch
import tensorflow as tf


def fix_seed(seed):
    # random
    random.seed(seed)
    # Numpy
    np.random.seed(seed)
    # Pytorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    # Tensorflow
    tf.random.set_seed(seed)
