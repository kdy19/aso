import collections
import random


def mersenne_twister(count: int) -> None:

    diff_list = list()
    zero_list = list()
    one_list = list()

    partition = '-' * 30
    print('\n\n')
    print(partition + str(count) + partition)

    for x in range(10):
        ratio = collections.defaultdict(int)

        for i in range(count):
            x = random.randint(0, 1)

            if x == 0:
                ratio['0'] += 1
            else:
                ratio['1'] += 1

        zero_ratio = round(ratio['0'] / (ratio['0'] + ratio['1']), 15)
        one_ratio = round(ratio['1'] / (ratio['0'] + ratio['1']), 15)
                
        diff_list.append(abs(zero_ratio - one_ratio))
        zero_list.append(zero_ratio)
        one_list.append(one_ratio)

        print('''
            Iterate : {}
            0 {:>7} {:>7}
            1 {:>7} {:>7}
        '''.format(format(count, ','), ratio['0'], zero_ratio, ratio['1'], one_ratio))

    print('''
        Max Ratio Difference {}\n
        Max Ratio Zero {}\t Min Ratio Zero {}
        Max Ratio One {}\t Min Ratio One {}
    '''.format(max(diff_list), max(zero_list), min(zero_list), max(one_list), min(one_list)))


def main():

    for x in range(1, 5+1):
        mersenne_twister(10**x)


if __name__ == '__main__':
    main()
