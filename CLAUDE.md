# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based portfolio/blog site using Minimal Mistakes remote theme. Hosted on GitHub Pages.

## Common Commands

```bash
# Install Ruby dependencies
bundle install

# Local development with live reload
bundle exec jekyll serve --livereload
# Or use the convenience script:
./bin/start.sh

# Build site (output to _site/)
bundle exec jekyll build

# Preview draft posts
bundle exec jekyll serve --drafts
```

### Python Environment (for Jupyter notebooks)

The `python-git-steven/` directory contains example notebooks referenced in blog posts.

```bash
# Install Python dependencies (Poetry required)
cd python-git-steven && poetry install

# Run Jupyter
poetry run jupyter lab
```

## Site Structure

- `_posts/` - Blog posts (markdown with YAML front matter)
- `_pages/` - Static pages (About, Projects, Archives)
- `_data/navigation.yml` - Site navigation menu
- `_config.yml` - Jekyll configuration and author metadata
- `assets/` - Images and static files
- `python-git-steven/` - Jupyter notebooks for blog post examples (PySpark, scikit-learn)

## Post Conventions

- Filename format: `YYYY-MM-DD-title-slug.md`
- Required front matter: `title`, `date`, `categories`
- Markdown processor: kramdown (GitHub-flavored markdown)
- Diagrams: Store `.drawio` files with posts; export using `draw.io.export <file>.drawio`

## Configuration Notes

- Theme skin: "dirt" (`_config.yml:30`)
- Pagination: 5 posts per page
- Default post layout includes: author profile, read time, comments, share buttons, related posts
