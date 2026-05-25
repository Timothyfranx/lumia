// ==========================================
// LUMIA Protocol - Dashboard Logic (ES6)
// Handles API calls, dynamic UI, and animations
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const scanForm = document.getElementById("scan-form");
    const recipientInput = document.getElementById("recipient-address");
    const amountInput = document.getElementById("tx-amount");
    const btnScan = document.getElementById("btn-scan");
    
    // Progress Steps
    const scanProgress = document.getElementById("scan-progress");
    const stepConnect = document.getElementById("step-connect");
    const stepIdentity = document.getElementById("step-identity");
    const stepSystem = document.getElementById("step-system");
    const stepAi = document.getElementById("step-ai");
    
    // Result Elements
    const resultContainer = document.getElementById("result-container");
    const emptyStateMsg = document.getElementById("empty-state-msg");
    const resultPanel = document.getElementById("result-panel");
    const riskLevelBadge = document.getElementById("risk-level-badge");
    const riskScoreVal = document.getElementById("risk-score-val");
    const reasonsList = document.getElementById("reasons-list");
    const aiBriefingText = document.getElementById("ai-briefing-text");
    
    // Gas Telemetry
    const valWeight = document.getElementById("val-weight");
    const valFee = document.getElementById("val-fee");
    const valDeposit = document.getElementById("val-deposit");
    
    // Registry Elements
    const btnRegister = document.getElementById("btn-register");
    const searchInput = document.getElementById("search-tx-hash");
    const btnSearchReceipt = document.getElementById("btn-search-receipt");
    const registryResult = document.getElementById("registry-result");

    // State Variables
    let currentScanResult = null;
    let currentTxHash = null;

    // --- Helper: Format Helper for Steps ---
    const updateStep = (element, status, text = null) => {
        const icon = element.querySelector("i");
        if (text) {
            element.querySelector("span").textContent = text;
        }
        
        element.className = `step-item ${status}`;
        
        if (status === "active") {
            icon.className = "fa-solid fa-circle-notch fa-spin step-icon";
        } else if (status === "completed") {
            icon.className = "fa-solid fa-circle-check step-icon";
        } else if (status === "pending") {
            icon.className = "fa-solid fa-circle step-icon";
        } else if (status === "failed") {
            icon.className = "fa-solid fa-circle-xmark step-icon";
            element.style.color = "var(--clr-high)";
        }
    };

    // --- Form Submission / Scanner Handler ---
    scanForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const recipient = recipientInput.value.trim();
        const amount = parseFloat(amountInput.value);
        
        if (!recipient) return;

        // Reset & Show progress UI
        scanProgress.classList.remove("hidden");
        btnScan.disabled = true;
        btnScan.style.opacity = "0.7";
        
        // Initialize step states
        updateStep(stepConnect, "active");
        updateStep(stepIdentity, "pending");
        updateStep(stepSystem, "pending");
        updateStep(stepAi, "pending");
        
        // Hide result panel during new scan
        resultPanel.classList.add("hidden");
        if (emptyStateMsg) emptyStateMsg.classList.remove("hidden");
        resultContainer.className = "result-container empty-state";

        try {
            // STEP 1: Connect RPC
            await new Promise(resolve => setTimeout(resolve, 800));
            updateStep(stepConnect, "completed", "Substrate RPC Handshake Established");
            updateStep(stepIdentity, "active");

            // STEP 2: Identity Pallet
            await new Promise(resolve => setTimeout(resolve, 800));
            updateStep(stepIdentity, "completed", "Identity Pallet Audited");
            updateStep(stepSystem, "active");

            // STEP 3: System Pallet
            await new Promise(resolve => setTimeout(resolve, 800));
            updateStep(stepSystem, "completed", "Account Nonce & Age Audited");
            updateStep(stepAi, "active");

            // Fetch Real-time backend scan
            const response = await fetch("/scan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    sender: "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", // Alice
                    recipient: recipient,
                    amount: amount,
                    token: "POT"
                })
            });

            if (!response.ok) {
                throw new Error("Scan request failed");
            }

            const data = await response.json();
            currentScanResult = data;
            
            // STEP 4: AI Completion
            await new Promise(resolve => setTimeout(resolve, 600));
            updateStep(stepAi, "completed", "Groq Llama-3.3 Intelligence Applied");

            // Render Results after a small transition
            await new Promise(resolve => setTimeout(resolve, 400));
            renderScanResults(data);

        } catch (error) {
            console.error("Scan Error:", error);
            updateStep(stepConnect, "failed", "Handshake Interrupted");
            updateStep(stepIdentity, "failed", "Audit Failed");
            updateStep(stepSystem, "failed", "System Query Failed");
            updateStep(stepAi, "failed", "AI Engine Unreachable");
            
            alert("Lumia Scan Failed. Check if FastAPI backend is fully active.");
        } finally {
            btnScan.disabled = false;
            btnScan.style.opacity = "1";
        }
    });

    // --- Render Results UI ---
    function renderScanResults(data) {
        // Hide progress & Empty State
        scanProgress.classList.add("hidden");
        if (emptyStateMsg) emptyStateMsg.classList.add("hidden");
        resultContainer.className = "result-container";
        resultPanel.classList.remove("hidden");
        
        // 1. Set Score & Radial Color
        const score = data.risk_score;
        riskScoreVal.textContent = score;
        
        // Reset container score classes
        const radialContainer = document.querySelector(".radial-score-container");
        radialContainer.style.borderColor = "var(--card-border)";
        
        // 2. Set Risk Badge
        riskLevelBadge.textContent = `${data.risk_level} RISK`;
        riskLevelBadge.className = "badge";
        
        if (data.risk_level.toLowerCase() === "low") {
            riskLevelBadge.classList.add("low");
            radialContainer.style.borderColor = "var(--clr-low)";
            radialContainer.style.boxShadow = "0 0 15px var(--clr-low-glow)";
        } else if (data.risk_level.toLowerCase() === "medium") {
            riskLevelBadge.classList.add("medium");
            radialContainer.style.borderColor = "var(--clr-med)";
            radialContainer.style.boxShadow = "0 0 15px var(--clr-med-glow)";
        } else {
            riskLevelBadge.classList.add("high");
            radialContainer.style.borderColor = "var(--clr-high)";
            radialContainer.style.boxShadow = "0 0 15px var(--clr-high-glow)";
        }

        // 3. Render Heuristic Reasons
        reasonsList.innerHTML = "";
        data.reasons.forEach(reason => {
            const li = document.createElement("li");
            
            // Check if reasons implies positive, warnings, or high risk
            let iconClass = "fa-circle-check";
            let liClass = "ok";
            
            const lowerReason = reason.toLowerCase();
            if (lowerReason.includes("no-chain identity") || lowerReason.includes("no on-chain identity") || lowerReason.includes("zero native")) {
                iconClass = "fa-triangle-exclamation";
                liClass = "warn";
            } else if (lowerReason.includes("brand new") || lowerReason.includes("0 transactions")) {
                iconClass = "fa-circle-xmark";
                liClass = "danger";
            }
            
            li.className = liClass;
            li.innerHTML = `<i class="fa-solid ${iconClass}"></i> <span>${reason}</span>`;
            reasonsList.appendChild(li);
        });

        // 4. Render AI Briefing (clean linebreaks support)
        aiBriefingText.innerHTML = formatMarkdown(data.ai_briefing);

        // 5. Update Telemetry
        updateTelemetry(score);
    }

    // --- Simple Markdown/Emoji formatter ---
    function formatMarkdown(text) {
        // Simple regex replace for markdown list bullet points
        let formatted = text
            .replace(/\n\n/g, "<br/><br/>")
            .replace(/\n/g, "<br/>")
            .replace(/\*\s/g, "• ")
            .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
        return formatted;
    }

    // --- Dynamic Telemetry Update ---
    function updateTelemetry(score) {
        // Base gas fee calculations
        const baseWeight = 205000000;
        const variableWeight = score * 500000;
        const totalWeight = baseWeight + variableWeight;
        const totalFee = (totalWeight / 50000000000).toFixed(5);
        
        valWeight.textContent = totalWeight.toLocaleString();
        valFee.textContent = `${totalFee} POT`;
        
        // Fill indicator
        const fillPercent = Math.min(100, Math.max(10, score));
        document.querySelector(".gas-fill").style.width = `${fillPercent}%`;
    }

    // --- Register Trust Receipt ---
    btnRegister.addEventListener("click", async () => {
        if (!currentScanResult) return;

        btnRegister.disabled = true;
        btnRegister.style.opacity = "0.7";
        btnRegister.querySelector("span").textContent = "Registering...";

        // Generate a valid mock hash
        const buffer = new Uint32Array(8);
        window.crypto.getRandomValues(buffer);
        const generatedHash = "0x" + Array.from(buffer, val => val.toString(16).padStart(8, '0')).join('');
        currentTxHash = generatedHash;

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    tx_hash: generatedHash,
                    risk_score: currentScanResult.risk_score
                })
            });

            if (!response.ok) throw new Error("Registry failed");

            const data = await response.json();
            
            // Show feedback
            btnRegister.querySelector("span").textContent = "Receipt Registered! View in Ledger";
            btnRegister.className = "btn-secondary completed";
            btnRegister.querySelector("i").className = "fa-solid fa-circle-check";
            btnRegister.style.color = "var(--clr-low)";
            btnRegister.style.border = "1px solid var(--clr-low)";
            
            // Allow clicking to switch to Ledger page and search automatically
            btnRegister.disabled = false;
            btnRegister.style.opacity = "1";
            btnRegister.onclick = (e) => {
                e.preventDefault();
                // Switch tab to Ledger
                const ledgerTabBtn = document.querySelector('.nav-btn[data-page="ledger"]');
                if (ledgerTabBtn) ledgerTabBtn.click();
                // Query immediately
                btnSearchReceipt.click();
            };

            // Auto-populate search box for verification demonstration
            searchInput.value = generatedHash;
            
            // Display receipt details in registry instantly
            displayRegistryReceipt(data.receipt);

        } catch (error) {
            console.error("Registry error:", error);
            alert("Could not register receipt on-chain.");
            btnRegister.disabled = false;
            btnRegister.style.opacity = "1";
            btnRegister.querySelector("span").textContent = "Register Trust Receipt";
        }
    });

    // --- Search Smart Contract Receipt ---
    btnSearchReceipt.addEventListener("click", async () => {
        const hash = searchInput.value.trim();
        if (!hash) return;

        registryResult.innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <i class="fa-solid fa-circle-notch fa-spin" style="font-size: 24px; color: var(--brand-clr);"></i>
                <p style="margin-top: 8px; font-size: 13px; color: var(--text-secondary);">Querying Lumia Registry Smart Contract...</p>
            </div>
        `;

        try {
            const response = await fetch(`/receipt/${hash}`);
            if (!response.ok) throw new Error("Query failed");

            const data = await response.json();
            if (data.success) {
                displayRegistryReceipt(data.receipt, hash);
            } else {
                registryResult.innerHTML = `
                    <div class="registry-result-details">
                        <span class="not-found-msg"><i class="fa-solid fa-triangle-exclamation"></i> Receipt Not Found</span>
                        <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Hash is not registered on the ink! 5.0 smart contract ledger.</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error("Query registry error:", error);
            registryResult.innerHTML = `
                <div class="registry-result-details">
                    <span class="not-found-msg"><i class="fa-solid fa-circle-xmark"></i> Connection Error</span>
                    <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Failed to interface with Lumia Registry server.</p>
                </div>
            `;
        }
    });

    function displayRegistryReceipt(receipt, hashVal = null) {
        const displayHash = hashVal || currentTxHash || "0x...";
        
        registryResult.innerHTML = `
            <div class="registry-result-details">
                <div class="success-msg" style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <i class="fa-solid fa-certificate"></i>
                    <span>VERIFIED TRUST RECEIPT</span>
                </div>
                
                <div class="registry-result-row">
                    <span>Transaction Hash:</span>
                    <span class="hash-val" style="font-size: 11px;">${displayHash.substring(0, 16)}...${displayHash.substring(displayHash.length - 12)}</span>
                </div>
                
                <div class="registry-result-row">
                    <span>Scanner Admin ID:</span>
                    <span class="hash-val" style="font-size: 11px;">${receipt.scanner_id.substring(0, 10)}...${receipt.scanner_id.substring(receipt.scanner_id.length - 8)}</span>
                </div>
                
                <div class="registry-result-row">
                    <span>Risk Score:</span>
                    <span style="font-weight: 700; color: ${receipt.risk_score > 70 ? 'var(--clr-high)' : receipt.risk_score > 30 ? 'var(--clr-med)' : 'var(--clr-low)'}">${receipt.risk_score}/100</span>
                </div>
                
                <div class="registry-result-row">
                    <span>Registry Proof:</span>
                    <span style="color: #a78bfa; font-weight: 600;">${receipt.onchain ? '🟢 ON-CHAIN CONTRACT (API v9+)' : '🛡️ HYBRID LEDGER (Fallback)'}</span>
                </div>
                
                <div class="registry-result-row" style="border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 8px; margin-top: 4px;">
                    <span>Signed Timestamp:</span>
                    <span style="font-size: 11px; color: var(--text-secondary);">${receipt.timestamp_readable || new Date(receipt.timestamp * 1000).toUTCString()}</span>
                </div>
            </div>
        `;
    }

    // --- Navigation Tabs switching ---
    const navButtons = document.querySelectorAll(".nav-btn");
    const pageContainers = document.querySelectorAll(".page-container");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const pageId = btn.getAttribute("data-page");
            
            // Toggle buttons active state
            navButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // Toggle pages visibility natively with CSS transitions (smooth fade/slide)
            pageContainers.forEach(container => {
                if (container.id === `page-${pageId}`) {
                    container.classList.add("active");
                    // Force browser reflow to trigger the smooth CSS opacity transition
                    container.offsetHeight;
                    container.classList.add("fade-in");
                } else {
                    container.classList.remove("fade-in");
                    container.classList.remove("active");
                }
            });
        });
    });
});
