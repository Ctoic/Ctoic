#!/usr/bin/env python3
"""
Script to update the contributors section in README.md with latest data
"""

import json
import re
from datetime import datetime
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
    
    # Format the date
    try:
        date_obj = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
        formatted_date = date_obj.strftime('%Y-%m-%d')
    except:
        formatted_date = last_updated
    
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
    <em>Last updated: {formatted_date}</em>
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

def update_readme_contributors_section(readme_path: str = 'README.md'):
    """Update the contributors section in README.md."""
    
    # Load contributors data
    data = load_contributors_data()
    
    # Generate new section
    new_section = generate_contributors_section(data)
    
    # Read current README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"README.md not found: {readme_path}")
        return False
    
    # Find and replace the contributors section
    # Look for the section between the border separators
    pattern = r'(!\[borderseparator\]\([^)]+\)\s*\n\s*<div align="center">\s*<h2>🤝 Contributors</h2>.*?</div>\s*\n\s*!\[borderseparator\]\([^)]+\))'
    
    # Create the replacement pattern
    replacement = f'![borderseparator](https://github.com/Ctoic/Ctoic/assets/90936436/b0885c98-6e49-4365-93f1-fd2fcaed194c)\n{new_section}\n![borderseparator](https://github.com/Ctoic/Ctoic/assets/90936436/b0885c98-6e49-4365-93f1-fd2fcaed194c)'
    
    # Try to replace the section
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # If no match found, try a simpler pattern
    if new_content == content:
        pattern2 = r'(<div align="center">\s*<h2>🤝 Contributors</h2>.*?</div>)'
        new_content = re.sub(pattern2, new_section, content, flags=re.DOTALL)
    
    # Write back to file
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated contributors section in {readme_path}")
    print(f"📊 Total contributors: {data.get('total_contributors', 0)}")
    print(f"🕒 Last updated: {data.get('last_updated', 'Unknown')}")
    
    return True

def main():
    """Main function."""
    print("🔄 Updating README contributors section...")
    
    success = update_readme_contributors_section()
    
    if success:
        print("✅ README updated successfully!")
    else:
        print("❌ Failed to update README")

if __name__ == '__main__':
    main() 