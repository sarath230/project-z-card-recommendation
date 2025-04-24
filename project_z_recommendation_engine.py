import json

def load_card_rules(path="card_rules.json"):
    """Load card reward rules from JSON, with error handling."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {path} not found. Make sure the file exists in this folder.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse {path}: {e}")
        exit(1)

card_rules = load_card_rules()

def recommend_card(transaction, card_rules):
    category = transaction["category"]
    amount = transaction["amount"]

    best_card = None
    best_cashback = 0
    for card, rules in card_rules.items():
        cashback_percent = rules.get(category, rules.get("default", 0))
        cashback_value = (cashback_percent / 100) * amount
        if cashback_value > best_cashback:
            best_cashback = cashback_value
            best_card = {
                "card_name": card,
                "cashback_percent": cashback_percent,
                "cashback_value": cashback_value
            }
    return best_card

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Smart Card Recommendation")
    parser.add_argument("amount", type=float, help="Transaction amount")
    parser.add_argument("merchant", type=str, help="Merchant name")
    parser.add_argument("category", type=str, help="Transaction category")
    args = parser.parse_args()

    transaction = {
        "amount": args.amount,
        "merchant": args.merchant,
        "category": args.category.lower()
    }

    best = recommend_card(transaction, card_rules)
    if best:
        print("🔍 Project Z – Smart Card Recommendation")
        print(f"Transaction: ₹{transaction['amount']} at {transaction['merchant']} (Category: {transaction['category']})")
        print(f"✅ Recommended Card: {best['card_name']}")
        print(f"💰 Cashback: {best['cashback_percent']}% → ₹{best['cashback_value']:.2f}")
    else:
        print("No recommendation available for the given transaction.")
