import sys


def grab_columns(num_columns, input_file):
    temp_stream = []
    in_stream = open(input_file, "r").readlines()

    while len(in_stream) > 0:
        line = in_stream.pop(0)
        while len(line) > 0:
            # clean input stream
            if line[0] == " " or line[0] == "\n":
                line = line.replace(line[0], "", 1)
            else:
                temp_stream.append(line[0])
                line = line.replace(line[0], "", 1)

    # make columns
    columns = [[], [], [], [], []]
    c_val = 0
    for letter in temp_stream:
        columns[c_val].append(letter)
        c_val = (c_val + 1) % 5

    return columns


def print_columns(columns, key, out_f):
    transposed = []
    for n in key:
        transposed.append(columns[n - 1])

    if len(out_f) > 0:
        out_stream = open(out_f, "w")

        format_int = 0
        for c in transposed:
            for letter in c:
                format_int += 1
                out_stream.write(letter)

                if format_int == 80:
                    out_stream.write("\n")
                    format_int = 0

    else:
        print(transposed)


def main(args):
    # only work when have enough commands
    if len(args) > 1:
        key = []
        num_columns = 0
        in_f = ""
        out_f = ""
        args.pop(0)

        # grab number of columns
        if args[0] == "-c":
            args.pop(0)
            num_columns = int(args.pop(0))
        else:
            print("lacking -c #")

        # get key
        if len(args) > 0 and args[0] == "-k":
            args.pop(0)
            while len(args) > 0 and args[0].isnumeric():
                key.append(int(args.pop(0)))
        else:
            print("missing -k #+")

        # get input file
        if len(args) > 0 and args[0] == "-i":
            args.pop(0)
            in_f = args.pop(0)
        else:
            print("missing -i input")

        # get out name
        if len(args) > 0 and args[0] == "-o":
            args.pop(0)
            out_f = args.pop(0)
        else:
            out_f = "transpo_output.txt"

        # actually grab columns and fun stuff
        if len(in_f) > 0:
            columns = grab_columns(num_columns, in_f)

            print_columns(columns, key, out_f)

    else:
        print("insufficient arguments")


# runs main() when called from command line
if __name__ == "__main__":
    main(sys.argv)
