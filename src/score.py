
import datetime

if __name__ == "__main__":
    with open("../result.txt", "r") as f:
        lines = f.readlines()
    s_time = datetime.datetime.strptime(lines[0][1:20], "%Y/%m/%d %H:%M:%S")
    t_time = datetime.datetime.strptime(lines[-1][1:20], "%Y/%m/%d %H:%M:%S")

    print((t_time - s_time).total_seconds())