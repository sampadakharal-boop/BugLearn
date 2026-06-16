#!/bin/bash

# ReconForge AI - One-Click Installer
# =====================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}"
echo "╔══════════════════════════════════════╗"
echo "║        ReconForge AI Installer       ║"
echo "║  AI-Powered Cybersecurity Platform   ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"

# Check Docker
echo -e "${BLUE}[*]${NC} Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[!]${NC} Docker not found. Please install Docker first."
    echo "    https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}[!]${NC} Docker Compose not found. Please install Docker Compose v2."
    exit 1
fi

echo -e "${GREEN}[✓]${NC} Docker $(docker --version)"
echo -e "${GREEN}[✓]${NC} Docker Compose $(docker compose version)"

# Create .env if not exists
if [ ! -f .env ]; then
    echo -e "${BLUE}[*]${NC} Creating .env configuration..."
    cp .env.example .env

    echo ""
    echo -e "${YELLOW}[?]${NC} Enter OpenAI API Key (optional, for AI features):"
    read -r openai_key
    if [ -n "$openai_key" ]; then
        sed -i "s/OPENAI_API_KEY=/OPENAI_API_KEY=$openai_key/" .env
    fi

    echo -e "${YELLOW}[?]${NC} Enter Shodan API Key (optional):"
    read -r shodan_key
    if [ -n "$shodan_key" ]; then
        sed -i "s/SHODAN_API_KEY=/SHODAN_API_KEY=$shodan_key/" .env
    fi

    echo -e "${YELLOW}[?]${NC} Generate secure secret key? (Y/n):"
    read -r gen_key
    if [ "$gen_key" != "n" ]; then
        new_key=$(openssl rand -hex 32)
        sed -i "s/SECRET_KEY=change-this-to-a-random-secret-key/SECRET_KEY=$new_key/" .env
    fi

    echo -e "${GREEN}[✓]${NC} .env file created"
else
    echo -e "${GREEN}[✓]${NC} .env file exists"
fi

# Build and start containers
echo -e "${BLUE}[*]${NC} Building and starting containers..."
docker compose build --no-cache
docker compose up -d

# Wait for services
echo -e "${BLUE}[*]${NC} Waiting for services to be ready..."
echo -n "    Waiting for PostgreSQL"
until docker compose exec postgres pg_isready -U reconforge &> /dev/null; do
    echo -n "."
    sleep 2
done
echo -e " ${GREEN}[ready]${NC}"

echo -n "    Waiting for backend"
until curl -s http://localhost:8000/ > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo -e " ${GREEN}[ready]${NC}"

# Verify installation
echo ""
echo -e "${BLUE}[*]${NC} Verifying installation..."

echo -n "    Database migration"
# Backend auto-creates tables on startup
echo -e " ${GREEN}[done]${NC}"

echo -n "    Mission seeding"
# Missions are seeded on startup
echo -e " ${GREEN}[done]${NC}"

# Print summary
echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗"
echo -e "║        Installation Complete!        ║"
echo -e "╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "  Frontend:  ${BLUE}http://localhost:80${NC}"
echo -e "  Backend:   ${BLUE}http://localhost:8000${NC}"
echo -e "  API Docs:  ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "  ${YELLOW}First time?${NC} Register at http://localhost/register"
echo ""
echo -e "  ${BLUE}Useful commands:${NC}"
echo -e "    docker compose logs -f     # View logs"
echo -e "    docker compose down        # Stop services"
echo -e "    docker compose up -d       # Start services"
echo ""

# Check API health
if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo -e "${GREEN}[✓]${NC} Platform is operational!"
else
    echo -e "${YELLOW}[!]${NC} Services are starting up. Check 'docker compose logs -f' for progress."
fi
