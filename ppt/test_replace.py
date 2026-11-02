import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def replace_picture_shape(slide, old_shape_name, new_image_path):
    for shape in list(slide.shapes):
        if shape.name == old_shape_name:
            left, top, width, height = shape.left, shape.top, shape.width, shape.height
            sp = shape._element
            sp.getparent().remove(sp)
            slide.shapes.add_picture(new_image_path, left, top, width, height)
            print(f"Replaced {old_shape_name} with {new_image_path}")
            return True
    return False

print("Helper defined")
