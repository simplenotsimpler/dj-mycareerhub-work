# common/github.py
import requests
from datetime import datetime
from decouple import config


def get_projects():
    """
    Fetch pinned repositories from GitHub GraphQL API.

    Returns:
        list[dict]: Flattened, sorted pinned repositories.
    """
    token = config('GH_TOKEN', default=None)
    url = config('GH_URL', default=None)

    if not token or not url:
        raise RuntimeError("Missing GH_TOKEN or GH_URL in environment variables (.env).")

    gh_query = {
        "query": """
        query {
          viewer {
            pinnedItems(first: 10) {
              repos: nodes {
                ... on Repository {
                  name
                  description
                  url
                  homepageUrl
                  openGraphImageUrl
                  stargazerCount
                  createdAt
                  updatedAt
                  pushedAt
                  forks { totalCount }
                  watchers { totalCount }
                  topics: repositoryTopics(first: 20) {
                    nodes { topic { name } }
                  }
                  languages(first: 20, orderBy: {field: SIZE, direction: DESC}) {
                    edges { node { name } }
                  }
                }
              }
            }
          }
        }
        """
    }

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.post(url, json=gh_query, headers=headers, timeout=3)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"GitHub API request failed: {e}")

    try:
        projects = response.json()["data"]["viewer"]["pinnedItems"]["repos"]
    except (KeyError, TypeError) as e:
        raise RuntimeError(f"Unexpected GitHub API response: {e}")

    projects_with_flat = []
    for project in projects:
        project["topics"] = [n["topic"]["name"] for n in project["topics"]["nodes"]]
        project["languages"] = [e["node"]["name"] for e in project["languages"]["edges"]]
        projects_with_flat.append(project)

    # Adjust Brickyard project manually
    for project in projects_with_flat:
        if project["name"] == "brickyard-ceramics":
            project["createdAt"] = "2020-06-15"
            project["pushedAt"] = "2021-10-08"
            project["languages"] = ["HTML", "CSS"]

    # Sort by pushedAt descending
    projects_sorted = sorted(
        projects_with_flat,
        key=lambda p: datetime.fromisoformat(p["pushedAt"].replace("Z", "+00:00")),
        reverse=True,
    )

    return projects_sorted
