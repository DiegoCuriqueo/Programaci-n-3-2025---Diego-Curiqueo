from BST_base import BST
#Definimos Arbol binario
mybst = BST()
#1) INSERT de numeros
numeros = [25, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 31, 44, 66, 90]
for valor in numeros: 
    mybst.insert(valor)
mybst.preorder()

#2) Busqueda y Visualización de Subarbol
def subarbol_inorder(nodo):
    values = []

    def get_subarbol_inorder(n):
        if n:
            get_subarbol_inorder(n.left)
            values.append(n.value)
            get_subarbol_inorder(n.right)

    get_subarbol_inorder(nodo)
    # Crear nuevo árbol con esos valores en orden
    nuevo_arbol = BST()
    for val in values:
        nuevo_arbol.insert(val)

    return nuevo_arbol

value24 = mybst.search(50)

subarbol24 = subarbol_inorder(value24)
subarbol24.preorder()
#2) Eliminación de valor
#mybst.delete(15)
mybst.bfs()

#2) Inserción y Postorder
#mybst.insert(55)
mybst.postorder()

#3) Analisis de Recorridos
print("Inorder")
mybst.inorder()
print("Preorder")
mybst.preorder()
print("Postorder")
mybst.postorder()
print("BFS")
mybst.bfs()

#4) Suma de valores
print(mybst.suma_nodos())

#5) Altura de ARBOL
print("Altura")
print(mybst.altura())

print("Preorder")
mybst.delete(15)
mybst.preorder()
print("Altura sin 15")
print(mybst.altura())

#6) Validacion
mybst.postorder()