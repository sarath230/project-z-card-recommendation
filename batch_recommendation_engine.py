import sys
import json
import csv

# Load card reward rules from JSON, with error handling
try:
    with open("card_rules.json", "r", encoding="utf-8") as f:
        card_rules = json.load(f)
except FileNotFoundError:
    print("Error: card_rules.json not found. Make sure the file exists in this folder.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse card_rules.json: {e}")
    sys.exit(1)

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
    input_file = "transactions.csv"
    output_file = "batch_recommendations.csv"

    # Attempt to open transactions file
    try:
        csv_in = open(input_file, newline='', encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        sys.exit(1)

    with csv_in as in_f, open(output_file, "w", newline="", encoding="utf-8") as out_f:
        reader = csv.DictReader(in_f)
        if reader.fieldnames is None:
            print(f"Error: {input_file} is empty or missing headers.")
            sys.exit(1)

        # Set up CSV writer with extra fields
        fieldnames = reader.fieldnames + ["card_name", "cashback_percent", "cashback_value"]
        writer = csv.DictWriter(out_f, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Validate required columns
            if not all(col in row for col in ("amount", "merchant", "category")):
                print(f"Warning: missing column(s) in row {reader.line_num}, skipping.")
                continue

            # Validate and parse amount
            try:
                amount = float(row["amount"])
                if amount < 0:
                    raise ValueError()
            except ValueError:
                print(f"Warning: invalid amount '{row['amount']}' on row {reader.line_num}, skipping.")
                continue

            # Clean merchant and category
            merchant = row["merchant"].strip()
            category = row["category"].strip().lower()
            if not merchant or not category:
                print(f"Warning: missing merchant or category on row {reader.line_num}, skipping.")
                continue

            # Get recommendation
            transaction = {"amount": amount, "merchant": merchant, "category": category}
            best = recommend_card(transaction, card_rules)
            if best is None:
                print(f"Warning: no rules for category '{category}' on row {reader.line_num}, skipping.")
                continue

            # Write output row
            out_row = row.copy()
            out_row["card_name"] = best["card_name"]
            out_row["cashback_percent"] = best["cashback_percent"]
            out_row["cashback_value"] = f"{best['cashback_value']:.2f}"
            writer.writerow(out_row)

    print(f"Batch recommendations written to {output_file}")
