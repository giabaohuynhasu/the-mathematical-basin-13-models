import os, sys, pypdf, re

sys.stdout.reconfigure(encoding='utf-8')

sub_dir = r"G:\Drive của tôi\06_Phil_and_Submissions_Archive\SUBMITTED"

selected_papers = [
    "THE_PERPETUAL_CORPORATION_v2.docx.pdf",
    "THE_FOURTH_FICTITIOUS_COMMODITY.docx.pdf",
    "The_Clock_Ibn_Khaldun_Assumed_enhanced.docx.pdf",
    "The_Sovereigns_Death_Warrant.docx.pdf",
    "The_Commission_As_Shogunate.docx.pdf",
    "The_Jiangnan_Genotype.docx.pdf",
    "THE_AUTOIMMUNE_MUNUS.docx.pdf",
    "THERMIDORS_RATCHET.docx.pdf",
    "sun-quan-unremembered-necessity.docx.pdf",
    "The_Speed_That_Costs_A_Demos.docx.pdf",
    "Biopower_Does_Not_Jump_Foucault_v2.docx.pdf",
    "The_Shadow_Over_The_Veil_Rawls.docx.pdf",
    "THE_EXCLUDABILITY_THRESHOLD.docx.pdf",
    "D2026 THE_BIOLOGICAL_ZERO_DAY_MECHANISM_2026d.pdf"
]

out_report = r"c:\Users\nswcl\.gemini\antigravity-ide\scratch\the-mathematical-basin-13-models\scripts\unread_papers_digest.txt"

with open(out_report, 'w', encoding='utf-8') as out_f:
    for fname in selected_papers:
        fpath = os.path.join(sub_dir, fname)
        if not os.path.exists(fpath):
            continue
        try:
            reader = pypdf.PdfReader(fpath)
            num_pages = len(reader.pages)
            first_text = ""
            for p in reader.pages[:2]: # first 2 pages
                first_text += p.extract_text() + "\n"
            first_text = re.sub(r'\s+', ' ', first_text).strip()
            out_f.write(f"\n{'='*70}\n")
            out_f.write(f"📄 PAPER: {fname} ({num_pages} pages)\n")
            out_f.write(f"{'='*70}\n")
            out_f.write(first_text[:2000] + "\n")
        except Exception as e:
            out_f.write(f"Error reading {fname}: {e}\n")

print(f"Digest written to {out_report}")
