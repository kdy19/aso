import argparse
import json


def dfs(j_data, v, s_list):
    
    for k in j_data.keys():
        s_list.append(k)
        t_data = j_data[k]
        s_print(v, s_list)

        if type(j_data[k]) == type(dict()):
            dfs(t_data, v+1, s_list)
        s_list.pop()


def s_print(v, s_list):

    print(v, end=' ')
    for idx, s in enumerate(s_list):
        if idx == len(s_list)-1:
            print(str(s))
        else:
            print(str(s) + ' -> ', end=' ')
            

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='File Path', required=True)

    args_p = parser.parse_args()
    
    with open(args_p.f, 'r') as jf:
        json_data = json.load(jf)

    select_list = []
    dfs(json_data, 0, select_list)
