# GitHub setup

Create a new public repository named:

`snapsign-ai`

Then from this folder:

```powershell
git init
git add .
git commit -m "Initial SnapSign AI prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/snapsign-ai.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

Before publishing:

- remove any private images/videos
- do not commit `.venv/`
- do not commit secrets/API keys
- review third-party model licenses
- add actual benchmark results only after hardware testing
