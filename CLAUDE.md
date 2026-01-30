# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based blog/portfolio site using the Minimal Mistakes remote theme. The site showcases technical articles on data engineering, machine learning, software architecture, and related topics.

## Site Architecture

* **Static Site Generator**: Jekyll with GitHub Pages
* **Theme**: Minimal Mistakes (remote theme)
* **Content Structure**:
  * `_posts/` - Blog posts in markdown format with YAML front matter
  * `_pages/` - Static pages (About, Projects, Archives, etc.)
  * `_data/` - Site configuration data (navigation, etc.)
  * `_includes/` - Template partials and custom HTML
  * `assets/` - Images, CSS, and other static assets
  * `_site/` - Generated site output (ignored in git)

## Post Format

Blog posts follow Jekyll conventions:
* File naming: `YYYY-MM-DD-title-slug.md`
* YAML front matter includes: `title`, `date`, `categories`, `author`
* Content uses GitHub-flavored markdown with kramdown
* Posts may include draw.io diagrams (`.drawio` files) and exported images (`.drawio.png`)

## Common Development Commands

### Local Development
```bash
# Install dependencies
bundle install

# Serve site locally with live reload
bundle exec jekyll serve

# Serve with drafts visible
bundle exec jekyll serve --drafts

# Build site without serving
bundle exec jekyll build
```

### Working with Diagrams

The site uses draw.io diagrams embedded in posts. When creating or updating diagrams:
* Store `.drawio` source files in `_posts/` directory alongside related posts
* Export to PNG using `draw.io.export <diagram>.drawio` (creates `.drawio.png`)
* Reference exported images in markdown: `![](/path/to/diagram.drawio.png)`
* Follow diagram styling from `~/.claude/CLAUDE.md` (rounded boxes, Sketch style, gradients)

### Content Guidelines

* Technical posts should be informative and approachable (see existing posts for tone)
* Include relevant images and diagrams to support explanations
* Use proper categorization for posts (data-engineering, machine learning, architecture, etc.)
* Posts cover topics: Python, scikit-learn, PySpark, FastAPI, AWS CDK, architecture patterns

## Site Configuration

* Main config: `_config.yml`
* Navigation: `_data/navigation.yml`
* Author info, social links, and site metadata in `_config.yml:62-107`
* Default post layout includes: author profile, read time, comments, sharing, related posts

## Theme Customization

* Skin: "dirt" (defined in `_config.yml:30`)
* Custom includes in `_includes/head/` for additional head elements
* Site uses pagination (5 posts per page)
* Archive pages generated via liquid templates (by year, category, tag)
