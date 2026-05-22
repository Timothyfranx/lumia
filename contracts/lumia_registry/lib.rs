#![cfg_attr(not(feature = "std"), no_std, no_main)]

#[ink::contract]
mod lumia_registry {
    use ink::storage::Mapping;

    /// A receipt structure stored on-chain to verify a transaction scan.
    #[derive(scale::Decode, scale::Encode, Debug)]
    #[cfg_attr(
        feature = "std",
        derive(scale_info::TypeInfo, ink::storage::traits::StorageLayout)
    )]
    pub struct Receipt {
        pub scanner_id: AccountId,
        pub risk_score: u8,
        pub timestamp: Timestamp,
        pub verified: bool,
    }

    #[ink(storage)]
    pub struct LumiaRegistry {
        /// Maps transaction hashes to their Lumia receipts.
        receipts: Mapping<Hash, Receipt>,
        /// The authorized scanner address (Lumia backend).
        admin: AccountId,
    }

    #[ink(event)]
    pub struct ReceiptGenerated {
        #[ink(topic)]
        tx_hash: Hash,
        #[ink(topic)]
        scanner: AccountId,
        risk_score: u8,
    }

    impl LumiaRegistry {
        /// Constructor that initializes the admin.
        #[ink(constructor)]
        pub fn new() -> Self {
            Self {
                receipts: Mapping::default(),
                admin: Self::env().caller(),
            }
        }

        /// Registers a new transaction receipt. Only callable by admin.
        #[ink(message)]
        pub fn register_receipt(&mut self, tx_hash: Hash, risk_score: u8) -> bool {
            let caller = self.env().caller();
            assert!(caller == self.admin, "Only admin can register receipts");

            let receipt = Receipt {
                scanner_id: caller,
                risk_score,
                timestamp: self.env().block_timestamp(),
                verified: true,
            };

            self.receipts.insert(tx_hash, &receipt);
            
            self.env().emit_event(ReceiptGenerated {
                tx_hash,
                scanner: caller,
                risk_score,
            });

            true
        }

        /// Retrieves a receipt by transaction hash.
        #[ink(message)]
        pub fn get_receipt(&self, tx_hash: Hash) -> Option<Receipt> {
            self.receipts.get(tx_hash)
        }

        /// Updates the admin address.
        #[ink(message)]
        pub fn transfer_admin(&mut self, new_admin: AccountId) {
            assert!(self.env().caller() == self.admin, "Unauthorized");
            self.admin = new_admin;
        }
    }
}
