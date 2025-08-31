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

Installation & Run Instructions (Windows)
These steps assume you have Python 3.11+ installed on Windows and git available in PowerShell.
1. Clone the Repository
Open PowerShell and run:
    cd C:\Users\baise\Documents\Python_Projects
    git clone https://github.com/BaisenSu/python_linux_test_platform.git
    cd python_linux_test_platform

2. Create a Virtual Environment
    python -m venv .venv

3. Activate the Virtual Environment
In PowerShell:
    .\.venv\Scripts\Activate
    ⚠ If you see “running scripts is disabled on this system”:
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Then re-run the activate command above.

4. Install Dependencies
    pip install -U pip
    pip install -r requirements.txt
If no requirements.txt is present, install manually:
    pip install pytest rich pyserial paramiko

5. Run Tests (Optional)
To confirm setup:
    pytest -q
You should see all tests PASS.

6. Run the Project
Depending on what you want to try:
Run the Diagnostic Shell:
    python -m test_framework.shell_cli
    Run the Test Runner:
python -m test_framework.runner_cli
Both commands launch interactive CLI tools for testing the framework.

7. Notes for Windows Users
    Serial Ports:
        Linux uses /dev/ttyUSB0.
        On Windows, use COM3, COM4, etc. Update configs accordingly.
    SSH Mode:
        Requires paramiko (already installed). Make sure you have network access to the target.
    Mock Mode:
        Use mode="mock" in SerialTalker if you want to run without real hardware.

Example (inside Python shell):
    from test_framework.serial_talker import SerialTalker
    talker = SerialTalker(mode="mock")
    print(talker.read_voltage())

Installation & Run Instructions (WSL / Linux)
These steps assume you have Python 3.11+ installed in WSL (Ubuntu).
1. Clone the Repository
Open your WSL terminal:
    cd ~/projects
    git clone https://github.com/BaisenSu/python_linux_test_platform.git
    cd python_linux_test_platform

2. Create a Virtual Environment
    python3 -m venv .venv

3. Activate the Virtual Environment
    source .venv/bin/activate
If successful, your prompt will change to:
    (.venv) baise@machine:~/projects/python_linux_test_platform$

4. Install Dependencies
    pip install -U pip
    pip install -r requirements.txt
If requirements.txt is missing:
    pip install pytest rich pyserial paramiko

5. Run Tests (Optional)
Verify everything works:
    pytest -q
You should see all tests PASS.

6. Run the Project
Launch tools from the repo root:
Diagnostic Shell
    python -m test_framework.shell_cli
Test Runner
    python -m test_framework.runner_cli

7. Notes for WSL/Linux Users

Serial Ports:
    Devices show up as /dev/ttyUSB0, /dev/ttyS0, etc.
    Make sure your user has access to serial devices (may need sudo usermod -a -G dialout $USER and re-login).

SSH Mode:
    Works directly with paramiko.

Mock Mode:
    Use mode="mock" in SerialTalker to run tests without hardware.

Example:

from test_framework.serial_talker import SerialTalker
talker = SerialTalker(mode="mock")
print(talker.read_voltage())


✅ That’s all — WSL/Linux setup is ready.

👉 Now you can see the symmetry:
    Windows: .\.venv\Scripts\Activate
    Linux/WSL: source .venv/bin/activate
    Everything else (clone → pip install → pytest → run CLI) is almost identical.














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

2. Stage changes
Add updated or new files to the next commit:
    git add .
(. means all changes; or use git add file.py for specific files.)

3. Commit changes
Save a snapshot with a message:
    git commit -m "Describe what you changed here"

4. Make sure you have a remote (origin)
Check:
    git remote -v
You should see:
    origin  https://github.com/BaisenSu/python_linux_test_platform.git (fetch)
    origin  https://github.com/BaisenSu/python_linux_test_platform.git (push)
If not, add it:
    git remote add origin https://github.com/BaisenSu/python_linux_test_platform.git

5. Push to GitHub
Push your branch to GitHub:
    git push origin main
(If it’s the first push from this repo/branch, you may need -u once:)
    git push -u origin main

6. Confirm on GitHub
Go to your repo page:
    https://github.com/BaisenSu/python_linux_test_platform
You should see your changes reflected.

7. Typical Daily Workflow
When you’ve done work and want to sync:
    git status
    git add .
    git commit -m "Fix test runner bug"
    git push

8. Extra: 
To bring down changes from GitHub:
    git pull origin main
To see commit history:
    git log --oneline --graph --decorate