import pdfplumber
import re
from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Extract text from PDF
def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(p.extract_text() for p in pdf.pages if p.extract_text())

# Split clauses by numbers (e.g. 1., 2.)
def segment_text(text):
    return re.split(r'\n(?=\d+\.)', text)

# Simplify each clause using summarization
def simplify_text(clause):
    if len(clause.split()) < 10:
        return clause  # Too short to simplify
    try:
        summary = summarizer(clause, max_length=60, min_length=15, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error simplifying clause: {e}"

# Main function to process the contract
def process_contract(file_path):
    print("Extracting text from PDF...")
    content = extract_text_from_pdf(file_path)
    print("Segmenting text into clauses...")
    clauses = segment_text(content)
    print(f"Found {len(clauses)} clauses.")

    for i, clause in enumerate(clauses, 1):
        print(f"\n🔹 Original Clause {i}:\n{clause.strip()}")
        simplified = simplify_text(clause)
        print(f"\n✅ Simplified Clause:\n{simplified}")
        print("-" * 60)

if _name_ == "_main_":
    process_contract("C:/project1/Sample.pdf")