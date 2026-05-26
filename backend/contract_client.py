import os
import json
import logging
from datetime import datetime
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LumiaContractClient")

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_PATH = os.path.join(BASE_DIR, "contracts", "lumia_registry", "target" , "ink", "lumia_registry.json")
MOCK_DB_PATH = os.path.join(BASE_DIR, "backend", "mock_contract_db.json")

class LumiaContractClient:
    """
    Interacts with the custom ink! 5.0 LumiaRegistry smart contract on-chain.
    Provides a seamless fallback database if no local contracts node is running.
    """
    def __init__(self, rpc_url: str = None, contract_address: str = None):
        self.rpc_url = rpc_url or os.getenv("LOCAL_CONTRACTS_RPC", "ws://127.0.0.1:9944")
        self.contract_address = contract_address or os.getenv("LUMIA_CONTRACT_ADDRESS")
        self.substrate = None
        self.contract = None
        self.use_fallback = True

        # Initialize mock fallback database if it doesn't exist
        if not os.path.exists(MOCK_DB_PATH):
            with open(MOCK_DB_PATH, "w") as f:
                json.dump({}, f)

        # Attempt to establish real Substrate Connection
        try:
            logger.info(f"Connecting to Substrate Contracts node at {self.rpc_url}...")
            self.substrate = SubstrateInterface(
                url=self.rpc_url,
                ss58_format=42,
                type_registry_preset='substrate-node-template'
            )
            
            # Verify if metadata exists
            if os.path.exists(METADATA_PATH) and self.contract_address:
                from substrateinterface.contracts import ContractInstance
                logger.info(f"Loading ink! contract metadata from {METADATA_PATH}...")
                self.contract = ContractInstance.create_from_address(
                    substrate=self.substrate,
                    contract_address=self.contract_address,
                    metadata_file=METADATA_PATH
                )
                self.use_fallback = False
                logger.info(f"Successfully bound to active contract at {self.contract_address}")
            else:
                logger.warning("Contract address or metadata missing. Operating in Hybrid Mock/Fallback mode.")
        except Exception as e:
            logger.warning(f"Could not connect to Substrate Contracts node ({e}). Operating in Graceful Fallback mode.")

    def register_receipt(self, tx_hash: str, risk_score: int, extra_data: dict = None) -> dict:
        """
        Registers a transaction scan receipt.
        If on-chain registration is active, calls register_receipt extrinsic.
        Otherwise, writes to the mock fallback JSON store.
        """
        # Normalize transaction hash
        if not tx_hash.startswith("0x"):
            tx_hash = "0x" + tx_hash

        # Format trust receipt structure
        receipt_data = {
            "scanner_id": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", # Alice (Standard Dev Admin)
            "risk_score": risk_score,
            "timestamp": int(datetime.utcnow().timestamp()),
            "timestamp_readable": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "verified": True,
            "onchain": not self.use_fallback
        }

        # Merge extra data (risk_level, ai_briefing) if provided
        if extra_data:
            receipt_data.update(extra_data)

        if not self.use_fallback and self.contract:
            try:
                # Use standard dev keypair (Alice) to sign the transaction
                keypair = Keypair.create_from_uri('//Alice')
                logger.info(f"Sending on-chain extrinsic to register receipt for tx {tx_hash}...")
                
                # Execute contract call
                contract_receipt = self.contract.exec(
                    keypair=keypair,
                    method_name='register_receipt',
                    args={'tx_hash': tx_hash, 'risk_score': risk_score},
                    gas_limit={'ref_time': 10000000000, 'proof_size': 500000}
                )
                
                if contract_receipt.is_success:
                    logger.info("Successfully registered trust receipt on-chain.")
                    return receipt_data
                else:
                    logger.error(f"On-chain contract execution failed: {contract_receipt.error_message}")
            except Exception as e:
                logger.error(f"Failed to submit on-chain contract transaction: {e}. Falling back...")

        # Fallback to local JSON store
        try:
            with open(MOCK_DB_PATH, "r") as f:
                db = json.load(f)
            
            db[tx_hash] = receipt_data
            
            with open(MOCK_DB_PATH, "w") as f:
                json.dump(db, f, indent=4)
                
            logger.info(f"Registered receipt in local fallback database for {tx_hash}")
            return receipt_data
        except Exception as e:
            logger.error(f"Failed to write to fallback database: {e}")
            return receipt_data

    def get_receipt(self, tx_hash: str) -> dict:
        """
        Retrieves a receipt by transaction hash from the smart contract or fallback database.
        """
        if not tx_hash.startswith("0x"):
            tx_hash = "0x" + tx_hash

        if not self.use_fallback and self.contract:
            try:
                # Query contract state
                result = self.contract.read(
                    keypair=Keypair.create_from_uri('//Alice'),
                    method_name='get_receipt',
                    args={'tx_hash': tx_hash}
                )
                if result and result.contract_result and result.contract_result.get('success'):
                    # Parse ink! Receipt struct output
                    value = result.contract_result.get('data')
                    if value:
                        return {
                            "success": True,
                            "tx_hash": tx_hash,
                            "receipt": {
                                "scanner_id": value.get('scanner_id'),
                                "risk_score": value.get('risk_score'),
                                "timestamp": value.get('timestamp'),
                                "verified": value.get('verified', True),
                                "onchain": True
                            }
                        }
            except Exception as e:
                logger.error(f"On-chain contract query failed: {e}. Falling back...")

        # Fallback query
        try:
            with open(MOCK_DB_PATH, "r") as f:
                db = json.load(f)
            
            if tx_hash in db:
                return {
                    "success": True,
                    "tx_hash": tx_hash,
                    "receipt": db[tx_hash]
                }
        except Exception as e:
            logger.error(f"Failed to read from fallback database: {e}")

        return {
            "success": False,
            "tx_hash": tx_hash,
            "message": "Receipt not found in Lumia Trust Registry."
        }
