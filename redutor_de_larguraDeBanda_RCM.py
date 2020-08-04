from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.io import mmread
import matplotlib.pyplot as plt
import time
import warnings 

warnings.filterwarnings("ignore")


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
		
		#plot da matriz
		plt.rcParams['figure.figsize'] = (15,15)
		fig, axs = plt.subplots(1, 2)
		ax1 = axs[0]
		ax2 = axs[1]

		matriz_densa = matriz.todense() #para auxiliar no plot e no calculo da largura de banda

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
		print("Largura de banda reduzida",self.larguraBanda(matriz_densa))

		ax2.spy(matriz_densa, markersize=1)
		ax2.set_title('Matriz Reordenada',y=1.08)
		plt.show()


	def reduzir_medirTempo(self,matriz_fileName, simetrica = True):

		#calcula o tempo de execução para reduzir a largura de banda, reordenando a matrix

		
		matriz = mmread(matriz_fileName)
		matriz = csr_matrix(matriz)
		
		inicio = time.time()

		##segundo a documentação do RCM do Scipy essa transformação é necessária para matrizes assimetricas
		if not simetrica:
			matriz = matriz + matriz.T

		#vetor de permutação obtido ao aplicar o algoritmo Reverse Cuthill Mckee, utilizado para reordenar a matrix	
		perm_array = reverse_cuthill_mckee(matriz,symmetric_mode=True)

		#reordenação da matriz
		matriz = self.reordenarMatriz(matriz,perm_array)

		fim = time.time()

		print(fim - inicio)



if __name__== '__main__':

	
	redutor = redutor_larguraBanda()


	#Para realizar os testes basta descomentar a linha com o comando da matriz de escolha

	#Plotar a matriz original e ordenada e printar a largura de banda inicial e reduzida
	
	#simetricas
	#redutor.reduzir('matrizes_teste/G22_naoDirecionado.mtx',simetrica = True)
	#redutor.reduzir('matrizes_teste/delaunay_n12_naoDirecionado.mtx',simetrica = True)
	#redutor.reduzir('matrizes_teste/ca-HepTh_naoDirecionado.mtx',simetrica = True)

	#assimetricas
	#redutor.reduzir('matrizes_teste/gre_1107_direcionado.mtx',simetrica = False)
	#redutor.reduzir('matrizes_teste/California_direcionado.mtx',simetrica = False)
	#redutor.reduzir('matrizes_teste/cage9_direcionado.mtx',simetrica = False)


	#Para medir os tempos:

	#simetricas
	#redutor.reduzir_medirTempo('matrizes_teste/G22_naoDirecionado.mtx',simetrica = True)
	#redutor.reduzir_medirTempo('matrizes_teste/delaunay_n12_naoDirecionado.mtx',simetrica = True)
	#redutor.reduzir_medirTempo('matrizes_teste/ca-HepTh_naoDirecionado.mtx',simetrica = True)

	

	#assimetricas
	#redutor.reduzir_medirTempo('matrizes_teste/gre_1107_direcionado.mtx',simetrica = False)
	#redutor.reduzir_medirTempo('matrizes_teste/California_direcionado.mtx',simetrica = False)
	#redutor.reduzir_medirTempo('matrizes_teste/cage9_direcionado.mtx',simetrica = False)





