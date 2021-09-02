import argparse


def base64_e(s):
    base64_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    bin_array = [bin(ord(c))[2:].zfill(8) for c in s]
    bin_string = ''.join(bin_array)

    while len(bin_string)%6:
        bin_string += '0'

    result = ''
    cnt = 0

    t = ''
    for c in bin_string:
        t += c
        cnt += 1
    
        if cnt%6 == 0:
            print(t, int(t, base=2))
            result += base64_char[int(t, base=2)]
            t = ''
            cnt = 0

    print(result)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help='string', required=True)

    args_p = parser.parse_args()

    if args_p.e:
        base64_e(args_p.e)

