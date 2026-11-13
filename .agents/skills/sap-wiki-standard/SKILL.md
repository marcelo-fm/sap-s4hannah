---
name: sap-wiki-standard
description: Padrão arquitetural e editorial para a documentação técnica de migração do SAP ECC para SAP S/4HANA. Define a estrutura obrigatória em 4 seções para todos os artigos técnicos da Wiki, diretrizes de tom de voz (focado em consultores seniores de ECC em transição), convenções de código/tabelas e boas práticas para MkDocs Material e exportação em PDF.
version: 1.0.0
author: Soluções SAP & Engenharia de Documentação Técnica
tags: [SAP, S/4HANA, ECC, Migração, Arquitetura, Documentação, MkDocs]
---

# Padrão de Redação Técnica: Wiki de Migração SAP ECC para SAP S/4HANA

Este padrão define a estrutura mandatória, o tom editorial e as convenções técnicas para todos os artigos criados na base de conhecimento de migração SAP ECC -> SAP S/4HANA.

## Público-Alvo e Tom Editorial
- **Público**: Consultores funcionais e técnicos experientes em SAP ECC (R/3, NetWeaver, tabelas legadas como BKPF/BSEG, MSEG, KNA1/LFA1, etc.) que estão liderando ou participando de projetos de migração para o SAP S/4HANA.
- **Tom de voz**: Técnico, direto ao ponto, pragmático e focado na realidade de projetos (evitar marketing corporativo superficial). Destacar "o que realmente quebra", decisões de arquitetura e mitigação de riscos.

---

## Estrutura Mandatória de Cada Artigo

Todo documento técnico em `docs/` deve conter, no mínimo, as seguintes 4 seções principais:

### 1. Contexto no SAP ECC (Como Funcionava Antes)
- Explicação do modelo legado no ERP clássico (R/3 / ECC 6.0).
- Tabelas envolvidas (ex: BSEG, BSIS, BSAS, FAGLFLEXA, MKPF, MSEG, VBUK, VBUP, etc.).
- Transações tradicionais (ex: XD01, XK01, MB01, MB1C, FS00, etc.).
- Gargalos arquiteturais inerentes ao modelo relacional antigo (tabelas de índices, agregados, reconciliações batch noturnas, redundância de dados, bloqueios de tabela).

### 2. O Que Mudou no SAP S/4HANA (Arquitetura e Conceito)
- Nova arquitetura simplificada proporcionada pelo SAP HANA in-memory.
- Novas tabelas centrais (ex: ACDOCA, MATDOC, BUT000, etc.) e eliminação de agregados.
- Visões de Compatibilidade (*Compatibility Views* / CDS Views de redirecionamento) para compatibilidade de leitura do código customizado (Z*).
- Nova experiência de usuário e paradigmas (SAP Fiori, Core Data Services, Clean Core, BTP).

### 3. Impacto Prático na Migração e Armadilhas Reais de Projetos
- **Impacto no Código Custom (Z / Y)**: Instruções SELECT diretas, INSERTs em tabelas que viraram views, performance e sintaxe SQL moderna.
- **Impacto nos Processos de Negócio**: Mudança na rotina dos usuários finais, fechamento contábil acelerado, novos fluxos de autorização (Business Roles).
- **Armadilhas de Projeto (*Gotchas*)**:
  - Dados inconsistentes no ECC que impedem a migração (ex: saldos contábeis não reconciliados, inconsistências de CVI entre cliente e fornecedor).
  - Prazos de downtime durante o SUM/DMO e conversão de dados.
  - Testes de regressão e armadilhas de autorizações/segurança no Fiori.

### 4. Tabela de Referências Cruzadas
- **Links Internos**: Conexões com outros tópicos relevantes da wiki (usando caminhos relativos Markdown como `[ACDOCA](../02-de-para-tecnico/universal-journal-acdoca.md)`).
- **Links Externos Oficiais SAP**: SAP Notes canônicas, Guias de Simplificação (*Simplification Item Catalog*), SAP Help Portal e Best Practices.

---

## Convenções de Formatação (MkDocs Material & PDF)
1. **Admonitions**: Use blocos estilizados do MkDocs Material para destacar pontos críticos:
   - `!!! danger "Atenção Crítica / Risco de Projeto"`: Para erros que paralisam a migração ou corrompem dados.
   - `!!! warning "Alerta de Migração"`: Para impactos em código Z ou mudanças de comportamento.
   - `!!! tip "Dica de Arquiteto"`: Para boas práticas e atalhos consolidados de projeto.
   - `!!! note "Nota de Versão"`: Para diferenças entre releases S/4HANA (ex: 1809, 2020, 2022, 2023).
2. **Diagramas**: Utilizar Mermaid (`mermaid`) para desenhar fluxos, arquiteturas e De-Para de tabelas.
3. **Compatibilidade com PDF**:
   - Evitar quebras inadequadas em tabelas e caixas de texto.
   - Usar títulos semânticos (`#`, `##`, `###`) bem nivelados.
   - Usar caminhos relativos válidos em imagens e links.
