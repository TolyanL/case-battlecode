from battlecode.stats_settings import RANKS, get_rank


def check_pts(user_profile: object) -> str:
    rank = get_rank(user_profile.pts)
    return RANKS[rank - 1][1][7:].lower().strip()
