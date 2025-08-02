# 🤝 Contributors Workflow

This repository includes an automated workflow to showcase contributors from your repositories in your GitHub profile README.

## 📋 How It Works

### 1. **Automated Data Collection**
- The GitHub Action runs weekly (every Sunday at 00:00 UTC)
- Fetches contributors from specified repositories using GitHub API
- Updates `data/contributors.json` with fresh contributor data

### 2. **Dynamic Display**
- Your README includes a JavaScript section that loads contributor data
- Displays top 12 contributors with their avatars and contribution counts
- Shows total contributor count and last update time
- Includes a link to the full contributors graph

## 🚀 Setup Instructions

### Step 1: Repository Configuration
1. The workflow is already configured in `.github/workflows/update-contributors.yml`
2. The script fetches contributors from repositories listed in `.github/scripts/update_contributors.py`

### Step 2: Add Your Repositories
Edit `.github/scripts/update_contributors.py` and add your repositories to the `REPOSITORIES` list:

```python
REPOSITORIES = [
    'Ctoic/Ctoic',  # Your profile repository
    'Ctoic/another-repo',  # Add more repositories
    'Ctoic/awesome-project',
    # Format: 'owner/repo-name'
]
```

### Step 3: Manual Trigger (Optional)
You can manually trigger the workflow:
1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Select "Update Contributors Data" workflow
4. Click "Run workflow"

## 🔧 Customization Options

### 1. **Change Update Frequency**
Edit the cron schedule in `.github/workflows/update-contributors.yml`:

```yaml
schedule:
  - cron: '0 0 * * 0'  # Every Sunday at 00:00 UTC
  # Other options:
  # '0 0 * * *' - Daily
  # '0 0 * * 1' - Every Monday
  # '0 12 * * *' - Daily at 12:00 UTC
```

### 2. **Modify Display Style**
Edit the JavaScript section in your README.md to change:
- Number of contributors shown (currently 12)
- Avatar size (currently 50px)
- Badge colors and styles
- Layout and formatting

### 3. **Add More Information**
You can enhance the contributor cards to show:
- Repository names where they contributed
- Contribution dates
- Pull request counts
- Issue counts

## 📊 Data Structure

The `data/contributors.json` file contains:

```json
{
  "last_updated": "2024-01-01T00:00:00",
  "total_contributors": 5,
  "repositories": ["Ctoic/Ctoic"],
  "contributors": [
    {
      "username": "contributor1",
      "avatar_url": "https://avatars.githubusercontent.com/...",
      "profile_url": "https://github.com/contributor1",
      "contributions": 15,
      "repository": "Ctoic/Ctoic"
    }
  ]
}
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Workflow not running**
   - Check if GitHub Actions are enabled for your repository
   - Verify the cron schedule is correct
   - Check the Actions tab for error messages

2. **No contributors showing**
   - Ensure repositories in the list are public
   - Check if repositories have contributors
   - Verify GitHub token permissions

3. **JavaScript not loading**
   - Check if the raw GitHub URL is accessible
   - Verify the JSON file path is correct
   - Check browser console for errors

### Debug Steps:
1. Run the workflow manually
2. Check the workflow logs in the Actions tab
3. Verify the `data/contributors.json` file is updated
4. Test the raw GitHub URL in your browser

## 🔒 Security Notes

- The workflow uses `GITHUB_TOKEN` (automatically provided)
- No personal tokens required
- Only fetches public repository data
- Respects GitHub API rate limits

## 📈 Benefits

1. **Automated Updates**: No manual work required
2. **Real-time Data**: Always shows current contributors
3. **Professional Look**: Enhances your GitHub profile
4. **Community Recognition**: Highlights contributors
5. **Easy Customization**: Simple to modify and extend

## 🤝 Contributing

Feel free to:
- Improve the workflow scripts
- Add new features
- Report issues
- Suggest enhancements

---

**Note**: This workflow is designed for GitHub profile repositories but can be adapted for any repository that wants to showcase contributors. 