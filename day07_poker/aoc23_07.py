import sys
import re
import math
from collections import Counter

def check_hand_type(cards):
    frequencies = Counter(cards)
    """
    Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456
    """
    type_counts = frequencies.values()

    if 5 in type_counts:
        return ["five of a kind", 7]
    elif 4 in type_counts:
        return ["four of a kind", 6]
    elif 3 in type_counts and 2 in type_counts:
        return ["full house", 5]
    elif 3 in type_counts:
        return ["three of a kind", 4]
    elif Counter(type_counts)[2] == 2:
        return ["two pair", 3]
    elif 2 in type_counts:
        return ["one pair", 2]
    else:
        return ["high card", 1]
    
def card_to_int(card):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 11
    elif card == "T":
        return 10
    else:
        return int(card)
    
def check_hand_type_wild(cards):
    frequencies = Counter(cards)
    """
    Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456
    """
    jack_count = frequencies["J"]
    del frequencies["J"]
    type_counts = frequencies.values()
    
    if jack_count == 0:
        if 5 in type_counts:
            return ["five of a kind", 7]
        elif 4 in type_counts:
            return ["four of a kind", 6]
        elif 3 in type_counts and 2 in type_counts:
            return ["full house", 5]
        elif 3 in type_counts:
            return ["three of a kind", 4]
        elif Counter(type_counts)[2] == 2:
            return ["two pair", 3]
        elif 2 in type_counts:
            return ["one pair", 2]
        else:
            return ["high card", 1]
    else:
        if jack_count == 5:
            return ["five of a kind", 7]
        elif max(type_counts) + jack_count == 5:
            return ["five of a kind", 7]
        elif max(type_counts) + jack_count == 4:
            return ["four of a kind", 6]
        elif Counter(type_counts)[2] == 2 and jack_count == 1:
            return ["full house", 5]
        elif max(type_counts) + jack_count == 3:
            return ["three of a kind", 4]
        elif Counter(type_counts)[2] == 1 and jack_count == 1:
            return ["two pair", 3]
        elif jack_count == 1:
            return ["one pair", 2]
        else:
            return ["high card", 1]
    
def card_to_int_wild(card):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 1
    elif card == "T":
        return 10
    else:
        return int(card)

def parse(file_name):
    hands = []

    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                values = re.findall(r"\w+", clean_line)
                hand = {
                    "cards": values[0],
                    "bet": int(values[1])
                }
                hands.append(hand)

    return hands

def part1(data):
    hands = []

    hands_by_type = {}
    for i in range(7):
        hands_by_type[i+1] = []

    sorted_hands_by_type = {}

    for hand in data:
        hand["card_ints"] = [card_to_int(card) for card in hand["cards"]]
        hand_type = check_hand_type(hand["cards"])
        hand["type"] = hand_type[0]
        hand["type_rank"] = hand_type[1]
        hands_by_type[hand["type_rank"]].append(hand)

    for hand_type in hands_by_type.keys():
        sorted_hands_by_type[hand_type] = sorted(hands_by_type[hand_type], key = lambda x: (x["card_ints"][0], x["card_ints"][1], x["card_ints"][2], x["card_ints"][3], x["card_ints"][4]), reverse=True)

    for hand_type in sorted_hands_by_type.keys():
        preceding_hands = 0
        if hand_type > 1:
            for i in range(1,hand_type):
                preceding_hands += len(sorted_hands_by_type[i])
        number_in_type = len(sorted_hands_by_type[hand_type])
        for hand_index in range(number_in_type):
            sub_rank = number_in_type - hand_index
            sorted_hands_by_type[hand_type][hand_index]["sub_rank"] = sub_rank
            sorted_hands_by_type[hand_type][hand_index]["global_rank"] = sub_rank + preceding_hands

    for hand_type in reversed(sorted_hands_by_type.keys()):
        hands.extend(sorted_hands_by_type[hand_type])

    winnings = 0

    for hand in hands:
        winnings += hand["bet"] * hand["global_rank"]

    return winnings

def part2(data):
    hands = []

    hands_by_type = {}
    for i in range(7):
        hands_by_type[i+1] = []

    sorted_hands_by_type = {}

    for hand in data:
        hand["card_ints"] = [card_to_int_wild(card) for card in hand["cards"]]
        hand_type = check_hand_type_wild(hand["cards"])
        hand["type"] = hand_type[0]
        hand["type_rank"] = hand_type[1]
        hands_by_type[hand["type_rank"]].append(hand)

    for hand_type in hands_by_type.keys():
        sorted_hands_by_type[hand_type] = sorted(hands_by_type[hand_type], key = lambda x: (x["card_ints"][0], x["card_ints"][1], x["card_ints"][2], x["card_ints"][3], x["card_ints"][4]), reverse=True)

    for hand_type in sorted_hands_by_type.keys():
        preceding_hands = 0
        if hand_type > 1:
            for i in range(1,hand_type):
                preceding_hands += len(sorted_hands_by_type[i])
        number_in_type = len(sorted_hands_by_type[hand_type])
        for hand_index in range(number_in_type):
            sub_rank = number_in_type - hand_index
            sorted_hands_by_type[hand_type][hand_index]["sub_rank"] = sub_rank
            sorted_hands_by_type[hand_type][hand_index]["global_rank"] = sub_rank + preceding_hands

    for hand_type in reversed(sorted_hands_by_type.keys()):
        hands.extend(sorted_hands_by_type[hand_type])

    winnings = 0

    for hand in hands:
        winnings += hand["bet"] * hand["global_rank"]

    return winnings

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))