# Lumia 8-Day Build Plan (The Golden Path)

- **Day 1-2: RPC & Identity Integration**
  - Connect to `wss://drip-backend-production-8d86.up.railway.app/node`.
  - Implement `Lumia Scanner` to check `identity.identityOf` for recipients.
- **Day 3-4: AI Risk Engine**
  - Integrate LLM to process pallet data (identity, balance, nonce).
- **Day 5: Native Trust Receipts**
  - Use the `uniques` pallet to "mint" a receipt NFT for every safe transaction.
- **Day 6: Reputation Updates**
  - Implement logic to set `identity` sub-accounts or metadata based on Lumia scans.
- **Day 7-8: Frontend & Demo**
  - Showcase "Lumia Verified" badges for safe wallets.
