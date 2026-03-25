---
layout: default
title: GitHub Issue Creator for Static Pages
parent: GitHub
nav_order: 3
---

# GitHub Issue Creator for Static Pages

This guide demonstrates how to implement a GitHub issue reporting tool for static websites (like GitHub Pages) using a secure OAuth popup flow. This setup allows users to authenticate via GitHub and submit issues directly to your repository without exposing sensitive credentials or redirecting away from your site.

## 1. Register a GitHub OAuth Application

To begin, you must register your application with GitHub to obtain the necessary credentials for authentication.

### Registration Steps
1. Navigate to **GitHub Developer Settings** > **OAuth Apps** and click **New OAuth App**.
2. **Application Name**: Enter a descriptive name, e.g., `My GH Issue Reporter`.
3. **Homepage URL**: Enter your site URL, e.g., `https://yourname.github.io`.
4. **Authorization callback URL**: This should also be your site URL or the specific path to your callback page, e.g., `https://yourname.github.io`.
5. Click **Register application**.
6. Save your **Client ID** and click **Generate a new client secret** to obtain your secret key. Keep these safe.

## 2. Deploy Gatekeeper to Render

Static sites cannot securely store a `Client Secret`. To solve this, we use **Gatekeeper**, a small Node.js proxy that acts as a bridge between your site and GitHub.

### Deployment Steps
1. Fork the [Gatekeeper Repository](https://github.com/prose/gatekeeper) to your own GitHub account.
2. Log in to [Render.com](https://render.com/) and create a **New + > Web Service**.
3. Connect your forked Gatekeeper repository.
4. In the **Environment Variables** section, add the following:
   - `OAUTH_CLIENT_ID`: Your Client ID from Step 1.
   - `OAUTH_CLIENT_SECRET`: Your Client Secret from Step 1.
5. Deploy the service. Once live, copy your Render URL (e.g., `https://gatekeeper-xyz.onrender.com`).

## 3. Create the Callback Handler

Create a file named `callback.html` in your GitHub Pages root directory. This page functions inside the popup window to capture the temporary authorization code sent by GitHub and pass it back to your main application.

```html
<!DOCTYPE html>
<html>
<head><title>Authenticating...</title></head>
<body>
  <script>
    // Extract the 'code' parameter from the URL sent by GitHub
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');

    if (code) {
      // Communicate the code to the parent window and close the popup
      window.opener.postMessage({ code }, window.location.origin);
      window.close();
    }
  </script>
</body>
</html>
```

## 4. Implement the Frontend Logic

Add the following JavaScript to your `index.html`. This script triggers the OAuth popup, listens for the authorization code, exchanges it for a token via Gatekeeper, and finally posts the issue to GitHub.

```javascript
const CLIENT_ID = "YOUR_GITHUB_CLIENT_ID";
const GATEKEEPER_URL = "https://your-gatekeeper-name.onrender.com";

let userToken = null;

/**
 * Opens the GitHub OAuth login in a popup window
 */
function login() {
  const url = `https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&scope=public_repo`;
  window.open(url, "GitHub Login", "width=600,height=700");
}

/**
 * Listens for the 'code' sent from callback.html via postMessage
 */
window.addEventListener("message", async (event) => {
  if (event.origin !== window.location.origin) return;

  const { code } = event.data;
  if (code) {
    try {
      // Exchange the temporary code for an access token via Gatekeeper
      const res = await fetch(`${GATEKEEPER_URL}/authenticate/${code}`);
      const data = await res.json();
      userToken = data.token;
      alert("Authentication successful! You can now submit your issue.");
    } catch (err) {
      console.error("Authentication error:", err);
    }
  }
});

/**
 * Submits the issue to the GitHub API using the acquired user token
 */
async function submitIssue() {
  if (!userToken) return alert("Please login first!");

  const response = await fetch("https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/issues", {
    method: "POST",
    headers: {
      "Authorization": `token ${userToken}`,
      "Accept": "application/vnd.github.v3+json"
    },
    body: JSON.stringify({
      title: "User Feedback",
      body: "Sent from my GitHub Pages site using OAuth popup logic!"
    })
  });

  if (response.ok) {
    alert("Issue created successfully!");
  } else {
    alert("Failed to create issue. Check the console for details.");
  }
}
```

## Summary of the OAuth Flow

1. **Trigger**: User clicks the login button, calling `window.open` to show the GitHub login screen.
2. **Handshake**: GitHub redirects the popup to `callback.html?code=XYZ`.
3. **Communication**: `callback.html` sends the code to the main page via `postMessage` and closes itself.
4. **Exchange**: The main page sends the code to your **Gatekeeper** instance on Render.
5. **Verification**: Gatekeeper communicates with GitHub using your `Client Secret` and returns a valid `access_token`.
6. **Execution**: The main page uses the token to post an issue directly to the GitHub API.

---
**Source:** [GitHub Issue #33](https://github.com/coltonchrane/AutoNotes/issues/33) | **Contributor:** @coltonchrane