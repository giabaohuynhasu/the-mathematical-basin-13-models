import os
import pypdf
import sys

root = r'G:\Drive của tôi'

with open('all_drive_pdfs.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

results = []

for line in lines:
    parts = line.split(' | ')
    size = int(parts[0].replace('bytes', '').strip())
    rel_path = parts[1].strip()
    full_path = os.path.join(root, rel_path)

    # Filter out obvious non-papers
    lower_path = rel_path.lower()
    if any(skip in lower_path for skip in ['cv', 'resume', 'transcript', 'application', 'fee_waiver', 'recommendation', 'libguides', 'dossier', 'apa_how_to', 'teaching and learning']):
        continue

    # Attempt to read first page text
    title = os.path.splitext(os.path.basename(rel_path))[0]
    first_page_snippet = ""
    is_authored = False
    author_found = ""
    
    try:
        reader = pypdf.PdfReader(full_path)
        if len(reader.pages) > 0:
            text = reader.pages[0].extract_text() or ""
            first_page_snippet = text[:400].replace('\n', ' ')
            if "gia bao huynh" in text.lower() or "huynh bao" in text.lower() or "huynhbao@asu.edu" in text.lower() or "0009-0008-2372-5852" in text.lower():
                is_authored = True
                author_found = "Gia Bao Huynh"
            elif "arizona state university" in text.lower():
                is_authored = True
                author_found = "ASU"
    except Exception as e:
        first_page_snippet = f"Error reading PDF: {e}"

    results.append({
        'path': rel_path,
        'size': size,
        'title': title,
        'is_authored': is_authored,
        'author_found': author_found,
        'snippet': first_page_snippet
    })

print(f"Total evaluated candidate papers: {len(results)}")
authored = [r for r in results if r['is_authored']]
print(f"Explicitly verified authored by Gia Bao Huynh: {len(authored)}")

with open('corpus_inventory_full.txt', 'w', encoding='utf-8') as out:
    for r in results:
        status = "[AUTHORED]" if r['is_authored'] else "[UNCONFIRMED/OTHER]"
        out.write(f"{status} {r['path']} ({r['size']} bytes)\n")
        out.write(f"   Snippet: {r['snippet'][:200]}\n\n")

print("Saved to corpus_inventory_full.txt")
