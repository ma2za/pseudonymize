import sys
import json
from pathlib import Path
from tokenizers import Tokenizer
import pseudonymize
from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.engine import Pseudonymizer
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.policy import Policy, NetworkPolicy
import traceback
import numpy as np
import re

onnx_path = Path('.cache/pseudonymize-tests/models/multilang-pii-ner-ml/model_int8.onnx')
tokenizer_path = Path('.cache/pseudonymize-tests/models/multilang-pii-ner-ml/tokenizer.json')
config_path = Path('.cache/pseudonymize-tests/models/multilang-pii-ner-ml/config.json')

backend = LocalONNXPIIBackend(model_path=onnx_path, tokenizer_path=tokenizer_path, config_path=config_path, entity_threshold=0.01)
text = "An obscure text with JohnXYZ and random unconfident bits."

backend._load_model()
policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)

def mock_detect_window(text, char_offset, policy, global_context):
    encoding = backend._tokenizer.encode(text, pair=global_context)
    ids = encoding.ids
    attention_mask = encoding.attention_mask
    type_ids = encoding.type_ids

    inputs = {
        "input_ids": [ids],
        "attention_mask": [attention_mask],
        "token_type_ids": [type_ids],
    }
    
    expected_inputs = [i.name for i in backend._session.get_inputs()]
    filtered_inputs = {
        k: np.array(v, dtype=np.int64) for k, v in inputs.items() if k in expected_inputs
    }
    
    logits = backend._session.run(None, filtered_inputs)[0]
    probs = (np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True))[0]
    
    for idx, token_probs in enumerate(probs):
        best_label = int(np.argmax(token_probs))
        best_prob = float(token_probs[best_label])
        runner_up_probs = np.copy(token_probs)
        runner_up_probs[best_label] = 0.0
        second_best = int(np.argmax(runner_up_probs))
        second_prob = float(runner_up_probs[second_best])

        label_str = (backend._id2label or {}).get(best_label)
        second_label_str = (backend._id2label or {}).get(second_best)
        print(f"Token {idx} '{encoding.tokens[idx]}': Best={label_str}({best_prob:.4f}), Second={second_label_str}({second_prob:.4f})")
        
mock_detect_window(text, 0, policy, None)
