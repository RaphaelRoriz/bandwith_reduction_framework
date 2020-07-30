from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.io import mmread
import numpy as np
import matplotlib.pyplot as plt
import time


class bandwidth_reductor():

	def reduce(self,matrix_fileName, simetrica = True):

		matrix = mmread(matrix_fileName)
		matrix = csr_matrix(matrix)
		matrix_densa = matrix.todense() #para auxiliar no plot
		#self.plotar_matrix(matrix_densa)
		
		plt.rcParams['figure.figsize'] = (15,15)
		fig, axs = plt.subplots(1, 2)
		ax1 = axs[0]
		ax2 = axs[1]

		ax1.spy(matrix_densa, markersize=1)
		ax1.set_title('Matriz Original',y=1.08)
		
		##segundo a documentação do RCM do Scipy essa transformação é necessária para matrizes assimetricas
		if not simetrica:
			matrix = matrix + matrix.T

		#vetor de permutação obtido ao aplicar o algoritmo Reverse Cuthill Mckee, utilizado para reordenar a matrix	
		perm_array = reverse_cuthill_mckee(matrix,symmetric_mode=True)

		tamanho = len(perm_array)

		#reordenação da matrix
		for i in range(tamanho):
			matrix[:,i] = matrix[perm_array,i]
		for i in range(tamanho):
			matrix[i,:] = matrix[i,perm_array]

		matrix_densa = matrix.todense()

		#self.plotar_matrix(matrix_densa,reordenada = True)
		ax2.spy(matrix_densa, markersize=1)
		ax2.set_title('Matriz Reordenada',y=1.08)
		plt.show()



if __name__== '__main__':

	
	reductor = bandwidth_reductor()
	
	#comentar as funções referentes a plotagem para não interferirem no tempo de execução
	inicio = time.time()
	#reductor.reduce('nomearquivo',simetrica = False)
	fim = time.time()
	print(fim - inicio)
	
	#simetricas
	#reductor.reduce('G22_naoDirecionado.mtx',simetrica = True)
	#reductor.reduce('ca-GrQc_naoDirecionado.mtx',simetrica = True)
	#reductor.reduce('delaunay_n12_naoDirecionado.mtx',simetrica = True)

	#assimetricas
	#reductor.reduce('gre_1107_direcionado.mtx',simetrica = False)
	#reductor.reduce('California_direcionado.mtx',simetrica = False)
	#reductor.reduce('cage9_direcionado.mtx',simetrica = False)
	



