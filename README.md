# Problem set 02 
Nome: Clicia Pereira de Freitas
Matéria: Linguagens de programação
Turma: cc3m

# Sobre

Nesse pset nós lidamos com questões de filtros de edição de imagens como nitidez, blur... 
Nos arquivos temos o arquivo test.py, para testar as funções, e o pset2.py, o que contêm as funções. E abaixo, nesse readme, tem as respostas para as questões do pset2. 

## Questão 1

#### Se você passar essa imagem pelo filtro de inversão, qual seria o output esperado?

A saída desejada é (4, 1, [226, 166, 119, 55]). Porque o filtro de inversão (inverted, em pset.py) irá refletir os pixels sobre o valor de cinza. Assim, os parâmetros passados (4, 1, [29, 89, 136, 200]), serão invertidos. Ficando assim:
[255 - 29, 255 - 89, 255 - 136, 255 - 200] = [226, 166, 119, 55]. 

## Questão 2

Após a depuração, executei meu filtro de inversão na imagem peixe.png e salvei o resultado como uma imagem PNG:

![questão2](https://user-images.githubusercontent.com/89753006/188334268-9bb1fb16-8c3d-40ce-a0b2-065cf67f0061.png)

## Questão 3

![image](https://user-images.githubusercontent.com/89753006/188334568-6a1a5586-d607-4e87-9b8b-387aa7879a22.png)

O cálculo do valor do pixel na imagem de saída no local indicado pelo destaque
vermelho é:
[0.00 -0.07 0.00, 0.45 1.20 -0.25, 0.00 -0.12 0.00] x [80, 53, 99, 129, 127, 148, 175, 174, 193] = [0 + (-3.71) + (0) + (-58.05) + (152.4) + (-37) + 0 + (-20.88) + 0] = 32.76

## Questão 4
Ao executar o código aplicando o seguinte kernel na imagem porco.png:
 kernel = [
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
 
Teremos a seguinte imagem: 

![questão4](https://user-images.githubusercontent.com/89753006/188334695-e3383304-49b6-49db-bc51-e830f07bdacd.png)

Executando o filtro blur na imagem gato.png:

![gato](https://user-images.githubusercontent.com/89753006/188335111-f429bf68-04cd-4687-99ec-48e3c31cfaac.png)

com um kernel de desfoque de caixa de tamanho 5, resulta em:

![questão4gato](https://user-images.githubusercontent.com/89753006/188335291-5df61eea-fd4c-4621-b045-f8b0176949ff.png)

## Questão 5 
O kernel aplicado na versão desfocada B é a a subtração de dois kernels. o Primeiro kernel duplica o valor original do pixel e o segundo borra a imagem.
Segundo a formula: S(x,y) = round(2*I(x,y) − B(x,y))
Sendo assim:
 kernel1 = [[0, 0, 0],
            [0, 2, 0],
            [0, 0, 0]]
 kernel2 = [[1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]]
 
 subtraindo o kernel1 pelo kernel2
 
 kernelResult = [[-1/9, -1/9, -1/9],
                 [-1/9, 17/9, -1/9],
                 [-1/9, -1/9, -1/9]]
                  
 Executando o filtro de nitidez na imagem python.png usando um kernel de tamanho 11, temos:
 ![python2](https://user-images.githubusercontent.com/89753006/188336455-d4f4ab72-ce20-414e-a7e7-00348ce6fc58.png)
 
 ## Questão 6
O kernel Kx detecta as bordas verticais e o Ky detecta as bordas horizontais.

 ![image](https://user-images.githubusercontent.com/89753006/188336524-1ed9e729-2340-40cd-acb0-9faa3ba2d7e7.png)

Executando o detector de borda na imagem obra.png, temos:

 ![obra2](https://user-images.githubusercontent.com/89753006/188336637-c208b9f2-7f8b-4740-b760-1933f187d0dc.png)
 
 Fim das questões do pset2!
 Creditos: Auxiliada pelo Lucas Zanon. 
