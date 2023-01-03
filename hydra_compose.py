from typing import List
import os
from hydra import compose, initialize
from omegaconf import OmegaConf


def get_cnf(config_path, overrides: List[str] = [], verbose=False):
    """
    設定値の辞書を取得
    @return
        cnf: OmegaDict
    """
    with initialize(config_path=os.path.dirname(config_path), version_base=None): # 1.2では、version_base=Noneという引数も必要になっていた
        cnf = compose(config_name=os.path.basename(config_path), overrides=overrides)
        if verbose:
            print(OmegaConf.to_yaml(cnf))
        return cnf
