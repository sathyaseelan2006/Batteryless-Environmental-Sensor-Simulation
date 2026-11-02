import pptx

prs = pptx.Presentation('ppt/reference ppt.pptx')
with open('ppt/font_analysis.txt', 'w', encoding='utf-8') as out:
    for idx, slide in enumerate(prs.slides):
        out.write(f"\n=== SLIDE {idx+1} ===\n")
        for s_idx, shape in enumerate(slide.shapes):
            if shape.has_text_frame:
                out.write(f"  Shape {s_idx} ({shape.name}):\n")
                for p_idx, p in enumerate(shape.text_frame.paragraphs):
                    fn = p.font.name
                    fs = p.font.size.pt if p.font.size else None
                    b = p.font.bold
                    # check runs
                    run_info = []
                    for r in p.runs:
                        r_fn = r.font.name or fn
                        r_fs = r.font.size.pt if r.font.size else fs
                        r_b = r.font.bold if r.font.bold is not None else b
                        run_info.append(f"(fn={r_fn}, fs={r_fs}, b={r_b})")
                    out.write(f"    p{p_idx} [{p.text[:40]!r}]: level={p.level}, font={fn}, size={fs}, bold={b}, runs={' '.join(run_info[:3])}\n")
