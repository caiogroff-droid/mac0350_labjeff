
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

# Como executar
Entre no ambiente de desenvolvimento .venv na pasta root, entre na pasta \Project e rode o webapp com o comando ```fastapi dev``` 
Em suma:

```cd <MAC0350_LABJEFF path>```
```source .venv/bin/activate```
```cd Project```
```fastapi dev```