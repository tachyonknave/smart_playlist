from dataclasses import dataclass, field

@dataclass
class VideoItem:
    title: str
    published_at: str = ""
    resourceId: dict = field(default_factory=dict)
