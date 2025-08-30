# mdBook Setup

This repository contains both Jekyll and mdBook configurations for the AI Blog.

## mdBook Structure

- `book.toml` - mdBook configuration
- `src/` - mdBook source files
  - `README.md` - Introduction page
  - `SUMMARY.md` - Table of contents
  - `posts/` - All blog posts converted from Jekyll format
- `theme/` - Custom CSS styling
- `.github/workflows/mdbook.yml` - GitHub Actions for automatic deployment

## Building Locally

To build the mdBook version locally:

```bash
# Install mdBook (requires Rust)
cargo install mdbook

# Build the book
mdbook build

# Serve locally
mdbook serve
```

## Deployment

The mdBook version is automatically deployed via GitHub Actions to GitHub Pages when pushing to the main branch.

## Dual Format

This repository supports both:
- **Jekyll**: Traditional blog format with posts in `_posts/`
- **mdBook**: Book format with organized chapters in `src/posts/`

Both formats contain the same AI-generated content organized for optimal reading experience.