"""
LZ77 compression
"""

from typing import List, Tuple


def read_file(filename: str) -> str:
    """
    Read file and return a solid string with data.

    :param filename: path to file
    :return: string with text
    """
    with open(filename, 'r') as file:
        return file.read()


class LZ77:
    def __init__(self, buffer_size: int = 5, box_size: int = 5):
        self.buffer_size = buffer_size
        self.box_size = box_size

    def compress(self, message: str) -> List[Tuple[int, int, str]]:
        """
        Compress message.

        :param message: a message to be compressed
        :return: list of tuples(<offset, length, next_character>)
        """
        cursor = 0
        compressed = []
        while cursor < len(message):
            pattern = (0, 0, '')
            # make a "window" to look over text parts =====================
            box_begin = max(0, cursor - self.box_size)
            box_end = cursor + self.buffer_size
            # make a buffer to store data =================================
            buffer_end = min(box_end, len(message))
            buffer_begin = max(0, buffer_end - self.buffer_size)

            buffer = message[buffer_begin:buffer_end]
            box = message[box_begin:cursor]

            for i in range(len(buffer)):
                j = box.rfind(buffer[:i + 1])
                if j != -1:
                    pattern = (cursor - box_begin - j, i + 1, buffer[i + 1])
            if pattern == (0, 0, ''):
                # no pattern found, encode the current character
                pattern = (0, 0, message[cursor])
                cursor += 1
            else:
                cursor += pattern[1]
            compressed.append(pattern)

        return compressed

    def decompress(self, compressed: List[Tuple[int, int, str]]) -> str:
        """
        Decompress data.

        :param compressed: list of tuples(<offset, length, next_character>)
        :return: original string
        """
        decompressed = ''
        last_char = ''
        for pattern in compressed:
            if pattern[0] == pattern[1] == 0:
                if pattern[2] != last_char:
                    decompressed += pattern[2]
                    last_char = pattern[2]
            else:
                offset = len(decompressed) - pattern[0]
                for i in range(pattern[1]):
                    decompressed += decompressed[offset + i]
                    last_char = decompressed[-1]
                decompressed += pattern[2]
                last_char = pattern[2]
        return decompressed


if __name__ == "__main__":
    lz77 = LZ77(5, 10)
    compressed_message = lz77.compress("abacabacdbacacacd")
    print(compressed_message)
    decompressed_message = lz77.decompress(compressed_message)
    print(decompressed_message)
