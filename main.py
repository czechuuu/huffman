import queue
import time
import os


class Node:
    value = 0
    right = None
    left = None
    char = ""

    def leaf(self):
        return self.char != ""

    def __init__(self, val, ch):
        self.value = val
        self.char = ch

    # less than <
    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        if not self.leaf() and other.leaf():
            return True
        if self.leaf() and not other.leaf():
            return False
        if self.leaf() and other.leaf():
            return ord(self.char[0]) < ord(other.char[0])
        return True


def createTree(text):
    nodes = queue.PriorityQueue()
    freq = {}
    rootNode = None
    for letter in text:
        if freq.__contains__(letter):
            freq[letter] += 1
        else:
            freq[letter] = 1
    for letter in freq.keys():
        node = Node(freq[letter], letter)
        nodes.put(node)
    while nodes.qsize() > 1:
        node1 = nodes.get()
        node2 = nodes.get()
        if node1.value == node2.value and not node1.leaf():
            node1, node2 = node2, node1
        parent = Node(node1.value + node2.value, "")
        rootNode = parent
        parent.left = node1
        parent.right = node2
        nodes.put(parent)
    return rootNode


def encode(n, str, txt):
    if n is None:
        return txt
    if n.leaf():
        txt = txt.replace(n.char, str)
    txt = encode(n.left, str + "0", txt)
    txt = encode(n.right, str + "1", txt)
    return txt


def decode(root, text):
    decoded = ""
    currNode = root
    for char in text:
        if char == '0':
            if currNode.left.leaf():
                decoded += currNode.left.char
                currNode = root
            else:
                currNode = currNode.left
        else:
            if currNode.right.leaf():
                decoded += currNode.right.char
                currNode = root
            else:
                currNode = currNode.right
    return decoded


file_in = input("Podaj plik do zakodowania: ")
choice = input("Czy wyświetlić zakodowany i odkodowany plik (y/n): ")

with open(file_in) as f_in:
    contents = f_in.readlines()
    contents = "".join(contents)

tree_start = time.perf_counter()
rootNode = createTree(contents)
tree_end = time.perf_counter()

encode_start = time.perf_counter()
encoded = encode(rootNode, "", contents)
encode_end = time.perf_counter()

decode_start = time.perf_counter()
decoded = decode(rootNode, encoded)
decode_end = time.perf_counter()

if choice.lower() == "y":
    print("\nTekst po zakodowaniu \n" + encoded)
    print("\nTekst po odkodowaniu \n" + decoded)

print("------------STATYSTYKI------------")
print("Rozmiar pliku: " + str(os.stat(file_in).st_size) + "B")
print("Czas stworzenia drzewa: " + str(tree_end-tree_start) + "ms")
print("Czas zakodowania: " + str(encode_end-encode_start) + "ms")
print("Czas odkodowania: " + str(decode_end-decode_start) + "ms")
