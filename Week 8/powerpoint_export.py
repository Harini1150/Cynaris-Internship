
from io import BytesIO
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


def create_powerpoint(insights, executive_summary, recommendations):
    """Create a seven-slide executive presentation and return its bytes."""
    if len(insights) != 5:
        raise ValueError("Exactly five insights are required.")

    if not recommendations:
        raise ValueError("At least one recommendation is required.")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    def add_text(slide, text, left, top, width, height,
                 font_size=24, bold=False):
        box = slide.shapes.add_textbox(
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        frame = box.text_frame
        frame.word_wrap = True
        frame.margin_left = Inches(0.12)
        frame.margin_right = Inches(0.12)
        frame.margin_top = Inches(0.08)

        paragraph = frame.paragraphs[0]
        paragraph.text = str(text)
        paragraph.font.size = Pt(font_size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = RGBColor(35, 48, 68)
        return box

    # Slide 1: Title and executive summary
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, "Executive Business Insights", 0.7, 0.7,
             12, 0.8, 30, True)
    add_text(slide, "EDA Report | Week 8 Day 1", 0.8, 1.7,
             11.5, 0.5, 18)
    add_text(slide, executive_summary, 0.8, 2.5,
             11.5, 4.2, 17)

    # Slides 2–6: Five insights
    for index, insight in enumerate(insights, start=1):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        add_text(slide, f"Insight {index}", 0.7, 0.7,
                 11.8, 0.8, 30, True)
        add_text(slide, insight, 0.9, 2.0,
                 11.2, 3.8, 23)

    # Slide 7: Recommendations
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, "Business Recommendations", 0.7, 0.7,
             12, 0.8, 30, True)

    recommendation_text = "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(recommendations, start=1)
    )
    add_text(slide, recommendation_text, 0.9, 1.8,
             11.5, 4.8, 21)

    output = BytesIO()
    prs.save(output)
    output.seek(0)
    return output.getvalue()
