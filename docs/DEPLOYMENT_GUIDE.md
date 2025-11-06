# 🚀 AI News Agent - Deployment Guide (Updated for Gemini)

Use free options like Docker locally or platforms (Railway/Render/Streamlit Cloud). Ensure `GEMINI_API_KEY` is set.

## Free Deployment Options

- Railway: one-click, free hours, easy env vars
- Render: free tier, stable, Streamlit friendly
- Streamlit Cloud: perfect for dashboard-only
- Cloud Run: generous free tier, needs Docker

## Env Vars
```env
GEMINI_API_KEY=your_gemini_api_key
LINKEDIN_ACCESS_TOKEN=...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
FACEBOOK_ACCESS_TOKEN=...
FACEBOOK_PAGE_ID=...
```

## Commands

- Build: `pip install -r requirements.txt`
- Dashboard: `streamlit run web_dashboard.py`
- Worker (scheduler): `python main.py run`


