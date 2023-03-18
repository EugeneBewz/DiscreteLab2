"""
LZW compression
"""

class Lzw:
    def __init__(self) -> None:
        self.encode_dict = {chr(i): i for i in range(256)}
        self.decode_dict = {i: chr(i) for i in range(256)}


    def encode(self, seq: str) -> list[int]:
        """
        Compress message.

        :param seq: string sequence to be compressed
        :return: list of numbers
        """
        add_dict = {}
        idx = 256
        pre_symbol = ""
        codes = []

        for symbol in seq:
            ps = pre_symbol+symbol
            if ps in self.encode_dict | add_dict:
                pre_symbol = ps
            else:
                try:
                    codes.append(self.encode_dict[pre_symbol])
                except KeyError:
                    codes.append(add_dict[pre_symbol])
                add_dict[ps] = idx
                idx += 1
                pre_symbol = symbol

        if pre_symbol != '':
            try:
                codes.append(self.encode_dict[pre_symbol])
            except KeyError:
                codes.append(add_dict[pre_symbol])
        return codes


    def decode(self, codes: list[int]) -> str:
        """
        Decompress data.

        :param codes: list of numbers
        :return: original string
        """
        add_dict = {}
        idx = 256
        result = []
        pre_symbol = codes.pop(0)
        result.append(self.decode_dict[pre_symbol])

        for symbol in codes:
            if symbol in self.decode_dict | add_dict:
                try:
                    entry = self.decode_dict[symbol]
                except KeyError:
                    entry = add_dict[symbol]
            result.append(entry)
            try:
                add_dict[idx] = self.decode_dict[pre_symbol] + entry[0]
            except KeyError:
                add_dict[idx] = add_dict[pre_symbol] + entry[0]
            idx += 1
            pre_symbol = symbol
        return ''.join(result)


if __name__ == '__main__':
    string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    lzw = Lzw()
    compressed = lzw.encode(string)
    decompressed = lzw.decode(compressed)
    print(string == decompressed)
