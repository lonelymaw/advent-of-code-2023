from dataclasses import dataclass
import re
from typing import Optional


@dataclass
class MappingRange:
    dest_start: int
    source_start: int
    length: int

    def map(self, source: int) -> Optional[int]:
        if not (
            source >= self.source_start and source < self.source_start + self.length
        ):
            return None
        return self.dest_start + source - self.source_start


@dataclass
class Map:
    maps: list[MappingRange]

    def __post_init__(self):
        self.maps.sort(key=lambda m: m.source_start)

    def map(self, source: int) -> int:
        for m in self.maps:
            if m.source_start > source:
                break
            mapped = m.map(source)
            if mapped is not None:
                return mapped
        return source


def map_seed_to_location(seed: int, maps: list[Map]) -> int:
    destination_types = [
        "soil",
        "fertilizer",
        "water",
        "light",
        "temperature",
        "humidity",
        "location",
    ]
    for m, dt in zip(maps, destination_types):
        seed = m.map(seed)
        print(f"{dt}: {seed}")
    return seed


with open("input.txt", "r") as f:
    text = f.read().split("\n\n")
seeds = [int(i) for i in re.sub("seeds:", "", text[0]).split()]
maps = []
for range_list in text[1:]:
    ranges = []
    for line in range_list.splitlines()[1:]:  # Ignore label
        values = [int(i) for i in line.split()]
        ranges.append(MappingRange(values[0], values[1], values[2]))
    maps.append(Map(ranges))
print(min(map_seed_to_location(s, maps) for s in seeds))
