# 🚀 How to Push ShadowRecon to GitHub

Your local repository is now initialized and ready! Follow these steps to push to GitHub:

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `ShadowRecon` (or your preferred name)
3. **Description**: "Advanced OSINT Framework - Professional intelligence gathering tool"
4. **Privacy**: Choose `Public` or `Private`
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

## Step 2: Add Remote and Push

After creating the repository on GitHub, you'll see commands. Run these in your PowerShell:

```powershell
cd "c:\Users\anton\OneDrive\Documents\osint tool\ShadowRecon"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ShadowRecon.git
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username.**

## Step 3: Authenticate

If you haven't authenticated yet, GitHub will prompt you:
- Use your GitHub username
- Create a **Personal Access Token** (PAT) instead of password:
  1. Go to https://github.com/settings/tokens
  2. Click "Generate new token (classic)"
  3. Select scopes: `repo`, `write:repo_hook`
  4. Copy the token
  5. Paste as password when prompted

## Step 4: Verify

Once pushed, verify on GitHub:

```powershell
git remote -v
# Should show: origin https://github.com/YOUR_USERNAME/ShadowRecon.git
```

## ✅ Your Repository is Now on GitHub!

You can:
- ✅ Access it at `https://github.com/YOUR_USERNAME/ShadowRecon`
- ✅ Share the link with others
- ✅ Make it part of your portfolio
- ✅ Continue development with version control

---

## 📊 What's Currently in Your Repository

- **23 files** including all source code and documentation
- **6,469 lines** of code and documentation
- **Commit hash**: `0bff3df`
- **Branch**: `main`
- **.gitignore**: Protects `.env` and sensitive files

---

## 🔄 Future Updates

After making changes locally:

```powershell
cd "c:\Users\anton\OneDrive\Documents\osint tool\ShadowRecon"

# Make your changes...

# Stage changes
git add .

# Commit
git commit -m "Your commit message"

# Push to GitHub
git push origin main
```

---

## 📝 Optional: Add README Badge

If you want to add a badge to your GitHub README, GitHub will auto-generate it.

---

## 🆘 Troubleshooting

### "remote: Repository not found"
- Verify you created the repo on GitHub
- Check your username spelling
- Ensure repo is not private (if using HTTPS)

### "Permission denied (publickey)"
- Use HTTPS instead of SSH
- Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### "fatal: 'origin' does not appear to be a 'git' repository"
- You might be in wrong directory
- Verify: `git remote -v` shows origin

---

## 📌 Key Files Now Version Controlled

✅ All Python code (main.py, modules/, report/)  
✅ All documentation (README.md, SETUP.md, etc.)  
✅ Configuration files (config.py, requirements.txt)  
✅ .gitignore (protects .env and scans/)  

❌ NOT tracked (as intended):
- .env (secrets protected)
- scans/ (local reports)
- __pycache__/ (Python cache)

---

## 🎉 Ready!

Your ShadowRecon framework is now set up for GitHub collaboration and version control!

**Next**: Push to GitHub using the commands in Step 2 above.
