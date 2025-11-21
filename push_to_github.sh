#!/bin/bash

##############################################################################
# GitHub Repository Setup Script
# This script will help you create and push to GitHub
##############################################################################

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║              🚀 GitHub Repository Setup 🚀                         ║"
echo "║                                                                    ║"
echo "║                     IPTrack Security Tool                          ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}This script will help you push IPTrack to GitHub${NC}"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${RED}Error: Git not initialized. Run: git init${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Git repository initialized${NC}"
echo ""

# Get GitHub username
echo -e "${YELLOW}Enter your GitHub username:${NC}"
read -p "> " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}Error: GitHub username is required${NC}"
    exit 1
fi

# Get repository name
echo ""
echo -e "${YELLOW}Enter repository name (default: iptrack):${NC}"
read -p "> " REPO_NAME
REPO_NAME=${REPO_NAME:-iptrack}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Repository Details:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "GitHub Username: ${GREEN}$GITHUB_USER${NC}"
echo -e "Repository Name: ${GREEN}$REPO_NAME${NC}"
echo -e "Repository URL:  ${GREEN}https://github.com/$GITHUB_USER/$REPO_NAME${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Confirm
echo -e "${YELLOW}Is this correct? (y/n)${NC}"
read -p "> " CONFIRM

if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo -e "${RED}Cancelled${NC}"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Step 1: Create GitHub Repository${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Please create a new repository on GitHub:"
echo ""
echo -e "1. Go to: ${GREEN}https://github.com/new${NC}"
echo -e "2. Repository name: ${GREEN}$REPO_NAME${NC}"
echo -e "3. Description: ${GREEN}Professional CLI security monitoring and IP blocking tool with real-time alerts${NC}"
echo "4. Make it Public (or Private if you prefer)"
echo "5. Do NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
echo -e "${YELLOW}Press Enter after creating the repository on GitHub...${NC}"
read

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Step 2: Configure Git${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Set up git config if not already set
if [ -z "$(git config user.name)" ]; then
    echo -e "${YELLOW}Enter your name for git commits:${NC}"
    read -p "> " GIT_NAME
    git config user.name "$GIT_NAME"
fi

if [ -z "$(git config user.email)" ]; then
    echo -e "${YELLOW}Enter your email for git commits:${NC}"
    read -p "> " GIT_EMAIL
    git config user.email "$GIT_EMAIL"
fi

echo -e "${GREEN}✓ Git configured${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Step 3: Add Remote and Push${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Add remote
REMOTE_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo -e "${BLUE}Adding remote: $REMOTE_URL${NC}"

git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE_URL"

echo -e "${GREEN}✓ Remote added${NC}"
echo ""

# Rename branch to main if needed
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${BLUE}Renaming branch to main...${NC}"
    git branch -M main
    echo -e "${GREEN}✓ Branch renamed to main${NC}"
fi

echo ""
echo -e "${BLUE}Pushing to GitHub...${NC}"
echo ""

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                    ║"
    echo "║                  ✅ Successfully Pushed to GitHub! ✅              ║"
    echo "║                                                                    ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${GREEN}Your repository is now live at:${NC}"
    echo -e "${BLUE}https://github.com/$GITHUB_USER/$REPO_NAME${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Visit your repository on GitHub"
    echo "  2. Add topics: security, monitoring, cli, python, firewall"
    echo "  3. Add a description"
    echo "  4. Share with others!"
    echo ""
    echo "To update later:"
    echo "  git add ."
    echo "  git commit -m 'Your update message'"
    echo "  git push"
    echo ""
else
    echo ""
    echo -e "${RED}Error: Failed to push to GitHub${NC}"
    echo ""
    echo "Please check:"
    echo "  1. Repository exists on GitHub"
    echo "  2. You have permissions"
    echo "  3. You're logged in (use gh CLI or SSH keys)"
    echo ""
    echo "Alternative: Use SSH URL"
    echo "  git remote set-url origin git@github.com:$GITHUB_USER/$REPO_NAME.git"
    echo "  git push -u origin main"
    echo ""
fi
