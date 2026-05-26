from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from backend.config import PORTALDOT_RPC, API_HOST, API_PORT
from backend.scanner import SubstrateScanner
from backend.risk_engine import AIRiskEngine
from backend.contract_client import LumiaContractClient
from backend.pdf_generator import LumiaReceiptGenerator
import io

app = FastAPI(
    title="Lumia Trust Layer API",
    description="Decentralized transaction safety scanner, AI risk rating engine, and trust receipt registry.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scanner, risk, and contract engines
scanner = SubstrateScanner()
risk_engine = AIRiskEngine()
contract_client = LumiaContractClient()
receipt_generator = LumiaReceiptGenerator()

# Mount frontend files under /static
app.mount("/static", StaticFiles(directory="/home/replytim/Desktop/portaldot/frontend"), name="static")

@app.get("/")
async def serve_index():
    """
    Serves the beautiful Lumia Trust Layer dashboard home page.
    """
    return FileResponse("/home/replytim/Desktop/portaldot/frontend/index.html")

class TransactionRequest(BaseModel):
    sender: str = Field(..., description="The sender Substrate address")
    recipient: str = Field(..., description="The recipient Substrate address to scan")
    amount: float = Field(..., description="The transaction amount")
    token: str = Field("POT", description="The token ticker (default: POT)")

class RegisterRequest(BaseModel):
    tx_hash: str = Field(..., description="The Substrate transaction hash")
    risk_score: int = Field(..., description="The risk score computed by Lumia scanner")
    risk_level: str = Field("Low", description="The human-readable risk level")
    ai_briefing: str = Field("", description="The AI security briefing text")

@app.get("/health")
async def health_check():
    """
    Returns API health status and target Substrate RPC network.
    """
    return {
        "status": "online",
        "target_node": PORTALDOT_RPC
    }

@app.post("/scan")
async def scan_transaction(request: TransactionRequest):
    """
    Scans a transaction using Portaldot native pallets and computes an AI safety rating.
    """
    try:
        # Perform native on-chain checks
        scan_results = scanner.scan_address(request.recipient)
        
        # Parse dynamic parameters for LLM briefing
        request_data = {
            "recipient": request.recipient,
            "amount": request.amount,
            "token": request.token
        }
        
        # Generate rich AI safety report
        ai_briefing = risk_engine.generate_briefing(scan_results, request_data)
        
        return {
            "success": True,
            "risk_score": scan_results["risk_score"],
            "risk_level": scan_results["risk_level"],
            "reasons": scan_results["reasons"],
            "recommendation": scan_results["recommendation"],
            "ai_briefing": ai_briefing,
            "onchain_details": scan_results["details"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lumia Scan Failure: {str(e)}"
        )

@app.post("/register")
async def register_receipt(request: RegisterRequest):
    """
    Registers a transaction safety receipt on the custom ink! 5.0 Lumia Registry contract.
    """
    try:
        # We pass additional fields for the fallback storage
        extra_data = {
            "risk_level": request.risk_level,
            "ai_briefing": request.ai_briefing
        }
        receipt = contract_client.register_receipt(request.tx_hash, request.risk_score, extra_data)
        
        # Generate QR code for immediate UI feedback
        qr_code = receipt_generator.generate_qr_base64(request.tx_hash)
        
        return {
            "success": True,
            "receipt": receipt,
            "qr_code_base64": qr_code
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lumia Contract Registry Failure: {str(e)}"
        )

@app.get("/receipt/{tx_hash}")
async def get_receipt(tx_hash: str):
    """
    Retrieves a trust receipt record directly from the Lumia Registry smart contract.
    """
    try:
        result = contract_client.get_receipt(tx_hash)
        if result["success"]:
            # Inject QR code into the result
            result["qr_code_base64"] = receipt_generator.generate_qr_base64(tx_hash)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lumia Registry Query Failure: {str(e)}"
        )

@app.get("/receipt/{tx_hash}/pdf")
async def get_receipt_pdf(tx_hash: str):
    """
    Generates and streams a professional PDF trust certificate for a transaction.
    """
    try:
        result = contract_client.get_receipt(tx_hash)
        if not result["success"]:
            raise HTTPException(status_code=404, detail="Receipt not found")
        
        pdf_bytes = receipt_generator.generate_pdf_bytes(result["receipt"], tx_hash)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=Lumia_Receipt_{tx_hash[:10]}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF Generation Failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
