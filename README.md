# 🛡️ Lumia: Decentralized Trust & Safety Layer for Portaldot

Lumia is a production-ready, high-performance infrastructure plugin and transaction scanner for the Portaldot ecosystem. It queries native Substrate pallets (Identity and System) to evaluate address risk in real-time, generates dynamic Llama-3.3-70b AI safety briefings, and registers immutable trust receipts on-chain via a custom ink! 5.0 contract.

Rather than being a standalone silo, Lumia is built as a **universal trust utility** that any Portaldot dApp can integrate to block malicious actors, protect users, and verify transactions.

---

## ⚡ 3-Line Integration Guide (dApp SDK Plugin)

Other Portaldot ecosystem projects (such as **TrashEarn** or **PortalMatch**) can integrate Lumia's trust scanning and receipt registration in just 3 steps:

```javascript
// Step 1: Scan recipient reputation and get AI-powered risk ratings
const scan = await fetch('https://lumia-api.portaldot.network/scan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ sender: "5Grw...", recipient: "5FHn...", amount: 25.0 })
}).then(r => r.json());

// Step 2: Block transactions if the trust score is too low (e.g., risk_score > 70)
if (scan.risk_score < 70) {
  const txHash = await sendPortaldotTransaction(); // Execute transaction on-chain

  // Step 3: Register the transaction trust receipt on the Lumia Registry contract
  await fetch('https://lumia-api.portaldot.network/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tx_hash: txHash, risk_score: scan.risk_score, risk_level: scan.risk_level, ai_briefing: scan.ai_briefing })
  });
}
```

---

## 🏗️ Technical Architecture

Lumia features a robust, multi-layer infrastructure designed to remain operational even during network volatility:

```
                  ┌──────────────────────────────┐
                  │      Lumia REST API (FastAPI)│
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼──────────────────────┐
         ▼                       ▼                      ▼
┌─────────────────┐     ┌─────────────────┐    ┌──────────────────┐
│Substrate Scanner│     │ AI Risk Engine  │    │  Registry Client │
│(Pallet Queries) │     │ (Groq/Llama 70B)│    │(ink! 5.0/AliceUri)│
└────────┬────────┘     └─────────────────┘    └────────┬─────────┘
         │                                              │
         ▼                                              ▼
┌──────────────────┐                           ┌──────────────────┐
│ Portaldot RPC    │                           │ Substrate Node / │
│ (Identity/System)│                           │ Local Contract db│
└──────────────────┘                           └──────────────────┘
```

### 1. Lumia Scanner (`backend/scanner.py`)
- Interfaces directly with the Portaldot blockchain via custom JSON-RPC calls.
- Inspects the `Identity` pallet for registrar-verified credentials (`KnownGood`, `Reasonable`) and the `System` pallet to verify address age and transaction history (nonce count).
- Includes **Graceful Scanner Fallbacks** to ensure the API remains fully operational even if the RPC node experiences downtime.

### 2. AI Risk Engine (`backend/risk_engine.py`)
- Employs the `Llama-3.3-70b` model via Groq cloud SDK to analyze scanner results.
- Synthesizes complex block data into human-scannable transaction security briefings.

### 3. Registry ink! Contract (`contracts/lumia_registry/lib.rs`)
- Written in **ink! 5.0** for low gas fees, extreme speed, and strict memory safety.
- Exposes `register_receipt` to index transaction scans on-chain and `get_receipt` to retrieve them.
- Employs a **Self-Healing Fallback Client (`backend/contract_client.py`)** that stores scans in a local JSON cache if the local Substrate Contracts node is temporarily offline.

---

## 🛠️ Quick Start & Development

### 1. Requirements
Ensure you have Python 3.10+ installed.

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Run Backend
```bash
python -m backend.app
```
The server will start on `http://localhost:8000`, serving the REST API endpoints and hosting the premium minimalist dashboard at `http://localhost:8000/`.

---

*Lumia is the proactive security layer making Portaldot safer for every user, one transaction at a time.*
