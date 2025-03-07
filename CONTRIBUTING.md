# 🚀 Contributing to Progress Bar

Thank you for your interest in contributing to **Progress Bar**! 🎉 This project is a **Python API** deployed on **Vercel** that generates **SVG badges** 🏅 to visualize progress.

## 🛠 Getting Started

Before you begin contributing, please ensure you have the following prerequisites:

### ✅ Requirements
- 🐍 **Python 3.10+**
- 📦 **pip** (Python package manager)
- ▲ **Vercel CLI** (for testing deployments)
- 🔧 **Git**

### 📥 Installation

1. **Clone the repository:**
   ```sh
   git clone git@github.com:guibranco/progressbar.git
   cd progressbar
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## ▶️ Running the API Locally

To start the API locally, use the following command:

```sh
vercel dev
```

This will run the API in a local environment using Vercel. 🌍

## 🧪 Testing Your Changes

Before submitting a pull request, test your changes:

### 🏠 Local Testing
- Run `vercel dev` and verify that your changes work as expected.
- Use **Postman**, **cURL**, or a browser to send requests to the local API. 🌐

### ⚡ Vercel Preview Deployment
After pushing your branch to GitHub, open a **Pull Request** (PR). Vercel will automatically create a **preview deployment**. Use the provided URL to test your changes before merging. 🚀

## 🔀 Submitting a Pull Request

1. **Fork the repository** (if you haven’t already).
2. **Create a new branch:**
   ```sh
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes:**
   ```sh
   git commit -m "✨ Add a brief description of your changes"
   ```
4. **Push to your branch:**
   ```sh
   git push origin feature/your-feature-name
   ```
5. **Open a pull request** on GitHub. 🔥

## 📌 Pull Request Guidelines

- Follow the **[Pull Request Template](https://github.com/guibranco/.github/blob/main/.github/pull_request_template.md)**. 📝
- Ensure your code follows best practices and includes comments where necessary. 💡
- Write clear commit messages. ✍️
- Squash unnecessary commits before submitting. 📌
- Wait for CI checks and Vercel preview tests to pass before requesting a review. ✅

## ❓ Need Help?
If you need any help, feel free to **open an issue** on GitHub 🐞.

Happy coding! 🎉🚀

