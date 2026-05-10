import cv2
import mediapipe as mp
import numpy as np

# ── Setup ──────────────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
h, w = frame.shape[:2]
canvas = np.zeros((h, w, 3), dtype=np.uint8)  # transparent drawing layer

# ── Color palette ──────────────────────────────────────────────────────────
COLORS = {
    "Red":    (0,   0,   255),
    "Green":  (0,   255, 0),
    "Blue":   (255, 0,   0),
    "Yellow": (0,   255, 255),
    "Purple": (255, 0,   255),
    "White":  (255, 255, 255),
    "Eraser": (0,   0,   0),   # draws black = erases on black canvas
}
color_names = list(COLORS.keys())
current_color = COLORS["Red"]
brush_size = 8
eraser_size = 30

prev_x, prev_y = None, None

def draw_palette(img):
    box_w = w // len(color_names)
    for i, name in enumerate(color_names):
        color = COLORS[name]
        x1, x2 = i * box_w, (i + 1) * box_w
        cv2.rectangle(img, (x1, 0), (x2, 60), color, -1)
        cv2.putText(img, name, (x1 + 4, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 0) if name == "White" else (255, 255, 255), 1)
        if COLORS[name] == current_color:
            cv2.rectangle(img, (x1, 0), (x2, 60), (255, 255, 255), 3)

def fingers_up(lm):
    tips = [8, 12, 16, 20]
    up = []
    for tip in tips:
        up.append(lm[tip].y < lm[tip - 2].y)
    return up  # [index, middle, ring, pinky]

def get_color_from_x(x):
    box_w = w // len(color_names)
    idx = min(x // box_w, len(color_names) - 1)
    return COLORS[color_names[idx]]

print("Finger Painter Started!")
print("   Two fingers up  -> select color from palette")
print("   One finger up   -> draw")
print("   Fist            -> pause drawing")
print("   Press C to clear | Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_lm in result.multi_hand_landmarks:
            lm = hand_lm.landmark
            mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

            # Index fingertip position
            ix = int(lm[8].x * w)
            iy = int(lm[8].y * h)

            up = fingers_up(lm)
            index_up  = up[0]
            middle_up = up[1]

            # ── Color selection: index + middle up ──
            if index_up and middle_up:
                prev_x, prev_y = None, None
                if iy < 60:
                    current_color = get_color_from_x(ix)
                cv2.circle(frame, (ix, iy), 12, current_color, -1)
                cv2.putText(frame, "SELECT", (ix - 20, iy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, current_color, 2)

            # ── Drawing: only index up ──
            elif index_up and not middle_up:
                size = eraser_size if current_color == (0,0,0) else brush_size
                if prev_x and prev_y and iy > 60:
                    cv2.line(canvas, (prev_x, prev_y), (ix, iy),
                             current_color, size)
                prev_x, prev_y = ix, iy
                cv2.circle(frame, (ix, iy), size // 2, current_color, -1)

            else:
                prev_x, prev_y = None, None

    # Merge canvas onto frame
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    combined = cv2.add(frame_bg, canvas_fg)

    draw_palette(combined)

    cv2.putText(combined, f"Brush: {brush_size}  |  C=Clear  Q=Quit",
                (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)

    cv2.imshow("AI Finger Painter", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
    elif key == ord('+') or key == ord('='):
        brush_size = min(brush_size + 2, 40)
    elif key == ord('-'):
        brush_size = max(brush_size - 2, 2)

cap.release()
cv2.destroyAllWindows()
print("👋 Painter closed.")
