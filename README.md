# PDF Handler

A small command-line tool to **merge**, **split**, and **extract text** from PDFs.
One file, one dependency ([`pypdf`](https://pypi.org/project/pypdf/)).

## Install

```bash
pip install -r requirements.txt
```

## Usage

**Merge** several PDFs into one (order is preserved):

```bash
python pdf_handler.py merge a.pdf b.pdf c.pdf -o combined.pdf
```

**Split** a PDF into one file per page:

```bash
python pdf_handler.py split report.pdf -o pages/
# → pages/report_page_1.pdf, report_page_2.pdf, ...
```

**Split** out a page range into a single PDF (1-indexed, inclusive):

```bash
python pdf_handler.py split report.pdf --pages 2-5 -o excerpt.pdf
```

**Extract text** to stdout, or to a file:

```bash
python pdf_handler.py extract report.pdf
python pdf_handler.py extract report.pdf -o report.txt
```

## Commands

| Command | What it does |
|---------|--------------|
| `merge` | Concatenate multiple PDFs into one |
| `split` | Explode into per-page PDFs, or pull out a `--pages` range |
| `extract` | Pull text out of a PDF (stdout or `-o` file) |

## Notes

- Text extraction works on PDFs that contain a real text layer. Scanned/image
  PDFs need OCR first (e.g. `ocrmypdf`) — this tool won't read text off an image.
- Invalid page ranges and missing files fail with a clear error and a non-zero
  exit code, so it's safe to use in scripts.

## License

MIT © Apoorva Verma
