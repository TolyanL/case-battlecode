RANKS = (
    ("1", "Lvl. 1 Noobius II"),
    ("2", "Lvl. 2 Noobius I"),
    ("3", "Lvl. 3 Strategist II"),
    ("4", "Lvl. 4 Strategist I"),
    ("5", "Lvl. 5 Innovator II"),
    ("6", "Lvl. 6 Innovator I"),
    ("7", "Lvl. 7 Zero Bug II"),
    ("8", "Lvl. 8 Zero Bug I"),
    ("9", "Lvl. 9 Code Father II"),
    ("10", "Lvl. 10 Code Father I"),
)

RANKS_COLORS = [
    "#90b8c9",  # 1
    "#90b8c9",  # 2
    "#96eaf7",  # 3
    "#47b2fa",  # 4
    "#3385ff",  # 5
    "#0fed17",  # 6
    "#ff5858",  # 7
    "#49e610",  # 8
    "#edb65e",  # 9
    "#ffc821",  # 10
]


def get_rank(pts: int) -> int:
    ranks_pts = [100, 500, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    for i, r_pts in enumerate(reversed(ranks_pts), 1):
        if pts >= r_pts:
            return len(ranks_pts) - i + 1
    return 1
