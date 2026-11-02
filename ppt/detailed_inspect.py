import pptx

prs = pptx.Presentation('ppt/reference ppt.pptx')
with open('ppt/detailed_slide_shapes.txt', 'w', encoding='utf-8') as out:
    for idx, slide in enumerate(prs.slides):
        out.write(f"=== SLIDE {idx+1} (Layout: {slide.slide_layout.name}) ===\n")
        for s_idx, shape in enumerate(slide.shapes):
            txt = ''
            if shape.has_text_frame:
                txt = ' | '.join(p.text.strip() for p in shape.text_frame.paragraphs if p.text.strip())
            out.write(f"  Shape {s_idx}: name='{shape.name}', type={shape.shape_type}, left={shape.left}, top={shape.top}, width={shape.width}, height={shape.height}, text='{txt[:80]}'\n")
