📘 About Git & GitHub Workflow
This project uses Git for version control and GitHub as the remote (origin).
All development should happen on local clones, with changes pushed via branches and Pull Requests (PRs).

Key Concepts:
Repository (Repo): The database of project history (local or on GitHub).
Clone: A full local copy of the repo.
Commit: A saved snapshot of changes.
Branch: A separate line of development (e.g., feature/new-cli).
Remote (origin): The GitHub copy of the repo.
Push / Pull: Sync changes to/from GitHub.
Pull Request (PR): The review/merge step from branch → main.

How Git/GitHub is normally used:
1. Code lives in GitHub → but that’s just the remote copy (the “origin”).
    You normally don’t edit code directly in the GitHub website (except for tiny fixes).
2.  You work on a local clone (on Windows, WSL, or any machine).
    This clone is a full Git repo with history.
    You make changes, commit them, and test locally.
3. When ready, push to GitHub
    "git push" sends your commits to the remote repo (origin).
    Now GitHub is updated and teammates (or your other machines) can pull it.
4. If others (or you, on another computer) push changes
    You bring them down with "git pull".

Professional workflow:
    Each developer works on their own clone.
    Work is organized on branches (e.g., feature-x, fix-bug).
    When a feature is done → push branch → open a Pull Request on GitHub → review → merge into main.

Commit Style:
Use semantic prefixes:
    feat: → new feature
    fix: → bug fix
    docs: → documentation
    test: → tests only
    refactor: → code restructure
    ci: → CI/CD updates

once you’ve cloned the repo from origin (GitHub) onto a machine (Windows or WSL), 
running it is basically the same process:
After cloning from GitHub (Origin)
1. Clone the repo
(Only once per machine, not every time)
# Windows PowerShell
git clone https://github.com/BaisenSu/python_linux_test_platform.git
cd python_linux_test_platform
# WSL/Linux
git clone https://github.com/BaisenSu/python_linux_test_platform.git
cd python_linux_test_platform

2. Create virtual environment (once per machine)
# Windows
python -m venv .venv
# WSL/Linux
python3 -m venv .venv

3. Activate venv (every session)
# Windows
.\.venv\Scripts\Activate
# WSL/Linux
source .venv/bin/activate

4. Install dependencies (once, or after updates)
pip install -r requirements.txt

5. Run tests (optional)
    pytest -q

6. Run the project

From repo root:

# Windows
python -m test_framework.shell_cli
python -m test_framework.runner_cli

# WSL/Linux
python -m test_framework.shell_cli
python -m test_framework.runner_cli

Daily routine after reopening
When you open the project later:
    cd python_linux_test_platform
    .\.venv\Scripts\Activate   # (Windows)
    # OR
    source .venv/bin/activate  # (WSL/Linux)

    python -m test_framework.shell_cli

That’s it. No need to repeat cloning, venv creation, or pip install unless dependencies change.

Steps to Push Project to GitHub:
1. Make sure you’re inside your project
    cd path/to/python_linux_test_platform
Check you’re in a Git repo:
    git status
If it shows “not a git repository” → run git init and connect to GitHub (see step 3).