from substrateinterface import SubstrateInterface
from backend.config import PORTALDOT_RPC

class SubstrateScanner:
    """
    SubstrateScanner connects to the Portaldot RPC endpoint and queries native
    runtime pallets (Identity and System) to evaluate wallet trust and history.
    """
    def __init__(self, rpc_url: str = PORTALDOT_RPC):
        self.rpc_url = rpc_url
        self._substrate = None

    @property
    def substrate(self) -> SubstrateInterface:
        """
        Lazy-loads the Substrate connection to handle connection drops and initialization.
        """
        if self._substrate is None:
            self._substrate = SubstrateInterface(url=self.rpc_url)
        return self._substrate

    def scan_address(self, address: str) -> dict:
        """
        Scans a wallet address using on-chain pallet checks.
        Returns a dictionary containing risk score, risk level, and explanations.
        """
        risk_score = 0
        reasons = []
        has_identity = False
        is_verified = False

        try:
            # 1. Query Identity Pallet (The "Golden Path" for trust verification)
            identity_info = self.substrate.query(
                module='Identity',
                storage_function='IdentityOf',
                params=[address]
            )

            if identity_info and identity_info.value:
                has_identity = True
                risk_score -= 30  # Registered identity significantly reduces risk
                reasons.append("Recipient has a registered on-chain identity.")
                
                # Check for registrar verification (judgments)
                judgments = identity_info.value.get('judgments', [])
                for j in judgments:
                    judgment_type = j[1]
                    if isinstance(judgment_type, dict):
                        judgment_name = next(iter(judgment_type.keys()), "")
                    else:
                        judgment_name = str(judgment_type)

                    if judgment_name in ["Reasonable", "KnownGood"]:
                        is_verified = True
                        risk_score -= 20
                        reasons.append(f"Identity is VERIFIED by a registrar ({judgment_name}).")
                        break
            else:
                risk_score += 20
                reasons.append("Recipient has NO on-chain identity.")

            # 2. Query System Pallet (Account Nonce/Age Verification)
            account_info = self.substrate.query(
                module='System',
                storage_function='Account',
                params=[address]
            )

            if account_info and account_info.value:
                nonce = account_info.value.get('nonce', 0)
                balance_data = account_info.value.get('data', {})
                free_balance = balance_data.get('free', 0)
            else:
                nonce = 0
                free_balance = 0

            if nonce == 0:
                risk_score += 40
                reasons.append("Recipient wallet is brand new (0 transactions).")
            else:
                reasons.append(f"Recipient wallet has active history ({nonce} transactions).")

            # 3. Balance validation
            if free_balance == 0:
                risk_score += 10
                reasons.append("Recipient has zero native POT balance.")

            # Clamping risk score between 0 and 100
            risk_score = max(0, min(100, risk_score))

            # Define risk levels
            if risk_score > 70:
                risk_level = "High"
                recommendation = "Cancel and Verify (High Fraud Risk)"
            elif risk_score > 30:
                risk_level = "Medium"
                recommendation = "Proceed with Caution (Unverified Active Address)"
            else:
                risk_level = "Low"
                recommendation = "Proceed (Trusted Wallet)"

            return {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "reasons": reasons,
                "recommendation": recommendation,
                "details": {
                    "has_identity": has_identity,
                    "is_verified": is_verified,
                    "nonce": nonce,
                    "free_balance": str(free_balance)
                }
            }

        except Exception as e:
            # Return scan failure details gracefully to backend app
            raise RuntimeError(f"Failed to scan address {address} on-chain: {str(e)}")
