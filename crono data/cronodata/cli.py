
import typer
from pathlib import Path

app = typer.Typer(help="Cronodata ⚙️  pipeline completo")

@app.command()
def fetch(source: str):
    """Baixa acervos digitalizados (ex.: brasiliana, iib, ufrj)."""
    typer.echo(f"Simulando coleta da fonte: {source}")
    # TODO: chamar collectors.<source>.run()

@app.command()
def ocr(input_dir: str = "data/raw", output_dir: str = "data/interim"):
    """Aplica OCR em lote."""
    typer.echo(f"OCRizando PDFs de {input_dir} → {output_dir}")
    # TODO: implementar cronodata.ocr.pdf_ocr.batch

@app.command()
def index():
    """Constrói índice de busca."""
    typer.echo("Indexando documentos...")
    # TODO: cronodata.index.builder.build()

@app.command()
def classify(model: str = "ada_lovelace", infile: str = "data/processed/text.parquet"):
    """Classifica conceitos com LLM fine‑tuned."""
    typer.echo(f"Classificando {infile} usando modelo {model}")
    # TODO: cronodata.nlp.classifier.run()

if __name__ == "__main__":
    app()
