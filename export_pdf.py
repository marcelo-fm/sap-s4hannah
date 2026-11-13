"""
Script de Exportação Automatizada da Wiki SAP S/4HANA para PDF Único.
Gera um documento HTML unificado com capa, índice e estilos corporativos,
e converte via Microsoft Edge ou Google Chrome Headless com qualidade gráfica nativa.
"""

import os
import sys
import re
import subprocess
import markdown

DOCS_DIR = os.path.join(os.path.dirname(__file__), 'docs')
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), 'Guia_Definitivo_Migracao_SAP_S4HANA.pdf')
TEMP_HTML = os.path.join(os.path.dirname(__file__), 'temp_unified_doc.html')

DOC_ORDER = [
    'index.md',
    '01-fundamentos/o-que-e-s4hana.md',
    '01-fundamentos/arquitetura-hana.md',
    '01-fundamentos/sap-btp-e-clean-core.md',
    '02-de-para-tecnico/universal-journal-acdoca.md',
    '02-de-para-tecnico/logistica-matdoc-sd.md',
    '02-de-para-tecnico/business-partner-cvi.md',
    '02-de-para-tecnico/fiori-vs-sap-gui.md',
    '03-estrategias-e-ferramentas/abordagens-migracao.md',
    '03-estrategias-e-ferramentas/metodologia-sap-activate.md',
    '03-estrategias-e-ferramentas/kit-ferramentas.md',
    '04-casos-reais-e-licoes/experiencias-clientes.md',
    '04-casos-reais-e-licoes/checklist-sobrevivencia.md',
    '05-referencias/glossario-e-conceitos.md',
    '05-referencias/links-oficiais.md'
]

CSS_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap');

@page {
    size: A4 portrait;
    margin: 20mm 15mm 20mm 15mm;
    @bottom-right {
        content: counter(page);
    }
}

body {
    font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1e293b;
    margin: 0;
    padding: 0;
}

/* Capa Corporativa */
.cover-page {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: linear-gradient(135deg, #001e3d 0%, #003366 50%, #005596 100%);
    color: #ffffff;
    padding: 40px;
    box-sizing: border-box;
    page-break-after: always;
}

.cover-title {
    font-size: 26pt;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 15px;
    line-height: 1.2;
}

.cover-subtitle {
    font-size: 14pt;
    font-weight: 300;
    color: #cbd5e1;
    margin-bottom: 40px;
    max-width: 80%;
}

.cover-badge {
    background-color: #f0ab00;
    color: #001e3d;
    font-weight: 700;
    font-size: 10pt;
    padding: 6px 18px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 30px;
}

.cover-footer {
    margin-top: 60px;
    font-size: 9pt;
    color: #94a3b8;
}

/* Títulos e Seções */
h1 {
    font-size: 18pt;
    color: #003366;
    border-bottom: 2px solid #003366;
    padding-bottom: 4px;
    margin-top: 30px;
    margin-bottom: 16px;
    page-break-before: always;
}

h2 {
    font-size: 13pt;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 3px;
    margin-top: 22px;
    margin-bottom: 12px;
    page-break-after: avoid;
}

h3 {
    font-size: 11pt;
    color: #334155;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
}

/* Tabelas */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}

th {
    background-color: #0f2744;
    color: #ffffff;
    text-align: left;
    padding: 8px 10px;
    font-weight: 600;
}

td {
    padding: 7px 10px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

/* Blocos de Alerta / Admonitions */
.admonition {
    border-left: 4px solid #003366;
    background-color: #f1f5f9;
    padding: 10px 14px;
    margin: 14px 0;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
}

.admonition-title {
    font-weight: 700;
    margin-bottom: 4px;
    color: #0f2744;
}

.admonition.danger {
    border-left-color: #dc2626;
    background-color: #fef2f2;
}

.admonition.danger .admonition-title {
    color: #991b1b;
}

.admonition.warning {
    border-left-color: #f59e0b;
    background-color: #fffbeb;
}

.admonition.warning .admonition-title {
    color: #92400e;
}

.admonition.tip {
    border-left-color: #10b981;
    background-color: #ecfdf5;
}

.admonition.tip .admonition-title {
    color: #065f46;
}

/* Código */
pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 10px 12px;
    border-radius: 4px;
    font-family: 'Roboto Mono', monospace;
    font-size: 8pt;
    overflow-x: auto;
    page-break-inside: avoid;
}

code {
    font-family: 'Roboto Mono', monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0f2744;
    padding: 1px 4px;
    border-radius: 3px;
}

pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
}

/* Diagramas Mermaid fallback para texto estruturado em impressão */
.mermaid {
    background-color: #f8fafc;
    border: 1px dashed #cbd5e1;
    padding: 10px;
    font-family: 'Roboto Mono', monospace;
    font-size: 7.5pt;
    margin: 10px 0;
    white-space: pre-wrap;
    border-radius: 4px;
}
"""

def clean_markdown_for_pdf(content):
    # Trata blocos de admonition do Material (!!! danger "Titulo")
    def replace_admonition(match):
        adm_type = match.group(1).lower()
        title = match.group(2)
        body = match.group(3)
        return f'<div class="admonition {adm_type}"><div class="admonition-title">{title}</div><p>{body.strip()}</p></div>\n'

    pattern = r'!!!\s+([a-zA-Z]+)\s+"([^"]+)"\n((?:\s{4}.*\n?)+)'
    content = re.sub(pattern, replace_admonition, content)
    
    # Corrige links internos para ficarem limpos no PDF impresso
    content = re.sub(r'\[([^\]]+)\]\([^)]+\.md(?:#[^)]*)?\)', r'**\1**', content)
    return content

def generate_unified_html():
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'def_list', 'toc'])
    unified_body = []
    
    # Capa
    cover_html = """
    <div class="cover-page">
        <div class="cover-badge">Manual de Engenharia de Transição</div>
        <div class="cover-title">Guia Definitivo de Migração<br>SAP ECC para SAP S/4HANA</div>
        <div class="cover-subtitle">Base de Conhecimento Técnica, Arquitetural e Prática para Consultores e Arquitetos de Soluções SAP</div>
        <div class="cover-footer">
            Versão 1.0 &bull; Compilação Oficial do Projeto &bull; Preparado para Cloudflare Pages & MkDocs Material
        </div>
    </div>
    """
    unified_body.append(cover_html)
    
    for doc_rel in DOC_ORDER:
        doc_path = os.path.join(DOCS_DIR, doc_rel)
        if not os.path.exists(doc_path):
            continue
        with open(doc_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        cleaned = clean_markdown_for_pdf(raw_text)
        rendered_html = md.convert(cleaned)
        md.reset()
        unified_body.append(f'<div class="chapter">\n{rendered_html}\n</div>')
        
    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Guia Definitivo de Migração SAP ECC para SAP S/4HANA</title>
    <style>
    {CSS_STYLES}
    </style>
</head>
<body>
    {''.join(unified_body)}
</body>
</html>"""

    with open(TEMP_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"HTML unificado gerado com sucesso em: {TEMP_HTML}")

def convert_html_to_pdf():
    # Detecta Edge ou Chrome
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    browser_exe = None
    for p in edge_paths + chrome_paths:
        if os.path.exists(p):
            browser_exe = p
            break
            
    if not browser_exe:
        print("Erro: Nenhum navegador (Edge/Chrome) encontrado para renderização do PDF.")
        return False
        
    print(f"Utilizando motor headless do navegador: {browser_exe}")
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUTPUT_PDF}",
        TEMP_HTML
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(OUTPUT_PDF) and os.path.getsize(OUTPUT_PDF) > 0:
        print(f"PDF consolidado gerado com sucesso: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF):,} bytes)")
        return True
    else:
        print("Falha ao gerar o PDF:", result.stderr)
        return False

if __name__ == '__main__':
    generate_unified_html()
    success = convert_html_to_pdf()
    if os.path.exists(TEMP_HTML):
        os.remove(TEMP_HTML)
    if not success:
        sys.exit(1)
