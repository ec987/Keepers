# Fishing rules app

Setup (about 10 minutes, all in the GitHub website):
1. Create a new public repository (for example `fishing-rules`).
2. Upload everything from this folder. The `.github/workflows/snapshot.yml` file must keep that exact path. If your computer hides the `.github` folder, use Add file > Create new file, type `.github/workflows/snapshot.yml`, and paste the contents.
3. Settings > Pages > Build and deployment > Deploy from a branch > `main` / root > Save. Your page appears at `https://<your-username>.github.io/fishing-rules/` after a minute or two.
4. Actions tab > "snapshot-sources" > Run workflow. When it finishes, open `data/status.json` in the repo. Every source should say `"ok": true`. Send me that file's contents.

What this does: once a day it saves a copy of each source page and map layer into `data/raw/`. Git history then shows exactly what changed and when, which is the review trail for rule changes. It does not yet turn the pages into rules; that is the next step.
