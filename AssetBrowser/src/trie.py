class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        """Return all words that start with the given prefix."""
        results = []
        node = self.root
        for char in prefix:
            if char not in node.children:
                return results  # No match
            node = node.children[char]
        self._find_all_words(node, prefix, results)
        return results

    def _find_all_words(self, node, prefix, results):
        """Helper function to recursively find all words from a given node."""
        if node.is_end_of_word:
            results.append(prefix)
        for char, child_node in node.children.items():
            self._find_all_words(child_node, prefix + char, results)
