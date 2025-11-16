# LinkedIn Posts Automation Guide

This guide explains how the automated LinkedIn posts sync system works.

## 📋 Overview

The system automatically syncs LinkedIn post embed codes from `posts.txt` to `index.html` using GitHub Actions.

## 🚀 How It Works

1. **You add posts** - Add LinkedIn embed codes to `posts.txt`
2. **Auto-sync** - GitHub Actions runs every 2 hours and syncs posts to `index.html`
3. **Auto-commit** - Changes are automatically committed and pushed to your repo
4. **Live update** - GitHub Pages automatically deploys the updated website

## 📝 Adding LinkedIn Posts

### Step 1: Get the Embed Code from LinkedIn

1. Go to the LinkedIn post you want to embed
2. Click the three dots (•••) in the top-right corner of the post
3. Select **"Embed"** from the dropdown menu
4. Copy the iframe code that appears

### Step 2: Add to posts.txt

1. Open `posts.txt` in your local repository
2. Paste the iframe code on a new line
3. Example format:

```html
<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:7394672680484036608" height="1846" width="504" frameborder="0" allowfullscreen="" title="Embedded post"></iframe>
<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:XXXXXXXXX" height="1846" width="504" frameborder="0" allowfullscreen="" title="Embedded post"></iframe>
```

### Step 3: Commit and Push

```bash
git add posts.txt
git commit -m "Add new LinkedIn post"
git push
```

## ⚙️ Automation Details

### GitHub Actions Workflow

The workflow (`.github/workflows/sync-linkedin-posts.yml`) runs:

- **Every 2 hours** - Scheduled sync via cron: `0 */2 * * *`
- **On push** - When you update `posts.txt`
- **Manual trigger** - You can manually run it from GitHub Actions tab

### What the Script Does

`sync_posts.py`:
1. Reads all iframe codes from `posts.txt`
2. Ignores comment lines (starting with `#`)
3. Updates the LinkedIn Posts section in `index.html`
4. Preserves all other content

## 🔧 Manual Sync (Optional)

To manually sync posts without waiting for GitHub Actions:

```bash
python sync_posts.py
```

## 📌 Important Notes

### Post Order
- Posts appear in the order they're listed in `posts.txt`
- First post = leftmost on desktop
- Reorder lines to change display order

### Comments in posts.txt
- Lines starting with `#` are ignored
- Use for organization:

```
# Recent AI posts
<iframe src="..." ...></iframe>

# Older posts
<iframe src="..." ...></iframe>
```

### Removing Posts
- Simply delete the iframe line from `posts.txt`
- The next sync will remove it from the website

### LinkedIn "Refused to Connect" Error

If you see this error when testing locally:
- **Cause**: LinkedIn embeds require HTTPS (file:// protocol doesn't work)
- **Solution**: The embeds will work fine on GitHub Pages (https://sharathreddy.in)
- Test on the live site, not locally

## 🎨 Styling

Posts automatically inherit your website's vibrant theme:
- Blue gradient border on hover
- Lift animation on hover
- Responsive grid layout (adapts to screen size)
- Matches other sections' width (1200px max)

## 🔍 Troubleshooting

### Posts not updating?
1. Check GitHub Actions tab for workflow runs
2. Look for errors in the workflow log
3. Verify `posts.txt` format is correct

### Workflow not running?
- Make sure GitHub Actions is enabled in repo settings
- Check if you have push permission to the repo

### Want to trigger sync immediately?
1. Go to GitHub → Actions tab
2. Click "Sync LinkedIn Posts"
3. Click "Run workflow"

## 📊 Monitoring

Check sync status:
- **GitHub Actions tab** - View all workflow runs
- **Commits** - Auto-commits show "Auto-sync LinkedIn posts from posts.txt"

---

**Questions?** Check the workflow logs or manually run `python sync_posts.py` to see detailed output.
