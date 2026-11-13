# Base de Conhecimento: Migração SAP ECC para SAP S/4HANA

Este repositório contém uma base de conhecimento completa, altamente técnica e estruturada em formato **Wiki Interativa (MkDocs Material)** e **Manual Técnico em PDF Único**, desenvolvida especificamente para consultores e arquitetos que dominam o SAP legado (ECC 6.0 / R/3) e estão liderando ou executando a transição para o **SAP S/4HANA**.

---

## 🎯 Arquitetura da Wiki

A documentação segue uma estrutura modular com 15 capítulos detalhados:

```text
docs/
├── index.md                          # Visão geral, mapa mental e guia de leitura rápida
├── 01-fundamentos/
│   ├── o-que-e-s4hana.md             # Evolução do R/3 e ECC para o S/4HANA, modelos On-Premise vs Cloud (RISE/GROW)
│   ├── arquitetura-hana.md           # Banco in-memory, colunar vs relacional tradicional, compressão e HTAP
│   └── sap-btp-e-clean-core.md       # Barramento SAP BTP, APIs OData/REST e paradigma de Clean Core
├── 02-de-para-tecnico/
│   ├── universal-journal-acdoca.md   # Unificação FI/CO/AA/ML, tabelas eliminadas e Compatibility Views
│   ├── logistica-matdoc-sd.md        # Tabela MATDOC (substituindo MKPF/MSEG) e eliminação de VBUK/VBUP em SD
│   ├── business-partner-cvi.md       # Unificação de Clientes/Fornecedores na transação BP e processo de CVI
│   └── fiori-vs-sap-gui.md           # Fiori Launchpad, Business Roles, Fiori Apps Library e tabela De-Para
├── 03-estrategias-e-ferramentas/
│   ├── abordagens-migracao.md        # Comparativo Brownfield (System Conversion), Greenfield e Selective Data
│   ├── metodologia-sap-activate.md   # Fases do Activate (Discover, Prepare, Explore, Realize, Deploy, Run) vs ASAP
│   └── kit-ferramentas.md            # SAP Readiness Check, Migration Cockpit (LTMC) vs LSMW, ATC e SUM/DMO
├── 04-casos-reais-e-licoes/
│   ├── experiencias-clientes.md      # Casos reais de migração, gargalos de dados mestres, performance e prazos
│   └── checklist-sobrevivencia.md    # Checklist prático para reuniões de Fit-to-Standard e levantamento
└── 05-referencias/
    ├── glossario-e-conceitos.md      # Explicação resumida de termos periféricos (AnyDB, ETL, RFC, IDoc, CDS Views)
    └── links-oficiais.md             # Diretório curado de portais SAP Help, Simplification List e Roadmaps
```

---

## 📋 Padrão Editorial Mandatório dos Artigos

Cada artigo técnico obedece rigorosamente ao padrão estabelecido na skill local `.agents/skills/sap-wiki-standard/SKILL.md`:
1. **Contexto no SAP ECC**: como a regra e as tabelas funcionavam no ambiente legado.
2. **O que mudou no SAP S/4HANA**: nova arquitetura física, lógica e funcional.
3. **Impacto prático na migração e armadilhas reais de projetos**: impactos no código customizado (Z), no negócio e erros impeditivos de cutover.
4. **Tabela de referências cruzadas**: links relativos entre os artigos da Wiki e links oficiais canônicos da SAP (Notas canônicas e Simplification Catalog).

---

## 🚀 Como Executar Localmente

### 1. Pré-Requisitos
- Python 3.10+ instalado
- Google Chrome ou Microsoft Edge (para exportação em PDF)

### 2. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar o Servidor de Documentação com Live-Reload
```bash
mkdocs serve
```
Acesse a Wiki interativa no seu navegador em: `http://127.0.0.1:8000`

---

## 📄 Como Exportar para PDF Único

Para compilar toda a base de conhecimento em um único manual PDF consolidado (com capa corporativa, índice e estilos de impressão):
```bash
python export_pdf.py
```
O arquivo gerado estará disponível na raiz como:  
**`Guia_Definitivo_Migracao_SAP_S4HANA.pdf`** (~59 páginas, alta definição).

---

## ☁️ Deploy no Cloudflare Pages

### Opção 1: Via Dashboard do Cloudflare Pages (Conectado ao GitHub/GitLab)
1. Conecte o repositório Git no Cloudflare Pages.
2. Em **Build settings**, configure:
   - **Framework preset**: `None`
   - **Build command**: `pip install -r requirements.txt && mkdocs build`
   - **Build output directory**: `site`
   - **Root directory**: `/`
3. Clique em **Save and Deploy**. O Cloudflare Pages compilará e servirá o site globalmente via CDN ultrarrápida.

### Opção 2: Via GitHub Actions
O repositório já inclui o fluxo pronto em `.github/workflows/deploy.yml`. Basta configurar no repositório os segredos `CLOUDFLARE_API_TOKEN` e `CLOUDFLARE_ACCOUNT_ID`.
