# Scytale GitHub PR Analyzer

## Description
This project is a Python-based script developed for the Scytale Junior Data Engineer home assignment. The script integrates with the GitHub API to fetch merged pull requests (PRs) from a specific repository, analyzes them for compliance, and generates a summary report.

The primary goal is to ensure that merged PRs have passed the required review and status checks before being integrated into the main branch.

---

## Core Features
- **GitHub Authentication**: Securely authenticates with the GitHub API using a Personal Access Token (PAT).
- **Data Extraction**: Fetches **all** merged pull requests from the `Scytale-exercise/dev-interviews` repository using robust pagination.
- **Compliance Analysis**: For each merged PR, the script checks:
    - **Code Review (`CR_Passed`)**: Was the PR approved by at least one reviewer?
    - **Status Checks (`CHECKS_PASSED`)**: Did all the required status checks for the head commit pass successfully?
- **Reporting**: Generates a final report in CSV format detailing the compliance status of each PR.
- **Modular Structure**: The code is logically separated into components like `extract.py`, `transform.py`, and `api_helpers.py`.

---
## Bonus Features Implemented
This project goes beyond the core requirements to include several bonus features for robustness and professional-grade quality:

- [x] **Robust API Pagination**: Handles repositories with hundreds of PRs by correctly parsing the `Link` header.
- [x] **Optional Date Range Filtering**: Allows users to generate reports for specific time periods via command-line arguments.
- [x] **Informative Logging**: Implements a structured logging system for clear, informative output and easier debugging.
- [x] **Incremental Progress & Professional Workflow**: Developed using a feature-branch workflow with clear, atomic commits and pull requests.
- [x] **Detailed API Documentation**: Includes a dedicated `API_DOCUMENTATION.md` file detailing the endpoints and authentication methods used.

---

## Project Structure
```
scytale_github_analyzer/
├── .env                  
├── .gitignore            
├── requirements.txt      
├── main.py               
├── README.md             
├── API_DOCUMENTATION.md  # API summary file
│
├── src/
│   ├── __init__.py       
│   ├── constants.py      # Centralized constants
│   ├── logging_config.py # Logging setup
│   ├── extract.py        
│   ├── transform.py      
│   └── api_helpers.py    # API enrichment functions
│
└── outputs/              
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
- Go to your GitHub **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
- Click **Generate new token**.
- Give it a name (e.g., `scytale-assignment-token`) and select the `repo` scope.
- **Copy the generated token immediately.**

### 4. Set Up Environment
- **Create and activate a virtual environment:**
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: .\venv\Scripts\activate
  ```

- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

### 5. Configure Environment Variables
- Create a file named `.env` in the root directory.
- Add your GitHub PAT to the `.env` file:
  ```
  GITHUB_PAT="paste_your_personal_access_token_here"
  ```

---

## How to Run

### Basic Usage
To run the analysis on all pull requests, execute the main script from the root directory:
```bash
python main.py
```

### Running with Optional Filters
You can filter the pull requests by their merge date using the `--start-date` and `--end-date` command-line arguments.

**Example 1: Get PRs merged in the year 2023**
```bash
python main.py --start-date 2023-01-01 --end-date 2023-12-31
```

**Example 2: Get all PRs merged since the beginning of 2024**
```bash
python main.py --start-date 2024-01-01
```

**To see all available options:**
```bash
python main.py --help
```

---

## Output
The script generates two primary outputs inside the `outputs/` directory:

1.  **Raw Data (`outputs/raw/pull_requests.json`)**: A JSON file containing the raw data for all merged pull requests.
2.  **Processed Report (`outputs/processed/pr_report.csv`)**: A CSV file containing the final analysis with the following columns:
    - `pr_number`, `pr_title`, `author`, `merge_date`, `CR_Passed`, `CHECKS_PASSED`.

---

## Project Documentation
For a detailed technical summary of the GitHub API endpoints, parameters, and authentication methods used in this project, please see the [**API Documentation**](./API_DOCUMENTATION.md) file.