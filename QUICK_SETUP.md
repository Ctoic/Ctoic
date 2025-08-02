# 🚀 Quick Setup Guide

## ✅ What's Already Done

1. **GitHub Action Workflow** - Created `.github/workflows/update-contributors.yml`
2. **Update Script** - Created `.github/scripts/update_contributors.py`
3. **Contributors Section** - Added to your README.md
4. **Data File** - Created `data/contributors.json`

## 🔧 Next Steps

### 1. **Enable GitHub Actions**
- Go to your repository on GitHub
- Click "Settings" → "Actions" → "General"
- Enable "Allow all actions and reusable workflows"
- Save the changes

### 2. **Add More Repositories** (Optional)
Run the helper script to add more repositories:
```bash
python3 add_repository.py
```

Or manually edit `.github/scripts/update_contributors.py`:
```python
REPOSITORIES = [
    'Ctoic/Ctoic',  # Your profile repository
    'Ctoic/another-repo',  # Add your other repositories
    'Ctoic/awesome-project',
]
```

### 3. **Test the Workflow**
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Find "Update Contributors Data" workflow
4. Click "Run workflow" → "Run workflow"

### 4. **Commit and Push**
```bash
git add .
git commit -m "Add contributors workflow and section"
git push
```

## 🎯 Expected Results

After the workflow runs successfully:
- Your README will show a "🤝 Contributors" section
- It will display contributor avatars and contribution counts
- The data will update automatically every week
- You can manually trigger updates anytime

## 📊 What You'll See

The contributors section will show:
- Total number of contributors
- Last update time
- Top 12 contributors with avatars
- Contribution badges
- Link to full contributors graph

## 🛠️ Troubleshooting

If the section shows "Loading...":
1. Check if `data/contributors.json` was created
2. Verify the workflow ran successfully
3. Check the Actions tab for any errors

## 📝 Customization

- **Change update frequency**: Edit the cron schedule in the workflow
- **Modify display**: Edit the JavaScript section in README.md
- **Add more info**: Enhance the contributor cards with additional data

---

**🎉 You're all set!** The contributors section will automatically update and showcase your project's contributors. 