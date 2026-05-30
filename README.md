# ES-PI1-2026-T1-G12
## LAD.PY
Projeto Integrador 1 - LAD.Py, criação de um sistema de votação digital.


## Descrição
Simulação de uma urna eletrônica, onde é possível cadastrar, buscar, listar e editar eleitores, cadastrar, buscar, listar e editar candidatos, transformar eleitores em mesários. Após o cadastro, é possível abrir o sistema de votação (apenas para os mesários), e dentro da urna, é possível efetuar os votos, apenas 1 voto por eleitor, e caso eleitor selecione números que não estejam diretamente ligados aos candidatos cadastrados, o voto será considerado com nulo. Após a votação apenas depois de encerrá - la é permitido o acesso à área de resultados e auditoria. O objetivo do projeto é por em prática todas as matérias aprendidas no semestre, sendo elas python, matrizes e criptografia e banco de dados.


## Integrantes 
Leonardo Furlan Curtulo
Vinicius Pansieri Chiarelli
Augusto Brufato Pereira dos Santos
Vitor Fachini Zanon


## Tecnologias
Mysql
Python
GITHUB

## Instruções:
1- Inicializar o sistema.

2- Fazer o cadastro:
    Eleitores - CPF e título de eleitor válidos apenas.
    Candidatos - Número de candidato autêntico.
    Mesário - Obrigatoriamente deve existir ao menos 1 mesário (para abrir e encerrar votação.)- É possível na hora do cadastro ou na propria função de tornar mesário.

3- Abrir votação: 
    Abrir a votação só é possível caso seja feita por um mesário, se não for ocasionará na invalidação.
    Ao abrir deverá ser inserido o título de eleitor do mesário, os primeiros 4 dígitos de seu CPF e sua chave de acesso.
    Após a abertura é realizada a zerézima, zerando todos os votos, liberando uma votação completamente nova.

4- Votação:
    Na hora da votação o eleitor precisará inserir seu título, cpf e chave de acesso.
    Então o eleitor deve inserir o número do candidato e confirmar sua decisão.
    Cada eleitor só pode votar uma única vez.

5- Encerramento:
    Mesário encerra a votação inserindo seu título cpf e chave de acesso (2 vezes para confirmação)

6- Resultados:
    Após encerrar a votação é possível acessar o menu de resultados e auditoria.
    O boletim informa o vencedor da votação.
    A estatística de comparecimento informa quantos eleitores sao cadastrados e quantos eleitores foram votar.
    O protocolo mostra os protocolos de votação.
    O menu de integridade mostra a quantidade de votos obtida com a quantidade de pessoas que votaram, conferindo a integridade do sistema.

OBS: Dados sensíveis são guardados criptografados.
    