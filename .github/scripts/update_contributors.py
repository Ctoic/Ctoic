#!/usr/bin/env python3
"""
Script to update contributors data from ALL GitHub repositories.
This script fetches contributors from all repositories owned by the user.
"""

import os
import json
import requests
import time
from datetime import datetime, timezone
from typing import Dict, List, Any

# GitHub API configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = 'ctoic'  # Your GitHub username

def get_github_headers():
    """Get headers for GitHub API requests."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Contributors-Update-Script'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def handle_rate_limit(response):
    """Handle GitHub API rate limiting."""
    if response.status_code == 403:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        wait_time = max(reset_time - time.time(), 0) + 60  # Add 60 seconds buffer
        print(f"⚠️ Rate limited. Waiting {wait_time:.0f} seconds...")
        time.sleep(wait_time)
        return True
    return False

def fetch_user_repositories(username: str) -> List[Dict[str, Any]]:
    """Fetch all repositories owned by the user with proper pagination."""
    url = f'https://api.github.com/users/{username}/repos'
    headers = get_github_headers()
    
    all_repos = []
    page = 1
    
    print(f"🔍 Fetching all repositories for user: {username}")
    
    while True:
        try:
            print(f"📄 Fetching page {page}...")
            response = requests.get(f'{url}?page={page}&per_page=100&sort=updated', headers=headers)
            
            if handle_rate_limit(response):
                continue
                
            response.raise_for_status()
            
            repos = response.json()
            if not repos:
                print(f"✅ No more repositories found on page {page}")
                break
                
            print(f"📦 Found {len(repos)} repositories on page {page}")
            all_repos.extend(repos)
            page += 1
            
            # Add a small delay to be respectful to the API
            time.sleep(0.5)
            
        except requests.RequestException as e:
            print(f"❌ Error fetching repositories page {page}: {e}")
            break
    
    print(f"🎯 Total repositories found: {len(all_repos)}")
    return all_repos

def fetch_repository_contributors(owner: str, repo: str) -> List[Dict[str, Any]]:
    """Fetch contributors from a specific repository with rate limit handling."""
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    headers = get_github_headers()
    
    try:
        response = requests.get(url, headers=headers)
        
        if handle_rate_limit(response):
            # Retry after rate limit
            time.sleep(2)
            response = requests.get(url, headers=headers)
            
        response.raise_for_status()
        
        contributors = response.json()
        return [
            {
                'username': contributor['login'],
                'avatar_url': contributor['avatar_url'],
                'profile_url': contributor['html_url'],
                'contributions': contributor['contributions'],
                'repository': f'{owner}/{repo}',
                'repository_name': repo,
                'repository_url': f'https://github.com/{owner}/{repo}'
            }
            for contributor in contributors
        ]
    except requests.RequestException as e:
        print(f"❌ Error fetching contributors from {owner}/{repo}: {e}")
        return []

def fetch_all_contributors_from_all_repos() -> Dict[str, Any]:
    """Fetch contributors from ALL repositories owned by the user."""
    print(f"🚀 Starting comprehensive contributor analysis for: {GITHUB_USERNAME}")
    
    # Get all repositories
    all_repos = fetch_user_repositories(GITHUB_USERNAME)
    
    if not all_repos:
        print("❌ No repositories found!")
        return {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'total_contributors': 0,
            'total_repositories': 0,
            'repositories_with_contributors': 0,
            'repositories': [],
            'contributors': [],
            'collaboration_stats': {
                'total_projects': 0,
                'projects_with_collaborators': 0,
                'total_contributions': 0,
                'unique_collaborators': 0
            }
        }
    
    print(f"📊 Processing {len(all_repos)} repositories...")
    
    all_contributors = []
    repositories_with_contributors = []
    processed_count = 0
    
    for repo in all_repos:
        repo_name = repo['name']
        repo_full_name = repo['full_name']
        repo_url = repo['html_url']
        repo_description = repo.get('description', '')
        repo_language = repo.get('language', 'Unknown')
        repo_stars = repo.get('stargazers_count', 0)
        repo_forks = repo.get('forks_count', 0)
        
        processed_count += 1
        print(f"🔍 [{processed_count}/{len(all_repos)}] Processing: {repo_full_name}")
        
        contributors = fetch_repository_contributors(GITHUB_USERNAME, repo_name)
        
        if contributors:
            print(f"✅ Found {len(contributors)} contributors in {repo_name}")
            repositories_with_contributors.append({
                'name': repo_name,
                'full_name': repo_full_name,
                'url': repo_url,
                'description': repo_description,
                'language': repo_language,
                'stars': repo_stars,
                'forks': repo_forks,
                'contributor_count': len(contributors)
            })
            
            # Add repository info to each contributor
            for contributor in contributors:
                contributor['repo_stars'] = repo_stars
                contributor['repo_forks'] = repo_forks
                contributor['repo_language'] = repo_language
                contributor['repo_description'] = repo_description
            
            all_contributors.extend(contributors)
        else:
            print(f"ℹ️ No contributors found in {repo_name}")
        
        # Add delay to respect rate limits
        time.sleep(0.2)
    
    print(f"🔄 Processing contributor data...")
    
    # Remove duplicates based on username and merge contributions
    unique_contributors = {}
    for contributor in all_contributors:
        username = contributor['username']
        if username not in unique_contributors:
            unique_contributors[username] = contributor
            unique_contributors[username]['repositories_contributed'] = [contributor['repository']]
            unique_contributors[username]['total_repos_contributed'] = 1
        else:
            # Merge contributions and add repository info
            existing = unique_contributors[username]
            existing['contributions'] += contributor['contributions']
            existing['repositories_contributed'].append(contributor['repository'])
            existing['total_repos_contributed'] = len(set(existing['repositories_contributed']))
    
    # Convert back to list and sort by total contributions
    final_contributors = list(unique_contributors.values())
    final_contributors.sort(key=lambda x: x['contributions'], reverse=True)
    
    total_contributions = sum(c['contributions'] for c in final_contributors)
    
    result = {
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'total_contributors': len(final_contributors),
        'total_repositories': len(all_repos),
        'repositories_with_contributors': len(repositories_with_contributors),
        'repositories': repositories_with_contributors,
        'contributors': final_contributors,
        'collaboration_stats': {
            'total_projects': len(all_repos),
            'projects_with_collaborators': len(repositories_with_contributors),
            'total_contributions': total_contributions,
            'unique_collaborators': len(final_contributors)
        }
    }
    
    print(f"🎉 Analysis complete!")
    print(f"📊 Summary:")
    print(f"   • Total repositories processed: {len(all_repos)}")
    print(f"   • Repositories with contributors: {len(repositories_with_contributors)}")
    print(f"   • Unique contributors found: {len(final_contributors)}")
    print(f"   • Total contributions: {total_contributions}")
    
    return result

def save_contributors_data(data: Dict[str, Any], filepath: str = 'data/contributors.json'):
    """Save contributors data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Contributors data saved to {filepath}")
    print(f"📊 Final Collaboration Statistics:")
    print(f"   • Total repositories: {data['total_repositories']}")
    print(f"   • Repositories with contributors: {data['repositories_with_contributors']}")
    print(f"   • Total unique contributors: {data['total_contributors']}")
    print(f"   • Total contributions: {data['collaboration_stats']['total_contributions']}")

def main():
    """Main function to update contributors data."""
    print("🔄 Starting comprehensive contributor analysis...")
    print("=" * 60)
    
    data = fetch_all_contributors_from_all_repos()
    save_contributors_data(data)
    
    print("=" * 60)
    print("✅ Contributors data update completed!")
    print("🎯 This showcases your collaboration and management skills across ALL projects!")

if __name__ == '__main__':
    main() 