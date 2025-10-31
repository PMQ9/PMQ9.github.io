# Connor Pham - Personal Portfolio Website

A professional single-page portfolio website showcasing my experience in embedded systems, AI safety, and cyber-physical systems.

## Features

- **Responsive Design**: Built with Bootstrap 5 for mobile, tablet, and desktop optimization
- **Modern UI**: Clean, professional design with smooth animations and transitions
- **Fast Navigation**: Quick links to all sections with active highlighting
- **Project Showcase**: Detailed descriptions of 6 featured projects with tech stacks
- **Skills Display**: Organized by category with visual badges
- **Contact Links**: Easy access to email, GitHub, and LinkedIn

## Sections

- **About**: Professional summary, education, and key strengths
- **Skills**: Technical skills organized by category (Programming, Embedded Systems, AI/ML, DevOps, Tools, Standards)
- **Projects**: Featured work with GitHub links and tech stacks
- **Contact**: Direct links to reach out

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Hosting**: GitHub Pages

## Local Development

To run locally:

```bash
# Clone the repository
git clone https://github.com/PMQ9/PMQ9.github.io.git
cd PMQ9.github.io

# Open in a local server (Python)
python -m http.server 8000

# Or use any other local server
# Then visit http://localhost:8000
```

## GitHub Pages Configuration

This site is automatically deployed via GitHub Pages. See [GitHub Pages Setup](#github-pages-setup) below.

### GitHub Pages Setup

1. **Repository Settings**
   - Go to your repository: `https://github.com/PMQ9/PMQ9.github.io`
   - Click **Settings** → **Pages**
   - Under "Build and deployment":
     - Source: Select `Deploy from a branch`
     - Branch: Select `main` (or your default branch)
     - Folder: Select `/ (root)`
   - Click **Save**

2. **Wait for Deployment**
   - GitHub will automatically build and deploy your site
   - You'll see a message: "Your site is live at `https://pmq9.github.io`"
   - It may take a few minutes for changes to appear

3. **Custom Domain (Optional)**
   - If you have a custom domain, add it in the "Custom domain" field under Pages settings
   - Update your domain's DNS settings to point to GitHub Pages

### File Structure

```
PMQ9.github.io/
├── index.html          # Main page
├── styles.css          # Custom styling
├── script.js           # JavaScript interactions
├── README.md           # This file
└── .github/
    └── workflows/      # (Optional) CI/CD workflows
```

## Deployment

The site is deployed automatically when you push to the `main` branch:

```bash
# Make changes locally
git add .
git commit -m "Update portfolio"
git push origin main
```

Your changes will be live at `https://pmq9.github.io` within a few minutes.

## Customization

### Colors

Edit the CSS variables in `styles.css`:

```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --accent-color: #17a2b8;
    --dark-color: #212529;
    --light-color: #f8f9fa;
}
```

### Content

Edit `index.html` to update:
- Hero section text
- About section content
- Skills and categories
- Project descriptions and links

### Responsive Design

The site is fully responsive with breakpoints at:
- `768px` (tablet)
- `576px` (mobile)

## Performance Optimization

The site uses:
- CDN-hosted Bootstrap and Font Awesome for faster loading
- Minimal custom CSS for quick rendering
- Lazy loading for images (future enhancement)
- Print-friendly styles

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

MIT License - Feel free to use this template for your own portfolio

## Contact

- Email: [phamminhquang289@gmail.com](mailto:phamminhquang289@gmail.com)
- GitHub: [@PMQ9](https://github.com/PMQ9)
- LinkedIn: [Connor Pham](https://www.linkedin.com/in/connor-pham-2b7a6a1b9/)

---

**Last Updated**: October 2024