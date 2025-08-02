#!/usr/bin/env python3
"""
Helper script to add repositories to the contributors tracking list.
"""

import re

def add_repository(repo_name):
    """Add a repository to the tracking list."""
    
    # Validate repository format
    if not re.match(r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$', repo_name):
        print("❌ Invalid repository format. Use: owner/repo-name")
        return False
    
    # Read the current script
    script_path = '.github/scripts/update_contributors.py'
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the REPOSITORIES list
        pattern = r'REPOSITORIES = \[(.*?)\]'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print("❌ Could not find REPOSITORIES list in the script")
            return False
        
        repositories_section = match.group(1)
        
        # Check if repository already exists
        if repo_name in repositories_section:
            print(f"✅ Repository '{repo_name}' is already in the tracking list")
            return True
        
        # Add the new repository
        new_repositories_section = repositories_section.rstrip() + f'\n    \'{repo_name}\',  # Added via script\n'
        
        # Replace in content
        new_content = re.sub(pattern, f'REPOSITORIES = [{new_repositories_section}]', content, flags=re.DOTALL)
        
        # Write back to file
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Successfully added '{repo_name}' to the tracking list")
        print("📝 Don't forget to commit and push the changes!")
        return True
        
    except FileNotFoundError:
        print("❌ Could not find the update_contributors.py script")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function."""
    print("🤝 Add Repository to Contributors Tracking")
    print("=" * 50)
    
    while True:
        repo_name = input("\nEnter repository name (format: owner/repo-name) or 'quit' to exit: ").strip()
        
        if repo_name.lower() == 'quit':
            break
        
        if not repo_name:
            print("❌ Please enter a repository name")
            continue
        
        add_repository(repo_name)
        
        another = input("\nAdd another repository? (y/n): ").strip().lower()
        if another != 'y':
            break
    
    print("\n👋 Done! Remember to:")
    print("1. Commit the changes: git add .github/scripts/update_contributors.py")
    print("2. Push to GitHub: git push")
    print("3. The workflow will automatically update on the next schedule")

if __name__ == '__main__':
    main() 