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
- 🧑‍🔧 Mining rewards for nodes performing Proof-of-Work

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
   ```

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
  "voterId": "your-unique-id",
  "vote": "Alice"
}
```

- `voterId` will be hashed internally to ensure voter privacy.
- If the same voter tries to vote again, the system will reject it.

---

## 🔗 How It Works (Simplified)

- Voters submit their vote by providing a unique `voterId` and a candidate name via the `/vote` endpoint.
- The `voterId` is hashed and stored to prevent double voting.
- Pending votes are stored in memory and are mined into new blocks using the `/mine` endpoint.
- Proof-of-Work (PoW) is used to ensure blocks are computationally difficult to forge.
- A mining reward is issued to the node performing the mining via the `/mine` endpoint.
- Each block is linked to the previous block using a hash, ensuring the integrity of the blockchain.

---

## 🎯 Why Use Blockchain?

- **Transparency**: All votes are visible on the chain.
- **Integrity**: Once added, blocks (and votes) can’t be altered.
- **Security**: Voter IDs are never stored directly, only as hashes, ensuring privacy.

---

## 🛠️ Next Steps

- Vote encryption (e.g., AES) for vote privacy
- Admin panel to view results
- Add voter registration route
- Simple CLI or UI for local testing

---

## 📘 Learn More

This project is a great starting point to learn:
- What blockchains are
- How hashing works
- How to build secure APIs using Flask

---

## 📄 License

Open-source under the [MIT License](LICENSE)
