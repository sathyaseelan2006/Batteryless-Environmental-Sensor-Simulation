import json

with open('ppt/reference_structure.json', 'r', encoding='utf-8') as f:
    slides = json.load(f)

with open('ppt/reference_summary.txt', 'w', encoding='utf-8') as out:
    for s in slides:
        out.write(f"=== SLIDE {s['slide_num']} ===\n")
        for sh in s['shapes']:
            txt = sh.get('text', '').strip()
            if txt:
                out.write(f"  [{sh['name']}]:\n")
                for p in sh.get('paragraphs', []):
                    if p.strip():
                        out.write(f"    - {p.strip()}\n")
