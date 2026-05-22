# 🏁 Portaldot Hackathon: Demo Day Review & Rating Criteria

This document details the official **Review Rating Criteria** and **Discord Submission Guidelines** for the Portaldot Online Mini Hackathon (Season 1) Demo Day. 

> [!IMPORTANT]
> **Deadline:** **Sunday, May 24, 2026 — 8:00 AM UTC**
> Late submissions may not receive a rating before Demo Day. Proactively submit early to receive mentor feedback!

---

## 📊 Review Rating Criteria

Submissions will be rated by mentors and organizers using a **traffic-light system** (Green, Yellow, Red) based on risk and execution completeness.

### 🟢 GREEN: Low Risk (Demo Day Ready)
Your project is stable, functional, and ready for showcase.

* **Requirements:**
  1. **Local Node Execution:** A local Portaldot node runs successfully.
  2. **Active Integration:** The project frontend/backend is fully connected to the local node.
  3. **On-Chain Evidence:** At least one real on-chain extrinsic/transaction executes successfully.
  4. **Fee Transparency:** POT gas consumption/fees are clearly displayed and demonstrated.
  5. **Closed-Loop MVP:** The core MVP user flow runs end-to-end without breaking.
  6. **Concise Presentation:** The demo flow fits comfortably within a **60–90 second** window.
  7. **Deliverables Ready:** GitHub repository, detailed README, and a crisp demo video are fully prepared.
  8. **Robust Integration:** Any mocked parts are secondary and do not affect or interrupt the core transactional flow.

---

### 🟡 YELLOW: Risky (Recoverable)
Your project has working parts but requires immediate stabilization.

* **Common Situations:**
  * The node runs, but the frontend connection is intermittent or not fully integrated.
  * Smart contracts deploy, but core transaction calls are unstable or frequently fail.
  * A plan for POT fee visualization exists, but direct evidence or UI display is incomplete.
  * The MVP only partially works (incomplete user loop).
  * The demo flow is too large, cluttered, and needs significant trimming to fit the time limit.

* **Required Action Plan:**
  * ⚠️ The team **must** submit a **Must-Fix List** before Demo Day ends.
  * ❌ **Do NOT add new features.** Focus strictly on what is already built.
  * ✅ **Stabilize ONE smallest flow first.** Make a single path bulletproof rather than multiple paths broken.

---

### 🔴 RED: High Risk (Not Demo Day Ready)
Your project faces critical showstoppers that will prevent a successful demo.

* **Common Situations (Any of the following):**
  * The local Portaldot node cannot run or crashes on startup.
  * The project cannot connect to Portaldot at all.
  * No real on-chain transactions or calls are demonstrated.
  * No plan or demonstration for POT gas / fee integration.
  * No closed-loop user MVP flow exists.
  * The core, critical functionality of the application relies entirely on mocked/simulated code.

* **Required Action Plan:**
  * ⚠️ **Must cut scope immediately.** Strip away all auxiliary screens and complex features.
  * ✅ **Keep only ONE smallest demonstrable action** (e.g., a single token mint or a single profile setup) and make sure it works flawlessly.

---

## 💬 Discord Submission Workflow

To be reviewed and graded by the hackathon mentors, follow these steps exactly:

1. **Navigate to Discord Channel:** Join the channel `<#1507257230603456573>` in the Portaldot server.
2. **Create Your Team Thread:**
   Submit a new thread named exactly in this format:
   `[XX] Team Name - Project Name` *(Replace `[XX]` with your assigned team number).*
3. **Fill Out Submission Template:** Paste the official submission template inside the thread and fill in all details thoroughly.
4. **Iterate with Mentors:** Mentors will review your thread, ask questions, and provide direct technical feedback.
5. **Address Feedback:** Respond to mentor questions promptly and apply suggested fixes to your codebase.
6. **Receive Final Grade:** Organizers will post your final **🟢 Green**, **🟡 Yellow**, or **🔴 Red** rating in your thread once review is complete.

---

*Good luck, builders! Let's build a green, high-performance future! 🚀*
