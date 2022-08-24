import numpy as np
from typing import List, Union

def get_quantiles_and_mean(array: Union[List[int], List[float], np.ndarray],
                           l_q: float = 0.25, h_q: float = 0.75):
    return np.quantile(array, l_q), np.mean(array), np.quantile(array, h_q)


def softmax(array: np.ndarray, T: Union[int, float] = 1, fix_unit_norm: Union[int, bool] = 1):
    """
    Computes softmax of an array.

    Parameters:
    ===========
        array: np.ndarray
        Array of logits.

        T: int or float: default = 1
        SoftMax temperature

        fix_unit_norm: int or bool, default = 1
            If int it defines index to add the difference between 1 and softmax(array).sum().
            If True, adds to the second proba.
            If False, no normalization fix.

    Returns:
    ========
        p: np.ndarray
        SoftMax probabilities
    """
    exp_array = np.exp(array / T)
    p = exp_array / np.sum(exp_array)
    if fix_unit_norm:
        p[int(fix_unit_norm)] += 1 - p.sum()
    return p