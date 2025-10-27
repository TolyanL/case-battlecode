from .stats_settings import RANKS, RANKS_COLORS


class DefaultBadges:
    COMPL_100_QUESTS = {
        "name": "Умник",
        "description": "Выполнил 100 квестов",
        "slug": "smartman",
        "color": "#54f9ff",
    }
    RANK_BADGES = [
        {
            "name": RANKS[i][1][7:],
            "slug": RANKS[i][1][7:].lower(),
            "description": f"Достичь ранга {i + 1}",
            "color": RANKS_COLORS[i - 1],
        }
        for i in range(len(RANKS))
    ]

    @property
    def ALL_BADGES(self) -> list[dict]:
        return self.RANK_BADGES + [
            self.COMPL_100_QUESTS,
        ]
