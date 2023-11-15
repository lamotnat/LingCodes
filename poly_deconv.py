import sys


def construct_grid(key: list) -> list:
    alphabet = list(map(chr, range(ord("A"), ord("Z") + 1)))
    alphabet.remove("J")

    if "J" in key:
        temp = key.index("J")
        key[temp] = "I"

    grid = []
    grid.append([])

    column = 0
    for letter in key:
        if column == 0 and len(grid[-1]) > 0:
            grid.append([])

        grid[-1].append(letter)
        column = (column + 1) % 5

    for letter in alphabet:
        if column == 0 and len(grid[-1]) > 0:
            grid.append([])

        if letter not in key:
            grid[-1].append(letter)
            column = (column + 1) % 5

    return grid


def construct_letter_dict(grid):
    top_row = grid[0]

    mapping = dict()
    val = 0
    for letter in top_row:
        mapping[letter] = val
        val += 1

    return mapping


def convert_letters(grid, letter_dict, input_file, out_string="de_poly_output.txt"):
    lines = input_file.readlines()
    left = None
    right = None
    wrap_text = 0

    out_file = open(out_string, "w")

    while len(lines) > 0:
        line = lines.pop(0)
        while len(line) > 0:
            if line[0] == " " or line[0] == "\n":
                line = line.replace(line[0], "", 1)

            elif left == None:
                left = (line[0]).upper()
                line = line.replace(line[0], "", 1)

            else:
                right = (line[0]).upper()
                line = line.replace(line[0], "", 1)

                l_val = letter_dict[left]
                r_val = letter_dict[right]

                out_file.write(grid[l_val][r_val])

                wrap_text = (wrap_text + 1) % 80
                if wrap_text == 0:
                    out_file.write("\n")

                left = None
                right = None


def main(args):
    # only work when have enough commands
    if len(args) > 1:
        key = []
        args.pop(0)

        # place key into an array
        while (
            len(args) > 0 and args[0].isalpha() and ord("A") <= ord(args[0]) <= ord("Z")
        ):
            key.append(args.pop(0))

        # construct the playfair grid
        playfair_grid = construct_grid(key)

        # if no flags (or further info) print grid
        if len(args) == 0:
            print(playfair_grid)

        # if flags follow behavior
        if args[0][0] == "-":
            if args[0] == "-ADFGX":
                # use ADFGX instead of first row for numbering
                args.pop(0)
                letter_mapping = construct_letter_dict([["A", "D", "F", "G", "X"]])
                args.pop(0)  # pop -l
            elif args[0] == "-l":
                # use first row for numbering
                args.pop(0)
                letter_mapping = construct_letter_dict(playfair_grid)
            else:
                print("unsupported flag")

            # convert and print to output
            in_text = open(args.pop(0))

            # if given output name, print that
            if len(args) > 0 and args[0] == "-out":
                args.pop(0)
                convert_letters(playfair_grid, letter_mapping, in_text, args.pop(0))
            else:
                convert_letters(playfair_grid, letter_mapping, in_text)

    else:
        print("insufficient arguments")


# EX:
# py poly_conv.py A -ADFGX -l input_t.txt -out out.txt


# runs main() when called from command line
if __name__ == "__main__":
    main(sys.argv)
