import os

FILE_PATH = "CHORDS/"


def main():
    for root, dirs, files in os.walk(FILE_PATH):

        for name in files:
            write = False

            # open in reading mode
            f = open(os.path.join(FILE_PATH, name), "r")
            lines = f.readlines()
            # open in writing mode
            f = open(os.path.join(FILE_PATH, name), "w")

            # go through the doc line by line
            for line in lines:
                if line.strip("\n") == "Chords w/ timepoints and roots:":
                    write = True

                if write == True:
                    f.write(line)


if __name__ == "__main__":
    main()
