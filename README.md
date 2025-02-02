# **life for the rules**
![Poster](https://github.com/DIVERSIUMx/pygame-project/blob/main/chert%20and%20diversium%20(3).png)
----
[![Python](https://img.shields.io/badge/Python-3.11-gold?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/pygame-2.6.1-gold?style=for-the-badge&logo=pygame&logoColor=white)](https://pypi.org/project/pygame/)
-----
+ [About this game](#about-this-game)
  + [Game mechanics](#game-mechanics)
  + [Game goals](#game-goals)
+ [About this project](#about-this-project)
  + [Code](#code)
  + [Authors](#authors)
-----
## **About this game**
*This game is puzlle-game. Where you control the character to complete levels.*

-------

### **Game mechanics**
Character movement - w/a/s/d  
**Object blocks:**
  + Box
  + Rock
  + Wall
  + Water
  + Skull
  + Character

*The sentences composed by moving text blocks are responsible for interactions with them.*  
**Text blocks:**
  + Action blocks
      + Push
      + Stop
      + Sink
      + Death
      + Win
      + You
      + Weak
  + IS
  + Any object block
  

When composing a sentence (from left to right / top to bottom) with the structure   
`Object block + THIS + Object block / Action block`,  
a new rule is created that controls the blocks depending on its content.  


[**RU VERSION**](## "Перемещение персонжа - w/a/s/d
Блоки объектов:
	+ Коробка
	+ Камень
	+ Стена
	+ Вода
	+ Череп
	+ Персонаж
За взаимодествия с ними отвечают составленные прдложения, путем перемещения блоков текста.
Блоки текста:
	+ ЭТО
	+ Любой блок объетка 
	+ Блоки действий
	  - Толкать
	  - Стоп
	  - Потопить
	  - Смерть
	  - Победа
	  - Ты
	  - Хлипкий
При составлении предложения (Слвево на право / сверху вниз) структурой 'Блок объектов + ЭТО + Блок объектов / Блок действий', сотсавляется новое правило, управляющее блоками в зависимости от его наполнения.")

 -----
### Game goals  
The goal is to make a winning combination and/or fulfill its conditions. 
> For example, after making `wall is win`, you need to 'touch the wall'. 

[**RU VERSION**](## "Цель - составить победную комбинацию и(или) выполнить ее условия. К примеру после составления `wall is win` требуется 'прикоснутся к стене'.")

-----

## About this project
This project was created during training at [**Yandex Lyceum**](https://lyceum.yandex.ru/)

------
### Code
Our code is quite heavy, here is an example of checking for creating a new rule.
   
`element[0]` - *a block of text on which some action has been performed*   
`ActiveBlocks...` - *classes of text blocks*  
`board` - *playing field*   
`new_rule` - *function to create a new rule*     
``` python
        if isinstance(element[0], ActiveBlocksAction):  # Проверяет на то, что блок текста являтся дейсвтием
            cord = x, y = element[1]
            if x >= 2:  # проверка новых правил по x
                if board[y][x - 1] and board[y][x - 2]:
                    if issubclass(board[y][x - 1][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y][x - 2][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y][x - 2][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x - 2, y), first_name=first_name, is_cord=(x - 1, y), finish_cord=cord,
                            finish_name=finish_name
                        )
            if y >= 2:  # проверка новых правил по y
                if board[y - 1][x] and board[y - 2][x]:
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y - 2][x][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y - 2][x][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x, y - 2), first_name=first_name, is_cord=(x, y - 1), finish_cord=cord,
                            finish_name=finish_name
                        )
```
------
### Authors   
[**DIVERSIUM(Konstantin)**](https://github.com/DIVERSIUMx) and [**CHERT(Ilya)**](https://github.com/CHERTvsINTERNET)
