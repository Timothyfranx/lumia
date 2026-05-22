# Lumia: Trust Layer for Portaldot

## Core Concept
Lumia is an AI-powered transaction safety system and multisig monitoring platform. It uses Portaldot's native runtime pallets to verify trust and issue decentralized receipts.

## Modules
1. **Lumia Scanner (Python):** 
   - Queries the `identity` pallet for verified credentials.
   - Analyzes transaction history via RPC.
   - Generates AI risk scores.
2. **Lumia Registry (Native):** 
   - Uses the `uniques` pallet to issue NFT-based "Trust Receipts."
   - Uses the `identity` pallet to store/update reputation scores for scanned wallets.
3. **Lumia UI:** Web dashboard for safe transaction initiation and receipt verification.

## Verified Infrastructure
- **Primary RPC:** `wss://drip-backend-production-8d86.up.railway.app/node`
- **Native Pallets:** `identity`, `uniques`, `assets`, `balances`.
