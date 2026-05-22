# 🟣 Antigravity Developer Master Log: Portaldot Hackathon

Welcome to the master control and resource center for the **Portaldot Online Mini Hackathon (Season 1)**. This file serves as the main entry point and navigation directory for all developer files, setup guides, and ideation notes in the workspace.

---

## ⚡ Critical Milestones & Deadlines

| Milestone | Date & Time | Status | Action Required |
| :--- | :--- | :--- | :--- |
| **Demo Day Thread Submission** | **May 24, 2026 — 8:00 AM UTC** | ⏳ **Upcoming** | Create team thread in Discord `<#1507257230603456573>` |
| **Hackathon Submission Deadline** | **May 31, 2026 — 11:59 PM UTC** | ⏳ **Upcoming** | Finalize codebase, README, and submit GitHub URL |

---

## 📂 Repository Directory Map (Modular Architecture)

The repository has been restructured into a modular, production-ready hierarchy:

### 🐍 1. Backend Module (`/backend`)
* 🌐 **[app.py](file:///home/replytim/Desktop/portaldot/backend/app.py)** - FastAPI entry point, handling middleware, routers, and CORS.
* 🔎 **[scanner.py](file:///home/replytim/Desktop/portaldot/backend/scanner.py)** - Core Substrate interface. Dynamically queries the `Identity` and `System` pallets on the Portaldot network.
* 🧠 **[risk_engine.py](file:///home/replytim/Desktop/portaldot/backend/risk_engine.py)** - AI Risk Assessment engine that analyzes on-chain metrics and generates contextual transaction briefs.
* ⚙️ **[config.py](file:///home/replytim/Desktop/portaldot/backend/config.py)** - Configuration module for port parameters and public/local RPC connections.
* 📦 **[requirements.txt](file:///home/replytim/Desktop/portaldot/backend/requirements.txt)** - Locked Python dependencies.

### 🦀 2. Smart Contract Module (`/contracts`)
* 📜 **[lumia_registry](file:///home/replytim/Desktop/portaldot/contracts/lumia_registry/lib.rs)** - The `ink! 5.0` smart contract that provides a cryptographically secure, on-chain mapping of `TransactionHash -> TrustReceipt`.

### 📚 3. Documentation Module (`/docs`)
* 🎯 **[demo_day_criteria.md](file:///home/replytim/Desktop/portaldot/demo_day_criteria.md)** - Review rating criteria (🟢 **Green**, 🟡 **Yellow**, 🔴 **Red**) and Discord thread templates.
* 🛡️ **[SUBSTRATE_NOTICE.md](file:///home/replytim/Desktop/portaldot/docs/SUBSTRATE_NOTICE.md)** - The mandatory core team disclaimer explaining the local node API limitation.
* 📚 **[portaldot_knowledge_base.md](file:///home/replytim/Desktop/portaldot/portaldot_knowledge_base.md)** - Comprehensive ecosystem technical maps, node runner guides, and workarounds.

### 📝 4. Capsule Logs & Automation
* 📋 **[summary.md](file:///home/replytim/Desktop/portaldot/summary.md)** - The real-time branch and commit log tracking our exact git history tree.
* 🐚 **[setup_node.sh](file:///home/replytim/Desktop/portaldot/setup_node.sh)** - Interactive shell script to manage local Substrate node sessions.

---

## 🏆 Current Hackathon Rating Readiness Check

To guarantee a **🟢 GREEN: Demo Day Ready** rating, we are tailoring our project architecture to directly fulfill the evaluation rules:

1. **Local Node Integration:** Automated through `setup_node.sh`. Supports switching to `substrate-contracts-node` for fully stable local smart contract deployment.
2. **On-Chain Evidence:** Proved by querying the Substrate RPC using `SubstrateScanner` to inspect actual active block data.
3. **POT Fee Demonstration:** Our frontend UI will explicitly capture and display the gas fees/extrinsic weight consumed by every transaction.
4. **90-Second Demo Focus:** We will design our project's user journey to fit within a tight **60–90 second** flow, showing one high-value action end-to-end.
5. **Smart Contract Portability:** Our custom `ink! 5.0` contracts compile cleanly under standard toolchains, allowing judges to test them instantly in vanilla Substrate environments or deployed live on the public dev node.

---

## 🛠️ Next Steps: Active Project Roadmap
1. 🧠 **Day 3-4 Plan:** Refine LLM prompt details or API credentials in `risk_engine.py` for advanced AI transaction security briefings.
2. 🎨 **Day 7-8 Plan:** Initialize the Lumia frontend dashboard using Vite (React + TypeScript) to communicate with the FastAPI backend and sign safe transactions via Polkadot{.js}.
