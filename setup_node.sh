#!/usr/bin/env bash

# Portaldot Automated Local Node Setup & Runner Script
# Designed for the Portaldot Online Mini Hackathon (Season 1)
# Simply run this script in your terminal to manage your node environment.

set -euo pipefail

# Harmonized styling tokens
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${PURPLE}======================================================${NC}"
echo -e "${CYAN}   🟣 PORTALDOT AUTOMATED LOCAL NODE RUNNER & CLEANER ${NC}"
echo -e "${PURPLE}======================================================${NC}"

# Verification of OS compatibility (Target: Ubuntu / Linux systems)
OS_TYPE=$(uname)
if [ "$OS_TYPE" != "Linux" ]; then
    echo -e "${RED}[WARNING] Portaldot node binary is compiled for x86_64 Ubuntu Linux.${NC}"
    echo -e "If you are on macOS or Windows (without WSL2), please use GitHub Codespaces."
    echo ""
fi

# Ensure temporary dirs exist
mkdir -p /tmp/alice /tmp/bob

# Main control loop
while true; do
    echo -e "\n${BLUE}Select an operation:${NC}"
    echo -e "  1) ${GREEN}Download & Extract Node Binary${NC} (if not already fetched)"
    echo -e "  2) ${GREEN}Run Alice (Bootnode / Port 9944)${NC}"
    echo -e "  3) ${GREEN}Run Bob (Peer / Port 9945)${NC}"
    echo -e "  4) ${CYAN}Kill Dangling Node Processes${NC} (Fixes 'Address already in use')"
    echo -e "  5) ${CYAN}Clear Databases & LOCK Files${NC} (Fixes 'LOCK: Resource unavailable')"
    echo -e "  6) Exit"
    echo -ne "Enter choice [1-6]: "
    read -r choice

    case $choice in
        1)
            echo -e "\n${BLUE}[*] Downloading portaldot-testnet-ubuntu.tar.gz...${NC}"
            if wget -q --show-progress https://github.com/portaldotVolunteer/Portaldot-node/raw/main/portaldot-testnet-ubuntu.tar.gz; then
                echo -e "${GREEN}[✓] Download successful. Extracting...${NC}"
                tar -xzvf portaldot-testnet-ubuntu.tar.gz
                chmod +x portaldot_dev
                echo -e "${GREEN}[✓] Setup complete! 'portaldot_dev' binary is ready.${NC}"
            else
                echo -e "${RED}[ERROR] Failed to download binary. Check internet connection or GitHub status.${NC}"
            fi
            ;;
        2)
            if [ ! -f "./portaldot_dev" ]; then
                echo -e "${RED}[ERROR] portaldot_dev binary not found. Please run Option 1 first.${NC}"
                continue
            fi
            echo -ne "Enter your custom node name (e.g. your username): "
            read -r node_name
            if [ -z "$node_name" ]; then
                node_name="developer"
            fi
            echo -e "\n${GREEN}[✓] Launching Alice node... Connect via ws://127.0.0.1:9944${NC}"
            echo -e "${CYAN}Press Ctrl+C to terminate the node.${NC}\n"
            ./portaldot_dev --dev --alice --name "$node_name" --base-path /tmp/alice
            ;;
        3)
            if [ ! -f "./portaldot_dev" ]; then
                echo -e "${RED}[ERROR] portaldot_dev binary not found. Please run Option 1 first.${NC}"
                continue
            fi
            echo -ne "Enter Alice's Peer ID from logs: "
            read -r peer_id
            if [ -z "$peer_id" ]; then
                echo -e "${RED}[ERROR] Peer ID cannot be empty. Alice must be running to establish connection.${NC}"
                continue
            fi
            echo -ne "Enter your custom node name for Bob: "
            read -r bob_name
            if [ -z "$bob_name" ]; then
                bob_name="developer_bob"
            fi
            echo -e "\n${GREEN}[✓] Launching Bob node connecting to Alice... RPC port: 9945${NC}"
            echo -e "${CYAN}Press Ctrl+C to terminate the node.${NC}\n"
            ./portaldot_dev --dev --bob --name "$bob_name" \
              --base-path /tmp/bob \
              --port 30334 \
              --rpc-port 9945 \
              --bootnodes "/ip4/127.0.0.1/tcp/30333/p2p/$peer_id"
            ;;
        4)
            echo -e "\n${BLUE}[*] Terminating any dangling portaldot_dev processes...${NC}"
            pkill portaldot_dev || true
            echo -e "${GREEN}[✓] Processes terminated successfully.${NC}"
            ;;
        5)
            echo -e "\n${BLUE}[*] Resetting databases and clearing lock files...${NC}"
            rm -rf /tmp/alice/chains/dev/db/LOCK /tmp/bob/chains/dev/db/LOCK || true
            echo -e "${GREEN}[✓] DB Lock files cleared. Database is unlocked.${NC}"
            ;;
        6)
            echo -e "\n${GREEN}Thank you for building on Portaldot! Good luck with the Hackathon! 🚀${NC}"
            break
            ;;
        *)
            echo -e "${RED}[ERROR] Invalid option. Enter 1-6.${NC}"
            ;;
    esac
done
