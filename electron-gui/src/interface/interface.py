import json

def main():
    f = open("aa.txt", "a")
    f.write("Now the file has more content!")
    f.close()

    while(True):
        input_stream = input()
        print(input_stream)


if __name__ == '__main__':
    main()
    print("Clean exit")
    sys.stdout.flush()