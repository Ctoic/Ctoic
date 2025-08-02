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

def generate_collaboration_stats_section(data: Dict[str, Any]) -> str:
    """Generate collaboration statistics section."""
    
    stats = data.get('collaboration_stats', {})
    total_repos = data.get('total_repositories', 0)
    repos_with_contributors = data.get('repositories_with_contributors', 0)
    
    return f"""
<div align="center">
  <h3>🎯 Collaboration & Management Excellence</h3>
  
  <table>
    <tr>
      <td align="center">
        <img src="https://img.shields.io/badge/Total%20Projects-{total_repos}-blue?style=for-the-badge&logo=github" alt="Total Projects"/>
      </td>
      <td align="center">
        <img src="https://img.shields.io/badge/Collaborative%20Projects-{repos_with_contributors}-green?style=for-the-badge&logo=users" alt="Collaborative Projects"/>
      </td>
      <td align="center">
        <img src="https://img.shields.io/badge/Total%20Contributions-{stats.get('total_contributions', 0)}-orange?style=for-the-badge&logo=code" alt="Total Contributions"/>
      </td>
      <td align="center">
        <img src="https://img.shields.io/badge/Unique%20Collaborators-{stats.get('unique_collaborators', 0)}-purple?style=for-the-badge&logo=user-friends" alt="Unique Collaborators"/>
      </td>
    </tr>
  </table>
</div>
"""

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
    
    # Generate contributor cards with enhanced info
    contributor_cards = []
    for contributor in sorted_contributors[:15]:  # Show top 15 contributors
        username = contributor['username']
        avatar_url = contributor['avatar_url']
        profile_url = contributor['profile_url']
        contributions = contributor['contributions']
        repos_contributed = contributor.get('total_repos_contributed', 1)
        
        card = f"""
    <a href="{profile_url}">
      <img src="{avatar_url}" width="50px;" alt="{username}"/>
      <br />
      <sub><b>{username}</b></sub>
    </a>
    <a href="{profile_url}" title="Contributions">
      <img src="https://img.shields.io/badge/Contributions-{contributions}-blue?style=flat-square" alt="Contributions"/>
    </a>
    <a href="{profile_url}" title="Projects Contributed">
      <img src="https://img.shields.io/badge/Projects-{repos_contributed}-green?style=flat-square" alt="Projects"/>
    </a>"""
        contributor_cards.append(card)
    
    # Create the enhanced section HTML
    collaboration_stats = generate_collaboration_stats_section(data)
    
    section = f"""
<div align="center">
  <h2>🤝 Contributors & Collaboration</h2>
  <p>Showcasing my ability to collaborate with diverse teams and manage multiple projects effectively!</p>
  
  {collaboration_stats}
  
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
  
  <br />
  
  <div align="center">
    <h3>🚀 Project Management Skills Demonstrated</h3>
    <p>• <strong>Multi-Project Coordination:</strong> Managing {data.get('total_repositories', 0)} repositories</p>
    <p>• <strong>Team Collaboration:</strong> Working with {total_contributors} unique contributors</p>
    <p>• <strong>Open Source Leadership:</strong> {data.get('repositories_with_contributors', 0)} collaborative projects</p>
    <p>• <strong>Code Quality:</strong> {data.get('collaboration_stats', {}).get('total_contributions', 0)} total contributions across projects</p>
    <p>• <strong>Technology Management:</strong> Coordinating teams across multiple tech stacks</p>
    <p>• <strong>Community Building:</strong> Fostering collaboration in open source projects</p>
  </div>
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
    pattern = r'(!\[borderseparator\]\([^)]+\)\s*\n\s*<div align="center">\s*<h2>🤝 Contributors.*?</div>\s*\n\s*!\[borderseparator\]\([^)]+\))'
    
    # Create the replacement pattern
    replacement = f'![borderseparator](https://github.com/Ctoic/Ctoic/assets/90936436/b0885c98-6e49-4365-93f1-fd2fcaed194c)\n{new_section}\n![borderseparator](https://github.com/Ctoic/Ctoic/assets/90936436/b0885c98-6e49-4365-93f1-fd2fcaed194c)'
    
    # Try to replace the section
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # If no match found, try a simpler pattern
    if new_content == content:
        pattern2 = r'(<div align="center">\s*<h2>🤝 Contributors.*?</div>)'
        new_content = re.sub(pattern2, new_section, content, flags=re.DOTALL)
    
    # Write back to file
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated contributors section in {readme_path}")
    print(f"📊 Collaboration Statistics:")
    print(f"   • Total repositories: {data.get('total_repositories', 0)}")
    print(f"   • Repositories with contributors: {data.get('repositories_with_contributors', 0)}")
    print(f"   • Total unique contributors: {data.get('total_contributors', 0)}")
    print(f"   • Total contributions: {data.get('collaboration_stats', {}).get('total_contributions', 0)}")
    
    return True

def main():
    """Main function."""
    print("🔄 Updating README contributors section...")
    
    success = update_readme_contributors_section()
    
    if success:
        print("✅ README updated successfully!")
        print("🎯 This showcases your collaboration and management skills!")
    else:
        print("❌ Failed to update README")

if __name__ == '__main__':
    main() 