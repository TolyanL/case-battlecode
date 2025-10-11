from battlecode.review_settings import GRADE_WEIGHT, CHECKLIST_WEIGHT


def calculate_pts(checklist_len: int, completed_count: int, quest_pts: int, grade: int) -> int:
    if checklist_len == 0:
        checklist_ratio = 1.0
    else:
        checklist_ratio = completed_count / checklist_len

    grade_ratio = max(0.0, min(1.0, (grade - 1) / 4))
    weighted_score = checklist_ratio * CHECKLIST_WEIGHT + grade_ratio * GRADE_WEIGHT

    return int(weighted_score * quest_pts)
