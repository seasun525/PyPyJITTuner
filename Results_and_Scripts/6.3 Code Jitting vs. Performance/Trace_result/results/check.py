import json

def lalala():
    for i in range(13):
        main(i)
        print i
def main(i):
    j = json.load(open(str(i)+'_requst.json', 'r'))
    for key in j.keys():
        lines = j[key]
        if max(lines) - min(lines) > 200:
            print key
            print lines

if __name__ == '__main__':
    lalala()
