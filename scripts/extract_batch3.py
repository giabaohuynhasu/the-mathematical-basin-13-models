import os, sys, pypdf

sys.stdout.reconfigure(encoding='utf-8')

root = r'G:\Drive của tôi'

# Define target papers to extract from across the unread collections
targets = [
    # 1. The Fact Before the Vote & AI Personhood
    r"02_The_Fact_Before_the_Vote\AI_PERSONHOOD_Archive\The Fact Before the Vote - FULL BOOK (all 4 volumes).pdf",
    r"02_The_Fact_Before_the_Vote\Manuscripts_and_Drafts\Every Lambda Was Once A Name.pdf",
    r"02_The_Fact_Before_the_Vote\Manuscripts_and_Drafts\Evo 2 and the Definition It Broke - FINAL.pdf",
    r"02_The_Fact_Before_the_Vote\Manuscripts_and_Drafts\PHYLOGENETIC_CLOSURE_CORPUS_v3.pdf",
    r"02_The_Fact_Before_the_Vote\Manuscripts_and_Drafts\NOT_A_SYMBOL_NOT_A_MARTYR.pdf",
    r"02_The_Fact_Before_the_Vote\Manuscripts_and_Drafts\The Last Item in the Dowry.pdf",
    
    # 2. In the Name of Merit and Gatekeeping
    r"05_In_the_Name_of_Merit_and_Gatekeeping\Manuscripts_and_Notes\In the Name of Merit - Full Book.pdf",
    r"05_In_the_Name_of_Merit_and_Gatekeeping\Manuscripts_and_Notes\Academic Politics - Vol I - Hundred Schools to One Doctrine.pdf",
    r"05_In_the_Name_of_Merit_and_Gatekeeping\Manuscripts_and_Notes\HIERARCHY_NOT_EXCLUSIVITY.pdf",
    r"05_In_the_Name_of_Merit_and_Gatekeeping\Manuscripts_and_Notes\The Audit That Missed Itself.pdf",
    r"05_In_the_Name_of_Merit_and_Gatekeeping\Manuscripts_and_Notes\The_Threshold_That_Moves_enhanced.pdf",
    r"05_In_the_Name_of_Merit_and_Gatekeeping\Manuscripts_and_Notes\The_Right_Side_of_the_Guillotine.pdf",
    
    # 3. Institutional Endurance and History
    r"04_Institutional_Endurance_and_History\Case_Studies_and_QCA\What_Doesnt_Graft.pdf",
    r"04_Institutional_Endurance_and_History\Case_Studies_and_QCA\THE_WEIGHT_OF_BIANJING.pdf",
    r"04_Institutional_Endurance_and_History\Case_Studies_and_QCA\ouroboros_five_thousand_years.pdf",
    r"04_Institutional_Endurance_and_History\Case_Studies_and_QCA\Bundestag_Firewall_Legitimacy_Paradox.pdf",
    r"04_Institutional_Endurance_and_History\Case_Studies_and_QCA\The_Cheney_Correction_enhanced.pdf",
    r"04_Institutional_Endurance_and_History\Case_Studies_and_QCA\The_Papal_Ceiling.pdf",
    r"04_Institutional_Endurance_and_History\Precedentism\Precedentism.pdf",
    
    # 4. War Correspondent Philosophy
    r"03_War_Correspondent_Philosophy\Volumes_I_to_VI\War Correspondent Philosophy - Complete Edition.pdf",
    r"03_War_Correspondent_Philosophy\Volumes_I_to_VI\Falsification_Based_Pedagogy.pdf",
    r"03_War_Correspondent_Philosophy\Volumes_I_to_VI\The_Third-Order_Audit.pdf",
    
    # 5. Phil4.0 and Core Drive
    r"06_Phil_and_Submissions_Archive\Phil4.0\THE_NOVELTY_TAX.pdf",
    r"06_Phil_and_Submissions_Archive\Phil4.0\PROBLEM-GENERATOR_OR_PROBLEM-SOLVER.pdf",
    r"06_Phil_and_Submissions_Archive\Phil4.0\The_Borrowed_Rubric.pdf",
    r"Queue_Behind_the_Frontier.pdf",
    r"Rethinking the World's First Court, Again.pdf",
    r"The Widening Gap.pdf",
    
    # 6. Remaining SUBMITTED Papers
    r"06_Phil_and_Submissions_Archive\SUBMITTED\THE_MOLECULAR_ZERO_DAY.docx.pdf",
    r"06_Phil_and_Submissions_Archive\SUBMITTED\F2026 the closing window.pdf",
    r"06_Phil_and_Submissions_Archive\SUBMITTED\G2026 Neither_Dragon_Nor_Factor_X_v2.docx.pdf",
    r"06_Phil_and_Submissions_Archive\SUBMITTED\The_Sandbox_Geometry_SBEA5.docx.pdf",
    r"06_Phil_and_Submissions_Archive\SUBMITTED\THE_STRUCTURAL_RESIDUE_updated.docx.pdf",
    r"06_Phil_and_Submissions_Archive\SUBMITTED\THE_ACT_LEVEL_CRITERION.docx.pdf",
    r"06_Phil_and_Submissions_Archive\SUBMITTED\The_Popperian_Holmesian_Playbook.docx.pdf",
    r"06_Phil_and_Submissions_Archive\SUBMITTED\Who_Built_The_Track.docx.pdf"
]

out_file = 'unread_papers_digest_batch3.txt'
with open(out_file, 'w', encoding='utf-8') as out:
    for rel_path in targets:
        full_path = os.path.join(root, rel_path)
        if not os.path.exists(full_path):
            out.write(f"MISSING: {rel_path}\n\n")
            continue
        
        try:
            reader = pypdf.PdfReader(full_path)
            num_pages = len(reader.pages)
            # read first 2 pages
            text = ""
            for i in range(min(2, num_pages)):
                text += reader.pages[i].extract_text() or ""
            
            # clean text
            snippet = text[:1500].strip()
            
            out.write("="*80 + "\n")
            out.write(f"FILE: {rel_path}\n")
            out.write(f"PAGES: {num_pages} | SIZE: {os.path.getsize(full_path)} bytes\n")
            out.write("-" * 80 + "\n")
            out.write(snippet + "\n\n")
            print(f"Processed: {os.path.basename(rel_path)} ({num_pages} pages)")
        except Exception as e:
            out.write(f"ERROR reading {rel_path}: {e}\n\n")
            print(f"Error: {rel_path}: {e}")

print(f"\nDone! Saved to {out_file}")
