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
    <input type="text" id="category" placeholder="e.g., Networking, Docker, Linux" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; background-color: #2e3440; color: #eceff4;">
  </div>

  <div style="margin-bottom: 15px;">
    <label for="title" style="display: block; font-weight: bold; margin-bottom: 5px;">Note Title</label>
    <input type="text" id="title" placeholder="e.g., How to Setup SSH" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; background-color: #2e3440; color: #eceff4;">
  </div>

  <div style="margin-bottom: 15px;">
    <label for="content" style="display: block; font-weight: bold; margin-bottom: 5px;">Note Content</label>
    <textarea id="content" rows="10" placeholder="Paste your raw notes, terminal output, or full guide here..." style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; background-color: #2e3440; color: #eceff4; font-family: monospace;"></textarea>
  </div>

  <a href="javascript:void(0)" id="submit-btn" onclick="submitNote()" style="display: inline-block; background-color: #5e81ac; color: white; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; text-decoration: none;">
    Generate Note with AI 🤖
  </a>
</div>

<script type="text/javascript">
function submitNote() {
  const category = document.getElementById('category').value;
  const title = document.getElementById('title').value;
  const content = document.getElementById('content').value;

  if (!title || !content) {
    alert('Please provide both a title and content for your note.');
    return;
  }

  const fullTitle = category ? `[${category}] ${title}` : title;
  const issueBody = `## Content\n${content}`;
  
  // Construct the GitHub New Issue URL
  const repoUrl = 'https://github.com/coltonchrane/AutoNotes/issues/new';
  const params = new URLSearchParams({
    template: 'contribution.md',
    title: fullTitle,
    body: issueBody,
    labels: 'contribution'
  });

  const finalUrl = `${repoUrl}?${params.toString()}`;
  
  // Provide some feedback on the page
  document.getElementById('contribution-form').innerHTML = `
    <div style="padding: 20px; background-color: #434c5e; border-radius: 8px; border: 1px solid #5e81ac; margin-top: 20px;">
      <h3>🚀 Redirecting...</h3>
      <p>If you are not redirected automatically, <a href="${finalUrl}" target="_blank" style="color: #88c0d0; text-decoration: underline;">click here to open the GitHub Issue</a>.</p>
      <p>Once the issue page opens, <strong>please click "Submit new issue"</strong> to start the AI automation.</p>
    </div>
  `;

  // Perform the redirection
  window.location.href = finalUrl;
}
</script>

---

### How it works:
1. **You Submit**: Your input is pre-filled into a GitHub Issue.
2. **AI Processes**: Our Gemini AI bot reads your issue and generates a formatted Markdown note.
3. **Review PR**: A new Pull Request is created with your note. Once merged, it appears here!
