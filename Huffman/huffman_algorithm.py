"""
Huffman algorythm for encoding messages
e.g. ANARONTERRAS ~ 00110010010011010101101010000111
"""


def read_file(filename: str) -> str:
    """
    Read file with message and return list of lines
    which will be encoded with Huffman algorithm. For now,
    we will assume that message consists of one line.
    :param filename: file with text to open
    :return: list of message lines
    """
    with open(filename, "r") as file:
        return file.read()


def count_symbols(message_to_encode: str) -> dict:
    """
    Count every symbol in text and return a dictionary
    that will represent the frequency of every
    symbol, including spaces and punctuation.
    :param message_to_encode: a message to be encoded; generally it's the whole file in one string
    :return: dictionary (e.g. {"A": 0.25, "B": 0.17, ...})
    """

    total_length = len(message_to_encode)
    symbol_percentage = {}

    # Generate a dictionary, that contains number of every symbol
    for symbol in message_to_encode:
        if symbol not in symbol_percentage:
            symbol_percentage[symbol] = 1
        else:
            symbol_percentage[symbol] += 1

    # Regenerate dictionary, changing values to floats
    # that represent the chance of the symbol to appear in text
    # Note: because we round the division results, tha accuracy may be slightly reduced
    for key, value in symbol_percentage.items():
        symbol_percentage[key] = value / total_length

    return symbol_percentage


class HuffmanTree:
    """
    Huffman algorythm for encoding messages and
    decoding messages.
    """

    def __init__(self, left_branch=None, right_branch=None):
        self.left_branch = left_branch
        self.right_branch = right_branch

    def child_nodes(self):
        """
        Returns children of the current node
        :return: left and right children
        """
        return self.left_branch, self.right_branch

    def __str__(self):
        return self.left_branch, self.right_branch

    def encode(self, node, b_str='') -> dict:
        """
        Encode the alphabet, using Huffman algorithm.
        Generates a code for each symbol and replaces
        every character with it.
        :param node: a node to be encoded
        :param b_str: a string that will end up being a code for symbol
        :return: an encoded message
        """
        if type(node) is str:
            return {node: b_str}
        (left, right) = node.child_nodes()
        node_dict = dict()
        node_dict.update(self.encode(left, b_str+"0"))
        node_dict.update(self.encode(right, b_str+"1"))
        return node_dict

    def decode(self, message: str, scrypt: dict) -> str:
        """
        Decode message encoded with Huffman algorithm. It adds digits and finds the pattern
        in given dictionary. If found - replace with a corresponding key.
        :param message: encoded message to decode
        :param scrypt: a dictionary {symbol: code}
        :return: a decoded message
        """
        current_code = ""
        decoded_text = ""

        for digit in message:
            current_code += digit
            if current_code in scrypt.values():
                # find the symbol corresponding to the current code
                for symbol, code in scrypt.items():
                    if code == current_code:
                        decoded_text += symbol
                        current_code = ""
                        break
        return decoded_text


def build_huffman_tree(nodes: list) -> HuffmanTree:
    """
    This function builds a Huffman tree based on
    incoming data about symbols in text. Either
    symbol count or percentage is valid.
    The function will return a HuffmanTree object with
    data about nodes and their children.
    :param nodes: list of nodes and their number (here -- percentage)
    :return: HuffmanTree object
    """
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = HuffmanTree(key1, key2)
        nodes.append((node, c1+c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]


def write_file(write_to: str, write_the: str, scrypt: dict) -> None:
    """
    Write an encoded file according to the Huffman code.
    :param write_to: destination to output file
    :param write_the: data to write
    :param scrypt: dictionary of symbols and their percentages: values show
    how often symbol appears in text.
    """
    with open(write_to, 'w') as encoded_file:
        for line in write_the:
            encoded = ""
            for symbol in line:
                if symbol in scrypt:
                    encoded += scrypt[symbol]
            encoded_file.write(encoded)


if __name__ == "__main__":
    message_short = read_file("huffman_message_short.txt")
    message_medium = read_file("huffman_message_medium.txt")
    message_long = read_file("huffman_message_long.txt")

    short_symbol_percentages = sorted(count_symbols(message_short).items(), key=lambda x: x[1], reverse=True)
    medium_symbol_percentages = sorted(count_symbols(message_medium).items(), key=lambda x: x[1], reverse=True)
    long_symbol_percentages = sorted(count_symbols(message_long).items(), key=lambda x: x[1], reverse=True)

    huffman_tree_small = build_huffman_tree(short_symbol_percentages)
    huffman_tree_medium = build_huffman_tree(medium_symbol_percentages)
    huffman_tree_large = build_huffman_tree(long_symbol_percentages)

    tree = HuffmanTree()

    small_code_dict = tree.encode(huffman_tree_small)
    medium_code_dict = tree.encode(huffman_tree_medium)
    large_code_dict = tree.encode(huffman_tree_large)

    write_file("encoded_short", message_short, small_code_dict)
    write_file("encoded_medium", message_medium, medium_code_dict)
    write_file("encoded_long", message_long, large_code_dict)

    short_message_to_decode = read_file("encoded_short")
    medium_message_to_decode = read_file("encoded_medium")
    long_message_to_decode = read_file("encoded_long")
