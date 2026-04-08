
This repository contains the projects and assignments developed for the Software Development Introduction (MAC0350) course.
The goal is to practice by doing weekly exercises as well as two projects. The following section describes my individual project.
# Game Ranking Web App
A simple web app where the pourpose is to save and rank your favourite games.
You can add, remove and edit the list as you please, moving up or down your game to classify them on the list, as well as edit its iformation and overall ranking.
Project made using `HTMX`, `FastApi` and `SQL database`

#Base Functionalities:
As mentioned early, the following functionalities will be implemented:
* Add a new game to the list, providing some crutial information, such as *name*, *platform*, *description*, *ranking*
* Ranking system calculation, for example, if you vallue more graphic design than gameplayability, you can change the formula of the overrall ranking
* As this is preference-based, games will be first ranked by its descending overall ranking, but you can change the list order and customize it, by selecting an option and dragging games 'up and down'
* Edit game information, outside its key value, such as *name*

# Como executar
 (todo)


-------------------------------------------------------------------------------------------------------------------------------------------
# Comentarios pós completo

# O que faltou fazer?
Não consegui implementar a função de arrastar os cards para mudar a ordem como eu havia planejado e, dado isso, também acabei nao implementando o que eu afirmei como sendo o calculo do rank do jogo.

# Sobre o uso de IAs
Foi utilizado o copilot para alguns estilos css e para agilizar a escrita do html, porém a maior parte dos estilos de botao, input e outros foi tirado de um sample na internet.
No backend, foi utilizado o chatGPT somente quando o código falhava em fazer o que era proposto, alguns exemplos que posso dar:
    - Programei o backend de criar o jogo e plataforma independentes até fazer a sincronização dos dois e, quando adicinei incorretamente o id da plataforma na criaçao do jogo, o programa falhava por conta da sessão ter sido encerrada antes da tabela de plataformas ter sido sincronizada
    - Os arquivos estaticos de assets não funcionaram corretamente com o script do tutorial, então tive que usar um outro script com a biblioteca os.
    - Grande parte dos códigos foi reaproveitado dos exemplos de sala

# Como executar
Entre no ambiente de desenvolvimento .venv na pasta root, entre na pasta \Project e rode o webapp com o comando ```fastapi dev``` 
Em suma:

```cd <MAC0350_LABJEFF path>```
```source .venv/bin/activate```
```cd Project```
```fastapi dev```