# Implement the following Node class API.
# If you delete something important, this code is copied in specification.py

class Node:
    def __init__(self, prefix, is_word=False):
        """
        Creates a Node with the given string prefix.
        The root node will be given prefix ''.
        Nodes track:
        - the prefix
        - whether this prefix is also a complete word
        - child nodes
        """

        self._prefix = prefix
        self._is_word = is_word
        self._children = []

    def get_prefix(self):
        """
        Returns the string prefix for this node.
        """

        return self._prefix

    def get_children(self):
        """
        Returns a list of child Node objects, in any order.
        """

        return self._children

    def is_word(self):
        """
        Returns True if this node prefix is also a complete word.
        """

        return self._is_word

    def set_as_word(self):
        self._is_word = True

    def add_word(self, word):
        """
        Adds the complete word into the trie, causing child nodes to be created
        as needed. Only to be called by user on the root node, e.g.
        >>> root = Node('')
        >>> root.add_word('cheese')
        """

        if not word:
            if self.get_prefix():
                # If the word passed in is empty, and this node is not the top:
                self.set_as_word()
            return

        for child in self.get_children():
            if child.get_prefix()[-1] == word[0]:
                node_to_build_from = child
                break

        try:
            node_to_build_from
        except NameError:
            node_to_build_from = Node(self.get_prefix() + word[0])
            self.get_children().append(node_to_build_from)

        node_to_build_from.add_word(word[1:])


    def find(self, prefix):
        """
        Returns the node that matches the given prefix, or None if not found.
        We will only call this method on the root node, e.g.
        >>> root = Node('')
        >>> node = root.find('te')
        """

        if not prefix:
            return self

        for child in self.get_children():
            if prefix[0] == child.get_prefix()[-1]:
                return child.find(prefix[1:])

    def words(self):
        """
        Returns a list of complete words that start with this node's prefix.
        The list should be in lexicographical order.
        """

        list_of_words = []

        if self.is_word():
            list_of_words.append(self.get_prefix())

        for child in self.get_children():
            list_of_words += child.words()

        return sorted(list_of_words)


if __name__ == '__main__':
    # Write your test code here. This code will not be run by the marker.

    # The first example in the question.
    root = Node('')
    for word in ['tea', 'ted', 'ten']:
        root.add_word(word)
    node = root.find('te')
    print(node.get_prefix())
    print(node.is_word())
    print(node.words())

    # The second example in the question.
    root = Node('')
    for word in ['inn', 'in', 'into', 'idle']:
        root.add_word(word)
    node = root.find('in')
    print(node.get_prefix())
    children = node.get_children()
    print(sorted([n.get_prefix() for n in children]))
    print(node.is_word())
    print(node.words())

    # The third example in the question.
    with open('the-man-from-snowy-river.txt') as f:
        words = f.read().split()
    root = Node('')
    for word in words:
        root.add_word(word)
    print(root.find('th').words())
