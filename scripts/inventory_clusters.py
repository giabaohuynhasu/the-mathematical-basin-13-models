import os, sys, pypdf

sys.stdout.reconfigure(encoding='utf-8')

targets = [
    r"G:\Drive của tôi\06_Phil_and_Submissions_Archive\SUBMITTED",
    r"G:\Drive của tôi\04_Institutional_Endurance_and_History",
    r"G:\Drive của tôi\01_Longevity_Asymmetry_and_LAC\Formal_Mechanisms_and_Data",
    r"G:\Drive của tôi\01_Longevity_Asymmetry_and_LAC\LONGEVITYWAVE",
    r"G:\Drive của tôi"
]

all_pdfs = {}

for target in targets:
    if not os.path.exists(target):
        continue
    for root, dirs, files in os.walk(target):
        # don't recurse too deep into node_modules or .git
        if '.git' in root or '.venv' in root:
            continue
        for f in files:
            if f.lower().endswith('.pdf'):
                f_low = f.lower()
                if any(k in f_low for k in ['resume', 'cv', 'transcript', 'application', 'screenshot']):
                    continue
                path = os.path.join(root, f)
                if path not in all_pdfs:
                    try:
                        sz = os.path.getsize(path)
                        all_pdfs[path] = (f, sz)
                    except:
                        pass

print(f"Total unique academic PDFs identified across all targets: {len(all_pdfs)}")

# Let's inspect abstracts / first page of key unread papers
# Group papers into clusters
clusters = {
    "Corporate & Economic Theory": ["perpetual_corporation", "fourth_fictitious", "excludability", "dose_reconstruction", "asset_and_the_axiom"],
    "Biological Mechanisms & Zero-Day": ["biological_zero_day", "molecular_zero_day", "closing_window", "patchable_body", "autoimmune_munus"],
    "Political Philosophy & Sovereignty": ["sovereigns_death_warrant", "speed_that_costs", "shadow_over_the_veil", "biopower", "thermidor", "commission_as_shogunate"],
    "Civilizational Clocks & History": ["clock_ibn_khaldun", "jiangnan_genotype", "sun-quan", "hundred schools", "endurance_or_density", "ouroboros"],
    "Philosophical Methodology & Reflexivity": ["popper_as_self_vaccination", "falsifiability_as_self", "embedded_witness", "immanent critique", "no_common_point"]
}

categorized = {k: [] for k in clusters}
uncategorized = []

for path, (fname, sz) in all_pdfs.items():
    matched = False
    f_low = fname.lower()
    for cat, keywords in clusters.items():
        if any(kw in f_low for kw in keywords):
            categorized[cat].append((fname, sz, path))
            matched = True
            break
    if not matched:
        uncategorized.append((fname, sz, path))

for cat, flist in categorized.items():
    print(f"\n==========================================")
    print(f"🔥 CLUSTER: {cat} ({len(flist)} papers)")
    print(f"==========================================")
    for fname, sz, path in sorted(flist, key=lambda x: -x[1])[:8]:
        print(f"   * {fname} ({sz/1024:.1f} KB)")

print(f"\nOther major standalone papers ({len(uncategorized)}):")
for fname, sz, path in sorted(uncategorized, key=lambda x: -x[1])[:15]:
    print(f"   - {fname} ({sz/1024:.1f} KB) in {os.path.basename(os.path.dirname(path))}")
