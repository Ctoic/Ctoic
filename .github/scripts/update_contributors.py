#!/usr/bin/env python3
"""
Script to update contributors data from GitHub repositories.
This script fetches contributors from specified repositories and updates a JSON file.
"""

import os
import json
import requests
from datetime import datetime, timezone
from typing import Dict, List, Any

# GitHub API configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = 'ctoic'  # Your GitHub username

# Repositories to fetch contributors from
REPOSITORIES = [
    'Ctoic/Ctoic',  # Your profile repository
    # Add more repositories here as needed
    # Format: 'owner/repo-name'
]

def get_github_headers():
    """Get headers for GitHub API requests."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Contributors-Update-Script'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def fetch_repository_contributors(owner: str, repo: str) -> List[Dict[str, Any]]:
    """Fetch contributors from a specific repository."""
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    headers = get_github_headers()
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        contributors = response.json()
        return [
            {
                'username': contributor['login'],
                'avatar_url': contributor['avatar_url'],
                'profile_url': contributor['html_url'],
                'contributions': contributor['contributions'],
                'repository': f'{owner}/{repo}'
            }
            for contributor in contributors
        ]
    except requests.RequestException as e:
        print(f"Error fetching contributors from {owner}/{repo}: {e}")
        return []

def fetch_all_contributors() -> Dict[str, Any]:
    """Fetch contributors from all specified repositories."""
    all_contributors = []
    
    for repo in REPOSITORIES:
        owner, repo_name = repo.split('/')
        contributors = fetch_repository_contributors(owner, repo_name)
        all_contributors.extend(contributors)
    
    # Remove duplicates based on username
    unique_contributors = {}
    for contributor in all_contributors:
        username = contributor['username']
        if username not in unique_contributors:
            unique_contributors[username] = contributor
        else:
            # Merge contributions if user appears in multiple repos
            unique_contributors[username]['contributions'] += contributor['contributions']
    
    return {
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'total_contributors': len(unique_contributors),
        'repositories': REPOSITORIES,
        'contributors': list(unique_contributors.values())
    }

def save_contributors_data(data: Dict[str, Any], filepath: str = 'data/contributors.json'):
    """Save contributors data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Contributors data saved to {filepath}")
    print(f"Total contributors: {data['total_contributors']}")

def main():
    """Main function to update contributors data."""
    print("Fetching contributors data...")
    
    data = fetch_all_contributors()
    save_contributors_data(data)
    
    print("Contributors data update completed!")

if __name__ == '__main__':
    main() 