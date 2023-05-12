import hashlib
import json

import numpy as np
import pandas as pd


# Collapse the dictionary to a single representation
def immutify_dictionary(d):
    d_new = {}
    for k, v in d.items():
        # convert to python native immutables
        if isinstance(v, (np.ndarray, pd.Series)):
            d_new[k] = tuple(v.tolist())

        # immutify any lists
        elif isinstance(v, list):
            d_new[k] = tuple(v)

        # recursion if nested
        elif isinstance(v, dict):
            d_new[k] = immutify_dictionary(v)

        # ensure numpy "primitives" are casted to json-friendly python natives
        else:
            # convert numpy types to native
            if hasattr(v, "dtype"):
                d_new[k] = v.item()
            else:
                d_new[k] = v

    return dict(sorted(d_new.items(), key=lambda item: item[0]))


# Make a json string from the sorted dictionary
# then hash that string
def hash_dictionary(d):
    d_hashable = immutify_dictionary(d)
    s_hashable = json.dumps(d_hashable).encode("utf-8")
    m = hashlib.sha256(s_hashable).hexdigest()
    return m
