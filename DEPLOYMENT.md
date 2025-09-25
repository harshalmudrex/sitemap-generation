# Deploying to Render

This guide will help you deploy your Flask sitemap generation application to Render.

## Prerequisites

1. A GitHub account with your code pushed to a repository
2. A Render account (sign up at [render.com](https://render.com))

## Deployment Steps

### 1. Push Your Code to GitHub

Make sure all your files are committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Connect to Render

1. Go to [render.com](https://render.com) and sign in
2. Click "New +" and select "Web Service"
3. Connect your GitHub account if you haven't already
4. Select your repository: `sitemap-generation`

### 3. Configure Your Service

Use these settings in the Render dashboard:

- **Name**: `sitemap-generation` (or any name you prefer)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free (or choose a paid plan for production)

### 4. Environment Variables (Optional)

If you need any environment variables, add them in the Render dashboard under "Environment Variables". Your app currently uses:
- `PORT` (automatically set by Render)

### 5. Deploy

Click "Create Web Service" and Render will:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Start your application with gunicorn
4. Provide you with a public URL

## Files Created for Deployment

The following files were created/modified for Render deployment:

- **`Procfile`**: Tells Render how to start your application
- **`render.yaml`**: Optional configuration file for advanced settings
- **`app.py`**: Modified to disable debug mode for production

## API Endpoints

Once deployed, your application will be available at:
- `https://your-app-name.onrender.com/get-active-coins-urls`
- `https://your-app-name.onrender.com/get-active-buy-urls`
- `https://your-app-name.onrender.com/get-active-converter-urls`

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check that all dependencies in `requirements.txt` are correct
2. **App Crashes**: Check the logs in the Render dashboard
3. **Slow Cold Starts**: This is normal on the free plan - consider upgrading for better performance

### Monitoring:

- Check the "Logs" tab in your Render dashboard for real-time logs
- Monitor the "Metrics" tab for performance data

## Free Plan Limitations

- Apps sleep after 15 minutes of inactivity
- Cold starts can take 30+ seconds
- Limited to 750 hours per month
- No custom domains on free plan

## Upgrading to Production

For production use, consider:
- Upgrading to a paid plan for better performance
- Setting up a custom domain
- Adding monitoring and alerting
- Implementing proper logging

## Security Notes

- Your app makes external API calls to `mudrex.com`
- No sensitive data is stored or processed
- The app is read-only and doesn't handle user input beyond API requests
