# 🚀 Deployment Guide - Personal RAG Learning Lab

This guide explains how to deploy your **Personal RAG Learning Lab** live on the web so anyone can access and test your RAG system with user login authentication.

---

## Option 1: Deploy on Streamlit Community Cloud (Recommended — 100% Free & Easy)

Streamlit Community Cloud is the easiest and fastest way to deploy Streamlit applications directly from GitHub.

### Steps:
1. **Push your code to GitHub**:
   Make sure your latest code (including `app.py`, `auth.py`, `rag_engine.py`, `requirements.txt`) is committed and pushed to your GitHub repository:
   ```bash
   git add .
   git commit -m "Add user authentication & login"
   git push origin main
   ```

2. **Sign up / Log in to Streamlit Cloud**:
   Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.

3. **Deploy App**:
   - Click **"New App"**.
   - Select your repository: `iakash2701/personal-rag-learning-lab`
   - Select Branch: `main`
   - Main file path: `app.py`
   - Click **"Deploy!"**

4. **Your Live URL**:
   Streamlit will build your app and provide a public URL (e.g. `https://personal-rag-learning-lab.streamlit.app`).

---

## Option 2: Deploy on Render

Your repository already includes a `render.yaml` configuration for Render.

### Steps:
1. Push your changes to GitHub.
2. Log in to [Render.com](https://render.com/).
3. Click **"New +"** -> **"Web Service"**.
4. Connect your GitHub repository `iakash2701/personal-rag-learning-lab`.
5. Render will automatically detect the settings from `render.yaml`:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Click **"Create Web Service"**.

---

## Option 3: Deploy on Hugging Face Spaces

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces).
2. Click **"Create new Space"**.
3. Choose **Streamlit** as the SDK.
4. Clone the Hugging Face repo or link it to your GitHub repository.
5. Your app will automatically deploy!

---

## 🔒 Default Login Credentials

Upon first run, the system initializes a default admin user:
- **Username**: `admin`
- **Password**: `admin123`

Any visitor can also click the **"Register Account"** tab to create their own username and password!
