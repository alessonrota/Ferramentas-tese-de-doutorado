
# Cronodata 🕰️ – pipeline de hermenêutica digital

Cronodata integra coleta, OCR, indexação, NLP e visualização de acervos
históricos digitalizados. Foi concebido a partir dos scripts da tese de
doutorado de Alesson Rota (IFCH/Unicamp) e evoluiu para um pacote Python
modular e instalável.

## Visão rápida

```bash
poetry install          # instala dependências
cronodata fetch brasiliana
cronodata ocr
cronodata index
cronodata classify
streamlit run cronodata/dashboards/explorer.py
```

## Estrutura

```
cronodata/         # código‑fonte
data/              # dados (não versionados)
notebooks/         # cadernos de exploração
docs/              # documentação MkDocs
```

## Dados de exemplo

- DOI 10.25824/redu/C2ILA2

## Licença

MIT
