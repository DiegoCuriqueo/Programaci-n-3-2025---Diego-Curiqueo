class Node:
    def __init__(self, key):
        # Completa los atributos que debe tener un nodo
        self.left = None  # Hijo izquierdo
        self.right = None  # Hijo derecho
        self.value = key   # Valor del nodo

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key): 
        def _insert(node, key):
            if node is None:
                return Node(key)
            if node.value == key:
                return node
            if key < node.value:
                node.left = _insert(node.left, key)
            else:
                node.right = _insert(node.right, key)
            return node

        self.root = _insert(self.root, key)

    def search(self, key):
        def _search(node, key):
            if node is None or node.value == key:
                return node
            if key < node.value:
                return _search(node.left, key)
            else:
                return _search(node.right, key)

        return _search(self.root, key)

    def get_successor(self, node):
        node = node.right
        while node and node.left:
            node = node.left
        return node

    def delete(self, key):
        def _delete(node, key):
            if node is None:
                return node
            if key < node.value:
                node.left = _delete(node.left, key)
            elif key > node.value:
                node.right = _delete(node.right, key)
            else:
                # Nodo con un solo hijo o sin hijos
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                # Nodo con dos hijos
                succ = self.get_successor(node)
                node.value = succ.value
                node.right = _delete(node.right, succ.value)

            return node

        self.root = _delete(self.root, key)

    def inorder(self):
        def _inorder(node):
            if node:
                _inorder(node.left)
                print(node.value, end=" ")
                _inorder(node.right)
        _inorder(self.root)
        print()

    def preorder(self):
        def _preorder(node):
            if node:
                print(node.value, end=" ")
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)
        print()

    def postorder(self):
        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                print(node.value, end=" ")
        _postorder(self.root)
        print()

    def bfs(self):
        if self.root is None:
            return

        queue = [self.root]
        while queue:
            curr = queue.pop(0)
            print(curr.value, end=" ")
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)
        print()
    #4) Función de sumar nodos
    def suma_nodos(self):
        def _sum(node):
            if node is None:
                return 0
            return node.value + _sum(node.left) + _sum(node.right)

        return _sum(self.root)
    #5) Altura de Árbol
    def altura(self):
        def _height(node):
            if node is None:
                return -1  # Altura de un nodo nulo
            left = _height(node.left)
            right = _height(node.right)
            return 1 + max(left, right)

        return _height(self.root)
