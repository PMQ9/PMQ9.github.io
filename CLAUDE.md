# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal portfolio website for Connor Pham, a software engineer specializing in embedded systems, AI safety, and cyber-physical systems. It's a **single-page application (SPA)** built with vanilla HTML, CSS, and JavaScript, hosted on GitHub Pages.

- **Repository**: `PMQ9/PMQ9.github.io` (GitHub Pages User Pages format)
- **Live Site**: https://pmq9.github.io
- **Hosting**: GitHub Pages (auto-deployed from main branch)

## Architecture

### Key Design Decisions

1. **Single Page Application (SPA)**: Uses smooth scrolling and anchor links (#home, #about, #skills, etc.) for navigation without page reloads
2. **Dark Mode Default**: Portfolio defaults to dark mode with localStorage persistence (`localStorage.setItem('theme', isDarkMode ? 'dark' : 'light')`)
3. **Bootstrap 5 Framework**: Responsive grid system with custom CSS overrides for theming
4. **CSS Variables**: Theme management uses CSS custom properties (--primary-color, --bg-primary, --text-primary, etc.) for easy customization
5. **No Build Process**: Pure HTML/CSS/JavaScript - no build tools, no dependencies except CDN-hosted frameworks

### File Structure

```
PMQ9.github.io/
├── index.html           # Main SPA page with all sections
├── styles.css           # Comprehensive styling with dark mode support
├── script.js            # SPA interactivity (smooth scroll, dark mode, animations)
├── README.md            # User-facing documentation
├── CLAUDE.md            # This file (developer guidance)
└── images/              # Award certificate images
    ├── q4_2024_spot_award.jpg
    ├── q3_2023_spot_award.jpg
    └── department_training.jpg
```

### Major Sections (in index.html)

1. **Hero Section** (`#home`): Name, title, location, social links
   - Layout: min-height auto, padding 3rem, compact design
   - Font sizes: h1 2.8rem, lead 1.1rem (reduced to save vertical space)

2. **About Section** (`#about`): Professional summary, education history
   - Education cards with university names, dates, and credentials

3. **Work Experience Section** (`#experience`): Career positions with descriptions
   - Current: Research Engineer at Institute for Software Integrated Systems (May 2025–Present)
   - Previous: Classroom Technology Staff at Vanderbilt IT (Feb–Aug 2025)
   - Main role: Embedded Software Engineer at Bosch Vietnam (Apr 2023–Dec 2024)
   - Features: Role descriptions, technologies, key achievements with badges

4. **Skills Section** (`#skills`): 6 skill categories with individual skill badges
   - Categories: Programming Languages, Embedded Systems, AI/ML, DevOps, Tools, Standards

5. **Achievements Section** (`#achievements`): Awards and research publications
   - **Awards Subsection**: 3 Bosch spot award certificates (images from `/images`)
   - **Publications Subsection**: 2 research papers with external links (ResearchGate and Springer)

6. **Projects Section** (`#projects`): 6 featured GitHub projects with descriptions and tech stacks
   - Each project includes: title, source link, brief description, tech badges

7. **Contact Section** (`#contact`): Links to email, GitHub, LinkedIn
   - Note: No generic resume link (user tailors resumes per position)

## Key Features & Implementation

### Dark Mode Toggle

**File**: script.js (lines 2-28)
- Button: `#theme-toggle` in navbar
- Icon changes: moon icon (light available) ↔ sun icon (dark available)
- State persisted in localStorage with key 'theme'
- Default: 'dark' mode on first visit
- CSS Variables automatically switch between light and dark palettes

**CSS Variables** (styles.css):
```css
:root {
    --bg-primary: #ffffff;      /* Light mode background */
    --text-primary: #212529;    /* Light mode text */
    --text-secondary: #6c757d;  /* Light mode secondary text */
}

body.dark-mode {
    --bg-primary: #1a1a2e;      /* Dark mode background */
    --text-primary: #e0e0e0;    /* Dark mode text (light gray) */
    --text-secondary: #b0b0b0;  /* Dark mode secondary (medium gray) */
}
```

**Critical Dark Mode Rules**:
- Use `!important` flags on dark mode color overrides (necessary for Bootstrap overrides)
- Apply colors to cards, text elements, and specific element types (p, h1-h6, etc.)
- Education cards need special handling: strong elements (#e0e0e0), paragraphs (#b0b0b0)
- Publication links in dark mode hover to #64b5f6

### Responsive Design

- **Tablet breakpoint**: 768px (Bootstrap 4 standard)
- **Mobile breakpoint**: 576px (Bootstrap 4 standard)
- Scroll-to-top button adapts size and position: 50px (desktop) → 45px (mobile)
- Nav toggles to hamburger menu at 992px (Bootstrap default)

### Animations

- **Page Load**: Cards fade in and slide up as user scrolls to them
- **Intersection Observer**: Used for scroll-triggered animations on project cards, education cards, and skill categories
- **Hover Effects**: Cards translateY(-5px to -8px), theme toggle rotates 20deg
- **Theme Toggle Animation**: Scroll-to-top button has @keyframes slideIn (0.3s)

## Development Workflow

### Local Testing

```bash
# Run local HTTP server (Python)
python -m http.server 8000

# Visit http://localhost:8000 in browser
```

### Deployment

- **Automatic**: Any push to `main` branch triggers GitHub Pages rebuild
- **No build step needed**: Static files deployed as-is
- **DNS**: Points to GitHub Pages (CNAME or A records)
- **Custom domain**: Optional, configured in GitHub Pages settings

```bash
git add .
git commit -m "Update portfolio"
git push origin main
# Site live at https://pmq9.github.io within minutes
```

### Private Repository Note

⚠️ **Important**: Making this repo private will **unpublish the GitHub Pages website** (with GitHub Free account). Only possible with GitHub Pro. Current setup requires public repo to keep website live.

## Important Git Workflow Note

⚠️ **CRITICAL**: Claude Code **cannot** execute `git add`, `git commit`, or `git push` commands. The user must perform these git operations manually in their terminal. When changes are made to files, inform the user that they need to commit and push the changes themselves.

## Common Customization Tasks

### Updating Content

- **Hero section**: Edit name, title, location in index.html lines 39-41
- **About section**: Modify summary and education cards in index.html lines 54-100
- **Experience section**: Work experience cards in index.html lines 95-175
- **Skills**: Add/remove categories and skill badges in index.html lines 177-256
- **Projects**: Update project cards, descriptions, and links in index.html lines 334-497
- **Contact**: Verify email, GitHub, LinkedIn links in index.html lines 513-521

### Updating Styling

- **Colors**: Edit CSS variables in styles.css lines 1-11 (light mode) and 14-19 (dark mode)
- **Dark mode specific rules**: Lines 21-153 in styles.css
- **Hero section sizing**: Lines 168-201 in styles.css (currently: h1 2.8rem, lead 1.1rem, padding 3rem)
- **Experience cards**: Lines 536-624 in styles.css (includes dark mode support for experience-card and highlight-badge)
- **Card hover effects**: Each card type has transform: translateY rules (project-card -5px, award-card -8px, experience-card -5px)

### Adding Award Images

1. Save JPG to `/images` folder with descriptive name
2. Reference in index.html award card: `<img src="images/filename.jpg" alt="Description">`
3. Images use max-height: 250px with object-fit: cover

### Adding Publications

- External links for research papers: ResearchGate and Springer URLs
- Publications structured with title (clickable), year badge, authors, description, and tags
- Link styling in dark mode: inherit color normally, #64b5f6 on hover

## Debugging Tips

### Text Not Visible in Dark Mode
- Check that dark mode CSS variables are applied with `!important` flags
- Verify element has explicit color rule in `body.dark-mode` selectors
- Common issue: Bootstrap default colors override without !important

### Hero Section Too Tall/Short
- Adjust: `min-height: auto` and `padding: 3rem 0` in .hero-section
- Font sizes: `h1 { font-size: 2.8rem }`, `.lead { font-size: 1.1rem }`

### Scroll-to-Top Button Not Appearing
- Script checks `window.pageYOffset > 300` (lines 66-82 in script.js)
- Button class: `scroll-to-top btn btn-primary`
- Check browser console for JS errors

### CSS Not Updating
- GitHub Pages may cache assets: Hard refresh (Ctrl+Shift+R) or clear cache
- Check that modified styles.css is properly committed and pushed

## Technologies

- **HTML5**: Semantic structure
- **CSS3**: Custom properties (variables), gradients, animations, media queries
- **JavaScript (Vanilla)**: No frameworks, uses modern APIs (localStorage, IntersectionObserver, classList)
- **Bootstrap 5**: CDN-hosted, responsive grid system
- **Font Awesome 6**: CDN-hosted icon library
- **Hosting**: GitHub Pages with automatic deployment
