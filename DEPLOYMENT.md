# Deploying Lucy Job Search App to Streamlit Cloud

This document outlines the steps to deploy the Lucy Job Search App to Streamlit Cloud.

## Prerequisites

- A GitHub account
- A Streamlit Cloud account (sign up at [https://streamlit.io/cloud](https://streamlit.io/cloud))

## Deployment Steps

1. **Push your code to GitHub**

   Make sure your repository includes:
   - `jobspy_app.py` (the main Streamlit application)
   - `requirements.txt` (Python dependencies)
   - `.streamlit/config.toml` (Streamlit configuration)
   - `packages.txt` (system dependencies)

2. **Log in to Streamlit Cloud**

   Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and log in with your GitHub account.

3. **Deploy the App**

   - Click "New app"
   - Select your repository, branch (main), and the main file path (`jobspy_app.py`)
   - Set any required secrets (if needed)
   - Click "Deploy"

4. **App Configuration**

   - Main file path: `jobspy_app.py`
   - Python version: 3.10
   - Packages: As specified in `requirements.txt`
   - System dependencies: As specified in `packages.txt`

## Troubleshooting

- If you encounter timeout issues during deployment, consider reducing the default number of jobs to search for in the app.
- Some job boards might have rate limiting or IP restrictions when deployed on Streamlit Cloud.
- Remember that the app might take a few minutes to deploy initially as it installs all dependencies.

## Updating the App

Simply push changes to your GitHub repository, and Streamlit Cloud will automatically redeploy your app. 