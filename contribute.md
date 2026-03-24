---
layout: default
title: Contribute
nav_order: 2
description: Contribute a new technical note to AutoNotes.
---

# ✍️ Contribute a New Note

Submit your technical guides or raw notes below. Our **Gemini AI Bot** will automatically refine your content, format it as a markdown note, and create a Pull Request for review.

---

<div id="contribution-form">
  <div style="margin-bottom: 15px;">
    <label for="category" style="display: block; font-weight: bold; margin-bottom: 5px;">Category</label>
    <select id="category" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; background-color: #2e3440; color: #eceff4;">
      <option value="Inbound">General (Inbound)</option>
      <option value="Networking">Networking</option>
      <option value="Docker">Docker</option>
      <option value="Disk_Management">Disk Management</option>
      <option value="Programming_Languages">Programming Languages</option>
      <option value="Linux">Linux</option>
    </select>
  </div>

  <div style="margin-bottom: 15px;">
    <label for="title" style="display: block; font-weight: bold; margin-bottom: 5px;">Note Title</label>
    <input type="text" id="title" placeholder="e.g., How to Setup SSH" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; background-color: #2e3440; color: #eceff4;">
  </div>

  <div style="margin-bottom: 15px;">
    <label for="content" style="display: block; font-weight: bold; margin-bottom: 5px;">Note Content</label>
    <textarea id="content" rows="10" placeholder="Paste your raw notes, terminal output, or full guide here..." style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; background-color: #2e3440; color: #eceff4; font-family: monospace;"></textarea>
  </div>

  <button id="submit-btn" style="background-color: #5e81ac; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold;">
    Generate Note with AI 🤖
  </button>
</div>

<script>
  document.getElementById('submit-btn').addEventListener('click', function() {
    const category = document.getElementById('category').value;
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;

    if (!title || !content) {
      alert('Please provide both a title and content for your note.');
      return;
    }

    const fullTitle = `[${category}] ${title}`;
    const issueBody = `## Content\n${content}`;
    const labels = 'contribution';
    
    // Construct the GitHub New Issue URL
    // Repository: coltonchrane/AutoNotes
    const repoUrl = 'https://github.com/coltonchrane/AutoNotes/issues/new';
    const params = new URLSearchParams({
      title: fullTitle,
      body: issueBody,
      labels: labels
    });

    const finalUrl = `${repoUrl}?${params.toString()}`;
    
    // Open the pre-filled issue in a new tab
    window.open(finalUrl, '_blank');
    
    // Provide some feedback on the page
    document.getElementById('contribution-form').innerHTML = `
      <div style="padding: 20px; background-color: #434c5e; border-radius: 8px; border: 1px solid #5e81ac; margin-top: 20px;">
        <h3>🚀 Almost there!</h3>
        <p>I've opened a pre-filled GitHub Issue for you in a new tab.</p>
        <p><strong>Please click "Submit new issue" on that page</strong> to start the AI automation.</p>
        <p>Once submitted, our bot will generate a Pull Request with your formatted note!</p>
      </div>
    `;
  });
</script>

---

### How it works:
1. **You Submit**: Your input is pre-filled into a GitHub Issue.
2. **AI Processes**: Our Gemini AI bot reads your issue and generates a formatted Markdown note.
3. **Review PR**: A new Pull Request is created with your note. Once merged, it appears here!
