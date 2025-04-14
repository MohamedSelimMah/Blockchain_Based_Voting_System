# 🗳️ Blockchain-Based Secure Voting System - v1.0

A simple and secure blockchain-powered voting system built with Python and Flask. This version is ideal for beginners who want to learn the basics of blockchain, REST APIs, and digital voting systems.

---

## ✅ Version 1.0 – MVP Features

- ⛓️ Basic blockchain implementation with Proof-of-Work (PoW)
- 🗳️ Cast votes using the `/vote` endpoint
- 🚫 Prevent double voting using hashed Voter IDs
- 🛠️ Mine pending votes into new blocks via `/mine`
- 🔍 View the full blockchain with `/chain`
- 🌐 Flask-based REST API

---

## 🚀 Getting Started

### Requirements

- Python 3.x
- Flask (Install via pip)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/blockchain-voting-system.git
   cd blockchain-voting-system

2. **Install dependencies**

   ```bash
   pip install flask
   ```

3. **Run the app**

   ```bash
   python app.py
   ```

The server will run on `http://127.0.0.1:5000`.

---

## 📡 API Endpoints

| Method | Endpoint    | Description                           |
|--------|-------------|---------------------------------------|
| POST   | `/vote`     | Submit a vote                         |
| GET    | `/mine`     | Mine pending votes into a block       |
| GET    | `/chain`    | View the current blockchain           |

---

## 🧾 Sample Vote Submission

POST a JSON payload to `/vote`:

```json
{
  "voter_id": "your-unique-id",
  "candidate": "Alice"
}
```

- `voter_id` will be hashed internally to ensure voter privacy.
- If the same voter tries to vote again, the system will reject it.

---

## 🔗 How It Works (Simplified)

- Votes are collected and stored in memory temporarily.
- When you mine using `/mine`, all pending votes are added to a block.
- Each block is linked to the previous one using a hash (like a digital fingerprint).
- Proof-of-Work ensures each block takes computing effort to mine — securing the chain from tampering.

---

## 🎯 Why Use Blockchain?

- **Transparency**: All votes are visible on the chain.
- **Integrity**: Once added, blocks (and votes) can’t be altered.
- **Security**: Voter IDs are never stored directly, only as hashes.

---

## 🛠️ Next Steps

- Encryption
- Admin dashboard
- Multi-node blockchain
- UI and visualization

---

## 📘 Learn More

This project is a great starting point to learn:
- What blockchains are
- How hashing works
- How to build secure APIs using Flask

---

## 📄 License

Open-source under the [MIT License](LICENSE)
