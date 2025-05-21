# 🗳️ Blockchain-Based Secure Voting System - v2.0 

A secure blockchain-powered voting system built with Python and Flask. Perfect for exploring blockchain, REST APIs, encryption, and secure digital voting in a **distributed** environment.

---

## ✅ Version 2.0 – Major Feature Upgrades

- ⚓️ Basic blockchain with Proof-of-Work (PoW)
- 🗳️ Cast votes using the `/vote` endpoint
- ⛔️ Prevent double voting via hashed Voter IDs
- 🛠️ Mine pending votes into blocks via `/mine`
- 🔍 View blockchain via `/chain`
- 🌐 Flask-based REST API
- 🧑‍👷 Mining rewards for PoW
- 🔐 **AES Vote Encryption** to protect vote content
- 🔑 **Decryption logic restricted to admin only**
- 📅 **Admin panel endpoints** for vote result visibility
- 🔧 **Registration and validation logic** to manage voter eligibility

### 🌐 Distributed Blockchain (New in v2.0)
- 🌍 **Multi-node network support**
- 🧠 **Consensus algorithm** to maintain single source of truth
- 🔗 **Node registration & broadcasting**
- 🔄 **Automatic chain syncing across nodes**

---

## 🚀 Getting Started

### Requirements

- Python 3.x
- Flask
- `pycryptodome` (for AES encryption)
- Requests (for inter-node communication)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/blockchain-voting-system.git
   cd blockchain-voting-system
   ```

2. **Install dependencies**

   ```bash
   pip install flask pycryptodome requests
   ```

3. **Run the app**

   ```bash
   python app.py
   ```

Server will run on `http://127.0.0.1:5000`

---

## 📱 API Endpoints

| Method | Endpoint               | Description                                  |
|--------|------------------------|----------------------------------------------|
| POST   | `/vote`                | Submit an encrypted vote                     |
| GET    | `/mine`                | Mine votes into a block                      |
| GET    | `/chain`               | View the entire blockchain                   |
| POST   | `/register`            | Register a new voter                         |
| POST   | `/admin/decrypt`       | Admin-only endpoint to decrypt votes         |
| GET    | `/admin/results`       | Admin-only endpoint to view vote counts      |
| POST   | `/nodes/register`      | Register new nodes to the network            |
| GET    | `/nodes/resolve`       | Consensus algorithm to resolve chain         |

---

## 📂 Sample Vote Submission

POST to `/vote`:

```json
{
  "voterId": "your-unique-id",
  "vote": "Alice"
}
```

- `voterId` is validated and hashed.
- Vote is AES-encrypted.
- One vote per voter enforced.

---

## 🔗 How It Works

1. **Registration**: Voter registers once via `/register`.
2. **Voting**: Voter submits encrypted vote via `/vote`.
3. **Mining**: Pending votes are mined with PoW.
4. **Distributed Network**:
   - Nodes register with each other
   - Chains are synced using a consensus algorithm
5. **Admin Panel**:
   - Admin-only decryption of votes
   - Vote results accessible via `/admin/results`

---

## 🤝 Why Use Blockchain?

- **Transparency**: Public, traceable blockchain
- **Integrity**: Tamper-resistant records
- **Security**: Encrypted, validated, and permission-controlled
- **Decentralization**: No single point of failure

---

## 🛠️ Coming Soon

- Web-based voting interface
- Role-based access control (voter, admin, observer)
- Enhanced consensus via PBFT or Raft

---

## 📘 Learn More

This project helps you learn:
- Distributed blockchain mechanics
- Proof-of-Work & Consensus algorithms
- AES encryption for privacy
- Flask APIs for full-stack blockchain apps
- Designing secure, decentralized systems

---

## 📄 License

Open-source under the [MIT License](LICENSE)
