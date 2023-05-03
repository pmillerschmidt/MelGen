import os


FILE_PATH = "../PROCESSED_DATA/MELODIES/"


def main():

    # rename the file, taking away the dt or tdc
    for root, dirs, files in os.walk(FILE_PATH, topdown=False):
        for name in files:

            old_name = name
            old_path = os.path.join(root, name)

            new_name = ("_").join(old_name.split("_")[:-1]) + ".txt"
            path = os.path.join(root, new_name)
            print(path)

            if os.path.isfile(new_name):
                print("The file already exists")
            else:
                # Rename the file
                os.rename(old_path, path)
                print(new_name)


if __name__ == "__main__":
    main()
