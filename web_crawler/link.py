from dataclasses import dataclass


@dataclass
class Link:
    href: str
    parent_url: str
    internal: bool

    def display(self):
        print(
            f"Found {'internal' if self.internal else 'external'} link '{self.href}' on '{self.parent_url}'"
        )
