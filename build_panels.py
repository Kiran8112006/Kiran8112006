import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSETS_DIR = 'assets'
BG_COLOR = (13, 17, 23, 255) # GitHub dark mode #0d1117

FONT_SANS_BOLD = r'C:\Windows\Fonts\segoeuib.ttf'
FONT_SANS = r'C:\Windows\Fonts\segoeui.ttf'
FONT_MONO = r'C:\Windows\Fonts\consola.ttf'

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def create_horizontal_fade_mask(w, h, fade_w, from_left=False):
    mask = Image.new('L', (w, h), 255)
    d = ImageDraw.Draw(mask)
    if from_left:
        for x in range(fade_w):
            alpha = int(255 * (x / fade_w))
            d.line([(x, 0), (x, h)], fill=alpha)
    else:
        for x in range(fade_w):
            alpha = int(255 * (1 - (x / fade_w)))
            d.line([(w - fade_w + x, 0), (w - fade_w + x, h)], fill=alpha)
    return mask

# ==========================================
# 1. SAO HERO (1600 x 550)
# ==========================================
def build_sao_hero():
    w, h = 1600, 550
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    # Load original sao hero
    src = Image.open(os.path.join(ASSETS_DIR, 'sao-hero.png')).convert('RGBA')
    # Fit into right side/full canvas with atmospheric fade
    # Crop/fit
    src_aspect = src.width / src.height
    new_h = h
    new_w = int(new_h * src_aspect)
    src_resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Position art on right half
    offset_x = w - new_w
    mask = create_horizontal_fade_mask(new_w, new_h, 300, from_left=True)
    canvas.paste(src_resized, (offset_x, 0), mask)
    
    # Draw typography on left
    draw = ImageDraw.Draw(canvas)
    f_eyebrow = get_font(FONT_MONO, 16)
    f_title = get_font(FONT_SANS_BOLD, 54)
    f_sub = get_font(FONT_SANS_BOLD, 22)
    f_tags = get_font(FONT_MONO, 18)
    f_quote = get_font(FONT_SANS, 20)
    
    x = 100
    y = 120
    draw.text((x, y), "SWORD ART ONLINE  //  ARCHIVE", font=f_eyebrow, fill=(138, 124, 248, 255))
    y += 35
    draw.text((x, y), "V S KIRAN", font=f_title, fill=(255, 255, 255, 255))
    y += 75
    draw.text((x, y), "E&I ENGINEERING STUDENT", font=f_sub, fill=(230, 237, 243, 255))
    y += 40
    draw.text((x, y), "software  ·  electronics  ·  ML  ·  VLSI", font=f_tags, fill=(139, 148, 158, 255))
    y += 50
    draw.text((x, y), "building things and figuring out how they work.", font=f_quote, fill=(110, 118, 129, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'sao-hero.png'), quality=95)
    print("Built sao-hero.png")

# ==========================================
# 2. ABOUT (1600 x 550)
# ==========================================
def build_about():
    w, h = 1600, 550
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    # Load Horimiya
    src = Image.open(os.path.join(ASSETS_DIR, 'horimiya.png')).convert('RGBA')
    art_size = 550
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_horizontal_fade_mask(art_size, art_size, 160, from_left=False)
    canvas.paste(src_resized, (60, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_header = get_font(FONT_SANS_BOLD, 36)
    f_body = get_font(FONT_SANS, 22)
    f_foot = get_font(FONT_MONO, 16)
    
    tx = 680
    ty = 110
    draw.text((tx, ty), "ABOUT ME", font=f_header, fill=(255, 255, 255, 255))
    draw.line([(tx, ty + 50), (tx + 120, ty + 50)], fill=(138, 124, 248, 255), width=2)
    
    line1 = "I'm Kiran, an Electronics & Instrumentation Engineering student\nat Bangalore Institute of Technology."
    draw.text((tx, ty + 75), line1, font=f_body, fill=(230, 237, 243, 255), spacing=12)
    
    line2 = "I like moving between software, electronics and sensor-based projects,\nand lately I've been getting more interested in VLSI and semiconductor\ntechnology."
    draw.text((tx, ty + 175), line2, font=f_body, fill=(139, 148, 158, 255), spacing=12)
    
    meta = "BANGALORE INSTITUTE OF TECHNOLOGY  ·  2024–2028  ·  CGPA: 9.14"
    draw.text((tx, ty + 310), meta, font=f_foot, fill=(110, 118, 129, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'about.png'), quality=95)
    print("Built about.png")

# ==========================================
# 3. PROJECTS (1600 x 700)
# ==========================================
def build_projects():
    w, h = 1600, 700
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    # Load AOT projects art
    src = Image.open(os.path.join(ASSETS_DIR, 'aot-projects.png')).convert('RGBA')
    # Place on right side with wide fade
    art_h = h
    art_w = int(art_h * (src.width / src.height))
    src_resized = src.resize((art_w, art_h), Image.Resampling.LANCZOS)
    mask = create_horizontal_fade_mask(art_w, art_h, 350, from_left=True)
    canvas.paste(src_resized, (w - art_w + 100, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_title = get_font(FONT_SANS_BOLD, 36)
    f_proj = get_font(FONT_SANS_BOLD, 22)
    f_desc = get_font(FONT_SANS, 16)
    f_tag = get_font(FONT_MONO, 14)
    
    x = 100
    y = 60
    draw.text((x, y), "PROJECTS", font=f_title, fill=(255, 255, 255, 255))
    draw.line([(x, y + 48), (x + 100, y + 48)], fill=(138, 124, 248, 255), width=2)
    
    # 1. RoadSOS
    py = y + 75
    draw.text((x, py), "RoadSOS", font=f_proj, fill=(255, 255, 255, 255))
    draw.text((x + 130, py + 4), "// SENSOR DETECTION & DISPATCH", font=f_tag, fill=(138, 124, 248, 255))
    r_desc = (
        "Sensor-driven accident detection and emergency response system combining\n"
        "smartphone accelerometer and gyroscope telemetry with machine-learning-based\n"
        "detection, live location, emergency alerts and backend services.\n"
        "Currently receiving further upgrades."
    )
    draw.text((x, py + 34), r_desc, font=f_desc, fill=(180, 190, 200, 255), spacing=8)
    
    # 2. GridSenti
    py += 165
    draw.text((x, py), "GridSenti", font=f_proj, fill=(255, 255, 255, 255))
    draw.text((x + 130, py + 4), "// HIGH-IMPEDANCE FAULT TELEMETRY", font=f_tag, fill=(138, 124, 248, 255))
    g_desc = (
        "Intelligent fault detection system focused on high-impedance and\n"
        "difficult-to-detect faults in electrical distribution networks using\n"
        "electrical telemetry, data-driven analysis, rule-based detection and\n"
        "machine learning."
    )
    draw.text((x, py + 34), g_desc, font=f_desc, fill=(180, 190, 200, 255), spacing=8)
    
    # 3. HireLoop
    py += 165
    draw.text((x, py), "HireLoop", font=f_proj, fill=(255, 255, 255, 255))
    draw.text((x + 130, py + 4), "// RECRUITMENT PIPELINE ENGINE", font=f_tag, fill=(138, 124, 248, 255))
    h_desc = (
        "Campus recruitment platform connecting students, recruiters and placement\n"
        "coordinators through application tracking, hiring-drive management,\n"
        "candidate workflows and centralized recruitment oversight."
    )
    draw.text((x, py + 34), h_desc, font=f_desc, fill=(180, 190, 200, 255), spacing=8)
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'projects.png'), quality=95)
    print("Built projects.png")

# ==========================================
# 4. ACHIEVEMENT (1600 x 500)
# ==========================================
def build_achievement():
    w, h = 1600, 500
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    # Load Blue Lock
    src = Image.open(os.path.join(ASSETS_DIR, 'blue-lock.png')).convert('RGBA')
    art_size = 500
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_horizontal_fade_mask(art_size, art_size, 150, from_left=False)
    canvas.paste(src_resized, (80, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_sub = get_font(FONT_MONO, 18)
    f_title = get_font(FONT_SANS_BOLD, 46)
    f_badge = get_font(FONT_SANS_BOLD, 26)
    f_quote = get_font(FONT_SANS, 22)
    
    tx = 660
    ty = 130
    draw.text((tx, ty), "COMPETITIVE SPRINT", font=f_sub, fill=(138, 124, 248, 255))
    ty += 32
    draw.text((tx, ty), "REVA HACKATHON", font=f_title, fill=(255, 255, 255, 255))
    ty += 68
    draw.text((tx, ty), "RUNNER-UP", font=f_badge, fill=(230, 237, 243, 255))
    ty += 48
    draw.text((tx, ty), "One of those weekends where sleep becomes optional.", font=f_quote, fill=(139, 148, 158, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'achievement.png'), quality=95)
    print("Built achievement.png")

# ==========================================
# 5. VLSI (1600 x 500)
# ==========================================
def build_vlsi():
    w, h = 1600, 500
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    # Load Solo Leveling
    src = Image.open(os.path.join(ASSETS_DIR, 'solo-leveling.png')).convert('RGBA')
    art_size = 500
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_horizontal_fade_mask(art_size, art_size, 160, from_left=True)
    canvas.paste(src_resized, (w - art_size - 80, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_eyebrow = get_font(FONT_MONO, 16)
    f_title = get_font(FONT_SANS_BOLD, 38)
    f_topics = get_font(FONT_SANS_BOLD, 22)
    f_note = get_font(FONT_SANS, 20)
    
    tx = 100
    ty = 100
    draw.text((tx, ty), "CURRENT QUEST", font=f_eyebrow, fill=(138, 124, 248, 255))
    ty += 30
    draw.text((tx, ty), "CURRENTLY EXPLORING", font=f_title, fill=(255, 255, 255, 255))
    ty += 65
    
    topics = "VLSI  ·  Digital Design  ·  Verilog  ·  Semiconductor Technology"
    draw.text((tx, ty), topics, font=f_topics, fill=(230, 237, 243, 255))
    ty += 50
    
    note = (
        "still figuring out how everything goes from logic on a screen\n"
        "to actual silicon."
    )
    draw.text((tx, ty), note, font=f_note, fill=(139, 148, 158, 255), spacing=8)
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'vlsi.png'), quality=95)
    print("Built vlsi.png")

# ==========================================
# 6. THOUGHTS (1600 x 500)
# ==========================================
def build_thoughts():
    w, h = 1600, 500
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    # Load Mindset
    src = Image.open(os.path.join(ASSETS_DIR, 'mindset.png')).convert('RGBA')
    art_size = 500
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_horizontal_fade_mask(art_size, art_size, 150, from_left=False)
    canvas.paste(src_resized, (80, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_eyebrow = get_font(FONT_MONO, 16)
    f_title = get_font(FONT_SANS_BOLD, 36)
    f_point = get_font(FONT_SANS, 22)
    
    tx = 660
    ty = 105
    draw.text((tx, ty), "COGNITIVE ARCHITECTURE", font=f_eyebrow, fill=(138, 124, 248, 255))
    ty += 30
    draw.text((tx, ty), "MENTAL NOTES", font=f_title, fill=(255, 255, 255, 255))
    draw.line([(tx, ty + 50), (tx + 120, ty + 50)], fill=(138, 124, 248, 255), width=2)
    ty += 70
    
    points = [
        "look at the data before guessing.",
        "understand the system before trying to fix it.",
        "debugging gets easier once you stop assuming."
    ]
    for p in points:
        draw.text((tx, ty), f"•  {p}", font=f_point, fill=(200, 210, 220, 255))
        ty += 48
        
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'thoughts.png'), quality=95)
    print("Built thoughts.png")

if __name__ == '__main__':
    build_sao_hero()
    build_about()
    build_projects()
    build_achievement()
    build_vlsi()
    build_thoughts()
    print("All 6 visual panels successfully generated!")
