import poly_deconv
import sys


def return_number_pair(plain_letter, grid):
    # remember! row then column!
    row_val = 0
    column_val = 0
    for row in grid:
        for cipher_letter in row:
            if cipher_letter == plain_letter:
                return (row_val, column_val)

            column_val += 1

        row_val += 1
        column_val = 0


def convert_letters(grid, letter_list, input_file, out_string="to_poly_output.txt"):
    lines = input_file.readlines()
    wrap_text = 0

    out_file = open(out_string, "w")

    while len(lines) > 0:
        line = lines.pop(0)
        while len(line) > 0:
            if not line[0].isalpha():
                line = line.replace(line[0], "", 1)

            else:
                temp = (line[0]).upper()
                line = line.replace(line[0], "", 1)

                if temp == "J":
                    temp = "I"

                print(return_number_pair(temp, grid))
                print("\n")
                (r_val, l_val) = return_number_pair(temp, grid)

                out_file.write(letter_list[r_val])
                out_file.write(letter_list[l_val])
                # out_file.write("\n")

                wrap_text = (wrap_text + 1) % 40
                if wrap_text == 0:
                    out_file.write("\n")


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
        playfair_grid = poly_deconv.construct_grid(key)

        # if no flags (or further info) print grid
        if len(args) == 0:
            print(playfair_grid)

        # if flags follow behavior
        if args[0][0] == "-":
            if args[0] == "-ADFGX":
                # use ADFGX instead of first row for numbering
                args.pop(0)
                letter_mapping = ["A", "D", "F", "G", "X"]
                args.pop(0)  # pop -l
            elif args[0] == "-l":
                # use first row for numbering
                args.pop(0)
                letter_mapping = playfair_grid[1]
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


# runs main() when called from command line
if __name__ == "__main__":
    main(sys.argv)
