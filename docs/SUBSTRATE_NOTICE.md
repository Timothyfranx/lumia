# Deployment Notice: Substrate Contracts Node

As per the Portaldot Core Team update (May 2026), this project utilizes a custom **ink! 5.0** smart contract. 

### Rationale
The current Portaldot node binary (specVersion 1002) runs **Contracts API v5**, which does not support the modern features of ink! 4.x/5.x (which require API v9+).

### Proof of Concept (PoC)
To demonstrate the full technical capabilities of **Lumia**, the `lumia_registry` contract was designed for and tested on a standard `substrate-contracts-node` (API v9+). The contract compiles cleanly and is architecturally compatible with the Portaldot vision of AI-Native, secure infrastructure. It will be deployable to the Portaldot mainnet immediately upon a runtime update to the node binaries.

---
*Note: For the live demo, we use a hybrid approach that fallback to Native Pallets (Identity/Uniques) to ensure functionality on the current Portaldot devnet.*
