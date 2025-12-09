#!/usr/bin/env python3
"""
Generate static HTML catalog site from app metadata.

This script reads the apps.json file and generates an index.html page
with a searchable, filterable catalog of all Streamlit apps.
"""

import json
import os
from datetime import datetime
from jinja2 import Template


INPUT_FILE = "data/apps.json"
OUTPUT_FILE = "index.html"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Apps Streamlit - DGB</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #1351B4 0%, #071D41 100%);
            color: #333;
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .search-filter {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }

        .search-box {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .search-box input {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        .search-box input:focus {
            outline: none;
            border-color: #1351B4;
        }

        .filter-tags {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .filter-tag {
            padding: 0.5rem 1rem;
            background: #f5f5f5;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9rem;
        }

        .filter-tag:hover {
            background: #e0e0e0;
        }

        .filter-tag.active {
            background: #1351B4;
            color: white;
            border-color: #1351B4;
        }

        .stats {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            flex: 1;
            text-align: center;
        }

        .stat-card .number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1351B4;
        }

        .stat-card .label {
            color: #666;
            margin-top: 0.5rem;
        }

        .apps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }

        .app-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            display: flex;
            flex-direction: column;
        }

        .app-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        }

        .app-header {
            display: flex;
            align-items: start;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .app-icon {
            font-size: 3rem;
            line-height: 1;
        }

        .app-title {
            flex: 1;
        }

        .app-title h3 {
            color: #1351B4;
            font-size: 1.3rem;
            margin-bottom: 0.25rem;
        }

        .app-title .version {
            color: #999;
            font-size: 0.85rem;
        }

        .app-description {
            color: #666;
            line-height: 1.6;
            margin-bottom: 1rem;
            flex-grow: 1;
        }

        .app-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.85rem;
            color: #999;
            margin-bottom: 1rem;
        }

        .app-tags {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }

        .tag {
            padding: 0.25rem 0.75rem;
            background: #f0f2f5;
            border-radius: 12px;
            font-size: 0.8rem;
            color: #666;
        }

        .app-footer {
            display: flex;
            gap: 0.5rem;
            margin-top: auto;
        }

        .btn {
            flex: 1;
            padding: 0.75rem;
            border: none;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            transition: all 0.3s;
        }

        .btn-primary {
            background: #1351B4;
            color: white;
        }

        .btn-primary:hover {
            background: #0d3f8f;
        }

        .btn-secondary {
            background: #f5f5f5;
            color: #333;
        }

        .btn-secondary:hover {
            background: #e0e0e0;
        }

        .no-results {
            text-align: center;
            padding: 3rem;
            color: white;
            font-size: 1.2rem;
        }

        .footer {
            text-align: center;
            color: white;
            margin-top: 3rem;
            opacity: 0.8;
        }

        .category-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #1351B4;
            color: white;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Catálogo de Apps Streamlit</h1>
            <p>Plataforma DGB - Destaques do Governo Brasileiro</p>
        </header>

        <div class="search-filter">
            <div class="search-box">
                <input
                    type="text"
                    id="searchInput"
                    placeholder="Buscar apps por nome, descrição ou palavras-chave..."
                    onkeyup="filterApps()"
                >
            </div>
            <div class="filter-tags" id="categoryFilters"></div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="number">{{ apps|length }}</div>
                <div class="label">Aplicações</div>
            </div>
            <div class="stat-card">
                <div class="number" id="categoriesCount">{{ categories|length }}</div>
                <div class="label">Categorias</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ total_stars }}</div>
                <div class="label">Stars</div>
            </div>
        </div>

        <div class="apps-grid" id="appsGrid">
            {% for app in apps %}
            <div class="app-card" data-category="{{ app.category }}" data-tags="{{ app.tags|join(',') }}" data-keywords="{{ app.keywords }}">
                <div class="app-header">
                    <div class="app-icon">{{ app.icon }}</div>
                    <div class="app-title">
                        <h3>{{ app.name }}</h3>
                        <div class="version">v{{ app.version }}</div>
                    </div>
                </div>

                <div class="app-description">
                    {{ app.description }}
                </div>

                <div class="app-meta">
                    <span class="category-badge">{{ app.category }}</span>
                    <span>⭐ {{ app._stars }}</span>
                    <span>👤 {{ app.owner.name }}</span>
                </div>

                {% if app.tags %}
                <div class="app-tags">
                    {% for tag in app.tags %}
                    <span class="tag">{{ tag }}</span>
                    {% endfor %}
                </div>
                {% endif %}

                <div class="app-footer">
                    <a href="{{ app._repo_url }}" class="btn btn-secondary" target="_blank">Código</a>
                    <a href="{{ app.documentation }}" class="btn btn-primary" target="_blank">Abrir App</a>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="no-results" id="noResults" style="display: none;">
            Nenhum app encontrado com os filtros selecionados.
        </div>

        <footer class="footer">
            <p>Atualizado em {{ update_time }}</p>
            <p>Plataforma Streamlit DGB</p>
        </footer>
    </div>

    <script>
        // Initialize category filters
        const categories = {{ categories|tojson }};
        let activeCategory = null;

        const filtersContainer = document.getElementById('categoryFilters');
        categories.forEach(category => {
            const tag = document.createElement('div');
            tag.className = 'filter-tag';
            tag.textContent = category;
            tag.onclick = () => toggleCategory(category, tag);
            filtersContainer.appendChild(tag);
        });

        function toggleCategory(category, element) {
            if (activeCategory === category) {
                activeCategory = null;
                element.classList.remove('active');
            } else {
                document.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
                activeCategory = category;
                element.classList.add('active');
            }
            filterApps();
        }

        function filterApps() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.app-card');
            let visibleCount = 0;

            cards.forEach(card => {
                const category = card.dataset.category;
                const tags = card.dataset.tags.toLowerCase();
                const keywords = card.dataset.keywords.toLowerCase();
                const text = card.textContent.toLowerCase();

                const matchesCategory = !activeCategory || category === activeCategory;
                const matchesSearch = !searchTerm ||
                    text.includes(searchTerm) ||
                    tags.includes(searchTerm) ||
                    keywords.includes(searchTerm);

                if (matchesCategory && matchesSearch) {
                    card.style.display = 'flex';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            document.getElementById('noResults').style.display = visibleCount === 0 ? 'block' : 'none';
        }
    </script>
</body>
</html>
"""


def main():
    """Generate static site from app metadata."""
    print("Generating catalog site...\n")

    # Load app metadata
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run fetch_app_metadata.py first.")
        return

    with open(INPUT_FILE, "r") as f:
        apps = json.load(f)

    # Sort apps by name
    apps.sort(key=lambda x: x.get("name", "").lower())

    # Extract unique categories
    categories = sorted(list(set(app.get("category", "other") for app in apps)))

    # Calculate total stars
    total_stars = sum(app.get("_stars", 0) for app in apps)

    # Generate HTML
    template = Template(HTML_TEMPLATE)
    html = template.render(
        apps=apps,
        categories=categories,
        total_stars=total_stars,
        update_time=datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    )

    # Save to file
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  - {len(apps)} apps")
    print(f"  - {len(categories)} categories")
    print(f"  - {total_stars} total stars")


if __name__ == "__main__":
    main()
