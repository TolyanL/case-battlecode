from battlecode.quest_settings import MIN_PTS


def count_quest_pts(difficulty: str, skills: list[object]) -> int:
    multiplyer = 1
    pts = MIN_PTS

    match difficulty:
        case "easy":
            pass
        case "medium":
            multiplyer += 1.5
        case "hard":
            multiplyer += 2.5

    multiplyer += _count_skill_pts(multiplyer, skills)
    pts = int(multiplyer * pts)

    return pts


def _count_skill_pts(multiplyer: int, skills: list[object]) -> int:
    skill_mult = 0.0
    for skill in skills:
        skill_mult += skill.value * 0.1
    return skill_mult
