"""
LZ77 compression
"""


class LZ77:
    """
    Compress data using LZ77 algorithm
    """

    def __init__(self, buffer_size: int = 5, box_size: int = 5):
        self.buffer_size = buffer_size
        self.box_size = box_size

    def compress(self, message: str) -> list:
        """
        Compress message.

        :param message: a message to be compressed
        :return: list of tuples(<offset, length, next>)
        """

    def decompress(self, compressed_message) -> str:
        """
        Decompress the compressed message

        :param compressed_message: compressed with lz77 message
        :return: decompressed message
        """