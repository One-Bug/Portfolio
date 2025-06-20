def main():
    extensions(input("File name: ").lower().rstrip().lstrip())


def extensions(e):
    if e.rpartition(".")[2] == "gif" or e.rpartition(".")[2] == "jpg" or e.rpartition(".")[2] == "jpeg" or e.rpartition(".")[2] == "png":
        if e.rpartition(".")[2] == "jpg":
            print("image/jpeg")
        else:
            print("image/" + e.rpartition(".")[2])
    elif e.rpartition(".")[2] == "txt":
        print("text/plain")
    elif e.rpartition(".")[2] == "pdf" or e.rpartition(".")[2] == "zip":
        print("application/" + e.rpartition(".")[2])
    else:
        print("application/octet-stream ")


main()
