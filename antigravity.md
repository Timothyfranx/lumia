# 🟣 Antigravity Developer Master Log: Portaldot Hackathon

Welcome to the master control and resource center for the **Portaldot Online Mini Hackathon (Season 1)**. This file serves as the main entry point and navigation directory for all developer files, setup guides, and ideation notes in the workspace.

---

## ⚡ Critical Milestones & Deadlines

| Milestone | Date & Time | Status | Action Required |
| :--- | :--- | :--- | :--- |
| **Demo Day Thread Submission** | **May 24, 2026 — 8:00 AM UTC** | ⏳ **Upcoming** | Create team thread in Discord `<#1507257230603456573>` |
| **Hackathon Submission Deadline** | **May 31, 2026 — 11:59 PM UTC** | ⏳ **Upcoming** | Finalize codebase, README, and submit GitHub URL |

---

## 📂 Repository Directory Map

Here are the key technical files and resources available in your workspace:

### 📢 Demo Day Readiness
* 🎯 **[demo_day_criteria.md](file:///home/replytim/Desktop/portaldot/demo_day_criteria.md)** 
  * The exact review criteria (🟢 **Green**, 🟡 **Yellow**, 🔴 **Red** ratings) used by mentors to evaluate projects, plus step-by-step instructions on submitting thread formats in the Discord server.

### 🧠 Developer Knowledge Base & Local Node Automation
* 📚 **[portaldot_knowledge_base.md](file:///home/replytim/Desktop/portaldot/portaldot_knowledge_base.md)**
  * Comprehensive documentation covering the runtime version blocks (Contracts API v5 vs. v9+), public dev endpoints, native Substrate pallets, and mobile/Codespace node running guides.
* 🐚 **[setup_node.sh](file:///home/replytim/Desktop/portaldot/setup_node.sh)**
  * An interactive, fully automated shell script to start, configure, clear lock files, and manage your local Portaldot node.

### 💡 Hackathon Ideation & Strategic Designs
* 🎨 **[hackathon_ideation.md](file:///home/replytim/.gemini/antigravity-cli/brain/75e5e62f-86ee-495d-82bf-2752d2559f63/hackathon_ideation.md)** *(Antigravity Brain Artifact)*
  * Five highly original, green-focused, RWA, and AI blueprints tailored to win Portaldot's specific ecosystem narrative.

---

## 🏆 Current Hackathon Rating Readiness Check

To guarantee a **🟢 GREEN: Demo Day Ready** rating, we are tailoring our project architecture to directly fulfill the evaluation rules:

1. **Local Node Integration:** Automated through `setup_node.sh`. Supports switching to `substrate-contracts-node` for fully stable local smart contract deployment.
2. **On-Chain Transactions:** Leverages modern `@polkadot/api` to execute extrinsics with clear, visual console outputs.
3. **POT Fee Demonstration:** Our frontend UI will explicitly capture and display the gas fees/extrinsic weight consumed by every transaction.
4. **90-Second Demo Focus:** We will design our project's user journey to fit within a tight **60–90 second** flow, showing one high-value action end-to-end.
5. **Smart Contract Portability:** Our custom `ink! 4.x` contracts will compile cleanly under standard toolchains, allowing judges to test them instantly in vanilla Substrate environments or deployed live on the public dev node.

---

## 🛠️ Next Steps: Active Project Roadmap
1. 🗳️ **Select MVP Concept:** Choose one of the 5 blueprints (e.g., **GreenAnchor** or **ReChain**) or define a custom hybrid.
2. 🚀 **Initialize Framework:** Spin up the web application skeleton (Vite or Next.js) using the `web_application_development` guidelines.
3. 📦 **Install Polkadot Dependencies:** Integrate `@polkadot/api` and `@polkadot/api-contract`.
4. 🏗️ **Write & Verify ink! Contracts:** Code custom business rules in Rust, validating them on a local `substrate-contracts-node`.
5. 🎨 **Craft Premium UI:** Build a stunning glassmorphic interface featuring live block feeds, POT gas transaction fees, and interactive maps.
