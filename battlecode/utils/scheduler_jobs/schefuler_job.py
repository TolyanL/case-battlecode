from dataclasses import dataclass

from apscheduler.triggers.cron import CronTrigger


@dataclass
class SchedulerJob:
    id: str
    trigger: CronTrigger
    max_instances: int = 1
    replace_existing: bool = True

    def func(self) -> any:
        pass
