import sys
import re


def parse(file_name):
    cards = []

    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                card_number = int(clean_line.split(":")[0].split()[1])
                numbers = clean_line.split(":")[1].split("|")
                winning_numbers = re.findall(r"\d+", numbers[0])
                held_numbers = re.findall(r"\d+", numbers[1])
                card = {
                    "card_number": card_number,
                    "winning_numbers": set(winning_numbers),
                    "held_numbers": held_numbers
                }
                card["matching_numbers"] = card["winning_numbers"].intersection(card["held_numbers"])
                card["matches"] = len(card["matching_numbers"])
                cards.append(card)
                
    return cards

def part1(data):
    """Solve part 1."""
    total_value = 0

    def get_score(card):
        number_of_matches = card["matches"]
        if number_of_matches == 1:
            return 1
        elif number_of_matches > 1:
            return 2**(number_of_matches-1)
        else:
            return 0

    for card in data:
        total_value += get_score(card)
    
    return total_value

def part2(data):
    total_cards = 0

    for card in reversed(data):
        card["value"] = 1
        matches = card["matches"]
        if matches >= 1:
            cards_to_check = data[card["card_number"]:card["card_number"]+matches]
            for check_card in cards_to_check:
                card["value"] += check_card["value"]

    for card in data:
        total_cards += card["value"]

    return total_cards

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