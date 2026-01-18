# 🚀 GitHub Setup Instructions for ShadowRecon

## Creating Your GitHub Repository

Follow these steps to upload ShadowRecon to GitHub:

### Step 1: Create a New Repository on GitHub

1. Go to [GitHub.com](https://github.com) and log in to your account
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `ShadowRecon`
4. Description: `Advanced OSINT Framework - Professional-grade Open Source Intelligence`
5. **Select Public or Private** (Public recommended for sharing)
6. **DO NOT** initialize with README, .gitignore, or license (we have them)
7. Click **Create repository**

### Step 2: Initialize Local Git Repository

If you haven't already, run the automated setup script:

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**Windows (Command Prompt):**
```cmd
setup.bat
```

**macOS/Linux:**
```bash
bash setup.sh
```

This automatically initializes Git and creates a `.env` file.

### Step 3: Add Remote and Push to GitHub

```bash
# Navigate to project directory
cd ShadowRecon

# Verify Git is initialized
git status

# Add your GitHub repository as remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/ShadowRecon.git

# Alternatively, if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/ShadowRecon.git

# Verify remote was added
git remote -v

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: ShadowRecon OSINT framework

- Automated setup scripts for Windows, macOS, and Linux
- Core OSINT modules for username, domain, IP, and email reconnaissance
- Integration with Shodan, VirusTotal, and HaveIBeenPwned APIs
- Comprehensive reporting and risk scoring system
- Professional logging and audit trails"

# Push to GitHub (main branch)
git branch -M main
git push -u origin main
```

### Step 4: Add GitHub Collaborators (Optional)

1. Go to your repository on GitHub
2. Click **Settings** → **Collaborators** → **Add people**
3. Enter GitHub username of collaborators
4. Select permission level (Pull, Triage, Push, Maintain, or Admin)

### Step 5: Setup GitHub Issues and Projects (Optional)

#### Enable Issues
1. Go to **Settings** → **Features**
2. Check **Issues** checkbox
3. Create issue templates for bug reports and feature requests

#### Create Project Board
1. Click **Projects** tab → **New project**
2. Choose a template (Kanban recommended)
3. Use for tracking development tasks

### Step 6: Add GitHub Workflows (CI/CD)

Create `.github/workflows/tests.yml` for automated testing:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with pylint
      run: |
        pip install pylint
        pylint modules/ --exit-zero
      continue-on-error: true
    
    - name: Run tests
      run: python -m pytest tests/ -v
      continue-on-error: true
```

## Cloning and Using from GitHub

### For Others to Clone Your Repository

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ShadowRecon.git
cd ShadowRecon

# Run automated setup (handles everything automatically)
# On Windows (PowerShell):
.\setup.ps1

# On Windows (Command Prompt):
setup.bat

# On macOS/Linux:
bash setup.sh

# That's it! Virtual environment is created, dependencies installed, and Git initialized.
```

## Git Workflow for Development

### Creating a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create new feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add your feature description"

# Push to GitHub
git push -u origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Keeping Fork Updated (if forked)

```bash
# Add upstream remote
git remote add upstream https://github.com/original-owner/ShadowRecon.git

# Fetch upstream changes
git fetch upstream

# Merge upstream main into local main
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

## GitHub Repository Settings to Configure

### 1. **Branch Protection Rules** (Recommended for team projects)
- Settings → Branches → Add rule
- Apply to: `main`
- Require pull request reviews before merging
- Dismiss stale pull request approvals when new commits are pushed

### 2. **Code Security and Analysis**
- Settings → Code security and analysis
- Enable:
  - Dependabot alerts
  - Dependabot security updates
  - Secret scanning (if private repo)
  - Code scanning with CodeQL

### 3. **Manage Access**
- Settings → Collaborators and teams
- Add team members with appropriate permissions

### 4. **Notifications**
- Settings → Notifications
- Configure who gets notified for issues and pull requests

## Updating Your Repository

### Make Changes Locally

```bash
# Create/edit files
# Then stage and commit

git add .
git commit -m "Descriptive message about changes"
git push origin main
```

### Sync with Main Branch

```bash
# Fetch latest changes
git fetch origin

# Merge or rebase
git rebase origin/main  # or git merge origin/main
```

## Common Git Commands

```bash
# Check status
git status

# View commit history
git log

# View specific file history
git log -- filename.py

# See changes since last commit
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Stash changes (save for later)
git stash

# Apply stashed changes
git stash pop
```

## Troubleshooting

### "Remote already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ShadowRecon.git
```

### "Permission denied (publickey)"
- Make sure you have SSH keys set up: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Or use HTTPS instead of SSH in remote URL

### "Detached HEAD state"
```bash
git checkout main
git pull origin main
```

### "Merge conflicts"
1. Open conflicting files
2. Resolve conflicts (look for `<<<<<<`, `======`, `>>>>>>`)
3. `git add .`
4. `git commit -m "Resolve merge conflicts"`
5. `git push origin branch-name`

## Resources

- [GitHub Documentation](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Push initial code
3. ✅ Setup branch protection and security
4. ✅ Add collaborators
5. ✅ Configure CI/CD workflows
6. ✅ Start development!

---

**Happy coding! 🚀**
