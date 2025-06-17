# EcoGenomics Suite

A frontend demo of an Environmental & Genomic Analytics Platform.

## Project Structure

The project is organized as follows:
- `index.html`: Main entry point HTML file
- `assets/`: Contains all static assets
  - `assets/js/`: JavaScript files including notice_dialog.js

## Local Development

To run the project locally, you can use any static file server. For example:

```bash
# Using Python
python3 -m http.server

# Using Node.js and serve
npm install -g serve
serve .
```

## Deployment to Vercel

This project is configured to deploy on Vercel. To deploy:

1. Make sure you have the Vercel CLI installed:
```bash
npm install -g vercel
```

2. Deploy the project:
```bash
vercel
```

3. Follow the prompts to complete the deployment process.

The `vercel.json` file is configured to route all requests to the index.html file, ensuring that the application works correctly on Vercel's hosting platform.

## Features

- Environmental monitoring dashboard
- Genomic analytics visualization
- Interactive charts and heatmaps
- Demo login functionality (any username/password will work)
