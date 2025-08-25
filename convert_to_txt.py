from pypdf import PdfReader
import re
import sys
from pathlib import Path

def extract_core_content(text):
    """
    Extract core content from Introduction/Prologue to final chapter/Epilogue/Conclusion
    """
    # Define start patterns (case insensitive)
    start_patterns = [
        r'\b(introduction|prologue|preface|chapter\s*1)\b',
        r'\bchapter\s*one\b',
        r'\bpart\s*i\b',
        r'\bsection\s*1\b'
    ]

    # Define end patterns (case insensitive)
    end_patterns = [
        r'\b(conclusion|epilogue|afterword|appendix|bibliography|references|index)\b',
        r'\bchapter\s*\d+\s*$',  # Last numbered chapter
        r'\bfinal\s*chapter\b'
    ]

    text_lower = text.lower()

    # Find start position
    start_pos = 0
    for pattern in start_patterns:
        match = re.search(pattern, text_lower)
        if match:
            start_pos = match.start()
            break

    # Find end position (search from the end backwards)
    end_pos = len(text)
    for pattern in end_patterns:
        matches = list(re.finditer(pattern, text_lower))
        if matches:
            # Take the last occurrence
            last_match = matches[-1]
            # Find the end of the section (next section start or end of text)
            section_end = text_lower.find('\n\n', last_match.end())
            if section_end == -1:
                section_end = len(text)
            end_pos = section_end
            break

    return text[start_pos:end_pos].strip()

def clean_text(text):
    """
    Clean extracted text by removing excessive whitespace and formatting artifacts
    """
    # Remove page numbers and headers/footers (common patterns)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)  # Standalone page numbers
    text = re.sub(r'\n\s*Page\s*\d+.*?\n', '\n', text, flags=re.IGNORECASE)

    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Multiple newlines to double
    text = re.sub(r' +', ' ', text)  # Multiple spaces to single

    # Remove common header/footer artifacts
    text = re.sub(r'\n\s*©.*?\n', '\n', text)  # Copyright lines
    text = re.sub(r'\n\s*www\..*?\n', '\n', text)  # Website URLs

    return text.strip()

def pdf_to_txt(pdf_path, output_path=None):
    """
    Convert PDF to TXT with core content extraction
    """
    try:
        # Open and read PDF
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)

            # Extract text from all pages
            # TODO: Consider grouping texts by chapters if possible
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text() + "\n"

        # Extract core content
        core_content = extract_core_content(full_text)

        # Clean the text
        cleaned_text = clean_text(core_content)

        # Determine output path
        if output_path is None:
            pdf_file = Path(pdf_path)
            output_path = pdf_file.with_suffix('.txt')

        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print(f"Successfully converted {pdf_path} to {output_path}")
        print(f"Extracted {len(cleaned_text)} characters of core content")

    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")

def main():
    """
    Main function to handle command line arguments
    """
    if len(sys.argv) < 2:
        print("Usage: python convert_to_txt.py <pdf_file> [output_file]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(pdf_file).exists():
        print(f"Error: File {pdf_file} not found")
        sys.exit(1)

    pdf_to_txt(pdf_file, output_file)

if __name__ == "__main__":
    main()