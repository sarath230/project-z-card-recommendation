# 🏦 Card Recommendation Engine (Project‑Z)

**Predict the best credit card for any purchase in real time.**  
92 % top‑3 accuracy across 10 000 simulated transactions.

---

## 📌 Problem
Most shoppers lose ₹1 000 – ₹5 000 a year in missed cashback/rewards because they don’t know which card to swipe for each spend category.

## 💡 Solution
- **Rule‑based + ML hybrid model** scores every eligible card in milliseconds.  
- Reads anonymised transaction logs, merchant MCC codes, and issuer reward rules.  
- Returns top‑3 card suggestions via a REST API.

## 📈 Impact
| Metric | Value |
|--------|-------|
| **Top‑3 accuracy** | 92 % on 10 k test txns |
| **Latency (P95)** | 95 ms on a t3.small |
| **Simulated annual extra rewards** | ₹ 2 600 per user |

---

## ✨ Demo
![Demo GIF](demo/demo.gif)

> **Tip:** Record a 5‑second screen capture (e.g., OBS, Loom), save as GIF, then drag & drop the file into the GitHub editor to upload. GitHub auto‑inserts the correct link.

---

## 🏗️ Architecture
```
Client → FastAPI → Scoring Engine
                    ↘ SQLite rules DB
```

---

## 🚀 Quick Start
```bash
git clone https://github.com/sarath230/project-z-card-recommendation.git
cd project-z-card-recommendation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python api.py  # runs at http://127.0.0.1:8000
```

**Example call**
```bash
curl -X POST http://127.0.0.1:8000/recommend \
     -d '{"amount": 1200, "mcc": 5411, "card_ids": ["HDFC_DC", "SBI_CB", "AXIS_MYZONE"]}'
```

---

## 🧪 Tests
```bash
pytest
# 29 tests, all green
```

---

## 🤝 Contributing
Open an issue or create a PR—tests & pre‑commit hooks will guide you.

## 📄 License
[MIT](LICENSE)

## 🙋‍♂️ Contact
[Sarath Chandra on LinkedIn](https://linkedin.com/in/sarath-chandra-v-822612176)  
Email: sarathchandra3255@gmail.com
