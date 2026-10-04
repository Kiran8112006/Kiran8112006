import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = 'assets'
BG_COLOR = (13, 17, 23, 255)  # GitHub native dark mode #0d1117

FONT_SANS_BOLD = r'C:\Windows\Fonts\segoeuib.ttf'
FONT_SANS = r'C:\Windows\Fonts\segoeui.ttf'
FONT_MONO = r'C:\Windows\Fonts\consola.ttf'

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def create_fade_mask(w, h, fade_w, from_left=False):
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
# 1. SAO HERO (1200 x 420)
# ==========================================
def make_sao_hero():
    w, h = 1200, 420
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    src = Image.open(os.path.join(ASSETS_DIR, 'raw-sao.png')).convert('RGBA')
    art_h = h
    art_w = int(art_h * (src.width / src.height))
    src_resized = src.resize((art_w, art_h), Image.Resampling.LANCZOS)
    
    mask = create_fade_mask(art_w, art_h, 240, from_left=True)
    canvas.paste(src_resized, (w - art_w, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_name = get_font(FONT_SANS_BOLD, 52)
    f_sub = get_font(FONT_SANS, 20)
    
    tx = 80
    ty = 160
    draw.text((tx, ty), "KIRAN", font=f_name, fill=(255, 255, 255, 255))
    ty += 70
    draw.text((tx, ty), "somewhere between circuits and code.", font=f_sub, fill=(160, 175, 195, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'sao-hero.png'), quality=95)
    print("Generated sao-hero.png")

# ==========================================
# 2. WHO AM I + CURRENT FOCUS (1000 x 360)
# ==========================================
def make_who_am_i():
    w, h = 1000, 360
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    src = Image.open(os.path.join(ASSETS_DIR, 'horimiya.png')).convert('RGBA')
    art_size = 360
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_fade_mask(art_size, art_size, 100, from_left=False)
    canvas.paste(src_resized, (20, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_title = get_font(FONT_SANS_BOLD, 26)
    f_body = get_font(FONT_SANS, 16)
    f_mono = get_font(FONT_MONO, 15)
    
    tx = 420
    ty = 42
    draw.text((tx, ty), "WHO AM I", font=f_title, fill=(255, 255, 255, 255))
    draw.line([(tx, ty + 36), (tx + 80, ty + 36)], fill=(138, 124, 248, 255), width=2)
    
    ty += 50
    b1 = "I'm Kiran, an Electronics & Instrumentation Engineering student."
    b2 = "I like building things and figuring out how they work."
    b3 = "Lately I've been getting more interested in VLSI\nand semiconductor technology."
    draw.text((tx, ty), b1, font=f_body, fill=(220, 230, 242, 255))
    draw.text((tx, ty + 26), b2, font=f_body, fill=(200, 212, 226, 255))
    draw.text((tx, ty + 52), b3, font=f_body, fill=(160, 175, 195, 255), spacing=5)
    
    ty += 125
    draw.text((tx, ty), "CURRENT FOCUS", font=get_font(FONT_SANS_BOLD, 18), fill=(255, 255, 255, 255))
    ty += 30
    focus_text = "learning  ·  VLSI     |     building  ·  software"
    draw.text((tx, ty), focus_text, font=f_mono, fill=(138, 124, 248, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'who-am-i.png'), quality=95)
    print("Generated who-am-i.png")

# ==========================================
# 3. CURRENT TOOLBOX (1000 x 280) - Clean Typography, No Borders
# ==========================================
def make_toolbox():
    w, h = 1000, 280
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)
    
    f_header = get_font(FONT_SANS_BOLD, 24)
    f_cat = get_font(FONT_MONO, 13)
    f_items = get_font(FONT_SANS_BOLD, 17)
    
    tx = 60
    draw.text((tx, 30), "CURRENT TOOLBOX", font=f_header, fill=(255, 255, 255, 255))
    draw.text((tx + 260, 36), "// things i actually use", font=f_cat, fill=(138, 124, 248, 255))
    draw.line([(tx, 70), (w - 60, 70)], fill=(33, 38, 45, 255), width=1)
    
    cols = [
        ("LANGUAGES", ["C", "C++", "Python"]),
        ("FRONTEND", ["HTML", "CSS", "JavaScript", "React", "Next.js"]),
        ("BACKEND", ["Node.js"]),
        ("WORKFLOW", ["Git", "GitHub"])
    ]
    
    cx = 60
    for title, items in cols:
        draw.text((cx, 95), title, font=f_cat, fill=(139, 148, 158, 255))
        iy = 125
        for item in items:
            draw.text((cx, iy), item, font=f_items, fill=(230, 237, 243, 255))
            iy += 26
        cx += 230
        
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'toolbox.png'), quality=95)
    print("Generated toolbox.png")

# ==========================================
# 4. SOLO LEVELING — NEXT SKILL (1000 x 360)
# ==========================================
def make_solo_leveling():
    w, h = 1000, 360
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    src = Image.open(os.path.join(ASSETS_DIR, 'solo-leveling.png')).convert('RGBA')
    art_size = 360
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_fade_mask(art_size, art_size, 120, from_left=True)
    canvas.paste(src_resized, (w - art_size - 20, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_sub = get_font(FONT_MONO, 14)
    f_title = get_font(FONT_SANS_BOLD, 32)
    f_items = get_font(FONT_SANS_BOLD, 18)
    f_loading = get_font(FONT_MONO, 16)
    
    tx = 60
    ty = 65
    draw.text((tx, ty), "NEXT SKILL", font=f_sub, fill=(138, 124, 248, 255))
    ty += 28
    draw.text((tx, ty), "VLSI", font=f_title, fill=(255, 255, 255, 255))
    draw.line([(tx, ty + 44), (tx + 70, ty + 44)], fill=(138, 124, 248, 255), width=2)
    
    ty += 65
    draw.text((tx, ty), "Digital Design   ·   Verilog   ·   Semiconductor Technology", font=f_items, fill=(220, 230, 242, 255))
    
    ty += 50
    draw.text((tx, ty), "loading...", font=f_loading, fill=(160, 175, 195, 255))
    
    # Draw custom crisp progress bar blocks
    bar_x = tx + 105
    bar_y = ty + 2
    draw.text((bar_x, ty), "[", font=f_loading, fill=(138, 124, 248, 255))
    bx = bar_x + 16
    for i in range(10):
        if i < 8:
            # filled block
            draw.rectangle([bx, bar_y, bx + 12, bar_y + 15], fill=(138, 124, 248, 255))
        else:
            # unfilled block
            draw.rectangle([bx, bar_y, bx + 12, bar_y + 15], outline=(60, 70, 85, 255), fill=(22, 27, 34, 255), width=1)
        bx += 16
    draw.text((bx + 4, ty), "]", font=f_loading, fill=(138, 124, 248, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'solo-leveling-quest.png'), quality=95)
    print("Generated solo-leveling-quest.png")

# ==========================================
# 5. HORIMIYA MOMENT (800 x 180)
# ==========================================
def make_horimiya_moment():
    w, h = 800, 180
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    src = Image.open(os.path.join(ASSETS_DIR, 'horimiya.png')).convert('RGBA')
    cropped = src.crop((100, 100, 700, 700))
    art_size = 180
    resized = cropped.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_fade_mask(art_size, art_size, 70, from_left=False)
    canvas.paste(resized, (30, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_text = get_font(FONT_SANS, 21)
    
    tx = 260
    ty = 58
    draw.text((tx, ty), "somewhere between classes", font=f_text, fill=(200, 212, 226, 255))
    draw.text((tx, ty + 32), "and late-night debugging.", font=f_text, fill=(139, 148, 158, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'horimiya-moment.png'), quality=95)
    print("Generated horimiya-moment.png")

# ==========================================
# 6. MENTAL NOTES (1000 x 340)
# ==========================================
def make_mental_notes():
    w, h = 1000, 340
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    src = Image.open(os.path.join(ASSETS_DIR, 'mindset.png')).convert('RGBA')
    art_size = 340
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_fade_mask(art_size, art_size, 100, from_left=False)
    canvas.paste(src_resized, (30, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_title = get_font(FONT_SANS_BOLD, 26)
    f_point = get_font(FONT_SANS, 18)
    
    tx = 420
    ty = 60
    draw.text((tx, ty), "mental notes", font=f_title, fill=(255, 255, 255, 255))
    draw.line([(tx, ty + 36), (tx + 80, ty + 36)], fill=(138, 124, 248, 255), width=2)
    
    points = [
        "Look at the data before guessing.",
        "Understand the system before trying to fix it.",
        "Debugging gets a lot easier once you stop assuming."
    ]
    
    ty += 60
    for p in points:
        draw.text((tx, ty), f"•  {p}", font=f_point, fill=(210, 222, 235, 255))
        ty += 42
        
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'mental-notes.png'), quality=95)
    print("Generated mental-notes.png")

# ==========================================
# 7. BLUE LOCK — REVA HACKATHON (1000 x 300)
# ==========================================
def make_blue_lock():
    w, h = 1000, 300
    canvas = Image.new('RGBA', (w, h), BG_COLOR)
    
    src = Image.open(os.path.join(ASSETS_DIR, 'blue-lock.png')).convert('RGBA')
    art_size = 300
    src_resized = src.resize((art_size, art_size), Image.Resampling.LANCZOS)
    mask = create_fade_mask(art_size, art_size, 90, from_left=False)
    canvas.paste(src_resized, (30, 0), mask)
    
    draw = ImageDraw.Draw(canvas)
    f_title = get_font(FONT_SANS_BOLD, 30)
    f_sub = get_font(FONT_SANS_BOLD, 20)
    f_quote = get_font(FONT_SANS, 17)
    
    tx = 380
    ty = 70
    draw.text((tx, ty), "REVA HACKATHON", font=f_title, fill=(255, 255, 255, 255))
    ty += 48
    draw.text((tx, ty), "Runner-up.", font=f_sub, fill=(138, 124, 248, 255))
    ty += 38
    draw.text((tx, ty), "One of those weekends where sleep becomes optional.", font=f_quote, fill=(139, 148, 158, 255))
    
    canvas.convert('RGB').save(os.path.join(ASSETS_DIR, 'hackathon.png'), quality=95)
    print("Generated hackathon.png")

if __name__ == '__main__':
    make_sao_hero()
    make_who_am_i()
    make_toolbox()
    make_solo_leveling()
    make_horimiya_moment()
    make_mental_notes()
    make_blue_lock()
    print("All fresh assets regenerated successfully!")
