# -*- encoding: utf-8 -*-
'''
@File    :   LZ.py
@Time    :   2023/03/28 13:09:39
@Author  :   zeroc 
'''
from tqdm import tqdm


class LZ78:
    @staticmethod
    def Encode(content: bytes, dic: list) -> list:
        content = [bytes([c]) for c in content]
        prev_sub = b""
        sub_dict = {b"": 0}
        for c in tqdm(content, desc="Encoding"):
            next_sub = prev_sub + c
            if next_sub not in sub_dict:
                i = sub_dict[prev_sub]
                dic.append([c, i])
                sub_dict[next_sub] = len(sub_dict)
                prev_sub = b""
            else:
                prev_sub = next_sub
        if prev_sub != b"":
            i = sub_dict[prev_sub]
            dic.append([b"", i])
        return dic

    @staticmethod
    def Decode(dic: list) -> list:
        content = []
        for d in tqdm(dic, desc="Decoding"):
            tmp = d[0]
            while d[1] != 0:
                d = dic[d[1] - 1]
                tmp += d[0]
            content.append(tmp[::-1])
        return content

if __name__ == "__main__":
    message = b"ABAABBABABABABBABBABAABBBABBAB"
    LZ = LZ78()
    dic = []
    dic = LZ.Encode(message, dic)
    print(dic)
    c = LZ.Decode(dic)
    print(c)
