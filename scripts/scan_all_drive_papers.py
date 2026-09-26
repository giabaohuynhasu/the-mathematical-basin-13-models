import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

drive_path = r"G:\Drive của tôi"

paper_extensions = ('.pdf', '.docx', '.md')
ignore_names = ['resume', 'cv', 'transcript', 'application', 'screenshot', 'passport', 'photo']

found_files = []

for root, dirs, files in os.walk(drive_path):
    for f in files:
        f_lower = f.lower()
        if any(f_lower.endswith(ext) for ext in paper_extensions):
            if any(ign in f_lower for ign in ignore_names):
                continue
            full_path = os.path.join(root, f)
            try:
                size = os.path.getsize(full_path)
            except Exception:
                size = 0
            found_files.append((full_path, f, size))

print(f"Total academic documents found: {len(found_files)}")

# Group by directory / topic
by_folder = {}
for path, name, size in found_files:
    folder = os.path.dirname(path)
    rel_folder = os.path.relpath(folder, drive_path)
    by_folder.setdefault(rel_folder, []).append((name, size, path))

for folder, files in sorted(by_folder.items()):
    print(f"\n📁 [{folder}] ({len(files)} files)")
    for name, size, path in sorted(files, key=lambda x: -x[1])[:10]: # top 10 largest
        print(f"   - {name} ({size/1024:.1f} KB)")
    if len(files) > 10:
        print(f"   ... and {len(files) - 10} more")
