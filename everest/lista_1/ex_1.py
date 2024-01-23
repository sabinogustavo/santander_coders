
def ultimoElementoLista2D(listaA):
    ultimo_elemento = []
    
    for i in range(len(listaA)):
        ultimo_elemento.append([listaA[i][-1]])	
    
    tuplas = zip(*[ultimo_elemento])

    
    lista_retorno = []
    
    for tupla in tuplas:
        print(tupla)
        lista_retorno.append(tupla[0][0])

    return lista_retorno


listaA = [[192, 193, 194],
        [507, 508, 509],
        [526, 527, 528, 529],
        [560, 561],
        [635, 636, 637]]

print(ultimoElementoLista2D(listaA))
