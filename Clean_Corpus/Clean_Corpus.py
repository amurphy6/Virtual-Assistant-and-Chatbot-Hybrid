if __name__ == "__main__":
    file = open('cornell movie-dialogs corpus/movie_lines.txt')
    my_file = file.readlines()

    file.close()
    my_file = [m.split("+++$+++ ")[-1] for m in my_file]
    file = open("cornell movie-dialogs corpus/movie_lines.txt", "w")
    new_file_contents = "".join(my_file)

    file.write(new_file_contents)
    file.close()
