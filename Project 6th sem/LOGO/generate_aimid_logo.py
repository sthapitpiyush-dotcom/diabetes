import subprocess
import sys
import math

try:
    import pptx
except ImportError:
    print("Installing required python-pptx library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    import pptx

from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def get_quadratic_bezier_points(p0, p1, p2, steps=20):
    """Calculates coordinates along a smooth quadratic Bezier curve."""
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        points.append((x, y))
    return points

def create_aimid_curved_logo(filename="aimid_curved_traces.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), 
        prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(3, 7, 18) # Deep obsidian #030712
    bg.line.fill.background() # No border

    # Scale mapping: 1 SVG pixel = 0.01333 Inches in PowerPoint
    scale = 0.01333

    # Main Headline Part 1: "ai"
    ai_box = slide.shapes.add_textbox(Inches(180 * scale), Inches(2.1), Inches(4.0), Inches(3.0))
    tf_ai = ai_box.text_frame
    tf_ai.word_wrap = True
    p_ai = tf_ai.paragraphs[0]
    p_ai.text = "ai"
    p_ai.font.name = 'Segoe UI'
    p_ai.font.size = pptx.util.Pt(140)
    p_ai.font.bold = True
    p_ai.font.color.rgb = RGBColor(79, 209, 197) # Teal/Cyan Accent

    # Main Headline Part 2: "mid"
    mid_box = slide.shapes.add_textbox(Inches(460 * scale), Inches(2.1), Inches(6.0), Inches(3.0))
    tf_mid = mid_box.text_frame
    tf_mid.word_wrap = True
    p_mid = tf_mid.paragraphs[0]
    p_mid.text = "mid"
    p_mid.font.name = 'Segoe UI'
    p_mid.font.size = pptx.util.Pt(140)
    p_mid.font.bold = True
    p_mid.font.color.rgb = RGBColor(96, 165, 250) # Sky Blue Accent

    # Node 1: Square frame over 'i'
    slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(358 * scale),
        Inches(163 * scale),
        Inches(46 * scale),
        Inches(46 * scale)
    )
    square_frame = slide.shapes[-1]
    square_frame.fill.solid()
    square_frame.fill.fore_color.rgb = RGBColor(3, 7, 18)
    square_frame.line.color.rgb = RGBColor(139, 92, 246) # Neon Purple Border
    square_frame.line.width = pptx.util.Pt(3.5)

    # Node 1 Inner Circle
    slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(365 * scale),
        Inches(170 * scale),
        Inches(32 * scale),
        Inches(32 * scale)
    )
    inner_circle = slide.shapes[-1]
    inner_circle.fill.solid()
    inner_circle.fill.fore_color.rgb = RGBColor(79, 209, 197)
    inner_circle.line.fill.background()

    # Node 2: Terminal Circle over 'm'
    slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(563 * scale),
        Inches(170 * scale),
        Inches(32 * scale),
        Inches(32 * scale)
    )
    node_right = slide.shapes[-1]
    node_right.fill.solid()
    node_right.fill.fore_color.rgb = RGBColor(96, 165, 250)
    node_right.line.fill.background()

    # Coordinates Setup
    gap_start_x = 404
    gap_end_x = 563
    center_y = 186
    lanes = 3
    spacing = 8
    start_offset = -((lanes - 1) * spacing) / 2

    for i in range(lanes):
        y_offset = start_offset + (i * spacing)
        current_y = center_y + y_offset

        # Transition bounds for the curves
        trans_start_x = gap_start_x + 42
        trans_end_x = gap_end_x - 42

        # 1. Left horizontal extension line
        slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(gap_start_x * scale),
            Inches((current_y - 1.5) * scale),
            Inches((trans_start_x - gap_start_x) * scale),
            Inches(3 * scale) # line weight of 3px
        )
        line_left = slide.shapes[-1]
        line_left.fill.solid()
        line_left.fill.fore_color.rgb = RGBColor(79, 209, 197)
        line_left.line.fill.background()

        # 2. Right horizontal extension line
        slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(trans_end_x * scale),
            Inches((current_y - 1.5) * scale),
            Inches((gap_end_x - trans_end_x) * scale),
            Inches(3 * scale)
        )
        line_right = slide.shapes[-1]
        line_right.fill.solid()
        line_right.fill.fore_color.rgb = RGBColor(96, 165, 250)
        line_right.line.fill.background()

        # 3. Dynamic Curved Trace Bridge (Symmetrical alternating curves)
        direction = -1 if (i % 2 == 0) else 1
        curve_offset = (12 + (i // 2) * 10) * direction

        # Control points for the quadratic Bezier path
        p0 = (trans_start_x, current_y)
        p1 = ((trans_start_x + trans_end_x) / 2, current_y + curve_offset)
        p2 = (trans_end_x, current_y)

        # Generate smooth points
        curve_coords = get_quadratic_bezier_points(p0, p1, p2, steps=15)

        # Draw the curve using freeform lines
        start_pt = curve_coords[0]
        builder = slide.shapes.build_freeform(Inches(start_pt[0] * scale), Inches(start_pt[1] * scale))
        for pt in curve_coords[1:]:
            builder.add_line_segments([(Inches(pt[0] * scale), Inches(pt[1] * scale))])

        curved_path = builder.convert_to_shape()
        curved_path.fill.background() # Line shape, transparent fill
        curved_path.line.color.rgb = RGBColor(139, 92, 246) # Neon Purple Trace color
        curved_path.line.width = pptx.util.Pt(2.5)

    tag_box = slide.shapes.add_textbox(Inches(1.66), Inches(5.6), Inches(10.0), Inches(0.8))
    tf_tag = tag_box.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.alignment = pptx.enum.text.PP_ALIGN.CENTER
    p_tag.text = "AI MIDDLEWARE FOR THE ENTERPRISE"
    p_tag.font.name = 'Segoe UI'
    p_tag.font.size = pptx.util.Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(100, 116, 139) # Modern slate grey color

    prs.save(filename)
    print(f"Success! Native PowerPoint slide vector file '{filename}' generated.")

if __name__ == "__main__":
    create_aimid_curved_logo()
