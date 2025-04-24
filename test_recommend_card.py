import json
import pytest

from project_z_recommendation_engine import recommend_card

@pytest.fixture
def rules():
    """Load card rules from the JSON file for testing."""
    with open('card_rules.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_known_category(rules):
    """Transactions in a known category pick the card with highest cashback for that category."""
    txn = {'amount': 100.0, 'merchant': 'TestShop', 'category': 'fashion'}
    best = recommend_card(txn, rules)
    assert best['card_name'] == 'Flipkart Axis'
    assert best['cashback_percent'] == 5
    assert best['cashback_value'] == pytest.approx(5.0)

def test_unknown_category_defaults(rules):
    """Transactions in an unknown category fallback to default rates."""
    txn = {'amount': 200.0, 'merchant': 'TestShop', 'category': 'unknown'}
    # All cards have default 1% => cashback 2.0, so the first card in rules is chosen
    best = recommend_card(txn, rules)
    assert best['cashback_value'] == pytest.approx(2.0)

def test_empty_rules():
    """No card rules provided returns None."""
    txn = {'amount': 150.0, 'merchant': 'TestShop', 'category': 'fashion'}
    best = recommend_card(txn, {})
    assert best is None

def test_tie_breaker():
    """When two cards yield equal cashback, the first one encountered is returned."""
    test_rules = {
        'CardA': {'fashion': 5, 'default': 1},
        'CardB': {'fashion': 5, 'default': 1}
    }
    txn = {'amount': 100.0, 'merchant': 'TestShop', 'category': 'fashion'}
    best = recommend_card(txn, test_rules)
    assert best['card_name'] == 'CardA'
    assert best['cashback_value'] == pytest.approx(5.0)
