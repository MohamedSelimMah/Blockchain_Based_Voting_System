# 🗳️ Blockchain-Based Secure Voting System - v1.5

A secure blockchain-powered voting system built with Python and Flask. Ideal for those exploring blockchain, REST APIs, encryption, and secure digital voting systems.

---

## ✅ Version 1.5 – Feature Enhancements

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

---

## 🚀 Getting Started

### Requirements

- Python 3.x
- Flask
- `pycryptodome` (for AES encryption)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/blockchain-voting-system.git
   cd blockchain-voting-system
   ```

2. **Install dependencies**

   ```bash
   pip install flask pycryptodome
   ```

3. **Run the app**

   ```bash
   python app.py
   ```

Server will run on `http://127.0.0.1:5000`

---

## 📱 API Endpoints

| Method | Endpoint           | Description                                |
|--------|--------------------|--------------------------------------------|
| POST   | `/vote`            | Submit an encrypted vote                   |
| GET    | `/mine`            | Mine votes into a block                    |
| GET    | `/chain`           | View the entire blockchain                 |
| POST   | `/register`        | Register a new voter                       |
| POST   | `/admin/decrypt`   | Admin-only endpoint to decrypt votes       |
| GET    | `/admin/results`   | Admin-only endpoint to view vote counts    |

---

## 📂 Sample Vote Submission

POST to `/vote`:

```json
{
  "voterId": "your-unique-id",
  "vote": "Alice"
}
```

- `voterId` is validated and hashed for integrity.
- Vote is encrypted using AES before storage.
- Duplicate votes are rejected.

---

## 🔗 How It Works

1. **Registration**: Voters register via `/register`. Validation logic ensures one-time registration.
2. **Voting**: Validated voters submit votes, which are AES-encrypted.
3. **Mining**: Pending votes mined into blocks with Proof-of-Work.
4. **Blockchain**: Each block is chained via secure hashing.
5. **Admin Panel**:
   - Only admin can decrypt and view vote contents.
   - View results via `/admin/results`.

---

## 🔗 Why Use Blockchain?

- **Transparency**: Chain is publicly viewable
- **Integrity**: Tamper-proof blocks
- **Security**: Encrypted, private, and validated votes

---

## 🛠️ Coming Soon

- Multi-node network
- Consensus protocol
- Web UI for voter interaction
- Role-based access control

---

## 📘 Learn More

This project covers:
- Blockchain basics
- Proof-of-Work
- AES encryption
- Flask API development
- Secure app design

---

## 📄 License

Open-source under the [MIT License](LICENSE)

