# Zombie Runner

Jogo 2D endless runner em Python e Pygame. Escolha Shinobi ou Samurai e sobreviva a zumbis e barreiras enquanto a pontuacao aumenta com o tempo.

## Objetivo

Desvie dos zumbis e das barreiras pelo maior tempo possivel. A partida termina ao colidir com uma ameaca; sobreviva ate 500 pontos para vencer.

## Controles

- `Espaco`: pular
- `S` ou `Seta para baixo`: abaixar
- `Setas esquerda/direita`: navegar na selecao de personagem
- `Enter`: iniciar, confirmar, reiniciar ou escolher uma opcao
- `Esc`: voltar ao menu ou sair

## Tecnologias

- Python 3.12 ou superior
- Pygame 2.6.1
- PyInstaller para gerar a versao Windows

## Estrutura

- `main.py`: ponto de entrada
- `Code/`: gameplay, entidades, telas e carregamento de recursos
- `asset/`: sprites e cenarios usados pelo codigo-fonte
- `assets/`: nome da pasta de recursos na distribuicao empacotada
- `dist/ZombieRunner/`: arquivos da versao distribuida

Os assets sao resolvidos relativamente a pasta do projeto ou do executavel. O codigo aceita `asset/` no projeto-fonte e `assets/` no pacote.

## Executar pelo codigo-fonte

Com Python 3.12 instalado, na raiz do projeto:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Com `uv`, tambem e possivel instalar e executar pelo projeto:

```powershell
uv sync
uv run python main.py
```

## Gerar a versao Windows

Em Windows, com Python 3.12 e `uv` instalados, execute:

```powershell
.\build_windows.ps1
```

O script cria o executavel e prepara a pasta `dist/ZombieRunner/` com os recursos necessarios.

## Executar a distribuicao

Abra `dist/ZombieRunner/` e execute `ZombieRunner.exe`. Mantenha a pasta `assets/` junto do executavel.