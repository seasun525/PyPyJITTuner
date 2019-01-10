from scipy.stats import ttest_ind
import sys

if __name__ == '__main__':
    list1 = map(float, sys.argv[1].split(','))
    list2 = map(float, sys.argv[2].split(','))

    stat, p_value = ttest_ind(list1, list2)
    print stat, p_value
