# Catálogo de Apps Streamlit DGB

Catálogo automatizado de todas as aplicações Streamlit da Plataforma DGB (Destaques do Governo Brasileiro).

🌐 **[Ver Catálogo](https://destaquesgovbr.github.io/streamlit-catalog/)**

## Sobre

Este repositório gera automaticamente um catálogo visual de todos os apps Streamlit desenvolvidos na organização `destaquesgovbr`. O catálogo é atualizado diariamente e publicado via GitHub Pages.

## Como Funciona

1. **Descoberta Automática**: O script `fetch_app_metadata.py` busca todos os repositórios que começam com `streamlit-` na organização
2. **Extração de Metadados**: Para cada repositório, extrai o arquivo `.streamlit-app.yaml` que contém informações sobre o app
3. **Geração do Site**: O script `generate_site.py` cria uma página HTML estática com todos os apps
4. **Publicação**: O GitHub Pages serve o catálogo em `https://destaquesgovbr.github.io/streamlit-catalog/`

## Estrutura do Repositório

```
streamlit-catalog/
├── .github/
│   └── workflows/
│       └── generate-catalog.yml  # Workflow para atualização automática
├── scripts/
│   ├── fetch_app_metadata.py    # Busca metadados dos apps
│   └── generate_site.py          # Gera o site HTML
├── data/
│   └── apps.json                 # Metadados dos apps (gerado)
├── index.html                    # Página do catálogo (gerado)
└── README.md
```

## Funcionalidades do Catálogo

- **Busca em Tempo Real**: Filtre apps por nome, descrição ou palavras-chave
- **Filtro por Categoria**: Veja apps de categorias específicas (analytics, visualization, etc.)
- **Informações Completas**: Nome, descrição, owner, tags, stars, e links
- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Tema DGB**: Cores oficiais do Design System do Governo

## Como Adicionar Seu App ao Catálogo

Para que seu app apareça no catálogo, ele deve:

1. **Estar na organização `destaquesgovbr`**
2. **Nome começar com `streamlit-`** (ex: `streamlit-my-app`)
3. **Ter um arquivo `.streamlit-app.yaml`** na raiz do repositório com a seguinte estrutura:

```yaml
name: "Nome da Aplicação"
description: "Breve descrição do que o app faz"
owner:
  name: "Nome do Time/Pessoa"
  email: "owner@example.com"
category: "analytics"  # analytics, visualization, exploration, admin
tags:
  - "tag1"
  - "tag2"
keywords: "palavras, chave, busca"
icon: "📊"
version: "1.0.0"
repository: "https://github.com/destaquesgovbr/streamlit-my-app"
documentation: "https://url-do-app.run.app"
```

O catálogo será atualizado automaticamente no próximo ciclo (diariamente às 6h UTC).

## Atualização Manual

Para forçar uma atualização do catálogo:

1. Vá em [Actions](https://github.com/destaquesgovbr/streamlit-catalog/actions)
2. Selecione o workflow "Generate Catalog"
3. Clique em "Run workflow"

## Desenvolvimento Local

Para testar a geração do catálogo localmente:

```bash
# Instalar dependências
pip install PyYAML requests jinja2

# Buscar metadados (requer GH_TOKEN)
export GH_TOKEN=your_github_token
python scripts/fetch_app_metadata.py

# Gerar site
python scripts/generate_site.py

# Abrir index.html no navegador
open index.html
```

## Tecnologias

- **Python 3.11**: Scripts de geração
- **GitHub Actions**: Automação
- **GitHub Pages**: Hospedagem
- **Jinja2**: Template engine
- **PyYAML**: Parse de metadados
- **GitHub API**: Descoberta de repositórios

## Contribuindo

Este repositório é gerado automaticamente. Se você encontrar problemas:

1. Verifique se o arquivo `.streamlit-app.yaml` do seu app está correto
2. Abra um issue neste repositório se houver problemas com os scripts de geração

## Licença

AGPL-3.0 License - ver [LICENSE](LICENSE) para detalhes.

## Links

- [Plataforma Streamlit DGB](https://github.com/destaquesgovbr/destaquesgovbr-infra)
- [Boilerplate Template](https://github.com/destaquesgovbr/streamlit-boilerplate)
- [Documentação](https://github.com/destaquesgovbr/destaquesgovbr-infra/blob/main/docs/streamlit-platform.md)
