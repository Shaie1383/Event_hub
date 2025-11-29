<#
PowerShell helper to initialize a git repo and push to GitHub.
Edit the `$remote` variable to your GitHub repo URL before running.

Usage:
  Open PowerShell in the project root and run:
    .\push_to_github.ps1
#>

$remote = 'https://github.com/<your-username>/<your-repo>.git'

Write-Host "Initializing Git repository and preparing initial commit..."

if (-not (Test-Path -Path .git)) {
    git init
}

git add .
git commit -m "chore: initial commit - consolidated README and deployment files" --allow-empty

# Create main branch if not present
git branch -M main

Write-Host "Setting remote to $remote"
git remote remove origin -ErrorAction SilentlyContinue
git remote add origin $remote

Write-Host "Pushing to GitHub (main)..."
git push -u origin main

Write-Host "Done. If push fails, ensure your repo URL is correct and you have permission."
