from tools import *

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []   # empty list, no exception

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)

##########################################################################################

def test_suggest_outfit_with_wardrobe():
    new_item = load_listings()[0]
    wardrobe = {"items": [load_listings()[1], load_listings()[2]]}
    result = suggest_outfit(new_item, wardrobe)
    assert isinstance(result, str)
    assert len(result.strip()) > 0

def test_suggest_outfit_empty_wardrobe():
    new_item = load_listings()[0]
    wardrobe = {"items": []}
    result = suggest_outfit(new_item, wardrobe)
    assert isinstance(result, str)
    assert len(result.strip()) > 0

def test_suggest_outfit_returns_string():
    new_item = load_listings()[0]
    wardrobe = {"items": [load_listings()[1]]}
    result = suggest_outfit(new_item, wardrobe)
    assert isinstance(result, str)
    
##########################################################################################

def test_create_fit_card_returns_caption():
    new_item = load_listings()[0]
    result = create_fit_card("vintage jeans with a white tee and sneakers", new_item)
    assert isinstance(result, str)
    assert len(result.strip()) > 0

def test_create_fit_card_empty_outfit():
    new_item = load_listings()[0]
    result = create_fit_card("", new_item)
    assert isinstance(result, str)
    assert len(result.strip()) > 0

def test_create_fit_card_whitespace_outfit():
    new_item = load_listings()[0]
    result = create_fit_card("   ", new_item)
    assert isinstance(result, str)
    assert len(result.strip()) > 0