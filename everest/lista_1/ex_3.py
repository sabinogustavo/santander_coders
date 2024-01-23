def adicionarElemento(listaA):
	listaA.append(int(42))
	posicao_central = int((len(listaA)/2))
	for i in range(posicao_central,int((len(listaA)/2)+1)):
		listaA[i+1] = listaA[i]
	listaA[posicao_central] = int(42)
	return listaA
	