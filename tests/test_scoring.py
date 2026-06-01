import numpy as np
from src.contextscore.scoring import embed

def test_embed_returns_expected_shape():
    texts = ["hello world", "goodbye"]
    result = embed(texts)
    assert isinstance(result, np.ndarray)
    assert result.shape == (2, 384)
    assert result.dtype == np.float32 or result.dtype == np.float64