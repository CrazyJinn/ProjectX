import matplotlib.pyplot as plt


def ShowData(labels, sbdValue, train_data_keys, train_data_values, magicNumber):
    result = list(zip(labels, sbdValue, train_data_keys, train_data_values))

    result = sorted(result, key=lambda x: (x[0]))  # 根据类型排序

    # print(result)

    plt.figure()
    flag0 = 0
    flag1 = 0
    flag2 = 0
    flag3 = 0
    for temp in result:
        if(temp[0] == -1 and temp[1] < 0.1 and flag0 < 4):
            plt.plot(range(magicNumber), temp[3], c="black")
            print(temp)
            flag0 += 1
        if(temp[0] == 0 and flag1 < 10):
            plt.plot(range(magicNumber), temp[3], c="red")
            print(temp[2])
            flag1 += 1
        if(temp[0] == 1 and flag2 < 10):
            plt.plot(range(magicNumber), temp[3], c="blue")
            print(temp[2])
            flag2 += 1
        if(temp[0] == 2 and flag3 < 1):
            plt.plot(range(magicNumber), temp[3], c="orange")
            print(temp[2])
            flag3 += 1

    plt.show()
