RANKS = (
    ("1", "Lvl. 1 Rookie"),
    ("2", "Lvl. 2 Recruit"),
    ("3", "Lvl. 3 Apprentice"),
    ("4", "Lvl. 4 Journeyman"),
    ("5", "Lvl. 5 Adept"),
    ("6", "Lvl. 6 Specialist"),
    ("7", "Lvl. 7 Expert"),
    ("8", "Lvl. 8 Champion"),
    ("9", "Lvl. 9 Master"),
    ("10", "Lvl. 10 Grandmaster"),
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
