def foo():
    flag = random.choice([True, False])
    if flag:
        print a
    else:
        print b

def loop_func(i):
    if i%2 == 0:
        foo()
    else:
        foo()

def main():
    for i  in range(10000):
        loop_func()
