"""PDF Handler — merge, split, and extract text from PDFs from the command line.

Examples:
    python pdf_handler.py merge a.pdf b.pdf c.pdf -o combined.pdf
    python pdf_handler.py split report.pdf -o pages/
    python pdf_handler.py split report.pdf --pages 2-5 -o excerpt.pdf
    python pdf_handler.py extract report.pdf            # prints text to stdout
    python pdf_handler.py extract report.pdf -o out.txt
"""

import argparse
import os
import sys

from pypdf import PdfReader, PdfWriter


def merge(inputs, output):
    writer = PdfWriter()
    for path in inputs:
        for page in PdfReader(path).pages:
            writer.add_page(page)
    with open(output, "wb") as f:
        writer.write(f)
    print(f"Merged {len(inputs)} file(s) into {output}")


def _parse_range(spec, total):
    """Turn '2-5' or '3' (1-indexed, inclusive) into a 0-indexed range."""
    if "-" in spec:
        start, end = spec.split("-", 1)
        start, end = int(start), int(end)
    else:
        start = end = int(spec)
    if start < 1 or end > total or start > end:
        raise ValueError(f"page range {spec} is out of bounds (1-{total})")
    return range(start - 1, end)


def split(input_path, output, pages=None):
    reader = PdfReader(input_path)
    total = len(reader.pages)

    if pages:
        # Write the selected range into a single output PDF.
        writer = PdfWriter()
        for i in _parse_range(pages, total):
            writer.add_page(reader.pages[i])
        with open(output, "wb") as f:
            writer.write(f)
        print(f"Wrote pages {pages} of {input_path} to {output}")
        return

    # No range: explode into one PDF per page inside the output directory.
    os.makedirs(output, exist_ok=True)
    stem = os.path.splitext(os.path.basename(input_path))[0]
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out = os.path.join(output, f"{stem}_page_{i}.pdf")
        with open(out, "wb") as f:
            writer.write(f)
    print(f"Split {input_path} into {total} page(s) in {output}/")


def extract(input_path, output=None):
    reader = PdfReader(input_path)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted text from {input_path} to {output}")
    else:
        print(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Merge, split, and extract text from PDFs.")
    sub = parser.add_subparsers(dest="command", required=True)

    m = sub.add_parser("merge", help="merge multiple PDFs into one")
    m.add_argument("inputs", nargs="+", help="input PDF files, in order")
    m.add_argument("-o", "--output", default="merged.pdf", help="output file")

    s = sub.add_parser("split", help="split a PDF into pages or extract a range")
    s.add_argument("input", help="input PDF file")
    s.add_argument("--pages", help="page range like 2-5 (1-indexed, inclusive)")
    s.add_argument("-o", "--output", required=True, help="output dir (per-page) or file (with --pages)")

    e = sub.add_parser("extract", help="extract text from a PDF")
    e.add_argument("input", help="input PDF file")
    e.add_argument("-o", "--output", help="write text to this file instead of stdout")

    args = parser.parse_args(argv)

    if args.command == "merge":
        merge(args.inputs, args.output)
    elif args.command == "split":
        split(args.input, args.output, args.pages)
    elif args.command == "extract":
        extract(args.input, args.output)


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
