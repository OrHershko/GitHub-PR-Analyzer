# API Usage and Authentication Summary

This document summarizes the GitHub API endpoints and the authentication method used in this project. It is intended for developers maintaining or reviewing this project.

## Authentication

- **Method**: Personal Access Token (PAT)
- **Usage**: The PAT is sent in the `Authorization` header of every API request to authenticate and identify the script.
- **Format**: `Authorization: token <YOUR_PAT>`
- **Security**: The PAT is not hardcoded. It is loaded securely from a `.env` file at runtime using the `python-dotenv` library. The `.env` file is explicitly excluded from version control via `.gitignore`.

---

## API Endpoints Used

### 1. Fetch Pull Requests

- **Endpoint**: `GET /repos/{owner}/{repo}/pulls`
- **Purpose**: To retrieve a list of pull requests from the specified repository. This is the primary data source for our application.
- **Key Parameters Used**:
    - `state=closed`: Fetches only closed PRs. We then filter these locally to keep only the ones that were actually merged.
    - `per_page=100`: Requests the maximum number of items per page to minimize the number of API calls.
- **Pagination**: Handled robustly by parsing the `Link` header in the API response to find the URL for the next page of results. The process continues until no 'next' link is provided.
- **Data Usage**: We extract `number`, `title`, `user.login`, `merged_at`, and `head.sha` from each pull request object.

### 2. Fetch Pull Request Reviews

- **Endpoint**: `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews`
- **Purpose**: To check if a specific pull request was formally approved by at least one reviewer. This is used to determine the `CR_Passed` value.
- **Data Usage**: We iterate through the list of returned review objects and check if any object has a `state` field with the value `"APPROVED"`. The check passes (`True`) on the first occurrence.

### 3. Fetch Commit Status

- **Endpoint**: `GET /repos/{owner}/{repo}/commits/{ref}/status`
- **Purpose**: To get the "combined status" for a specific commit. This endpoint conveniently summarizes the results of all status checks (e.g., CI builds, linters) associated with that commit. This is used to determine the `CHECKS_PASSED` value.
- **Data Usage**: We use the `head.sha` from the pull request object as the `{ref}` in the URL. The check passes (`True`) only if the top-level `state` field in the response is `"success"`.