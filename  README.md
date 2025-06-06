# Scytale GitHub PR Analyzer

## Description
This project is a Python-based script developed for the Scytale Junior Data Engineer home assignment. The script integrates with the GitHub API to fetch merged pull requests (PRs) from a specific repository, analyzes them for compliance, and generates a summary report.

The primary goal is to ensure that merged PRs have passed the required review and status checks before being integrated into the main branch.

---

## Core Features
- **GitHub Authentication**: Securely authenticates with the GitHub API using a Personal Access Token (PAT).
- **Data Extraction**: Fetches all merged pull requests from the `Scytale-exercise/dev-interviews` repository.
- **Compliance Analysis**: For each merged PR, the script checks:
    - **Code Review (`CR_Passed`)**: Was the PR approved by at least one reviewer?
    - **Status Checks (`CHECKS_PASSED`)**: Did all the required status checks for the head commit pass successfully?
- **Reporting**: Generates a final report in CSV format detailing the compliance status of each PR.
- **Modular Structure**: The code is logically separated into two main components:
    - `extract.py`: Responsible for fetching raw data from the API.
    - `transform.py`: Responsible for processing, analyzing, and reporting the data.

---

## Project Structure
```
scytale_ex/
├── .env                  # For storing the GitHub PAT (not committed)
├── .gitignore            # Specifies files to be ignored by Git
├── requirements.txt      # Lists project dependencies
├── main.py               # Main script to orchestrate the ETL process
├── README.md             # This file
│
├── src/
│   ├── __init__.py       # Makes 'src' a Python package
│   ├── extract.py        # Data extraction logic
│   └── transform.py      # Data transformation and analysis logic
│
└── outputs/              # (Generated on runtime, not committed)
    ├── raw/
    │   └── pull_requests.json
    └── processed/
        └── pr_report.csv
```

---

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites
- Python 3.8 or higher.
- A GitHub account.

### 2. Clone the Repository
```bash
git clone <your-repository-url>
cd scytale_github_analyzer
```

### 3. Create a GitHub Personal Access Token (PAT)
The script requires a PAT to access the GitHub API.
- Go to **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
- Click **Generate new token**.
- Give it a name (e.g., `scytale-assignment-token`) and select the `repo` scope.
- **Copy the generated token immediately.** You will not be able to see it again.

### 4. Set Up Environment
- **Create a virtual environment:**
  ```bash
  python -m venv venv
  ```
- **Activate the environment:**
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
  - On Windows:
    ```bash
    .\venv\Scripts\activate
    ```

- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

### 5. Configure Environment Variables
- Create a file named `.env` in the root directory of the project.
- Add your GitHub PAT to the `.env` file as follows:
  ```
  GITHUB_PAT="paste_your_personal_access_token_here"
  ```
  The `.gitignore` file is configured to prevent this file from being committed.

---

## How to Run
Once the setup is complete, run the main script from the root directory:
```bash
python main.py
```
The script will print its progress to the console, from fetching the data to generating the final report.

---

## Output
The script generates two primary outputs inside the `outputs/` directory:

1.  **Raw Data (`outputs/raw/pull_requests.json`)**: A JSON file containing the raw, unfiltered data for all merged pull requests fetched from the API.
2.  **Processed Report (`outputs/processed/pr_report.csv`)**: A CSV file containing the final analysis with the following columns:
    - `pr_number`: The pull request number.
    - `pr_title`: The title of the pull request.
    - `author`: The GitHub username of the PR author.
    - `merge_date`: The timestamp when the PR was merged.
    - `CR_Passed`: `True` if the PR received at least one approval, otherwise `False`.
    - `CHECKS_PASSED`: `True` if the head commit's status checks were successful, otherwise `False`.