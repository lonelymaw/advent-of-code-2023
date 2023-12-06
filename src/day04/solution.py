import math
import re


def parse_card(card: str) -> tuple[set[int], set[int]]:
    parsed = re.sub(r"Card.+:\s*", "", card).split("|")
    return (set(parsed[0].split()), set(parsed[1].split()))


def multiplicative_points(card: str) -> int:
    (winning, player) = parse_card(card)
    return math.floor(math.pow(2, len(winning.intersection(player)) - 1))


def copy_points(card: str):
    (winning, player) = parse_card(card)
    return len(winning.intersection(player))


def copy_card_count(cards: list[str], cur: int, memo_counts: dict[int, int]):
    if cur in memo_counts:
        return memo_counts[cur]
    won_cards = range(1, copy_points(cards[cur]) + 1)
    count = copy_points(cards[cur]) + sum(
        copy_card_count(cards, cur + i, memo_counts) for i in won_cards
    )
    memo_counts[cur] = count
    return count


with open("input.txt", "r") as f:
    cards = f.readlines()
print(sum(multiplicative_points(card) for card in cards))
print(len(cards) + sum(copy_card_count(cards, i, {}) for i in range(0, len(cards))))
