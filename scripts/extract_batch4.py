import os, sys, pypdf

sys.stdout.reconfigure(encoding='utf-8')

root = r'G:\Drive của tôi'

targets = [
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\THE_BEST_CASE_ALREADY_FAILED_v2.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\THE_CALIBRATION_TRAP.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\THE_SEPARATION_THAT_DOESNT_REGISTER.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\THE_THIRD_LEG_THAT_NEVER_EXISTED_v4.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\THE_UNPROTECTED_FLOOR.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\The_Fertilizing_Question.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\The_Shape_of_the_Gap.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\two_clocks_v2.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\ARSILONGEVITYDOCTRINE.pdf",
    r"01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data\AI_DRIVEN_LONGEVITY_ECONOMICS_v2.pdf",
    r"01_Longevity_Asymmetry_and_LAC\LONGEVITYWAVE\When_Death_Becomes_Poverty.docx.pdf",
    r"01_Longevity_Asymmetry_and_LAC\LONGEVITYWAVE\Temporal_Estate.pdf"
]

out_file = 'unread_papers_digest_batch4.txt'
with open(out_file, 'w', encoding='utf-8') as out:
    for rel_path in targets:
        full_path = os.path.join(root, rel_path)
        if not os.path.exists(full_path):
            out.write(f"MISSING: {rel_path}\n\n")
            continue
        try:
            reader = pypdf.PdfReader(full_path)
            num_pages = len(reader.pages)
            text = ""
            for i in range(min(2, num_pages)):
                text += reader.pages[i].extract_text() or ""
            snippet = text[:1500].strip()
            out.write("="*80 + "\n")
            out.write(f"FILE: {rel_path}\n")
            out.write(f"PAGES: {num_pages} | SIZE: {os.path.getsize(full_path)} bytes\n")
            out.write("-" * 80 + "\n")
            out.write(snippet + "\n\n")
            print(f"Processed: {os.path.basename(rel_path)} ({num_pages} pages)")
        except Exception as e:
            out.write(f"ERROR reading {rel_path}: {e}\n\n")

print("Done batch 4!")
