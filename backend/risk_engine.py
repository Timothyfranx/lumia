import os
from groq import Groq

class AIRiskEngine:
    """
    AIRiskEngine analyzes on-chain pallet data and generates
    rich, natural-language safety briefings using the Groq Llama-3 model.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate_briefing(self, scan_results: dict, request_data: dict) -> str:
        """
        Generates a natural-language transaction safety briefing via Groq LLM.
        Falls back to a rule-based generator if no API key is available.
        """
        if not self.client:
            return self._generate_fallback_briefing(scan_results, request_data)

        prompt = f"""
        Analyze the following Portaldot blockchain transaction and provide a concise, 3-point security briefing for a user.
        
        CONTEXT:
        - Recipient: {request_data['recipient']}
        - Amount: {request_data['amount']} {request_data['token']}
        - Risk Score: {scan_results['risk_score']}/100
        - Risk Level: {scan_results['risk_level']}
        - On-chain Details: {scan_results['details']}
        - On-chain Reasons: {", ".join(scan_results['reasons'])}
        
        REQUIREMENTS:
        1. Tone: Professional, authoritative, yet simple.
        2. Format: Exactly 3 bullet points starting with appropriate emojis (✅, ⚠️, or 🛑).
        3. Goal: Tell the user if they should proceed and why.
        """

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Lumia, an AI Trust Layer for the Portaldot blockchain. You provide security briefings for transactions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"AI Briefing Unavailable (Error: {str(e)}). \nFallback:\n{self._generate_fallback_briefing(scan_results, request_data)}"

    def _generate_fallback_briefing(self, scan_results: dict, request_data: dict) -> str:
        # (Existing rule-based logic remains here as a safe fallback)
        risk_score = scan_results["risk_score"]
        risk_level = scan_results["risk_level"]
        recipient = request_data["recipient"]
        
        briefing = [f"System Scan: {risk_level} Risk ({risk_score}/100)"]
        if scan_results["details"]["nonce"] == 0:
            briefing.append("🛑 Warning: New wallet detected.")
        else:
            briefing.append(f"✅ Active history: {scan_results['details']['nonce']} transactions.")
        
        return "\n".join(briefing)
