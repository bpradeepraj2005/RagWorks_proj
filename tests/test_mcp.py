import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from mcp_server.api import ecommerce_api

def test_api_search_products():
    """Test if the ecommerce adapter successfully parses dummyJSON."""
    results = ecommerce_api.search_products("laptop")
    assert isinstance(results, list)
    if len(results) > 0:
        assert "id" in results[0]
        assert "price" in results[0]

def test_api_price_comparisons():
    """Test mock competitor comparison logic."""
    comps = ecommerce_api.get_price_comparisons("1")
    assert len(comps) == 3
    assert "store" in comps[0]
    assert comps[0]["store"] in ["Mockzon", "Walmock", "Targmock"]
