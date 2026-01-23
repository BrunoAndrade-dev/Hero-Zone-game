# Projeto de jogo feito para o teste da empresa Kodland

### Aqui você verá como fiz para solucionar a situação que englobou O TESTE 1 da empresa Kodland, na qual estou  em processo de admissão para trabalhar como tutor de programação com Python e Scratch.

## Regras do Jogo
- Você é um héroi espacial que precisa utilizar sua super velocidade para desviar de inimigos
- Sobreviva 2 minutos e ganhe 
- Caso toque em um dos inimigos, será game over e o jogo poderá ser reiniciado

## Divisão do Projeto 

nome-do-seu-jogo/
│
├── images/                  
│   ├── hero_idle_0.png
│   ├── hero_walk_0.png
│   ├── enemy_idle_0.png
│   └── background.png
│
├── sounds/                  
│   ├── hit.wav
│   └── click.ogg
│
├── music/                   
│   └── background_theme.mp3
│
├── fonts/                   
│   └── custom_font.ttf
│
├── main.py                  
├── README.md                
├── .gitignore               
└── requirements.txt

## Estrutura Resumida da Lógica utilizada

### Criação de Classes 
-> Classe de animação dos personagens (AnimetedSprite)
    . Contendo as definições que possibilitam a animação com os parâmetros (prefix, frame_count, pos, animation_speed)

-> Classe Heroi
    . Traz como parâmetro a classe de animação e aqui definimos a imagem do heroi e sua posição 

-> Classe Enemy e EnemyType2
    . Traz como parâmetro a classe de animação e as configurações dos inimigos são colocadas aqui além da sua velocidade

-> Classe Game
    . Aqui os botões do MENU ganham posição, background e posição dos personagens no cenário

## Biblioteca Utilizada

-> Pgzero

## Instruções para rodar o programa 

### Clonar o repositório do github
        -> git clone "Link"
        cd nome
    
### Baixar as bilbiotecas necessárias 
        -> pip install -r requirements.txt

### Run 
        -> pgzrun main.py