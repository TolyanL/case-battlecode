from dataclasses import dataclass

from .page_data import MenuItem


@dataclass
class App:
    name: str
    menu_item: MenuItem
