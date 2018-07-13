# My first Python codes
Arquivos em phyton devem ser salvos com extensão .py
ex: helloworld.py

Para compilar/execultar
>> python nome.py 

Para intalar pacotes
>> pip install nome_do_pacotenumpy
Ex:
>> pip install numpy

OBS1: A identação no phyton é extremamente importante.
Os loop, if são discriminados por meio da identação.

O phyton é sensitive case. 


Para trabalhar com uma biblioteca eu devo inicializar ela no inicio do
programa
>>import numpy as rodrigo

==================================================

Fazendo um loop em python no tipo "Do".

Cada loop pode ter a configuração 1:
>> for x in range(3, 8, 2):
 3 - indica o inicio do loop
 8 - indica o fim do loop. Ou seja vai de 3 até o número menor que 8, ou seja 7
    3....7
 2 - indica o passo.

Ou ainda sem indicar o passo:
>> for x in range(3, 8):
 3 - indica o inicio do loop
 8 - indica o fim do loop. Ou seja vai de 3 até o número menor que 8, ou seja 7
    3....7 
Como não foi indicado o passo, o intervalo padrão será igual a 1.


Ou ainda sem indicar o passo e o inicio:
>> for x in range(8):
 8 - indica o fim do loop
 o inicio será padrão igual a zero e o passo igual a 1


==================================================


Fazendo loop do tipo "While"

A configuração é unica da forma:

>> while count < 5:

Ou seja, faz enquanto uma condição é satisfeita.



==================================================
Trabalhando com loops condiionais "Else"

>> for x in range(8):
		Codigo 1
   else:
   		codigo 2






==================================================
Concatenar nome e vetores
Se :
>> A=[2,3,4]; B=[2,3]
print(A+B) = [2, 3, 4, 2, 3]
print(3*A) = [2, 3, 4, 2, 3, 4, 2, 3, 4]
Se :
>> A="Rodrigo"; B=" Santana"
print(A+B) = Rodrigo Santana

Diferente do que ocorre no fortran em que se eu somo dois vetores A+B,
o resultado será a um vetor com o mesmo tamanh de A e B, comos elementos
sendo a soma dos elementos de A e B nas referidas posições. Perceba que 
No python, operações com vetores deve ser feita elemento por elemento.

==================================================

Iteratividade.
Quando queremos que o usuário digite alguma coisa no momento da excecução
do programa uma função útil é :raw_input(''). Essa função recebe uma
escrita entendida como string e então essa pode ser trabalhada como string, real, ou inteiro.
Ex:
>>> an =raw_input('Quanto gastou Ana? ')

Quando o programa for execultado irá aparece na tela: Quanto gastou Ana?.

O usuário nesse momento deve digitar um valor. E esse valor será atribuido a variavel 'an'.
OBS:: Esse valor é passado em forma de string, para trabalhar com ele em forma de real ou 
inteiro, deve-se dizer ao codigo o que ele é, isso porque '+' quando é usado em string concatena
quando é usado em real, soma.

Ex: 
>>> an =raw_input('Quanto gastou Ana? ')
Na tela: Quanto gastou Ana? 54
>>> Print(an+an)
Na tela: 5454
>>> Print(float(an)+float(an)
Na tela: 108 
OBS:: Note o uso da função float é importante, pois a função raw_input não
retorna números, e sim strings.


Se você quiser que no momento exato da entrada se converta em real ou interiro
use
>>> an =int(raw_input('Quanto gastou Ana? '))
ou
>>> an =float(raw_input('Quanto gastou Ana? '))



Para usar biblioteca use o import:
>>> import math
print math.pow

===============================================
Estrutura do 'if elseif"

if vf == 0:
	print 'Alunissagem perfeita!'
elif vf <= 2:
	print 'Alunissagem dentro do padrao.'
elif vf <= 10:
	print 'Alunissagem com avarias leves.'
elif vf <= 20:
	print 'Alunissagem com avarias severas.'
else:
	print 

Numa sequencia de if/elif/elif/.../else é garantido que um, e apenas um dos blocos será executado.



===============================================

Print

O print pode ter diferentes estruturas
Ex:
>>> Print("Exiba essa mensagem na tela")   = Exiba essa mensagem na tela
>>> Print "Exiba essa mensagem na tela"    = Exiba essa mensagem na tela

E="essa"
>>> Print "Exiba %s mensagem na tela" %E   = Exiba essa mensagem na tela
E1="essa"
E2="na tela"
>>> Print "Exiba %s mensagem %s agora" %(E1,E2)  = Exiba essa mensagem na tela agora

O %s indica que o que for inserido será em forma de string. O % fora das aspas indicam 
o que será colocado no % dentro da aspas. Nesse exemplo coloquei nomes, poderiam ser números

E1=11
E2=13
>>> Print "Primeiro vem %s depois %s na sequência dos primos" %(E1,E2)  = Primeiro vem 11 depois 13 na sequência dos primos.

===============================================
raw_input('')

A entrada é realizada pelo comando raw_input(''). Esse comando realiza a interação entre o teclado e o código. Quando
o programador quiser solicitar que o usuário enfie alguma informação no codigo no momento da execução deve-se se usar
esse comando. 
EX:
>>> a=raw_input('Digite seu nome:')
>>> print 'Seu nome é %s' %a        = Seu nome é Nome_digitado

A entrada sempre é entendida pelo computador como string, por isso se for um número o desejado, converta
no momento que a variavel entrar no código. Uma opção seria
>>> a=float(raw_input('Digite um número real:'))
>>> b=int(raw_input('Digite um número inteiro:'))
>>> c=float(raw_input('Digite outro número real:'))
>>> d=a+b
>>> Print '%s' %d
Se a=2 c=3 d=5

Mais se não fosse usado a opção de conversão, o codigo iria achar que trata-se de uma string, dai a operção '+' iria
concatenar.
Se a=2 c=3 d=23

===============================================
break e continue

Esses comandos são usados dentro de um loop. Se o compilador encontra um 'continue' em qualquer ponto do loop, ele retorna imediatamente 
para o inicio do bloco de comandos do loop para realizar mais uma iteração, ignorando os comandos abaixo do continue. 

O break por outro lado finaliza o loop imediatamente. Se no meio do caminho existe um break, o loop é finalizado independentemente da iteração.
EX:
>>> n=1
>>> m=0
>>> while n==1:
		m=m+1
		if m<=5:
			print'%s' %m
			continue
		break
Nesse caso vai aparecer na tela
	1
	2
	3
	4
	5
Isso porque o break ta fora e depois do if, só que dentro do if tem o continue, o que faz com que sempre que o codigo entre no if,
ele seja empurrado pra cima novamente, e quando ele não entra, o break finaliza o loop.


===============================================
try: except:

São dois comandos para evitar que o programa apresente erros. Se em algum momento do código for pedido para você digitar um número e 
seu dedo tocar numa letra isso vai gerar um erro, mas e ai ?. Se o seu programa contém try: except: ele pode salvar sua execução.

try:
	Ele vai tentar execultar o que está aqui dentro, mas se ele não consegui, ele vai entrar no 
except:
	e vai execultar o que tem aqui.

================================================