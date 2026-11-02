import pptx

prs = pptx.Presentation('ppt/final project.pptx')
print(f"Total slides: {len(prs.slides)}")

with open('ppt/final_verification_report.txt', 'w', encoding='utf-8') as out:
    for idx, slide in enumerate(prs.slides):
        out.write(f"\n==================== SLIDE {idx+1} ====================\n")
        title = slide.shapes.title.text if slide.shapes.title else "No Title"
        out.write(f"Slide Title: {title}\n")
        for s_idx, shape in enumerate(slide.shapes):
            out.write(f"  Shape {s_idx} ({shape.name}, type={shape.shape_type}):\n")
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    t = p.text.strip()
                    if t:
                        out.write(f"    - {t[:100]}\n")
            elif shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
                img = shape.image
                out.write(f"    [IMAGE]: size={img.size}, bytes={len(img.blob)}, ext={img.ext}\n")

print("Verification report generated at ppt/final_verification_report.txt")
