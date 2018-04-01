import argparse
import itertools
import time


def find_common_ordered_substrings(strings):
    # Generate all combinations of index selections. Done once because they're the same for all strings.
    # Each one represents a pair such as ([1, 3, 4, 6], [2, 5]) which means that letters at idex 1 3 4 6 go into substring 1, and the rest into substring 2
    # This is done through the cartesian product of [index, -index] for each letter, with a negative value indicating that index goes into substring 2
    # Ex: for 3 characters: [1, -1] x [2, -2] x [3, -3] = [(1, 2, 3), (1, 2, -3), (1, -2, 3), (1, -2, -3), (-1, 2, 3), (-1, 2, -3), (-1, -2, 3), (-1, -2, -3)]
    # Indexes start at 1 because its less trouble than dealing with negative 0s
    indexes = list(range(len(strings[0])))
    selections_choices = [[x + 1, -(x + 1)] for x in indexes]
    selections = list(itertools.product(*selections_choices))
    selection_pairs = {(tuple([(x - 1) for x in perm if x >= 0]), tuple([-(x + 1) for x in perm if x < 0])) for perm in selections}

    # Remove redundant flipped pairs, those where first[0] == second[1] and second[0] == first[1]
    # Instead, when doing the set intersection later, we consider a match if a pair or its flipped pair is present
    # Reducing the size of the selection samples saves much more processing than what's added by the extra test for a flipped pair
    # TODO there's probably a better way to generate only the pairs that are non-flipped, rather than generate all pairs and dump half of them
    # But this is a one-time task, no matter how many strings are processed, so its not that big a deal
    selection_pairs_without_flipped_pairs = set()
    for pair in selection_pairs:
        if (pair[1], pair[0]) not in selection_pairs_without_flipped_pairs:
            selection_pairs_without_flipped_pairs.add(pair)
    selection_pairs = selection_pairs_without_flipped_pairs

    # For each string, list all its possible substrings
    # Letters that go into each substring are based on each precalculated selections
    substring_pairs_per_string = []
    for current_string in strings:
        all_pairs = set()
        for pair in selection_pairs:
            part1 = ''.join([current_string[i] for i in indexes if i in pair[0]])
            part2 = ''.join([current_string[i] for i in indexes if i in pair[1]])
            all_pairs.add((part1, part2))
        substring_pairs_per_string.append(all_pairs)

    # Starting with the set of potential substrings of the first string, intersect with all the other strings' subsets
    final_set = substring_pairs_per_string[0]
    for subset_pairs in substring_pairs_per_string[1:]:
        updated_set = set()
        for pair in subset_pairs:
            if pair in final_set or (pair[1], pair[0]) in final_set:
                updated_set.add(pair)
        final_set = updated_set

    return final_set


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find ordered substrings that are common to multiple strings")
    parser.add_argument('strings_to_process', nargs='*', help='An optional integer positional argument')
    parser.add_argument('--benchmark', dest='benchmark', action='store_true', help='run in benchmark mode')
    args = parser.parse_args()

    strings = args.strings_to_process
    if len(strings) == 0:
        strings = [
        "hellogoodbye",
        "helgoloodbye",
        "goheodlbyleo",
        "gheolodlbyoe",
    ]

    print("Finding common ordered substrings for strings: {}".format(', '.join(strings)))
    runs_count = 10 if args.benchmark is True else 1
    results = set()
    total_time = 0
    for i in range(runs_count):
        time_start = time.time()
        results = find_common_ordered_substrings(strings)
        time_taken = time.time() - time_start
        total_time += time_taken
        print('Took {} seconds to find {} common pairs of substrings'.format(time_taken, len(results)))

    if args.benchmark is True:
        print("{} runs. Total time: {} seconds. Average: {} seconds".format(runs_count, total_time, total_time / runs_count))

    print(results)
