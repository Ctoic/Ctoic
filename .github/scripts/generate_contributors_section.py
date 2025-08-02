#!/usr/bin/env python3
"""
Script to generate contributors section for README.md
"""

import json
import os
from typing import Dict, List, Any

def load_contributors_data(filepath: str = 'data/contributors.json') -> Dict[str, Any]:
    """Load contributors data from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Contributors data file not found: {filepath}")
        return {
            "last_updated": "2024-01-01T00:00:00",
            "total_contributors": 0,
            "repositories": [],
            "contributors": []
        }

def generate_contributors_section(data: Dict[str, Any]) -> str:
    """Generate the contributors section HTML for README."""
    
    contributors = data.get('contributors', [])
    total_contributors = data.get('total_contributors', 0)
    last_updated = data.get('last_updated', 'Unknown')
    
    if not contributors:
        return """
<div align="center">
  <h2>🤝 Contributors</h2>
  <p>No contributors found yet. Be the first to contribute!</p>
</div>
"""
    
    # Sort contributors by contributions (descending)
    sorted_contributors = sorted(contributors, key=lambda x: x['contributions'], reverse=True)
    
    # Generate contributor cards
    contributor_cards = []
    for contributor in sorted_contributors[:12]:  # Show top 12 contributors
        username = contributor['username']
        avatar_url = contributor['avatar_url']
        profile_url = contributor['profile_url']
        contributions = contributor['contributions']
        
        card = f"""
<a href="{profile_url}">
  <img src="{avatar_url}" width="50px;" alt="{username}"/>
  <br />
  <sub><b>{username}</b></sub>
</a>
<a href="{profile_url}" title="Contributions">
  <img src="https://img.shields.io/badge/Contributions-{contributions}-blue?style=flat-square" alt="Contributions"/>
</a>"""
        contributor_cards.append(card)
    
    # Create the section HTML
    section = f"""
<div align="center">
  <h2>🤝 Contributors</h2>
  <p>Thanks to all the amazing contributors who have helped make this project better!</p>
  
  <p align="center">
    <strong>Total Contributors: {total_contributors}</strong>
  </p>
  
  <p align="center">
    <em>Last updated: {last_updated}</em>
  </p>
  
  <br />
  
  <p align="center">
    {''.join(contributor_cards)}
  </p>
  
  <br />
  
  <p align="center">
    <a href="https://github.com/ctoic/Ctoic/graphs/contributors">
      <img src="https://contrib.rocks/image?repo=ctoic/Ctoic" alt="Contributors" />
    </a>
  </p>
</div>
"""
    
    return section

def main():
    """Main function to generate contributors section."""
    data = load_contributors_data()
    section = generate_contributors_section(data)
    
    # Save the section to a file for easy copying
    with open('contributors_section.md', 'w', encoding='utf-8') as f:
        f.write(section)
    
    print("Contributors section generated and saved to 'contributors_section.md'")
    print("\nGenerated section:")
    print(section)

if __name__ == '__main__':
    main() 