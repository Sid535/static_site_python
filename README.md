# static_site_python

A simple static site generator built from scratch in Python. It converts Markdown content into a fully linked, styled HTML website.

## Features
 
- Recursively converts a directory of Markdown files into HTML pages
- Supports headings, bold/italic text, links, images, blockquotes, unordered/ordered lists, and code blocks
- Uses a single `template.html` to wrap every generated page
- Configurable base path, so the same codebase works for local development and GitHub Pages deployment
- Mirrors the `content/` directory structure into the output directory which is `docs/`

### Local Development
 
Build the site with the default `/` base path and serve it locally at `http://localhost:8888`:
 
```bash
./main.sh
```
 
This will:
1. Copy everything from `static/` into `docs/`
2. Generate an HTML page for every Markdown file in `content/`
3. Start a local HTTP server serving the `docs/` directory
### Production Build (GitHub Pages)
 
```bash
./build.sh
```
 
This builds the site using `/static_site_python/` as the base path, matching this repo's GitHub Pages URL structure. The output is written to `docs/`, which is what GitHub Pages serves from on the `main` branch.
 
After building, commit and push the updated `docs/` directory to deploy:
 
```bash
git add docs/
git commit -m "Rebuild site"
git push
```
 
The live site is available at:
**https://sid535.github.io/static_site_python/**

## Base Path Configuration
 
Because GitHub Pages serves this project from a subdirectory (`/static_site_python/`) rather than the domain root, all internal links and asset references need a matching prefix. The base path is passed as a CLI argument to `main.py` from `build.sh`:
 
```bash
python3 src/main.py "/static_site_python/"
```
 
If no argument is provided, it defaults to `/`, which is correct for local development where the site is served from the root.


