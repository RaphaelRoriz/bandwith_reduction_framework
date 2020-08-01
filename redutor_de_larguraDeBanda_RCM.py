from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.io import mmread
import numpy as np
import matplotlib.pyplot as plt
import time



class redutor_larguraBanda():

	def larguraBanda(self,matrizBase):
		#Atributos
		tamanho = len(matrizBase)
		#Largura atual
		largura = 0
		#Índices
		i = 0
		j = 1	
		
		diagonal = 1
		while(diagonal < tamanho):
			i = 0
			j = diagonal
			continua = True
			while(j < tamanho and continua):
				elemento = matrizBase[i,j]
				if(elemento != 0):
					largura = diagonal
					continua = False
				i += 1
				j += 1
			diagonal += 1
		
		return largura

	def reordenarMatriz(self,matriz,perm_array):
		
		tamanho = len(perm_array)

		#reordenação da matrix
		for i in range(tamanho):
			matriz[:,i] = matriz[perm_array,i]
		for i in range(tamanho):
			matriz[i,:] = matriz[i,perm_array]

		return matriz	


	def reduzir(self,matriz_fileName, simetrica = True):

		matriz = mmread(matriz_fileName)
		matriz = csr_matrix(matriz)
		
		
		plt.rcParams['figure.figsize'] = (15,15)
		fig, axs = plt.subplots(1, 2)
		ax1 = axs[0]
		ax2 = axs[1]

		matriz_densa = matriz.todense() #para auxiliar no plot
		ax1.spy(matriz_densa, markersize=1)
		ax1.set_title('Matriz Original',y=1.08)
		
		##segundo a documentação do RCM do Scipy essa transformação é necessária para matrizes assimetricas
		if not simetrica:
			matriz = matriz + matriz.T

		print("Largura de banda original",self.larguraBanda(matriz_densa))

		#vetor de permutação obtido ao aplicar o algoritmo Reverse Cuthill Mckee, utilizado para reordenar a matrix	
		perm_array = reverse_cuthill_mckee(matriz,symmetric_mode=True)

		
		#reordenação da matriz
		matriz = self.reordenarMatriz(matriz,perm_array)

		matriz_densa = matriz.todense() #para auxiliar no plot
		ax2.spy(matriz_densa, markersize=1)
		ax2.set_title('Matriz Reordenada',y=1.08)
		plt.show()

		print("Largura de banda reduzida",self.larguraBanda(matriz_densa))

	def reduzir_medirTempo(self,matriz_fileName, simetrica = True):

		inicio = time.time()

		matriz = mmread(matriz_fileName)
		matriz = csr_matrix(matriz)
			
		##segundo a documentação do RCM do Scipy essa transformação é necessária para matrizes assimetricas
		if not simetrica:
			matriz = matriz + matriz.T

		#vetor de permutação obtido ao aplicar o algoritmo Reverse Cuthill Mckee, utilizado para reordenar a matrix	
		perm_array = reverse_cuthill_mckee(matriz,symmetric_mode=True)

		#reordenação da matriz
		matriz = self.reordenarMatriz(matriz,perm_array)

		fim = time.time()

		return  fim - inicio



if __name__== '__main__':

	
	redutor = redutor_larguraBanda()


	#Plotar a matriz original e ordenada e printar a largura de banda inicial e reduzida
	
	#simetricas
	redutor.reduzir('G22_naoDirecionado.mtx',simetrica = True)
	#redutor.reduzir('ca-GrQc_naoDirecionado.mtx',simetrica = True)
	#redutor.reduzir('delaunay_n12_naoDirecionado.mtx',simetrica = True)

	#assimetricas
	#redutor.reduzir('gre_1107_direcionado.mtx',simetrica = False)
	#redutor.reduzir('California_direcionado.mtx',simetrica = False)
	#redutor.reduzir('cage9_direcionado.mtx',simetrica = False)


	#Para medir os tempos:

	#simetricas
	#tempo = redutor.reduzir_medirTempo('G22_naoDirecionado.mtx',simetrica = True)
	#tempo = redutor.reduzir_medirTempo('ca-GrQc_naoDirecionado.mtx',simetrica = True)
	#tempo = redutor.reduzir_medirTempo('delaunay_n12_naoDirecionado.mtx',simetrica = True)

	#assimetricas
	#tempo = redutor.reduzir_medirTempo('gre_1107_direcionado.mtx',simetrica = False)
	#tempo = redutor.reduzir_medirTempo('California_direcionado.mtx',simetrica = False)
	#tempo = redutor.reduzir_medirTempo('cage9_direcionado.mtx',simetrica = False)

	#print(tempo)
	


