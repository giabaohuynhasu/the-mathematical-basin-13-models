import os, sys, pypdf, re

sys.stdout.reconfigure(encoding='utf-8')

sub_dir = r"G:\Drive của tôi\06_Phil_and_Submissions_Archive\SUBMITTED"

second_batch = [
    "ACTUARIAL_BARE_LIFE.docx.pdf",
    "THE_MOLECULAR_ZERO_DAY.docx.pdf",
    "THE_OPTIONAL_DEATH.docx.pdf",
    "THE_GRIEVABILITY_GATE.docx.pdf",
    "THE_PRE_REGISTERED_AFTERLIFE.docx.pdf",
    "THE_SIEVE_NOT_THE_MOLD.docx.pdf",
    "The_Asset_And_The_Axiom.docx.pdf",
    "one_level_down.docx.pdf",
    "Equal_In_Death_fixed.docx.pdf",
    "A_Country_With_No_Land_fixed.docx.pdf",
    "Two_Arrows_One_Target_fixed.docx.pdf",
    "they_who_remain_v2.docx.pdf",
    "FALSIFIABILITY_AS_SELF_VACCINATION_v4.docx.pdf",
    "POPPER_AS_SELF_VACCINATION_v2.docx.pdf",
    "Endurance_Or_Density_ERI_v2.docx.pdf"
]

out_report = r"c:\Users\nswcl\.gemini\antigravity-ide\scratch\the-mathematical-basin-13-models\scripts\unread_papers_digest_batch2.txt"

with open(out_report, 'w', encoding='utf-8') as out_f:
    for fname in second_batch:
        fpath = os.path.join(sub_dir, fname)
        if not os.path.exists(fpath):
            continue
        try:
            reader = pypdf.PdfReader(fpath)
            num_pages = len(reader.pages)
            first_text = ""
            for p in reader.pages[:2]:
                first_text += p.extract_text() + "\n"
            first_text = re.sub(r'\s+', ' ', first_text).strip()
            out_f.write(f"\n{'='*70}\n")
            out_f.write(f"📄 PAPER: {fname} ({num_pages} pages)\n")
            out_f.write(f"{'='*70}\n")
            out_f.write(first_text[:2000] + "\n")
        except Exception as e:
            out_f.write(f"Error reading {fname}: {e}\n")

print(f"Batch 2 digest written to {out_report}")
