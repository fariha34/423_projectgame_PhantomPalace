from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
from OpenGL.GLUT import fonts
 
WIN_W, WIN_H  = 1000,800
fovY          = 60
ROOM_SIZE     = 400
MOVE_SPEED    = 8.0
CROUCH_SPEED  = 3.5
ROT_SPEED     = 4.0
BULLET_SPEED  = 14.0
BULLET_SIZE   = 10
SLASH_RANGE   = 80
SLASH_FRAMES  = 18

GHOST_SPEED_BY_LEVEL = [0.05, 0.06, 0.08, 0.09, 0.1, 0.1]
GHOSTS_PER_LEVEL     = [2, 4, 5, 6, 7, 8]
GHOST_HP_BY_LEVEL    = [2, 3, 4, 5, 6, 8]
GHOST_CONTACT_DAMAGE_RATE = 120

cam_angle_h  = 0.0
cam_angle_v  = 28.0
cam_dist     = 230.0
first_person = False

player_x   = 0.0
player_y   = 0.0
player_z   = 0.0
player_rot = 0.0
player_hp  = 100
player_score = 0
game_over  = False
player_won = False
current_level = 0

is_crouching    = False
crouch_scale    = 1.0
invincible_timer = 0
INVINCIBLE_FRAMES = 90
hp_damage_accum  = 0.0

walk_frame  = 0
walk_swing  = 0.0
slash_active = False
slash_frame  = 0

player_energy = 100.0
MAX_ENERGY    = 100.0
is_moving = False
ENERGY_DRAIN_MOVE   = 0.04
ENERGY_DRAIN_CROUCH = 0.08
ENERGY_DRAIN_SLASH  = 8.0
ENERGY_DRAIN_SHOT   = 10.0
ENERGY_REGEN_IDLE   = 0.06

bullets = []
arrows  = []
cheat_mode = False

SHOP_ITEMS = [
   {"name": "Bread",        "cost": 50,  "draw": "bread",    "desc": "+30 Energy"},
   {"name": "Meat",         "cost": 80,  "draw": "meat",     "desc": "+40 HP"},
   {"name": "Royal Potion", "cost": 100, "draw": "potion",   "desc": "+50 HP & Energy"},
   {"name": "Short Sword",  "cost": 100, "draw": "sword",    "desc": "Sword dmg x2"},
   {"name": "Shield",       "cost": 200, "draw": "shield",   "desc": "-50% ghost dmg"},
   {"name": "Crossbow",     "cost": 300, "draw": "crossbow", "desc": "Bullets x2 dmg"},
   {"name": "Magic Aura", "cost": 550, "draw": "magic_aura", "desc": "Reflects 35% ghost dmg"},
]
shop_open     = False
shop_selected = 0
has_shield    = False
has_crossbow  = False
has_magic_shield = False
MAGIC_SHIELD_REFLECT_CHANCE = 0.35
sword_level   = 1
BULLET_DAMAGE = 1
SLASH_DAMAGE  = 1
SHIELD_ACTIVE = False
active_weapon = None

ghosts = []

ripple_active = False
ripple_radius = 0.0
ripple_x      = 0.0
ripple_y      = 0.0
MAX_RIPPLE    = 80.0

treasure_rot       = 0.0
treasure_collected = False
TREASURE_X, TREASURE_Y, TREASURE_Z = -120.0, 90.0, 10.0

pickup_active = False
pickup_radius = 0.0
pickup_alpha  = 1.0
idle_clock = 0

level_menu_open  = False
level_menu_sel   = 0
LEVEL_MENU_ITEMS = ["Next Level", "Back (Replay)", "Restart Game"]

spider_intro_active = True
spider_line_idx     = 0
spider_char_idx     = 0
spider_frame_count  = 0
SPIDER_CHAR_DELAY   = 2
SPIDER_LINE_PAUSE   = 80
spider_line_pause_timer = 0
spider_leg_anim     = 0.0

SPIDER_LINES = [
    "Oh. Another treasure hunter. Fantastic.",
    "Let me guess -- you heard about Phantom Palace, Want treasures ? Cool.",
    "There are ghosts. LOTS of them. They will absolutely wreck you.",
    "You have got a crossbow, a sword, and questionable life choices.",
    "Clear levels. Kill the ghosts, grab the loot, don't die.",
    "Good luck. You'll need it.",
    "  [ Press ENTER to confirm your bad decisions ]",
]

WIN_SPIDER_LINES = [
    "...",
    "You... actually won.",
    "I've watched adventurers fail for three centuries.",
    "You cleared every level, slew every ghost.",
    "Honestly? I'm a little impressed.",
    "The Palace is yours. Don't redecorate.",
    "  [ Press R to play again, or bask in glory ]",
]
win_spider_active       = False
win_spider_line_idx     = 0
win_spider_char_idx     = 0
win_spider_frame_count  = 0
win_spider_line_pause   = 0
win_spider_leg_anim     = 0.0

torch_flicker_frame = 0.0
TORCH_POSITIONS = [
    (-ROOM_SIZE + 8,  -200, 130),
    (-ROOM_SIZE + 8,   200, 130),
    ( ROOM_SIZE - 8,  -200, 130),
    ( ROOM_SIZE - 8,   200, 130),
    (-150,  ROOM_SIZE - 8, 130),
    ( 150,  ROOM_SIZE - 8, 130),
    (-150, -ROOM_SIZE + 8, 130),
    ( 150, -ROOM_SIZE + 8, 130),
]

blood_drips = []
wall_cracks = []

SKULL_POSITIONS = [
    (-ROOM_SIZE + 12,  -80, 95, "left"),
    (-ROOM_SIZE + 12,   80, 90, "left"),
    ( ROOM_SIZE - 12, -120, 100,"right"),
    ( ROOM_SIZE - 12,  100,  95,"right"),
    (-60,  ROOM_SIZE - 12,  92, "back"),
    ( 60,  ROOM_SIZE - 12,  98, "back"),
]

CHAIN_DATA = [
    (-280,  280, 9, 0.0),
    ( 280,  280, 7, 1.2),
    (-280, -280, 8, 2.4),
    ( 280, -280, 6, 0.8),
    (   0,  380, 8, 1.8),
    (   0, -380, 7, 0.5),
]
chain_sway = 0.0

cobweb_sway   = 0.0
COBWEB_CORNERS = [
    (-ROOM_SIZE + 2, -ROOM_SIZE + 2, 200),
    ( ROOM_SIZE - 2, -ROOM_SIZE + 2, 200),
    (-ROOM_SIZE + 2,  ROOM_SIZE - 2, 200),
    ( ROOM_SIZE - 2,  ROOM_SIZE - 2, 200),
]

ghost_bob_frame = 0.0

BAT_DATA = [
    {"x": -250, "y": 150, "z": 160, "speed": 1.5, "color": (0.8, 0.2, 0.2)},
    {"x": 280, "y": -180, "z": 140, "speed": 1.8, "color": (0.2, 0.8, 0.3)},
    {"x": -180, "y": -250, "z": 170, "speed": 2.0, "color": (0.9, 0.5, 0.1)},
    {"x": 200, "y": 280, "z": 150, "speed": 1.2, "color": (0.3, 0.3, 0.9)},
    {"x": -300, "y": 50, "z": 180, "speed": 2.2, "color": (0.9, 0.2, 0.8)},
    {"x": 150, "y": -100, "z": 130, "speed": 1.6, "color": (0.2, 0.9, 0.9)},
    {"x": -100, "y": 300, "z": 165, "speed": 1.9, "color": (0.95, 0.9, 0.2)},
    {"x": 320, "y": 100, "z": 145, "speed": 1.4, "color": (0.6, 0.2, 0.8)},
]
bat_frame = 0.0
CROSSBOW_TIP_FORWARD = 75.0
CROSSBOW_TIP_RIGHT   = 18.0
CROSSBOW_TIP_Z       = 56.0

# ===== NEW FEATURES: DAMAGE NUMBERS =====
damage_numbers = []
DAMAGE_NUM_LIFE = 40

def spawn_damage_number(x, y, z, damage, is_crit=False):
    color = (1.0, 0.2, 0.2) if not is_crit else (1.0, 0.9, 0.1)
    size = 22 if is_crit else 16
    damage_numbers.append({
        "x": x, "y": y, "z": z + 30,
        "damage": damage,
        "life": DAMAGE_NUM_LIFE,
        "color": color,
        "size": size,
        "is_crit": is_crit
    })

def update_damage_numbers():
    global damage_numbers
    for dn in damage_numbers:
        dn["life"] -= 1
        dn["z"] += 1.5
    damage_numbers = [dn for dn in damage_numbers if dn["life"] > 0]

def draw_damage_numbers():
    if not damage_numbers:
        return
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    for dn in damage_numbers:
        alpha = dn["life"] / DAMAGE_NUM_LIFE
        glColor4f(dn["color"][0], dn["color"][1], dn["color"][2], alpha)
        glRasterPos2f(dn["x"] * 1.2 + WIN_W//2, dn["z"] * 1.5 + WIN_H//2)
        text = str(dn["damage"])
        font = GLUT_BITMAP_TIMES_ROMAN_24 if dn["is_crit"] else GLUT_BITMAP_HELVETICA_18
        for ch in text:
            glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

# ===== NEW FEATURES: CRACKLING FLOOR TILES =====
floor_tiles = []
TILE_SIZE = 80

def init_floor_tiles():
    global floor_tiles
    floor_tiles = []
    for ix in range(-int(ROOM_SIZE//TILE_SIZE), int(ROOM_SIZE//TILE_SIZE)):
        for iy in range(-int(ROOM_SIZE//TILE_SIZE), int(ROOM_SIZE//TILE_SIZE)):
            x0, y0 = ix * TILE_SIZE, iy * TILE_SIZE
            x1, y1 = x0 + TILE_SIZE, y0 + TILE_SIZE
            is_cracked = random.random() < 0.12  # 12% start cracked
            floor_tiles.append({
                "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                "cracked": is_cracked
            })

def update_floor_tiles():
    global floor_tiles
    for tile in floor_tiles:
        if tile["x0"] <= player_x <= tile["x1"] and tile["y0"] <= player_y <= tile["y1"]:
            if not tile["cracked"] and is_moving:
                if random.random() < 0.0008:
                    tile["cracked"] = True

def draw_floor_tiles():
    for tile in floor_tiles:
        if tile["cracked"]:
            # Original pattern + crack lines
            glColor3f(0.18, 0.14, 0.09)
            glBegin(GL_QUADS)
            glVertex3f(tile["x0"], tile["y0"], 0.1)
            glVertex3f(tile["x1"], tile["y0"], 0.1)
            glVertex3f(tile["x1"], tile["y1"], 0.1)
            glVertex3f(tile["x0"], tile["y1"], 0.1)
            glEnd()
            # Crack lines on top
            glColor3f(0.05, 0.03, 0.02)
            glLineWidth(1.5)
            cx, cy = (tile["x0"] + tile["x1"]) / 2, (tile["y0"] + tile["y1"]) / 2
            glBegin(GL_LINES)
            glVertex3f(cx - 15, cy - 15, 1.2)
            glVertex3f(cx + 10, cy + 5, 1.2)
            glVertex3f(cx + 10, cy + 5, 1.2)
            glVertex3f(cx + 20, cy - 10, 1.2)
            glVertex3f(cx - 5, cy + 15, 1.2)
            glVertex3f(cx + 5, cy + 5, 1.2)
            glEnd()
            glLineWidth(1.0)
        else:
            # Normal tile - original pattern
            glColor3f(0.18, 0.14, 0.09)
            glBegin(GL_QUADS)
            glVertex3f(tile["x0"], tile["y0"], 0.1)
            glVertex3f(tile["x1"], tile["y0"], 0.1)
            glVertex3f(tile["x1"], tile["y1"], 0.1)
            glVertex3f(tile["x0"], tile["y1"], 0.1)
            glEnd()

# =====MAGIC aura REFLECTION =====
magic_shield_reflect_effect = 0

def check_magic_shield_reflection(g):
    if not has_magic_shield:
        return False
    dist = math.hypot(player_x - g["x"], player_y - g["y"])
    if dist < 50 and invincible_timer == 0:
        if random.random() < MAGIC_SHIELD_REFLECT_CHANCE:
            return True
    return False

def spawn_reflect_effect(x, y, z):
    global magic_shield_reflect_effect
    magic_shield_reflect_effect = 25
    for _ in range(6):
        angle = random.uniform(0, math.pi * 2)
        damage_numbers.append({
            "x": x + math.cos(angle) * 20,
            "y": y + math.sin(angle) * 20,
            "z": z + random.uniform(20, 50),
            "damage": 0,
            "life": 25,
            "color": (0.4, 0.6, 1.0),
            "size": 10,
            "is_crit": False
        })

def draw_magic_shield_effect():
    global magic_shield_reflect_effect
    if magic_shield_reflect_effect > 0:
        magic_shield_reflect_effect -= 1
        alpha = magic_shield_reflect_effect / 25
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WIN_W, 0, WIN_H)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glColor4f(0.3, 0.5, 1.0, alpha * 0.12)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(WIN_W, 0)
        glVertex2f(WIN_W, WIN_H)
        glVertex2f(0, WIN_H)
        glEnd()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

def draw_magic_shield_visuals():
    if not has_magic_shield:
        return
    q = gluNewQuadric()
    glPushMatrix()
    glTranslatef(player_x, player_y, player_z + 50)
    pulse = 0.5 + 0.3 * math.sin(idle_clock * 0.15)
    glColor4f(0.3, 0.5, 1.0, pulse * 0.35)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    gluSphere(q, 45 + pulse * 8, 12, 8)
    glDisable(GL_BLEND)
    glPopMatrix()
def draw_royal_portrait(x, y, z, portrait_type="king", wall="left"):
    glPushMatrix()
    glTranslatef(x, y, z)
    if wall == "left":
        glRotatef(90, 0, 1, 0)
    elif wall == "right":
        glRotatef(-90, 0, 1, 0)
    elif wall == "back":
        glRotatef(180, 0, 1, 0)
    glColor3f(0.65, 0.50, 0.10)
    glBegin(GL_QUADS)
    glVertex3f(-35, -50, 0)
    glVertex3f(35, -50, 0)
    glVertex3f(35, 50, 0)
    glVertex3f(-35, 50, 0)
    glEnd()
    glColor3f(0.50, 0.38, 0.08)
    glBegin(GL_QUADS)
    glVertex3f(-35, 50, 0)
    glVertex3f(35, 50, 0)
    glVertex3f(35, 55, 0)
    glVertex3f(-35, 55, 0)
    glVertex3f(-35, -55, 0)
    glVertex3f(35, -55, 0)
    glVertex3f(35, -50, 0)
    glVertex3f(-35, -50, 0)
    glEnd()
    glColor3f(0.25, 0.10, 0.10)
    glBegin(GL_QUADS)
    glVertex3f(-28, -42, 0.5)
    glVertex3f(28, -42, 0.5)
    glVertex3f(28, 42, 0.5)
    glVertex3f(-28, 42, 0.5)
    glEnd()
    glPushMatrix()
    glTranslatef(0, 2, 3)
    glColor3f(1.0, 0.85, 0.65)
    glutSolidSphere(10, 16, 16)
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(-3, 8, 8)
    glutSolidSphere(1.2, 8, 8)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(3, 8, 8)
    glutSolidSphere(1.2, 8, 8)
    glPopMatrix()
    glColor3f(0.9, 0.7, 0.6)
    glPushMatrix()
    glTranslatef(0, 4, 10)
    glutSolidSphere(1, 8, 8)
    glPopMatrix()
    glColor3f(0.4, 0.1, 0.1)
    glBegin(GL_LINES)
    glVertex3f(-2, 0, 10)
    glVertex3f(2, 0, 10)
    glEnd()
    if portrait_type == "king":
        glColor3f(1, 0.85, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(-8, 12, 0)
        glVertex3f(-5, 18, 0)
        glVertex3f(-2, 12, 0)
        glVertex3f(-2, 12, 0)
        glVertex3f(0, 20, 0)
        glVertex3f(2, 12, 0)
        glVertex3f(2, 12, 0)
        glVertex3f(5, 18, 0)
        glVertex3f(8, 12, 0)
        glEnd()
    else:
        glColor3f(1, 0.8, 0.2)
        glBegin(GL_TRIANGLES)
        glVertex3f(-7, 12, 0)
        glVertex3f(-3, 19, 0)
        glVertex3f(1, 12, 0)
        glVertex3f(1, 12, 0)
        glVertex3f(5, 19, 0)
        glVertex3f(8, 12, 0)
        glEnd()
        glColor3f(1, 1, 0)
        glPushMatrix()
        glTranslatef(0, 16, 1)
        glutSolidSphere(1.5, 8, 8)
        glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def draw_palace_portraits():
    draw_royal_portrait(-ROOM_SIZE + 5, 100, 145, "king", "left")
    draw_royal_portrait(ROOM_SIZE - 5, 90, 145, "queen", "right")
    draw_royal_portrait(0, ROOM_SIZE - 5, 145, "king", "back")

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def dist2d(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)

def ghost_speed():
    lvl = min(current_level, len(GHOST_SPEED_BY_LEVEL) - 1)
    return GHOST_SPEED_BY_LEVEL[lvl]

def make_ghost(gtype):
    while True:
        x = random.uniform(-ROOM_SIZE + 70, ROOM_SIZE - 70)
        y = random.uniform(-ROOM_SIZE + 70, ROOM_SIZE - 70)
        if math.hypot(x, y) > 200:
            break
    hp = GHOST_HP_BY_LEVEL[min(current_level, len(GHOST_HP_BY_LEVEL) - 1)]
    waypoints = []
    for _ in range(4):
        wx = random.uniform(-ROOM_SIZE + 80, ROOM_SIZE - 80)
        wy = random.uniform(-ROOM_SIZE + 80, ROOM_SIZE - 80)
        waypoints.append((wx, wy))
    return {"x": x, "y": y, "z": 30.0, "type": gtype, "pulse": random.random(), "hp": hp, "alive": True, "hit_flash": 0, "contact_accum": 0.0, "state": "patrol", "waypoints": waypoints, "wp_idx": 0}
def init_ghosts():
    global ghosts
    ghosts = []
    
    n = GHOSTS_PER_LEVEL[min(current_level, len(GHOSTS_PER_LEVEL) - 1)]
    n0 = max(1,n)
    n1 = 0   
    for _ in range(n0):
        ghosts.append(make_ghost(0))
    for _ in range(n1):
        ghosts.append(make_ghost(1))


def init_game():
    global player_x, player_y, player_z, player_rot, player_hp, player_score, game_over, current_level
    global walk_frame, walk_swing, slash_active, slash_frame, treasure_rot, treasure_collected
    global pickup_active, pickup_radius, pickup_alpha, cam_angle_h, cam_angle_v, first_person
    global is_crouching, crouch_scale, invincible_timer, hp_damage_accum, bullets, player_energy, player_won
    global shop_open, shop_selected, has_shield, has_crossbow, has_magic_shield, sword_level
    global BULLET_DAMAGE, SLASH_DAMAGE, SHIELD_ACTIVE, ripple_active, ripple_radius, ripple_x, ripple_y
    global is_moving, active_weapon, level_menu_open, level_menu_sel
    global spider_intro_active, spider_line_idx, spider_char_idx, spider_frame_count, spider_line_pause_timer, spider_leg_anim
    global torch_flicker_frame, blood_drips, wall_cracks, chain_sway, cobweb_sway, ghost_bob_frame
    global win_spider_active, win_spider_line_idx, win_spider_char_idx, win_spider_frame_count, win_spider_line_pause, win_spider_leg_anim
    player_x = player_y = player_z = 0.0
    player_rot = 0.0
    player_hp = 100
    player_score = 0
    game_over = False
    current_level = 0
    walk_frame = 0
    walk_swing = 0.0
    slash_active = False
    slash_frame = 0
    treasure_rot = 0.0
    treasure_collected = False
    pickup_active = False
    pickup_radius = 0.0
    pickup_alpha = 1.0
    cam_angle_h = 0.0
    cam_angle_v = 28.0
    first_person = False
    is_crouching = False
    crouch_scale = 1.0
    invincible_timer = 0
    hp_damage_accum = 0.0
    bullets = []
    player_energy = MAX_ENERGY
    shop_open = False
    shop_selected = 0
    has_shield = False
    has_crossbow = False
    has_magic_shield = False
    sword_level = 1
    BULLET_DAMAGE = 1
    SLASH_DAMAGE = 1
    SHIELD_ACTIVE = False
    ripple_active = False
    player_won = False
    ripple_radius = 0.0
    ripple_x = 0.0
    ripple_y = 0.0
    is_moving = False
    active_weapon = None
    level_menu_open = False
    level_menu_sel = 0
    spider_intro_active = True
    spider_line_idx = 0
    spider_char_idx = 0
    spider_frame_count = 0
    spider_line_pause_timer = 0
    spider_leg_anim = 0.0
    torch_flicker_frame = 0.0
    blood_drips = _gen_blood_drips()
    wall_cracks = _gen_wall_cracks()
    chain_sway = 0.0
    cobweb_sway = 0.0
    ghost_bob_frame = 0.0
    win_spider_active = False
    win_spider_line_idx = 0
    win_spider_char_idx = 0
    win_spider_frame_count = 0
    win_spider_line_pause = 0
    win_spider_leg_anim = 0.0
    init_ghosts()
    init_floor_tiles()

def switch_weapon(weapon_key):
    global active_weapon, BULLET_DAMAGE, SLASH_DAMAGE, SHIELD_ACTIVE
    if weapon_key == "shield" and not has_shield:
        return
    if weapon_key == "crossbow" and not has_crossbow:
        return
    if active_weapon == weapon_key:
        active_weapon = None
        BULLET_DAMAGE = 1
        SLASH_DAMAGE = 1
        SHIELD_ACTIVE = False
        return
    active_weapon = weapon_key
    BULLET_DAMAGE = 1
    SLASH_DAMAGE = 1
    SHIELD_ACTIVE = False
    if weapon_key == "sword":
        if sword_level > 1:
            SLASH_DAMAGE = 2
    elif weapon_key == "shield":
        SHIELD_ACTIVE = True
    elif weapon_key == "crossbow":
        BULLET_DAMAGE = 3

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text_col(x, y, text, r, g, b, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(r, g, b)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def _gen_blood_drips():
    drips = []
    R = ROOM_SIZE
    for _ in range(6):
        drips.append([-R, random.uniform(-R+50, R-50), "left", random.uniform(120, 195), random.uniform(0, 30), random.uniform(0.08, 0.22)])
    for _ in range(6):
        drips.append([R, random.uniform(-R+50, R-50), "right", random.uniform(120, 195), random.uniform(0, 30), random.uniform(0.08, 0.22)])
    for _ in range(5):
        drips.append([random.uniform(-R+50, R-50), R, "back", random.uniform(120, 195), random.uniform(0, 30), random.uniform(0.08, 0.22)])
    for _ in range(5):
        drips.append([random.uniform(-R+50, R-50), -R, "front", random.uniform(120, 195), random.uniform(0, 30), random.uniform(0.08, 0.22)])
    return drips

def _gen_wall_cracks():
    cracks = []
    R = ROOM_SIZE - 1
    def branch(ox, oy, oz, dx, dy, dz, steps, wall):
        pts = [(ox, oy, oz)]
        for _ in range(steps):
            ox += dx + random.uniform(-4, 4)
            oy += dy + random.uniform(-4, 4)
            oz += dz + random.uniform(-6, 6)
            oz = max(5, min(195, oz))
            pts.append((ox, oy, oz))
        return pts
    for _ in range(5):
        y0 = random.uniform(-280, 280)
        z0 = random.uniform(30, 160)
        cracks.append(("left", branch(-R, y0, z0, 0, random.uniform(3,8), random.uniform(-3,3), random.randint(5,10), "left")))
        cracks.append(("left", branch(-R, y0, z0, 0, -random.uniform(3,8), random.uniform(-3,3), random.randint(4,8), "left")))
    for _ in range(5):
        y0 = random.uniform(-280, 280)
        z0 = random.uniform(30, 160)
        cracks.append(("right", branch(R, y0, z0, 0, random.uniform(3,8), random.uniform(-3,3), random.randint(5,10), "right")))
        cracks.append(("right", branch(R, y0, z0, 0, -random.uniform(3,8), random.uniform(-3,3), random.randint(4,8), "right")))
    for _ in range(5):
        x0 = random.uniform(-280, 280)
        z0 = random.uniform(30, 160)
        cracks.append(("back", branch(x0, R, z0, random.uniform(3,8), 0, random.uniform(-3,3), random.randint(5,10), "back")))
        cracks.append(("back", branch(x0, R, z0, -random.uniform(3,8), 0, random.uniform(-3,3), random.randint(4,8), "back")))
    return cracks

def draw_torches():
    q = gluNewQuadric()
    t = torch_flicker_frame
    for (tx, ty, tz) in TORCH_POSITIONS:
        glPushMatrix()
        glTranslatef(tx, ty, tz)
        glColor3f(0.35, 0.25, 0.10)
        gluCylinder(q, 3, 3, 18, 6, 1)
        glTranslatef(0, 0, 18)
        glColor3f(0.50, 0.30, 0.08)
        gluCylinder(q, 6, 4, 6, 8, 1)
        flick = 0.5 + 0.5 * math.sin(t * 0.37 + tx * 0.1 + ty * 0.07)
        flick2 = 0.5 + 0.5 * math.sin(t * 0.53 + tx * 0.13)
        glTranslatef(0, 0, 6)
        glColor3f(1.0, 0.35 + 0.25 * flick, 0.02)
        gluSphere(q, 7 + 2 * flick2, 8, 6)
        glColor3f(1.0, 0.80 + 0.20 * flick, 0.10)
        glTranslatef(0, 0, 8)
        gluCylinder(q, 3, 0.2, 10 + 4 * flick2, 6, 2)
        glColor3f(0.80, 0.30 + 0.20 * flick, 0.00)
        glTranslatef(0, 0, -8)
        gluCylinder(q, 10 + flick2 * 3, 10 + flick2 * 2, 1.5, 12, 1)
        glPopMatrix()

def draw_blood_drips():
    glColor3f(0.55, 0.02, 0.02)
    R = ROOM_SIZE - 2
    for d in blood_drips:
        wx, wy, wall, start_z, length, _ = d
        if length <= 0:
            continue
        end_z = start_z - length
        W = 2.5
        glBegin(GL_QUADS)
        if wall == "left":
            glVertex3f(-R, wx - W, start_z)
            glVertex3f(-R, wx + W, start_z)
            glVertex3f(-R, wx + W, end_z)
            glVertex3f(-R, wx - W, end_z)
        elif wall == "right":
            glVertex3f(R, wy - W, start_z)
            glVertex3f(R, wy + W, start_z)
            glVertex3f(R, wy + W, end_z)
            glVertex3f(R, wy - W, end_z)
        elif wall == "back":
            glVertex3f(wx - W, R, start_z)
            glVertex3f(wx + W, R, start_z)
            glVertex3f(wx + W, R, end_z)
            glVertex3f(wx - W, R, end_z)
        elif wall == "front":
            glVertex3f(wx - W, -R, start_z)
            glVertex3f(wx + W, -R, start_z)
            glVertex3f(wx + W, -R, end_z)
            glVertex3f(wx - W, -R, end_z)
        glEnd()
        glPushMatrix()
        if wall == "left":
            glTranslatef(-R, wx, end_z)
        elif wall == "right":
            glTranslatef(R, wy, end_z)
        elif wall == "back":
            glTranslatef(wx, R, end_z)
        else:
            glTranslatef(wx, -R, end_z)
        q = gluNewQuadric()
        gluSphere(q, 4, 6, 4)
        glPopMatrix()

def draw_wall_cracks():
    glColor3f(0.06, 0.04, 0.03)
    glLineWidth(1.5)
    for (wall, pts) in wall_cracks:
        glBegin(GL_LINE_STRIP)
        for (px, py, pz) in pts:
            glVertex3f(px, py, pz)
        glEnd()
    glLineWidth(1.0)

def draw_skull(wall):
    q = gluNewQuadric()
    glColor3f(0.82, 0.78, 0.68)
    gluSphere(q, 12, 10, 8)
    glColor3f(0.75, 0.70, 0.60)
    glPushMatrix()
    glTranslatef(0, 3, -8)
    glScalef(1.0, 0.85, 0.45)
    gluSphere(q, 10, 8, 6)
    glPopMatrix()
    glColor3f(0.04, 0.02, 0.02)
    glPushMatrix()
    glTranslatef(-5, 12, 2)
    gluSphere(q, 4, 6, 4)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(5, 12, 2)
    gluSphere(q, 4, 6, 4)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 13, -3)
    gluSphere(q, 2.5, 5, 4)
    glPopMatrix()
    glColor3f(0.88, 0.84, 0.72)
    for tx in [-6, -2, 2, 6]:
        glPushMatrix()
        glTranslatef(tx, 11, -9)
        glScalef(0.25, 0.15, 0.35)
        glutSolidCube(12)
        glPopMatrix()

def draw_skulls():
    for (sx, sy, sz, wall) in SKULL_POSITIONS:
        glPushMatrix()
        glTranslatef(sx, sy, sz)
        if wall == "left":
            glRotatef(-90, 0, 0, 1)
            glRotatef(90, 0, 1, 0)
        elif wall == "right":
            glRotatef(90, 0, 0, 1)
            glRotatef(-90, 0, 1, 0)
        elif wall == "back":
            glRotatef(180, 0, 0, 1)
            glRotatef(180, 1, 0, 0)
        draw_skull(wall)
        glPopMatrix()

def draw_chain_link(q, r=4.5, h=8):
    glColor3f(0.30, 0.28, 0.24)
    segs = 12
    for i in range(segs):
        a0 = 2 * math.pi * i / segs
        a1 = 2 * math.pi * (i + 1) / segs
        x0, y0 = r * math.cos(a0), r * math.sin(a0)
        x1, y1 = r * math.cos(a1), r * math.sin(a1)
        glBegin(GL_QUADS)
        glVertex3f(x0 - 1.5, y0 - 1.5, 0)
        glVertex3f(x1 - 1.5, y1 - 1.5, 0)
        glVertex3f(x1 + 1.5, y1 + 1.5, h)
        glVertex3f(x0 + 1.5, y0 + 1.5, h)
        glEnd()

def draw_hanging_chains():
    q = gluNewQuadric()
    H = 200
    for (cx, cy, nlinks, offset) in CHAIN_DATA:
        sway_angle = chain_sway + offset * 30.0
        glPushMatrix()
        glTranslatef(cx, cy, H)
        glRotatef(sway_angle, 1, 0, 0)
        link_h = 9
        for i in range(nlinks):
            glPushMatrix()
            if i % 2 == 0:
                glRotatef(90, 0, 0, 1)
            glTranslatef(0, 0, -i * link_h)
            draw_chain_link(q)
            glPopMatrix()
        glTranslatef(0, 0, -nlinks * link_h)
        glColor3f(0.25, 0.22, 0.18)
        gluCylinder(q, 3, 0.5, 10, 6, 2)
        glPopMatrix()

def draw_cobweb_at(cx, cy, cz, sway_deg):
    RINGS = 5
    SPOKES = 8
    MAX_R = 70.0
    glPushMatrix()
    glTranslatef(cx, cy, cz)
    glRotatef(sway_deg, 0, 1, 0)
    glColor3f(0.55, 0.52, 0.48)
    for s in range(SPOKES):
        ang = 2 * math.pi * s / SPOKES
        dx = math.cos(ang)
        dz = -math.sin(ang) * 0.6
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(dx * MAX_R, 0, dz * MAX_R)
        glEnd()
    for r_idx in range(1, RINGS + 1):
        rad = MAX_R * r_idx / RINGS
        glBegin(GL_LINE_LOOP)
        for s in range(SPOKES):
            ang = 2 * math.pi * s / SPOKES
            dx = math.cos(ang) * rad
            dz = -math.sin(ang) * rad * 0.6
            glVertex3f(dx, 0, dz)
        glEnd()
    glPopMatrix()

def draw_cobwebs():
    for (cx, cy, cz) in COBWEB_CORNERS:
        sx = 1 if cx < 0 else -1
        sy = 1 if cy < 0 else -1
        draw_cobweb_at(cx + sx * 50, cy + sy * 50, cz - 10, cobweb_sway)


# ═══════════════════════════════════════════════════════════════════════════
#  SPIDER BODY (shared by intro and win screen)
# ═══════════════════════════════════════════════════════════════════════════

def draw_spider_body(leg_t):
    q = gluNewQuadric()
    breath_scale = 1.0 + 0.04 * math.sin(leg_t * 1.5)
    glScalef(breath_scale, breath_scale, breath_scale)
    glColor3f(0.45, 0.10, 0.55)
    gluSphere(q, 28, 12, 8)
    glColor3f(0.35, 0.08, 0.42)
    glPushMatrix()
    glTranslatef(0, 32, 4)
    gluSphere(q, 18, 10, 8)
    glPopMatrix()
    glow_intensity = 0.5 + 0.5 * math.sin(leg_t * 2.5)
    glColor3f(1.0, 0.4 + glow_intensity * 0.4, 0.0)
    for ex, ey in [(-6, 44), (-2, 46), (2, 46), (6, 44)]:
        glPushMatrix()
        glTranslatef(ex, ey, 8)
        gluSphere(q, 5 + glow_intensity * 2, 8, 6)
        glPopMatrix()
    for ex, ey in [(-6, 44), (-2, 46), (2, 46), (6, 44)]:
        glColor3f(0.90, 0.05, 0.05)
        glPushMatrix()
        glTranslatef(ex, ey, 8)
        gluSphere(q, 3, 6, 4)
        glPopMatrix()
        glColor3f(1.0, 0.8, 0.6)
        glPushMatrix()
        glTranslatef(ex, ey + 1, 9)
        gluSphere(q, 1.2, 5, 4)
        glPopMatrix()
    glColor3f(0.55, 0.30, 0.60)
    for fx in [-5, 5]:
        glPushMatrix()
        glTranslatef(fx, 52, 2)
        glRotatef(20 * (1 if fx > 0 else -1), 0, 0, 1)
        gluCylinder(q, 2.5, 0.5, 12, 6, 2)
        glPopMatrix()
    for side in [-1, 1]:
        for li in range(4):
            base_ang = 30 + li * 28
            sway     = 12 * math.sin(leg_t + li * 1.2) * (1 if li % 2 == 0 else -1)
            ang_out  = math.radians(base_ang + sway)
            lx       = side * 20
            ly       = 28 + li * 6
            ux = side * 60 * math.cos(ang_out * 0.6)
            uz = 30  * math.sin(ang_out * 0.5) - 10
            glColor3f(0.40, 0.12, 0.50)
            glBegin(GL_LINES)
            glVertex3f(lx, ly, 0)
            glVertex3f(lx + ux, ly, uz)
            glEnd()
            glPushMatrix()
            glTranslatef(lx, ly, 0)
            glColor3f(0.42, 0.14, 0.52)
            gluSphere(q, 4, 6, 4)
            glPopMatrix()
            lx2 = lx + ux + side * 50 * math.cos(ang_out * 0.4)
            lz2 = uz - 40
            glColor3f(0.40, 0.12, 0.50)
            glBegin(GL_LINES)
            glVertex3f(lx + ux, ly, uz)
            glVertex3f(lx2, ly, lz2)
            glEnd()

# ═══════════════════════════════════════════════════════════════════════════
#  WIN SPIDER OVERLAY  (congratulations scene)
# ═══════════════════════════════════════════════════════════════════════════

def draw_win_spider_overlay():
    """Full-screen congratulations overlay with spider and gold particle burst."""
    global win_spider_leg_anim, bat_frame

    if not win_spider_active:
        return

    bat_frame += 0.02
    win_spider_leg_anim += 0.12

    glDisable(GL_DEPTH_TEST)

    # --- dark gold overlay ---
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Deep background
    glColor3f(0.04, 0.03, 0.01)
    glBegin(GL_QUADS)
    glVertex2f(0,0); glVertex2f(WIN_W,0)
    glVertex2f(WIN_W,WIN_H); glVertex2f(0,WIN_H)
    glEnd()

    # Golden particle burst from top-centre (simulated as radiating lines)
    cx_p = WIN_W // 2
    cy_p = WIN_H - 80
    t = win_spider_leg_anim
    for i in range(40):
        ang = 2 * math.pi * i / 40 + t * 0.3
        length = 60 + 40 * math.sin(t * 1.5 + i * 0.4)
        brightness = 0.5 + 0.5 * math.sin(t * 2.0 + i * 0.8)
        glColor3f(1.0, 0.75 * brightness + 0.25, 0.0)
        glLineWidth(1.5)
        glBegin(GL_LINES)
        glVertex2f(cx_p, cy_p)
        glVertex2f(cx_p + math.cos(ang) * length, cy_p + math.sin(ang) * length * 0.5)
        glEnd()
    glLineWidth(1.0)

    # Confetti coins  
    for i in range(25):
        ang = 2 * math.pi * i / 25
        r2  = 90 + 30 * math.sin(t * 0.7 + i)
        cx2 = cx_p + math.cos(ang + t * 0.2) * r2
        cy2 = cy_p + math.sin(ang + t * 0.2) * r2 * 0.55
        glColor3f(1.0, 0.85, 0.10)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex2f(cx2, cy2)
        glEnd()

    # "YOU WIN!" banner at top
    draw_text_col(WIN_W//2 - 160, WIN_H - 55,
                  "★  YOU WIN!  PHANTOM PALACE CONQUERED  ★",
                  1.0, 0.84, 0.10, GLUT_BITMAP_TIMES_ROMAN_24)

    # Score line
    draw_text_col(WIN_W//2 - 80, WIN_H - 90,
                  f"Final Score: {player_score}",
                  0.90, 0.80, 0.40)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    # --- Spider viewport (left side) ---
    glViewport(20, WIN_H // 2 - 150, 280, 280)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, 280.0 / 280.0, 1.0, 800.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 180, 60, 0, 0, 10, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)

    # Happy spider animation: gentle bob
    bob = math.sin(win_spider_leg_anim * 1.2) * 5
    glTranslatef(0, 0, bob)
    glRotatef(180, 0, 1, 0)
    glRotatef(15, 1, 0, 0)
    glRotatef(win_spider_leg_anim *10, 0, 0, 1)  # slow spin showing off

    draw_spider_body(win_spider_leg_anim)

    glDisable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glViewport(0, 0, WIN_W, WIN_H)

    # --- Dialogue text (right of spider) ---
    visible_lines = []
    for li, line in enumerate(WIN_SPIDER_LINES):
        if li < win_spider_line_idx:
            visible_lines.append(line)
        elif li == win_spider_line_idx:
            visible_lines.append(line[:win_spider_char_idx])
            break

    tx = 340
    ty = WIN_H // 2 + 120

    draw_text_col(tx, ty + 30,
                  "ARACHNIS  [ grudgingly impressed ]",
                  0.80, 0.65, 0.10, GLUT_BITMAP_HELVETICA_18)

    for i, vl in enumerate(visible_lines):
        # Earlier lines dimmer, current line bright gold
        if i < len(visible_lines) - 1:
            col = (0.70, 0.65, 0.45)
        else:
            col = (1.0, 0.95, 0.70)
        draw_text_col(tx, ty - i * 34, vl, *col, GLUT_BITMAP_HELVETICA_18)

    # Blinking cursor on current line
    if win_spider_line_idx < len(WIN_SPIDER_LINES):
        cur_y = ty - (len(visible_lines) - 1) * 34
        draw_text_col(tx + len(visible_lines[-1]) * 10 if visible_lines else tx,
                      cur_y,
                      "_" if (win_spider_frame_count // 15) % 2 == 0 else " ",
                      0.9, 0.9, 0.9)

    # Silk thread from spider to text box
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0.50, 0.45, 0.30)
    glLineWidth(1.2)
    glBegin(GL_LINES)
    glVertex2f(280, WIN_H // 2 + 20)
    glVertex2f(tx - 10, ty + 5)
    glEnd()
    glLineWidth(1.0)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)


def draw_spider_intro():
    global bat_frame

    if not spider_intro_active:
        return

    bat_frame += 0.02

    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.03, 0.01, 0.04)
    glBegin(GL_QUADS)
    glVertex2f(0,0); glVertex2f(WIN_W,0)
    glVertex2f(WIN_W,WIN_H); glVertex2f(0,WIN_H)
    glEnd()

    colors = [
        (1.0, 0.3, 0.3),
        (0.3, 1.0, 0.4),
        (1.0, 0.7, 0.2),
        (0.4, 0.4, 1.0),
    ]
    for i in range(4):
        angle = bat_frame * 2 + i * 1.5
        x = WIN_W - 100 + math.sin(angle) * 30
        y = WIN_H - 60 + math.cos(angle * 1.5) * 15
        wing = math.sin(bat_frame * 2 + i) * 5
        r, g, b = colors[i]
        glColor3f(r, g, b)
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y)
        glVertex2f(x - 12 - wing, y + 10)
        glVertex2f(x - 5, y - 3)
        glVertex2f(x, y)
        glVertex2f(x + 12 + wing, y + 10)
        glVertex2f(x + 5, y - 3)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glPointSize(3.0)
        glBegin(GL_POINTS)
        glVertex2f(x - 3, y + 2)
        glVertex2f(x + 3, y + 2)
        glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glViewport(0, WIN_H // 2 - 120, 280, 240)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, 280.0 / 240.0, 1.0, 800.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 180, 60, 0, 0, 10, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)

    rot_y = treasure_rot *2.0
    rot_x = 10.0
    glRotatef(180, 0, 1, 0)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)

    draw_spider_body(spider_leg_anim)
    glDisable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glViewport(0, 0, WIN_W, WIN_H)

    visible_lines = []
    for li, line in enumerate(SPIDER_LINES):
        if li < spider_line_idx:
            visible_lines.append(line)
        elif li == spider_line_idx:
            visible_lines.append(line[:spider_char_idx])
            break

    tx = 350
    ty = WIN_H // 2 + 140

    draw_text_col(tx, ty + 30, "ARACHNIS  [ palace spider, very tired of adventurers ]",
                  0.50, 0.05, 0.05, GLUT_BITMAP_HELVETICA_18)
    for i, vl in enumerate(visible_lines):
        col = (0.85, 0.80, 0.72) if i < len(visible_lines) - 1 else (1.0, 0.95, 0.85)
        draw_text_col(tx, ty - i * 32, vl, *col, GLUT_BITMAP_HELVETICA_18)

    if spider_line_idx < len(SPIDER_LINES):
        cur_y = ty - (len(visible_lines) - 1) * 32
        draw_text_col(tx + len(visible_lines[-1]) * 10 if visible_lines else tx,
                      cur_y,
                      "_" if (spider_frame_count // 15) % 2 == 0 else " ",
                      0.8, 0.8, 0.8)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0.38, 0.35, 0.32)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex2f(260, WIN_H // 2 + 30)
    glVertex2f(tx - 10, ty + 10)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)

def draw_room():
   R = ROOM_SIZE
   H = 200
   glBegin(GL_QUADS)
   glColor3f(0.22, 0.17, 0.12)
   glVertex3f(-R,-R,0); glVertex3f(R,-R,0); glVertex3f(R,R,0); glVertex3f(-R,R,0)
   glColor3f(0.16, 0.13, 0.10)
   glVertex3f(-R,-R,H); glVertex3f(-R,R,H); glVertex3f(R,R,H); glVertex3f(R,-R,H)
   glColor3f(0.28, 0.20, 0.13)
   glVertex3f(-R,R,0); glVertex3f(R,R,0); glVertex3f(R,R,H); glVertex3f(-R,R,H)
   glColor3f(0.25, 0.18, 0.11)
   glVertex3f(R,-R,0); glVertex3f(-R,-R,0); glVertex3f(-R,-R,H); glVertex3f(R,-R,H)
   glColor3f(0.24, 0.17, 0.10)
   glVertex3f(R,-R,0); glVertex3f(R,R,0); glVertex3f(R,R,H); glVertex3f(R,-R,H)
   glColor3f(0.30, 0.22, 0.14)
   glVertex3f(-R,R,0); glVertex3f(-R,-R,0); glVertex3f(-R,-R,H); glVertex3f(-R,R,H)
   glEnd()
   
   # Draw floor tiles with cracks
   tile = 80
   for ix in range(-int(R//tile), int(R//tile)):
       for iy in range(-int(R//tile), int(R//tile)):
           if (ix + iy) % 2 == 0:
               x0, x1 = ix * tile, (ix + 1) * tile
               y0, y1 = iy * tile, (iy + 1) * tile
               
               # Find if this tile is cracked
               tile_cracked = False
               for t in floor_tiles:
                   if t["x0"] == x0 and t["y0"] == y0:
                       tile_cracked = t["cracked"]
                       break
               
               # Draw tile
               glBegin(GL_QUADS)
               glColor3f(0.18, 0.14, 0.09)
               glVertex3f(x0, y0, 1); glVertex3f(x1, y0, 1)
               glVertex3f(x1, y1, 1); glVertex3f(x0, y1, 1)
               glEnd()
               
               # Draw cracks on top
               if tile_cracked:
                   glColor3f(0.06, 0.04, 0.03)
                   glLineWidth(1.5)
                   cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                   glBegin(GL_LINES)
                   glVertex3f(cx - 15, cy - 15, 1.2)
                   glVertex3f(cx + 10, cy + 5, 1.2)
                   glVertex3f(cx + 10, cy + 5, 1.2)
                   glVertex3f(cx + 20, cy - 10, 1.2)
                   glVertex3f(cx - 5, cy + 15, 1.2)
                   glVertex3f(cx + 5, cy + 5, 1.2)
                   glEnd()
                   glLineWidth(1.0)


def draw_pillar(x, y):
   glPushMatrix()
   glTranslatef(x, y, 0)
   glColor3f(0.52, 0.42, 0.28)
   gluCylinder(gluNewQuadric(), 14, 12, 160, 10, 4)
   glTranslatef(0, 0, 160)
   glColor3f(0.62, 0.52, 0.33)
   glutSolidCube(30)
   glPopMatrix()

def draw_furniture():
   for px, py in [(-300,-300),(300,-300),(-300,300),(300,300)]:
       draw_pillar(px, py)
   glPushMatrix()
   glTranslatef(0, 340, 0)
   glColor3f(0.48, 0.28, 0.08)
   glScalef(1.5, 0.4, 1.8)
   glutSolidCube(60)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(0, 330, 54)
   glColor3f(0.58, 0.36, 0.10)
   glScalef(1.5, 0.25, 2.0)
   glutSolidCube(40)
   glPopMatrix()

def draw_helmet(q):
   glColor3f(0.45, 0.45, 0.50)
   glPushMatrix()
   glTranslatef(0, 0, 2)
   gluSphere(q, 14.5, 12, 8)
   glPopMatrix()
   glColor3f(0.25, 0.25, 0.28)
   glPushMatrix()
   glTranslatef(0, 10, -2)
   glScalef(1.6, 0.25, 0.35)
   glutSolidCube(18)
   glPopMatrix()
   glColor3f(0.40, 0.40, 0.45)
   for sx in [-1, 1]:
       glPushMatrix()
       glTranslatef(sx * 13, 4, -4)
       glScalef(0.20, 0.5, 0.6)
       glutSolidCube(18)
       glPopMatrix()
   glColor3f(0.70, 0.15, 0.15)
   glPushMatrix()
   glTranslatef(0, 0, 13)
   gluCylinder(q, 2.5, 1.0, 12, 8, 2)
   glPopMatrix()

def draw_slash_arc():
   if not slash_active:
       return
   glColor3f(0.9, 0.9, 1.0)
   cx, cy, cz = 0.0, 0.0, 65.0
   inner = 10.0
   glBegin(GL_QUADS)
   for i in range(16):
       a0 = math.radians(-50 + 100 * i / 16)
       a1 = math.radians(-50 + 100 * (i + 1) / 16)
       glVertex3f(math.sin(a0) * inner,       math.cos(a0) * inner,       cz)
       glVertex3f(math.sin(a1) * inner,       math.cos(a1) * inner,       cz)
       glVertex3f(math.sin(a1) * SLASH_RANGE, math.cos(a1) * SLASH_RANGE, cz)
       glVertex3f(math.sin(a0) * SLASH_RANGE, math.cos(a0) * SLASH_RANGE, cz)
   glEnd()

# ═══════════════════════════════════════════════════════════════════════════
#  SHIELD IN HAND  —  face points forward (+Y), sits at arm tip
# ═══════════════════════════════════════════════════════════════════════════
def draw_shield_in_hand(q):
    """Shield face pointing forward (+Y local) positioned at arm tip."""
    # The arm tip is at ~30 units along arm from shoulder.
    # We place the shield centred on that tip, face pointing +Y (forward).
    glColor3f(0.30, 0.35, 0.60)
    glPushMatrix()
    glScalef(2.0, 0.22, 2.4)    # wide(X) x thin(Y) x tall(Z) → face points Y
    glutSolidCube(18)
    glPopMatrix()
    glColor3f(0.20, 0.22, 0.45)
    glPushMatrix()
    glScalef(2.2, 0.14, 2.6)
    glutSolidCube(18)
    glPopMatrix()
    glColor3f(0.80, 0.65, 0.10)
    glPushMatrix()
    glTranslatef(0, 6, 0)       # boss on front (+Y) face
    gluSphere(q, 5, 10, 8)
    glPopMatrix()
    glColor3f(0.75, 0.60, 0.10)
    for rx, rz in [(-12, 12), (12, 12), (-12, -12), (12, -12)]:
        glPushMatrix()
        glTranslatef(rx, 5, rz)
        gluSphere(q, 2, 6, 4)
        glPopMatrix()

# ═══════════════════════════════════════════════════════════════════════════
#  CROSSBOW IN HAND  —  stock gripped, barrel aimed forward along +Y
# ═══════════════════════════════════════════════════════════════════════════
def draw_crossbow_in_hand(q):
    """Crossbow gripped with barrel aimed forward (+Y world after arm rotation)."""
    # Stock along Y (forward), grip below
    glColor3f(0.42, 0.24, 0.08)
    glPushMatrix()
    glScalef(0.55, 3.5, 0.45)
    glutSolidCube(18)
    glPopMatrix()
    glColor3f(0.30, 0.18, 0.06)
    glPushMatrix()
    glTranslatef(0, -10, -6)
    glScalef(0.4, 0.8, 0.8)
    glutSolidCube(10)
    glPopMatrix()
    # Limbs (horizontal, along X)
    glColor3f(0.55, 0.35, 0.12)
    glPushMatrix()
    glTranslatef(-16, 18, 0)
    glRotatef(90, 0, 0, 1)
    gluCylinder(q, 2.5, 1.5, 32, 8, 2)
    glPopMatrix()
    # Bowstring
    glColor3f(0.85, 0.80, 0.70)
    glBegin(GL_QUADS)
    glVertex3f(-16, 18, 0); glVertex3f(0, 13, 0)
    glVertex3f(0,   8,  0); glVertex3f(16, 18, 0)
    glEnd()
    # Barrel along +Y
    glColor3f(0.50, 0.30, 0.10)
    glPushMatrix()
    glTranslatef(0, 6, 3)
    gluCylinder(q, 2.2, 1.8, 34, 8, 2)
    glPopMatrix()

def draw_player_weapon(q):
    """
    Called inside the right-arm glPushMatrix.
    The arm is already rotated (arm tip = local +Z end of the 30-unit cylinder).
    We push to arm tip then orient each weapon.
    """
    # Move to arm tip (arm cylinder is 30 units long along local +Z)
    glTranslatef(0, 0, 30)

    if active_weapon == "shield":
        # Arm points forward (-Y world → local arm dir after -75° X rot).
        # We want shield face = outward (same dir as arm).
        # Rotate shield so its face (+Y local) aligns with arm direction.
        glRotatef(90, 1, 0, 0)   # face shield outward (forward)
        draw_shield_in_hand(q)

    elif active_weapon == "crossbow":
        # Arm already angled forward; align barrel with arm direction.
        # A small tilt so the barrel faces forward-down (natural aim).
        glRotatef(90, 1, 0, 0)
        glRotatef(10, 1, 0, 0)   # slight downward aim correction
        draw_crossbow_in_hand(q)

    else:
        # Sword / basic sword: blade extends upward from fist
        glTranslatef(0, 0, -2)
        if sword_level > 1:
            glColor3f(0.95, 0.82, 0.20)
        else:
            glColor3f(0.80, 0.80, 0.85)
        glScalef(0.15, 0.08, 1.0)
        glutSolidCube(40)

def draw_player():
   if first_person:
       return
   glPushMatrix()
   glTranslatef(player_x, player_y, player_z)
   glRotatef(player_rot, 0, 0, 1)
   glScalef(1.0, 1.0, crouch_scale)
   if game_over:
       glRotatef(90, 1, 0, 0)
   q = gluNewQuadric()
   # Legs
   glPushMatrix()
   glTranslatef(-8, 0, 0)
   glRotatef(walk_swing, 1, 0, 0)
   glColor3f(0.15, 0.15, 0.50)
   gluCylinder(q, 7, 6, 36, 8, 2)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(8, 0, 0)
   glRotatef(-walk_swing, 1, 0, 0)
   glColor3f(0.15, 0.15, 0.50)
   gluCylinder(q, 7, 6, 36, 8, 2)
   glPopMatrix()
   # Torso
   glPushMatrix()
   glTranslatef(0, 0, 36)
   glColor3f(0.20, 0.35, 0.65)
   gluCylinder(q, 14, 11, 28, 10, 4)
   glPopMatrix()
   # Left arm
   glPushMatrix()
   glTranslatef(-18, 0, 56)
   glRotatef(-walk_swing, 1, 0, 0)
   glColor3f(0.20, 0.35, 0.65)
   gluCylinder(q, 5, 4, 30, 8, 2)
   glPopMatrix()
   # Right arm — weapon hand
   glPushMatrix()
   glTranslatef(18, 0, 56)
   if slash_active:
       # Slash arc: arm sweeps forward
       glRotatef(-80, 1, 0, 0)
   elif active_weapon in ("shield", "crossbow"):
       # Arm extended forward, slight down-angle for natural hold
       glRotatef(-80, 1, 0, 0)
   else:
       glRotatef(walk_swing if is_moving else 0.0, 1, 0, 0)
   glColor3f(0.20, 0.35, 0.65)
   gluCylinder(q, 5, 4, 30, 8, 2)
   draw_player_weapon(q)
   glPopMatrix()
   # Head with bob when moving
   bob_z = 3.0 * math.sin(ghost_bob_frame * 2.0) if is_moving else 0.0
   glPushMatrix()
   glTranslatef(0, 0, 78 + bob_z)
   glColor3f(0.90, 0.72, 0.55)
   gluSphere(q, 13, 12, 8)
   draw_helmet(q)
   glPopMatrix()
   if slash_active:
       draw_slash_arc()
   glPopMatrix()

def draw_crouch_shadow():
   if not is_crouching:
       return
   glBegin(GL_QUADS)
   glColor3f(0.05, 0.05, 0.05)
   r = 40
   glVertex3f(player_x - r, player_y - r, 2)
   glVertex3f(player_x + r, player_y - r, 2)
   glVertex3f(player_x + r, player_y + r, 2)
   glVertex3f(player_x - r, player_y + r, 2)
   glEnd()

def draw_noise_ripple():
   if not ripple_active:
       return
   glPushMatrix()
   glTranslatef(ripple_x, ripple_y, 4)
   glColor3f(1.0, 1.0, 1.0)
   segments = 48
   glLineWidth(2.0)
   glBegin(GL_LINE_LOOP)
   for i in range(segments):
       a = 2.0 * math.pi * i / segments
       glVertex3f(math.cos(a) * ripple_radius,
                  math.sin(a) * ripple_radius,
                  0.0)
   glEnd()
   glBegin(GL_LINE_LOOP)
   for i in range(segments):
       a = 2.0 * math.pi * i / segments
       glVertex3f(math.cos(a) * (ripple_radius + 3),
                  math.sin(a) * (ripple_radius + 3),
                  0.0)
   glEnd()
   glLineWidth(1.0)
   glPopMatrix()

# ═══════════════════════════════════════════════════════════════════════════
#  CROSSHAIR  (first-person only)
# ═══════════════════════════════════════════════════════════════════════════

def draw_crosshair():
    """Simple dot+cross crosshair for first-person aiming."""
    if not first_person:
        return
    cx = WIN_W // 2
    cy = WIN_H // 2
    size = 12
    gap  = 4
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0.9, 0.9, 0.9)
    glLineWidth(1.5)
    glBegin(GL_LINES)
    # Horizontal
    glVertex2f(cx - size, cy); glVertex2f(cx - gap, cy)
    glVertex2f(cx + gap,  cy); glVertex2f(cx + size, cy)
    # Vertical
    glVertex2f(cx, cy - size); glVertex2f(cx, cy - gap)
    glVertex2f(cx, cy + gap);  glVertex2f(cx, cy + size)
    glEnd()
    glLineWidth(1.0)
    # Centre dot
    glPointSize(3.0)
    glBegin(GL_POINTS)
    glVertex2f(cx, cy)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_elite_ghost(g):
   pulse = 1.0 + 0.08 * math.sin(g["pulse"] * math.pi * 2)
   bob   = math.sin(ghost_bob_frame + g["pulse"] * 6.28) * 6.0
   q = gluNewQuadric()
   glPushMatrix()
   glTranslatef(g["x"], g["y"], g["z"] + bob)
   glScalef(pulse, pulse, pulse)
   if g["hit_flash"] > 0:
       glColor3f(1.0, 0.3, 0.3)
       gluSphere(q, 26, 12, 8)
       glTranslatef(0, 0, 36)
       gluSphere(q, 16, 10, 7)
       glPopMatrix()
       return
   glColor3f(0.10, 0.05, 0.18)
   gluSphere(q, 26, 14, 10)
   glColor3f(0.55, 0.05, 0.05)
   for side in (-1, 1):
       glPushMatrix()
       glTranslatef(side * 24, 0, 12)
       glRotatef(side * 50, 0, 1, 0)
       gluCylinder(q, 4, 0.5, 22, 8, 2)
       glPopMatrix()
   glColor3f(0.30, 0.00, 0.00)
   for rz in [4, -4, -12]:
       glBegin(GL_QUADS)
       glVertex3f(-18, 22, rz);     glVertex3f(18, 22, rz)
       glVertex3f(18,  22, rz+2);   glVertex3f(-18, 22, rz+2)
       glEnd()
   glTranslatef(0, 0, 40)
   glColor3f(0.08, 0.04, 0.14)
   gluSphere(q, 18, 14, 10)
   glColor3f(1.0, 0.05, 0.05)
   glPushMatrix(); glTranslatef( 7, 16,  4); gluSphere(q, 4.5, 8, 6); glPopMatrix()
   glPushMatrix(); glTranslatef(-7, 16,  4); gluSphere(q, 4.5, 8, 6); glPopMatrix()
   glColor3f(1.0, 0.8, 0.0)
   glPushMatrix(); glTranslatef( 7, 18,  4); gluSphere(q, 2.0, 6, 4); glPopMatrix()
   glPushMatrix(); glTranslatef(-7, 18,  4); gluSphere(q, 2.0, 6, 4); glPopMatrix()
   glColor3f(0.40, 0.00, 0.00)
   for hx, ha in [(-10, -20), (0, 0), (10, 20)]:
       glPushMatrix()
       glTranslatef(hx, 5, 16)
       glRotatef(ha, 0, 0, 1)
       gluCylinder(q, 3, 0.3, 24, 8, 2)
       glPopMatrix()
   glColor3f(0.15, 0.08, 0.20)
   glPushMatrix()
   glTranslatef(0, 14, -10)
   glScalef(1.6, 0.25, 0.8)
   glutSolidCube(16)
   glPopMatrix()
   glColor3f(0.20, 0.00, 0.30)
   for ang in range(0, 360, 45):
       glPushMatrix()
       rad_a = math.radians(ang)
       glTranslatef(math.cos(rad_a)*18, math.sin(rad_a)*18, -44)
       glRotatef(ang + 90, 0, 0, 1)
       glRotatef(15, 1, 0, 0)
       gluCylinder(q, 2.5, 0.5, 32, 6, 2)
       glPopMatrix()
   glPopMatrix()

def draw_ghost_hair(q):
   glColor3f(0.05, 0.30, 0.10)
   glPushMatrix()
   glTranslatef(0, 0, 13)
   gluCylinder(q, 2.5, 0.5, 13, 6, 2)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(-5, 3, 11)
   glRotatef(-25, 1, 0, 0)
   gluCylinder(q, 2.0, 0.4, 11, 6, 2)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(5, 3, 11)
   glRotatef(-25, 1, 0, 0)
   gluCylinder(q, 2.0, 0.4, 11, 6, 2)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(0, -5, 11)
   glRotatef(20, 1, 0, 0)
   gluCylinder(q, 1.8, 0.3, 10, 6, 2)
   glPopMatrix()

def draw_ghost_shape(g):
   if current_level >= 5:
       draw_elite_ghost(g)
       return
   pulse = 1.0 + 0.12 * math.sin(g["pulse"] * math.pi * 2)
   bob   = math.sin(ghost_bob_frame + g["pulse"] * 6.28) * 5.0
   q = gluNewQuadric()
   glPushMatrix()
   glTranslatef(g["x"], g["y"], g["z"] + bob)
   glScalef(pulse, pulse, pulse)
   if g["hit_flash"] > 0:
       glColor3f(1.0, 0.3, 0.3)   # red flash instead of white (more visible)
       gluSphere(q, 22, 12, 8)
       glTranslatef(0, 0, 30)
       gluSphere(q, 14, 10, 7)
   elif g["type"] == 0:
       glColor3f(0.55, 0.90, 0.95)
       gluSphere(q, 22, 12, 8)
       glTranslatef(0, 0, 30)
       glColor3f(0.75, 0.95, 1.00)
       gluSphere(q, 14, 10, 7)
       glColor3f(0.10, 0.10, 0.20)
       glPushMatrix(); glTranslatef( 5, 12, 3); gluSphere(q, 3, 6, 4); glPopMatrix()
       glPushMatrix(); glTranslatef(-5, 12, 3); gluSphere(q, 3, 6, 4); glPopMatrix()
   else:
       glColor3f(0.08, 0.48, 0.15)
       gluSphere(q, 22, 12, 8)
       glTranslatef(0, 0, 30)
       glColor3f(0.45, 0.95, 0.40)
       gluSphere(q, 14, 10, 7)
       glColor3f(0.95, 0.05, 0.05)
       glPushMatrix(); glTranslatef( 5, 12, 3); gluSphere(q, 3, 6, 4); glPopMatrix()
       glPushMatrix(); glTranslatef(-5, 12, 3); gluSphere(q, 3, 6, 4); glPopMatrix()
       draw_ghost_hair(q)
   glPopMatrix()

def draw_ghosts():
   for g in ghosts:
       if g["alive"]:
           draw_ghost_shape(g)

def draw_gold_coins():
   q = gluNewQuadric()
   offsets = [(0, 0, 0), (5, 3, 8), (-4, 5, 16)]
   for ox, oy, oz in offsets:
       glPushMatrix()
       glTranslatef(ox, oy, oz)
       glColor3f(1.0, 0.82, 0.10)
       gluCylinder(q, 12, 12, 3, 16, 1)
       glColor3f(1.0, 0.90, 0.40)
       glBegin(GL_QUADS)
       for i in range(16):
           a0 = 2 * math.pi * i / 16
           a1 = 2 * math.pi * (i + 1) / 16
           glVertex3f(0, 0, 3)
           glVertex3f(12 * math.cos(a0), 12 * math.sin(a0), 3)
           glVertex3f(12 * math.cos(a1), 12 * math.sin(a1), 3)
           glVertex3f(0, 0, 3)
       glEnd()
       glColor3f(0.85, 0.68, 0.05)
       glBegin(GL_QUADS)
       for i in range(16):
           a0 = 2 * math.pi * i / 16
           a1 = 2 * math.pi * (i + 1) / 16
           glVertex3f(0, 0, 0)
           glVertex3f(12 * math.cos(a0), 12 * math.sin(a0), 0)
           glVertex3f(12 * math.cos(a1), 12 * math.sin(a1), 0)
           glVertex3f(0, 0, 0)
       glEnd()
       glPopMatrix()

def draw_jeweled_goblet():
   q = gluNewQuadric()
   glColor3f(0.72, 0.45, 0.10)
   glPushMatrix()
   gluCylinder(q, 10, 8, 4, 12, 1)
   glPopMatrix()
   glColor3f(0.80, 0.55, 0.15)
   glPushMatrix()
   glTranslatef(0, 0, 4)
   gluCylinder(q, 4, 3, 14, 8, 2)
   glPopMatrix()
   glColor3f(0.75, 0.12, 0.12)
   glPushMatrix()
   glTranslatef(0, 0, 26)
   gluSphere(q, 12, 12, 8)
   glPopMatrix()
   glColor3f(0.90, 0.70, 0.15)
   glPushMatrix()
   glTranslatef(0, 0, 34)
   gluCylinder(q, 11, 11, 3, 12, 1)
   glPopMatrix()
   gem_colors = [(1.0, 0.84, 0.0), (0.0, 0.78, 0.80), (0.90, 0.20, 0.60)]
   for i, col in enumerate(gem_colors):
       a = math.radians(i * 120)
       glColor3f(*col)
       glPushMatrix()
       glTranslatef(math.cos(a) * 10, math.sin(a) * 10, 26)
       gluSphere(q, 3.5, 8, 6)
       glPopMatrix()

def draw_ancient_artifacts():
   q = gluNewQuadric()
   glPushMatrix()
   glTranslatef(-10, 0, 0)
   glColor3f(0.78, 0.58, 0.28)
   gluCylinder(q, 6, 9, 18, 10, 3)
   glColor3f(0.65, 0.45, 0.18)
   glTranslatef(0, 0, 18)
   gluSphere(q, 9, 10, 6)
   glTranslatef(0, 0, 6)
   glColor3f(0.78, 0.58, 0.28)
   gluCylinder(q, 5, 4, 6, 10, 2)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(10, 0, 0)
   glColor3f(0.55, 0.40, 0.25)
   glutSolidCube(14)
   glColor3f(0.15, 0.08, 0.04)
   glPushMatrix(); glTranslatef(-3, 7, 3); gluSphere(q, 2, 6, 4); glPopMatrix()
   glPushMatrix(); glTranslatef( 3, 7, 3); gluSphere(q, 2, 6, 4); glPopMatrix()
   glPopMatrix()

def draw_royal_crown_jewels():
   q = gluNewQuadric()
   glColor3f(1.0, 0.82, 0.10)
   gluCylinder(q, 14, 14, 10, 16, 2)
   glColor3f(0.90, 0.70, 0.05)
   glPushMatrix()
   glTranslatef(0, 0, 10)
   gluCylinder(q, 14, 14, 2, 16, 1)
   glPopMatrix()
   for i in range(5):
       a = math.radians(i * 72)
       h = 18 if i % 2 == 0 else 12
       glPushMatrix()
       glTranslatef(math.cos(a) * 12, math.sin(a) * 12, 10)
       glColor3f(1.0, 0.85, 0.15)
       gluCylinder(q, 2.5, 0.3, h, 8, 2)
       glTranslatef(0, 0, h)
       col = [(1,0.1,0.1),(0.1,0.4,1.0),(0.7,0.1,0.9),(0.1,0.8,0.5),(1.0,0.6,0.0)][i]
       glColor3f(*col)
       gluSphere(q, 3, 8, 6)
       glPopMatrix()
   glColor3f(0.0, 0.78, 0.80)
   glPushMatrix()
   glTranslatef(0, 14, 5)
   gluSphere(q, 4, 10, 8)
   glPopMatrix()

def draw_magic_relics():
   q = gluNewQuadric()
   glColor3f(0.30, 0.18, 0.55)
   glPushMatrix()
   glutSolidCube(14)
   glPopMatrix()
   glColor3f(0.40, 0.25, 0.70)
   glPushMatrix()
   glTranslatef(0, 0, 7)
   gluCylinder(q, 4, 3, 12, 8, 2)
   glPopMatrix()
   glColor3f(0.55, 0.20, 0.95)
   glPushMatrix()
   glTranslatef(0, 0, 26)
   gluSphere(q, 10, 14, 10)
   glPopMatrix()
   glColor3f(0.85, 0.70, 1.00)
   glPushMatrix()
   glTranslatef(0, 0, 26)
   gluSphere(q, 5, 10, 8)
   glPopMatrix()
   glColor3f(0.90, 0.80, 1.00)
   q2 = gluNewQuadric()
   glPushMatrix()
   glTranslatef(0, 0, 26)
   gluCylinder(q2, 15, 15.5, 1.5, 24, 1)
   glPopMatrix()

def draw_legendary_sword():
   q = gluNewQuadric()
   glColor3f(0.50, 0.28, 0.08)
   glPushMatrix()
   gluCylinder(q, 4, 4, 16, 8, 2)
   glPopMatrix()
   glColor3f(0.85, 0.65, 0.10)
   glPushMatrix()
   glTranslatef(0, 0, -5)
   gluSphere(q, 6, 10, 8)
   glPopMatrix()
   glColor3f(0.85, 0.68, 0.08)
   glPushMatrix()
   glTranslatef(0, 0, 16)
   glScalef(3.5, 0.6, 0.4)
   glutSolidCube(14)
   glPopMatrix()
   glColor3f(0.82, 0.82, 0.90)
   glPushMatrix()
   glTranslatef(0, 0, 18)
   gluCylinder(q, 3.5, 0.3, 42, 8, 4)
   glPopMatrix()
   glColor3f(1.0, 0.84, 0.10)
   glPushMatrix()
   glTranslatef(0, 0, 18)
   gluCylinder(q, 1.2, 0.1, 38, 6, 2)
   glPopMatrix()
   glColor3f(0.90, 0.10, 0.10)
   glPushMatrix()
   glTranslatef(0, 0, 16)
   gluSphere(q, 4, 10, 8)
   glPopMatrix()

def draw_short_sword():
   q = gluNewQuadric()
   glColor3f(0.45, 0.25, 0.08)
   gluCylinder(q, 3.5, 3.5, 12, 8, 2)
   glColor3f(0.70, 0.50, 0.10)
   glPushMatrix()
   glTranslatef(0, 0, -4)
   gluSphere(q, 5, 8, 6)
   glPopMatrix()
   glColor3f(0.75, 0.60, 0.10)
   glPushMatrix()
   glTranslatef(0, 0, 12)
   glScalef(3.0, 0.5, 0.35)
   glutSolidCube(12)
   glPopMatrix()
   glColor3f(0.78, 0.78, 0.85)
   glPushMatrix()
   glTranslatef(0, 0, 14)
   gluCylinder(q, 3, 0.2, 26, 8, 3)
   glPopMatrix()

def draw_shield():
   q = gluNewQuadric()
   glColor3f(0.30, 0.35, 0.60)
   glPushMatrix()
   glScalef(1.8, 0.25, 2.0)
   glutSolidCube(18)
   glPopMatrix()
   glColor3f(0.20, 0.22, 0.45)
   glPushMatrix()
   glScalef(2.0, 0.15, 2.2)
   glutSolidCube(18)
   glPopMatrix()
   glColor3f(0.80, 0.65, 0.10)
   glPushMatrix()
   glTranslatef(0, 6, 0)
   gluSphere(q, 5, 10, 8)
   glPopMatrix()
   glColor3f(0.75, 0.60, 0.10)
   for rx, rz in [(-10, 10), (10, 10), (-10, -10), (10, -10)]:
       glPushMatrix()
       glTranslatef(rx, 4, rz)
       gluSphere(q, 2, 6, 4)
       glPopMatrix()

def draw_crossbow():
   q = gluNewQuadric()
   glColor3f(0.42, 0.24, 0.08)
   glPushMatrix()
   glScalef(0.55, 3.5, 0.45)
   glutSolidCube(18)
   glPopMatrix()
   glColor3f(0.30, 0.18, 0.06)
   glPushMatrix()
   glTranslatef(0, -10, -3)
   glScalef(0.4, 0.8, 0.6)
   glutSolidCube(10)
   glPopMatrix()
   glColor3f(0.55, 0.35, 0.12)
   glPushMatrix()
   glTranslatef(-20, 18, 0)
   glRotatef(90, 0, 0, 1)
   gluCylinder(q, 2.5, 1.5, 20, 8, 2)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(0, 18, 0)
   glRotatef(90, 0, 0, 1)
   gluCylinder(q, 2.5, 1.5, 20, 8, 2)
   glPopMatrix()
   glColor3f(0.85, 0.80, 0.70)
   glBegin(GL_QUADS)
   glVertex3f(-20, 18, 0)
   glVertex3f(  0, 13, 0)
   glVertex3f(  0,  8, 0)
   glVertex3f( 20, 18, 0)
   glEnd()
   glColor3f(0.50, 0.30, 0.10)
   glPushMatrix()
   glTranslatef(0, 5, 4)
   glScalef(0.25, 3.0, 0.25)
   glutSolidCube(10)
   glPopMatrix()

def draw_magic_shield_item():
    q = gluNewQuadric()
    glColor3f(0.30, 0.50, 0.80)
    glPushMatrix()
    glScalef(1.8, 0.25, 2.0)
    glutSolidCube(18)
    glPopMatrix()
    glColor3f(0.60, 0.80, 1.00)
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glutSolidSphere(15, 12, 8)
    glPopMatrix()

def draw_bread():
   q = gluNewQuadric()
   glColor3f(0.70, 0.45, 0.15)
   glPushMatrix()
   glScalef(1.6, 1.2, 0.3)
   glutSolidCube(14)
   glPopMatrix()
   glColor3f(0.85, 0.60, 0.20)
   glPushMatrix()
   glTranslatef(0, 0, 8)
   glScalef(1.5, 1.0, 0.75)
   gluSphere(q, 10, 12, 8)
   glPopMatrix()
   glColor3f(0.72, 0.42, 0.10)
   glPushMatrix()
   glTranslatef(0, 0, 14)
   glScalef(1.4, 0.9, 0.35)
   gluSphere(q, 10, 12, 6)
   glPopMatrix()
   glColor3f(0.55, 0.30, 0.08)
   for off in [-5, 0, 5]:
       glBegin(GL_QUADS)
       glVertex3f(off - 6, -6, 12)
       glVertex3f(off + 6,  6, 12)
       glVertex3f(off + 6,  6, 14)
       glVertex3f(off - 6, -6, 14)
       glEnd()
   glColor3f(0.40, 0.65, 0.15)
   glPushMatrix()
   glTranslatef(4, 0, 18)
   gluCylinder(q, 1, 0.5, 8, 6, 2)
   glPopMatrix()

def draw_meat():
   q = gluNewQuadric()
   glColor3f(0.95, 0.92, 0.85)
   glPushMatrix()
   gluCylinder(q, 3, 3, 20, 8, 2)
   glPopMatrix()
   glColor3f(0.90, 0.87, 0.80)
   glPushMatrix()
   glTranslatef(0, 0, -4)
   gluSphere(q, 5, 8, 6)
   glPopMatrix()
   glColor3f(0.72, 0.22, 0.08)
   glPushMatrix()
   glTranslatef(0, 0, 26)
   gluSphere(q, 14, 14, 10)
   glPopMatrix()
   glColor3f(0.88, 0.55, 0.25)
   for ax, ay, az in [(8, 5, 30), (-7, 8, 28), (3, -10, 32)]:
       glPushMatrix()
       glTranslatef(ax, ay, az)
       gluSphere(q, 4, 8, 6)
       glPopMatrix()

def draw_royal_potion():
   q = gluNewQuadric()
   glColor3f(0.50, 0.15, 0.80)
   glPushMatrix()
   glTranslatef(0, 0, 2)
   gluCylinder(q, 9, 10, 20, 12, 3)
   glPopMatrix()
   glColor3f(0.40, 0.10, 0.65)
   glPushMatrix()
   glBegin(GL_QUADS)
   for i in range(12):
       a0 = 2 * math.pi * i / 12
       a1 = 2 * math.pi * (i + 1) / 12
       glVertex3f(0, 0, 2)
       glVertex3f(9 * math.cos(a0), 9 * math.sin(a0), 2)
       glVertex3f(9 * math.cos(a1), 9 * math.sin(a1), 2)
       glVertex3f(0, 0, 2)
   glEnd()
   glPopMatrix()
   glColor3f(0.55, 0.18, 0.85)
   glPushMatrix()
   glTranslatef(0, 0, 22)
   gluCylinder(q, 10, 6, 8, 12, 2)
   glPopMatrix()
   glColor3f(0.50, 0.15, 0.80)
   glPushMatrix()
   glTranslatef(0, 0, 30)
   gluCylinder(q, 5, 4, 8, 10, 2)
   glPopMatrix()
   glColor3f(0.72, 0.50, 0.28)
   glPushMatrix()
   glTranslatef(0, 0, 38)
   gluCylinder(q, 4, 3, 6, 8, 2)
   glPopMatrix()
   glPushMatrix()
   glTranslatef(0, 0, 44)
   gluSphere(q, 3.5, 8, 6)
   glPopMatrix()
   glColor3f(0.95, 0.85, 1.00)
   glPushMatrix()
   glTranslatef(0, 0, 16)
   gluSphere(q, 6, 10, 8)
   glPopMatrix()
   glColor3f(1.0, 0.84, 0.10)
   glBegin(GL_QUADS)
   for i in range(10):
       a0 = math.radians(i * 36)
       a1 = math.radians((i + 1) * 36)
       r0 = 6 if i % 2 == 0 else 3
       r1 = 6 if (i + 1) % 2 == 0 else 3
       glVertex3f(0, 10, 16)
       glVertex3f(r0 * math.sin(a0), 10 + r0 * math.cos(a0), 16)
       glVertex3f(r1 * math.sin(a1), 10 + r1 * math.cos(a1), 16)
       glVertex3f(0, 10, 16)
   glEnd()

def fire_bullet():
   global player_energy
   if game_over or player_won:
       return
   if player_energy < ENERGY_DRAIN_SHOT:
       return
   player_energy = max(0, player_energy - ENERGY_DRAIN_SHOT)
   rad = math.radians(player_rot)
   dx  = math.sin(rad) * BULLET_SPEED
   dy  = math.cos(rad) * BULLET_SPEED
   bx  = player_x + math.sin(rad) * 30
   by  = player_y + math.cos(rad) * 30
   bz  = player_z + 65
   bullets.append([bx, by, bz, dx, dy, True])

def draw_bullets():
    for b in bullets:
        if not b[5]:
            continue
        glPushMatrix()
        glTranslatef(b[0], b[1], b[2])
        if len(b) > 6 and b[6] == "arrow":
            draw_arrow()
        elif len(b) > 6 and b[6] == "dark_bolt":
            draw_dark_bolt()
        else:
            glColor3f(0.80, 0.55, 0.20)
            glutSolidCube(BULLET_SIZE)
        glPopMatrix()

def draw_arrow():
   q = gluNewQuadric()
   glColor3f(0.50, 0.35, 0.10)
   glPushMatrix()
   glRotatef(90, 1, 0, 0)
   gluCylinder(q, 2, 2, 20, 6, 1)
   glPopMatrix()
   glColor3f(0.9, 0.9, 0.9)
   glPushMatrix()
   glTranslatef(0, 0, 20)
   glRotatef(90, 1, 0, 0)
   gluCylinder(q, 3, 0, 8, 6, 1)
   glPopMatrix()
   glColor3f(0.8, 0.1, 0.1)
   for angle in [0, 120, 240]:
       glPushMatrix()
       glRotatef(angle, 0, 0, 1)
       glTranslatef(0, -3, 0)
       glBegin(GL_QUADS)
       glVertex3f( 0,  0, 0)
       glVertex3f(-4, -8, 0)
       glVertex3f( 0, -6, 0)
       glVertex3f( 4, -8, 0)
       glEnd()
       glPopMatrix()

def spawn_arrow():
   global player_energy
   if game_over or player_won:
       return
   if player_energy < ENERGY_DRAIN_SHOT:
       return
   player_energy -= ENERGY_DRAIN_SHOT
   rad = math.radians(player_rot)
   sin_r = math.sin(rad)
   cos_r = math.cos(rad)
   arm_rot_deg = 80.0
   arm_rot_rad = math.radians(arm_rot_deg)
   arm_len     = 30.0
   barrel_fwd  = 40.0
   total_fwd   = arm_len * math.cos(arm_rot_rad) + barrel_fwd
   loc_x =  18.0
   loc_y =  total_fwd
   loc_z =  56.0 + arm_len * math.sin(arm_rot_rad) + 2.0
   wx = player_x + loc_x * cos_r + loc_y * sin_r
   wy = player_y - loc_x * sin_r + loc_y * cos_r
   wz = player_z + loc_z
   dx = sin_r * BULLET_SPEED
   dy = cos_r * BULLET_SPEED
   bullets.append([wx, wy, wz, dx, dy, True, "arrow"])

def spawn_treasure():
   global TREASURE_X, TREASURE_Y
   if game_over or player_won:
       return
   TREASURE_X = random.uniform(-ROOM_SIZE + 80, ROOM_SIZE - 80)
   TREASURE_Y = random.uniform(-ROOM_SIZE + 80, ROOM_SIZE - 80)

def draw_treasure():
   if not treasure_collected:
       glPushMatrix()
       glTranslatef(TREASURE_X, TREASURE_Y, TREASURE_Z)
       glRotatef(treasure_rot, 0, 0, 1)
       lvl = current_level % 6
       if lvl == 0:
           draw_gold_coins()
       elif lvl == 1:
           draw_jeweled_goblet()
       elif lvl == 2:
           draw_ancient_artifacts()
       elif lvl == 3:
           draw_royal_crown_jewels()
       elif lvl == 4:
           draw_magic_relics()
       elif lvl == 5:
           draw_legendary_sword()
       glPopMatrix()
   if pickup_active:
       glPushMatrix()
       glTranslatef(TREASURE_X, TREASURE_Y, 5)
       glRotatef(-90, 1, 0, 0)
       glColor3f(1.0, 0.9, 0.2)
       qp = gluNewQuadric()
       gluCylinder(qp, pickup_radius, pickup_radius + 2.0, 1.0, 32, 1)
       glPopMatrix()

def draw_ortho_overlay(alpha_dark=True):
   glMatrixMode(GL_PROJECTION)
   glPushMatrix()
   glLoadIdentity()
   gluOrtho2D(0, WIN_W, 0, WIN_H)
   glMatrixMode(GL_MODELVIEW)
   glPushMatrix()
   glLoadIdentity()
   if alpha_dark:
       glColor3f(0.04, 0.02, 0.07)
   glBegin(GL_QUADS)
   glVertex2f(0,     0)
   glVertex2f(WIN_W, 0)
   glVertex2f(WIN_W, WIN_H)
   glVertex2f(0,     WIN_H)
   glEnd()

def pop_ortho_overlay():
   glPopMatrix()
   glMatrixMode(GL_PROJECTION)
   glPopMatrix()
   glMatrixMode(GL_MODELVIEW)

def draw_shop():
   if not shop_open:
       return
   glDisable(GL_DEPTH_TEST)
   draw_ortho_overlay()
   pop_ortho_overlay()
   draw_text_col(WIN_W//2 - 80, WIN_H - 60,
                 "=== PALACE SHOP ===", 1.0, 0.84, 0.10, GLUT_BITMAP_TIMES_ROMAN_24)
   draw_text_col(WIN_W//2 - 200, WIN_H - 90,
                 f"Score (currency): {player_score}  UP/DOWN=Browse  E=Buy  B=Close",
                 0.8, 0.8, 0.8)
   for i, item in enumerate(SHOP_ITEMS):
       base_y = WIN_H - 140 - i * 70
       col = (1.0, 0.84, 0.10) if i == shop_selected else (0.7, 0.7, 0.7)
       draw_text_col(WIN_W//2 - 250, base_y + 10,
                     f"{item['name']:<16}  Cost: {item['cost']:<6} {item['desc']}",
                     *col)
   draw_shop_preview()
   glEnable(GL_DEPTH_TEST)

def draw_shop_preview():
   item = SHOP_ITEMS[shop_selected]
   glViewport(WIN_W - 200, WIN_H//2 - 100, 180, 180)
   glMatrixMode(GL_PROJECTION)
   glPushMatrix()
   glLoadIdentity()
   gluPerspective(40, 1.0, 1.0, 1000.0)
   glMatrixMode(GL_MODELVIEW)
   glPushMatrix()
   glLoadIdentity()
   gluLookAt(0, -80, 60, 0, 0, 20, 0, 0, 1)
   glEnable(GL_DEPTH_TEST)
   glClear(GL_DEPTH_BUFFER_BIT)
   glRotatef(treasure_rot, 0, 0, 1)
   d = item["draw"]
   if d == "bread":
       draw_bread()
   elif d == "meat":
       draw_meat()
   elif d == "potion":
       draw_royal_potion()
   elif d == "sword":
       draw_short_sword()
   elif d == "shield":
       draw_shield()
   elif d == "crossbow":
       draw_crossbow()
   elif d == "magic_shield":  
        draw_magic_shield_item()
   glPopMatrix()
   glMatrixMode(GL_PROJECTION)
   glPopMatrix()
   glMatrixMode(GL_MODELVIEW)
   glViewport(0, 0, WIN_W, WIN_H)

def draw_level_menu():
   if not level_menu_open:
       return
   glDisable(GL_DEPTH_TEST)
   draw_ortho_overlay()
   pop_ortho_overlay()
   cx = WIN_W // 2
   cy = WIN_H // 2
   draw_text_col(cx - 130, cy + 100,
                 f"=== Level {current_level} Complete! ===",
                 1.0, 0.84, 0.10, GLUT_BITMAP_TIMES_ROMAN_24)
   draw_text_col(cx - 180, cy + 60,
                 f"Score: {player_score}   UP/DOWN to select   LEFT CLICK to confirm",
                 0.7, 0.7, 0.7)
   for i, label in enumerate(LEVEL_MENU_ITEMS):
       col = (0.20, 1.00, 0.30) if i == level_menu_sel else (0.75, 0.75, 0.75)
       prefix = ">> " if i == level_menu_sel else "   "
       draw_text_col(cx - 90, cy + 10 - i * 40, prefix + label, *col)
   glEnable(GL_DEPTH_TEST)

def shop_buy():
   global player_score, player_hp, player_energy
   global has_shield, has_crossbow, sword_level
   global BULLET_DAMAGE, SLASH_DAMAGE, SHIELD_ACTIVE
   global has_magic_shield 

   item = SHOP_ITEMS[shop_selected]
   if player_score < item["cost"]:
       return
   player_score -= item["cost"]
   d = item["draw"]
   if d == "bread":
       player_energy = min(MAX_ENERGY, player_energy + 30)
   elif d == "meat":
       player_hp = min(100, player_hp + 40)
   elif d == "potion":
       player_hp     = min(100, player_hp + 50)
       player_energy = min(MAX_ENERGY, player_energy + 50)
   elif d == "sword":
       sword_level = 2
   elif d == "shield":
       has_shield = True
   elif d == "crossbow":
       has_crossbow = True
   elif d == "magic_shield":  
        has_magic_shield = True

def draw_hud():
   bx, bw, bh = 20, 160, 18
   by = WIN_H - 40
   glBegin(GL_QUADS)
   glColor3f(0.30, 0.05, 0.05)
   glVertex3f(bx,    by,    0); glVertex3f(bx+bw, by,    0)
   glVertex3f(bx+bw, by+bh, 0); glVertex3f(bx,    by+bh, 0)
   glEnd()
   hp_w = int(bw * max(player_hp, 0) / 100)
   if invincible_timer > 0 and (invincible_timer // 6) % 2 == 0:
       glColor3f(1.0, 1.0, 1.0)
   else:
       glColor3f(0.85, 0.10, 0.10)
   glBegin(GL_QUADS)
   glVertex3f(bx,      by,    0); glVertex3f(bx+hp_w, by,    0)
   glVertex3f(bx+hp_w, by+bh, 0); glVertex3f(bx,      by+bh, 0)
   glEnd()
   draw_text(bx+2, by+2, f"HP  {player_hp}/100")
   eby = by - 25
   glBegin(GL_QUADS)
   glColor3f(0.05, 0.25, 0.05)
   glVertex3f(bx,    eby,    0); glVertex3f(bx+bw, eby,    0)
   glVertex3f(bx+bw, eby+bh, 0); glVertex3f(bx,    eby+bh, 0)
   glEnd()
   en_w = int(bw * player_energy / MAX_ENERGY)
   glBegin(GL_QUADS)
   glColor3f(0.10, 0.85, 0.20)
   glVertex3f(bx,      eby,    0); glVertex3f(bx+en_w, eby,    0)
   glVertex3f(bx+en_w, eby+bh, 0); glVertex3f(bx,      eby+bh, 0)
   glEnd()
   draw_text(bx+2, eby+2, f"EN  {int(player_energy)}/100")
   alive_g = sum(1 for g in ghosts if g["alive"])
   draw_text(WIN_W - 240, WIN_H - 40,  f"SCORE : {player_score}")
   draw_text(WIN_W - 240, WIN_H - 65,  f"LEVEL : {current_level}")
   draw_text(WIN_W - 240, WIN_H - 90,  f"Ghosts: {alive_g} remaining")
   inv_y = WIN_H - 120
   if has_shield:
       col = (0.20, 1.00, 0.30) if active_weapon == "shield"   else (0.30, 0.50, 1.00)
       draw_text_col(WIN_W - 240, inv_y,      "[SHIELD]  (5)", *col)
   if has_crossbow:
       col = (0.20, 1.00, 0.30) if active_weapon == "crossbow" else (0.80, 0.60, 0.10)
       draw_text_col(WIN_W - 240, inv_y - 22, "[CROSSBOW](6)", *col)
   if sword_level > 1:
       col = (0.20, 1.00, 0.30) if active_weapon == "sword"    else (0.80, 0.80, 0.90)
       draw_text_col(WIN_W - 240, inv_y - 44, "[SHORT SWORD](4)", *col)
   if has_magic_shield:
       draw_text_col(WIN_W - 240, inv_y - 66, "[MAGIC AURA]", 0.4, 0.6, 1.0)   
   if active_weapon is None:
       aw_label = "WEAPON: BASIC SWORD"
   elif active_weapon == "sword":
       aw_label = "WEAPON: SHORT SWORD"
   elif active_weapon == "shield":
       aw_label = "WEAPON: SHIELD"
   elif active_weapon == "crossbow":
       aw_label = "WEAPON: CROSSBOW"
   else:
       aw_label = "WEAPON: BASIC SWORD"
   draw_text_col(WIN_W//2 - 80, WIN_H - 65, aw_label, 0.20, 1.00, 0.30)
   mode_str = "CHEAT ON" if cheat_mode else ""
   if mode_str:
       draw_text(10, 700, mode_str)
   cam_lbl = "CAM: First-Person" if first_person else "CAM: Follow"
   draw_text(WIN_W//2 - 80, WIN_H - 40, cam_lbl)
   if is_crouching:
       draw_text_col(WIN_W//2 - 40, WIN_H - 90, "CROUCHING", 0.8, 0.8, 0.2)
   if alive_g == 0 and not treasure_collected and not level_menu_open:
       draw_text_col(WIN_W//2 - 180, WIN_H//2 - 120,
                     "All ghosts cleared!  Walk to treasure OR press B for Shop",
                     0.9, 0.85, 0.2)
   draw_text(10, 72, "WASD=Move  A/D=Turn  Space=Slash/Arrow  LMB=Fire(Cheat)  RMB=Cam")
   draw_text(10, 50, "G=Crouch  B=Shop  R=Restart  4=Sword  5=Shield  6=Crossbow  C=Cheat")
   if game_over:
       if player_won:
           draw_text_col(WIN_W//2 - 100, WIN_H//2 + 60, "YOU WIN!!!",
                         0.0, 1.0, 0.0, GLUT_BITMAP_TIMES_ROMAN_24)
       draw_text_col(WIN_W//2 - 90, WIN_H//2 + 20,
                     "GAME OVER!", 1.0, 0.1, 0.1)
       draw_text_col(WIN_W//2 - 80, WIN_H//2 - 20,
                     f"Score: {player_score}", 1.0, 1.0, 1.0)
       draw_text_col(WIN_W//2 - 80, WIN_H//2 - 50,
                     "Press R to restart", 1.0, 1.0, 0.0)
def setup_camera():
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   gluPerspective(fovY, WIN_W / WIN_H, 1.0, 3000.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   if first_person:
       rad    = math.radians(player_rot)
       eye_z  = player_z + 75 * crouch_scale
       look_x = player_x + math.sin(rad) * 50
       look_y = player_y + math.cos(rad) * 50
       gluLookAt(player_x, player_y, eye_z,
                 look_x,  look_y,  eye_z,
                 0, 0, 1)
   else:
       h_rad = math.radians(player_rot + cam_angle_h)
       v_rad = math.radians(cam_angle_v)
       cx = player_x - cam_dist * math.sin(h_rad) * math.cos(v_rad)
       cy = player_y - cam_dist * math.cos(h_rad) * math.cos(v_rad)
       cz = player_z + cam_dist * math.sin(v_rad) + 60
       gluLookAt(cx, cy, cz,
                 player_x, player_y, player_z + 50,
                 0, 0, 1)

def check_treasure():
   global treasure_collected, pickup_active, pickup_radius, pickup_alpha
   global player_score, level_menu_open, level_menu_sel
   if treasure_collected:
       return
   alive_g = sum(1 for g in ghosts if g["alive"])
   if math.hypot(player_x - TREASURE_X, player_y - TREASURE_Y) < 30:
       if alive_g == 0:
           treasure_collected = True
           scores = [50, 75, 100, 150, 200, 500]
           player_score += scores[min(current_level, 5)]
           pickup_active = True
           pickup_radius = 5.0
           pickup_alpha  = 1.0
           level_menu_open = True
           level_menu_sel  = 0
   

def advance_level():
   global current_level, treasure_collected, player_won, game_over
   global pickup_active, pickup_radius, pickup_alpha
   global win_spider_active, win_spider_line_idx, win_spider_char_idx
   global win_spider_frame_count, win_spider_line_pause, win_spider_leg_anim

   current_level += 1
   if current_level >= 10 and not game_over:
       print("YOU WIN!")
       player_won = True
       game_over  = True
       ghosts.clear()
       # Trigger win spider!
       win_spider_active      = True
       win_spider_line_idx    = 0
       win_spider_char_idx    = 0
       win_spider_frame_count = 0
       win_spider_line_pause  = 0
       win_spider_leg_anim    = 0.0
       return
   treasure_collected = False
   pickup_active = False
   pickup_radius = 0.0
   pickup_alpha  = 1.0
   init_ghosts()
   spawn_treasure()

def keyboardListener(key, x, y):
   global player_x, player_y, player_rot, game_over, is_crouching
   global slash_active, slash_frame, player_energy, is_moving
   global shop_open, shop_selected, cheat_mode
   global ripple_active, ripple_radius, ripple_x, ripple_y
   global level_menu_open
   global spider_intro_active

   if spider_intro_active:
       if key == b'\r':
           spider_intro_active = False
           init_ghosts()
       glutPostRedisplay()
       return

   is_moving = False
   if key == b'r':
       init_game()
       return
   if game_over:
       return
   if level_menu_open:
       return
   if key == b'4':
       switch_weapon("sword")
       glutPostRedisplay()
       return
   if key == b'5':
       switch_weapon("shield")
       glutPostRedisplay()
       return
   if key == b'6':
       switch_weapon("crossbow")
       glutPostRedisplay()
       return
   rad = math.radians(player_rot)
   spd = CROUCH_SPEED if is_crouching else MOVE_SPEED
   if key == b'w':
       nx = player_x + math.sin(rad) * spd
       ny = player_y + math.cos(rad) * spd
       player_x = clamp(nx, -ROOM_SIZE + 30, ROOM_SIZE - 30)
       player_y = clamp(ny, -ROOM_SIZE + 30, ROOM_SIZE - 30)
       is_moving = True
       if is_crouching:
           if not ripple_active:
               ripple_active = True
               ripple_radius = 0.0
               ripple_x      = player_x
               ripple_y      = player_y
   elif key == b's':
       nx = player_x - math.sin(rad) * spd
       ny = player_y - math.cos(rad) * spd
       player_x = clamp(nx, -ROOM_SIZE + 30, ROOM_SIZE - 30)
       player_y = clamp(ny, -ROOM_SIZE + 30, ROOM_SIZE - 30)
       is_moving = True
       if is_crouching:
           if not ripple_active:
               ripple_active = True
               ripple_radius = 0.0
               ripple_x      = player_x
               ripple_y      = player_y
   elif key == b'a':
       player_rot = (player_rot - ROT_SPEED) % 360
   elif key == b'd':
       player_rot = (player_rot + ROT_SPEED) % 360
   elif key == b'g':
       is_crouching = not is_crouching
   elif key == b'b':
       alive_g = sum(1 for g in ghosts if g["alive"])
       if alive_g == 0 and not treasure_collected:
           shop_open = not shop_open
   elif key == b'e':
       if shop_open:
           shop_buy()
   elif key == b'c':
       cheat_mode = not cheat_mode
   elif key == b' ':
       if active_weapon == "crossbow":
           if player_energy >= ENERGY_DRAIN_SHOT:
               spawn_arrow()
       elif active_weapon is None or active_weapon == "sword":
           if player_energy >= ENERGY_DRAIN_SLASH and not slash_active:
               slash_active = True
               slash_frame  = 0
               player_energy -= ENERGY_DRAIN_SLASH
       if cheat_mode:
           fire_bullet()
   if is_moving:
       drain = ENERGY_DRAIN_CROUCH if is_crouching else ENERGY_DRAIN_MOVE
       player_energy = max(0, player_energy - drain)
   check_treasure()
   glutPostRedisplay()

def specialKeyListener(key, x, y):
   global cam_angle_v, cam_angle_h, shop_open, shop_selected
   global level_menu_open, level_menu_sel, treasure_collected, current_level

   if level_menu_open:
       if key == GLUT_KEY_UP:
           level_menu_sel = (level_menu_sel - 1) % len(LEVEL_MENU_ITEMS)
       elif key == GLUT_KEY_DOWN:
           level_menu_sel = (level_menu_sel + 1) % len(LEVEL_MENU_ITEMS)
       glutPostRedisplay()
       return

   if shop_open:
       if key == GLUT_KEY_UP:
           shop_selected = (shop_selected - 1) % len(SHOP_ITEMS)
       elif key == GLUT_KEY_DOWN:
           shop_selected = (shop_selected + 1) % len(SHOP_ITEMS)
       glutPostRedisplay()
       return

   if key == GLUT_KEY_UP:
       cam_angle_v = min(80, cam_angle_v + 3)
   elif key == GLUT_KEY_DOWN:
       cam_angle_v = max(5,  cam_angle_v - 3)
   elif key == GLUT_KEY_LEFT:
       cam_angle_h = (cam_angle_h - 5) % 360
   elif key == GLUT_KEY_RIGHT:
       cam_angle_h = (cam_angle_h + 5) % 360
   glutPostRedisplay()

def mouseListener(button, state, x, y):
   global first_person, level_menu_open, level_menu_sel
   global treasure_collected, current_level

   if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
       if level_menu_open:
           if level_menu_sel == 0:
               level_menu_open = False
               advance_level()
           elif level_menu_sel == 1:
               level_menu_open = False
               treasure_collected = False
               init_ghosts()
               spawn_treasure()
           elif level_menu_sel == 2:
               level_menu_open = False
               init_game()
           glutPostRedisplay()
           return
       if not game_over:
           if active_weapon == "crossbow":
               spawn_arrow()
           elif cheat_mode:
               fire_bullet()
   elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
       first_person = not first_person
   glutPostRedisplay()


def idle():
   global treasure_rot, walk_frame, walk_swing
   global pickup_active, pickup_radius, pickup_alpha
   global slash_active, slash_frame
   global player_hp, game_over
   global invincible_timer, hp_damage_accum
   global is_crouching, crouch_scale
   global player_score, player_energy
   global ripple_active, ripple_radius
   global spider_intro_active, spider_line_idx, spider_char_idx
   global torch_flicker_frame, chain_sway, cobweb_sway, ghost_bob_frame
   global spider_frame_count, spider_line_pause_timer, spider_leg_anim
   global idle_clock
   global bat_frame,level_menu_open
   global win_spider_active, win_spider_line_idx, win_spider_char_idx
   global win_spider_frame_count, win_spider_line_pause, win_spider_leg_anim

   idle_clock += 1

   # === SPIDER INTRO ===
   if spider_intro_active:
       if spider_line_pause_timer > 0:
           spider_line_pause_timer -= 1
       elif spider_char_idx < len(SPIDER_LINES[spider_line_idx]):
           if spider_frame_count % SPIDER_CHAR_DELAY == 0:
               spider_char_idx += 1
       elif spider_line_idx < len(SPIDER_LINES) - 1:
           if spider_frame_count % SPIDER_LINE_PAUSE == 0:
               if len(SPIDER_LINES) > 0:
                   spider_line_idx += 1
                   spider_char_idx = 0
       spider_frame_count += 1
       spider_leg_anim += 0.15
       treasure_rot = (treasure_rot + 1.5) % 360
       glutPostRedisplay()
       return

   # === WIN SPIDER OVERLAY ===
   if win_spider_active:
       win_spider_frame_count += 1
       win_spider_leg_anim    += 0.12
       if win_spider_line_pause > 0:
           win_spider_line_pause -= 1
       elif win_spider_char_idx < len(WIN_SPIDER_LINES[win_spider_line_idx]):
           if win_spider_frame_count % SPIDER_CHAR_DELAY == 0:
               win_spider_char_idx += 1
       elif win_spider_line_idx < len(WIN_SPIDER_LINES) - 1:
           if win_spider_frame_count % SPIDER_LINE_PAUSE == 0:
               win_spider_line_idx += 1
               win_spider_char_idx  = 0
       glutPostRedisplay()
       return

   # === GAME OVER ===
   if game_over:
       glutPostRedisplay()
       return

   # === ENVIRONMENT UPDATES ===
   torch_flicker_frame += 1.0
   chain_sway = math.sin(idle_clock * 0.02) * 8.0
   cobweb_sway = math.sin(idle_clock * 0.015) * 5.0
   ghost_bob_frame += 0.08

   for d in blood_drips:
       d[4] = min(d[4] + 0.3, 30.0)

   # === ENERGY REGEN ===
   player_energy = min(MAX_ENERGY, player_energy + ENERGY_REGEN_IDLE)
   
   if is_moving:
       walk_frame = (walk_frame + 1) % 30
       walk_swing = 25.0 * math.sin(walk_frame * math.pi / 15.0)
   else:
       walk_swing += (0.0 - walk_swing) * 0.15

   treasure_rot = (treasure_rot + 1.5) % 360

   # === CROUCH ANIMATION ===
   target_scale = 0.55 if is_crouching else 1.0
   crouch_scale += (target_scale - crouch_scale) * 0.18

   # === SLASH ANIMATION ===
   if slash_active:
       if active_weapon not in (None, "sword"):
           slash_active = False
       else:
           slash_frame += 1
           if slash_frame >= SLASH_FRAMES:
               slash_active = False

   # === INVINCIBILITY FRAMES ===
   if invincible_timer > 0:
       invincible_timer -= 1

   # === RIPPLE EFFECT ===
   if ripple_active:
       ripple_radius += 2.5
       if ripple_radius >= MAX_RIPPLE:
           ripple_active = False
           ripple_radius = 0.0

   # === GHOST AI ===
   spd = ghost_speed()
   effective_spd = spd * (0.5 if is_crouching else 1.0)
   detect_radius = 100.0 if is_crouching else 220.0

   for g in ghosts:
       if not g["alive"]:
           continue
       g["pulse"] = (g["pulse"] + 0.008) % 1.0
       if g["hit_flash"] > 0:
           g["hit_flash"] -= 1
       
       dx_to_player = player_x - g["x"]
       dy_to_player = player_y - g["y"]
       dist = math.hypot(dx_to_player, dy_to_player)
       
       if dist < detect_radius:
           g["state"] = "chase"
       else:
           if g["state"] == "chase" and dist > detect_radius + 40:
               g["state"] = "patrol"
       
       if g["state"] == "chase":
           if dist > 0:
               g["x"] += (dx_to_player / dist) * effective_spd
               g["y"] += (dy_to_player / dist) * effective_spd
       else:
           wp = g["waypoints"][g["wp_idx"]]
           dx_wp = wp[0] - g["x"]
           dy_wp = wp[1] - g["y"]
           d_wp  = math.hypot(dx_wp, dy_wp)
           if d_wp < 5:
               g["wp_idx"] = (g["wp_idx"] + 1) % len(g["waypoints"])
           else:
               g["x"] += (dx_wp / d_wp) * effective_spd
               g["y"] += (dy_wp / d_wp) * effective_spd
       
       dist = math.hypot(player_x - g["x"], player_y - g["y"])
       
       # Slash damage with damage numbers
       if slash_active and dist < SLASH_RANGE:
           g["hp"] -= SLASH_DAMAGE
           g["hit_flash"] = 6
           spawn_damage_number(g["x"], g["y"], g["z"], SLASH_DAMAGE, SLASH_DAMAGE >= 2)
           if g["hp"] <= 0:
               g["alive"] = False
               player_score += 25
       
       # Contact damage with magic shield reflection
       if dist < 38 and invincible_timer == 0:
           # Check for magic shield reflection
           if check_magic_shield_reflection(g):
               spawn_reflect_effect(g["x"], g["y"], g["z"])
               g["hp"] -= 3
               spawn_damage_number(g["x"], g["y"], g["z"], 3, True)
               if g["hp"] <= 0:
                   g["alive"] = False
                   player_score += 25
           else:
               g["contact_accum"] = g.get("contact_accum", 0.0) + 1.0
               if g["contact_accum"] >= GHOST_CONTACT_DAMAGE_RATE:
                   g["contact_accum"] = 0.0
                   dmg = 1
                   if SHIELD_ACTIVE:
                       dmg = 0 if random.random() < 0.50 else 1
                   player_hp = max(0, player_hp - dmg)
                   invincible_timer = INVINCIBLE_FRAMES
                   if player_hp == 0:
                       game_over = True

   # === BULLETS ===
   for b in bullets:
       if not b[5]:
           continue
       b[0] += b[3]
       b[1] += b[4]
       if abs(b[0]) > ROOM_SIZE or abs(b[1]) > ROOM_SIZE:
           b[5] = False
           continue
       for g in ghosts:
           if not g["alive"]:
               continue
           if math.hypot(b[0] - g["x"], b[1] - g["y"]) < 26 + BULLET_SIZE:
               b[5] = False
               g["hp"] -= BULLET_DAMAGE
               g["hit_flash"] = 6
               spawn_damage_number(g["x"], g["y"], g["z"], BULLET_DAMAGE, BULLET_DAMAGE >= 3)
               if g["hp"] <= 0:
                   g["alive"] = False
                   player_score += 25
               break
   bullets[:] = [b for b in bullets if b[5]]


   # === PICKUP EFFECT ===
   if pickup_active:
       pickup_radius += 4.0
       pickup_alpha  -= 0.03
       if pickup_alpha <= 0:
           pickup_active = False

   # === FLOOR TILES ===
   update_floor_tiles()     
   update_damage_numbers()
   glutPostRedisplay()

def showScreen():
   glClearColor(0.04, 0.02, 0.07, 1.0)
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glEnable(GL_DEPTH_TEST)
   # Reset matrix stacks to a clean state every frame
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   glViewport(0, 0, WIN_W, WIN_H)
   setup_camera()
   draw_room()

   draw_furniture()
   draw_torches()
   draw_blood_drips()
   draw_wall_cracks()
   draw_skulls()

   draw_palace_portraits()
   draw_hanging_chains()
   draw_cobwebs()
   draw_treasure()

   if spider_intro_active:
       draw_spider_intro()
       glutSwapBuffers()
       return

   # Win spider overlays everything when active
   if win_spider_active:
       draw_win_spider_overlay()
       glutSwapBuffers()
       return

   draw_ghosts()
   
   draw_bullets()
   draw_crouch_shadow()
   draw_noise_ripple()
   if not first_person:
       draw_player()
   draw_magic_shield_visuals() 

   glDisable(GL_DEPTH_TEST)
   draw_hud()
   draw_damage_numbers()      
   draw_magic_shield_effect() 
   draw_crosshair()
   draw_shop()
   draw_level_menu()
   glEnable(GL_DEPTH_TEST)
   glutSwapBuffers()


def main():
   init_game()
   glutInit()
   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
   glutInitWindowSize(WIN_W, WIN_H)
   glutInitWindowPosition(0, 0)
   glutCreateWindow(b"Phantom Treasure - Haunted Palace")
   glEnable(GL_DEPTH_TEST)
   glutDisplayFunc(showScreen)
   glutKeyboardFunc(keyboardListener)
   glutSpecialFunc(specialKeyListener)
   glutMouseFunc(mouseListener)
   glutIdleFunc(idle)
   glutMainLoop()


if __name__ == "__main__":
   main()