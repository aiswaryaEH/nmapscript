import requests

# GitHub configuration
GITHUB_TOKEN = "your_github_token"  # Generate a GitHub Personal Access Token
REPO_OWNER = "your_github_username"
REPO_NAME = "your_repo_name"
FILE_PATH = "scan_results.txt"
COMMIT_MESSAGE = "Add new scan results"

# GitHub API endpoint
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"

def get_file_sha():
    """Check if the file already exists to retrieve its SHA for updates."""
    response = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def upload_to_github():
    """Upload or update the file on GitHub."""
    with open(FILE_PATH, "r") as file:
        content = file.read()

    data = {
        "message": COMMIT_MESSAGE,
        "content": content.encode("utf-8").decode("utf-8"),
    }

    sha = get_file_sha()
    if sha:
        data["sha"] = sha  # Add SHA if updating the file

    response = requests.put(url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code in [201, 200]:
        print("File uploaded successfully.")
    else:
        print("Failed to upload file:", response.json())

if __name__ == "__main__":
    upload_to_github()
