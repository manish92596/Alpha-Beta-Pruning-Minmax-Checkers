# Alpha-Beta-Pruning-Minmax-Checkers
&nbsp;
&nbsp;
&nbsp;

## Bot won the match !!!

<p align="center">
  <img src="https://github.com/manish92596/Alpha-Beta-Pruning-Minmax-Checkers/assets/98229122/06f790a9-ab8a-4fdb-bd27-edf9e9e1d177" width="1000" height="400" />
</p>
&nbsp;
&nbsp;
&nbsp;

## Bot double capture move !!!

<p align="center">
  <img src="https://github.com/manish92596/Alpha-Beta-Pruning-Minmax-Checkers/assets/98229122/fbf38b06-a2b8-4477-8ccc-ae1f231e3052" width="1000" height="400" />
</p>
&nbsp;
&nbsp;
&nbsp;

## Both You and Bot become king !!! 

<p align="center">
  <img src="https://github.com/manish92596/Alpha-Beta-Pruning-Minmax-Checkers/assets/98229122/5161c77b-ce2d-4356-9dbe-fad22f9af5b0" width="1000" height="400" />
</p>
&nbsp;
&nbsp;
&nbsp;

## You won the match !!!

<p align="center">
  <img src="https://github.com/manish92596/Alpha-Beta-Pruning-Minmax-Checkers/assets/98229122/6b1c62a6-2d5a-4e02-abd2-8e2b3cfc3d57" width="1000" height="400" />
</p>
&nbsp;
&nbsp;
&nbsp;



1. The code uses the Pygame library, which is a popular library for game development in Python. It provides functionality for graphics, sound, and user input handling.

2. The code defines a "Board" class that represents the game board. It initializes the board, creates and manages the game pieces, and provides methods for moving pieces and evaluating the game state.

3. The "Piece" class represents individual pieces on the board. Each piece has attributes such as position, color, and whether it is a king. It also has methods for drawing the piece on the screen and updating its position.

4. The "Game" class manages the overall game flow. It handles player input, updates the game state, and manages the game loop. It uses the "Board" class to keep track of the board state and evaluate the game outcome.

5. The "minimax" function is an implementation of the minimax algorithm with alpha-beta pruning. It is used for AI move selection. The function recursively evaluates the possible moves and selects the best move based on the evaluation score.

6. The "get_all_moves" function generates all possible moves for a given board and color. It iterates over the "board" to find all pieces of the specified color and calls the "get_valid_moves" method of the Board class to get the valid moves for each piece.

7. The code uses images for visual elements such as the crown for king pieces and winning screens for white and black players.

8. The "main" game loop is implemented in the main function, where it continuously updates the game state, handles player input, and checks for a winner. It also displays the winning screen when a player wins and allows for a delay before quitting the game.

&nbsp;
&nbsp;
&nbsp;

## This code demonstrates the use of object-oriented programming (OOP) principles in creating a checkers game using the Pygame library. Here are a few technical points related to OOP in this code:

## 1. Class Definition: 
    The code defines several classes, including Board, Game, and Piece, which encapsulate related data and behavior.

## 2. Encapsulation: 
    Each class encapsulates its own data and methods. For example, the Board class encapsulates the game board and related operations, such as creating the board, evaluating the state, and making moves.

## 3. Inheritance: 
    The Game class inherits from the Board class, allowing it to access and modify the board and its state. Inheritance enables code reuse and supports the "is-a" relationship between classes.

## 4. Data Hiding: 
    The attributes of the classes are often defined as private or protected by convention, using the underscore prefix. For example, self._init() and self._move() are internal methods of the Game class.

## 5. Abstraction: 
    The classes provide an abstraction layer, hiding the implementation details and exposing only the necessary interfaces. For instance, the Game class provides methods like select() and update() to interact with the game, while the internal logic is abstracted away.

## 6. Polymorphism: 
    The draw() method is implemented differently in each class (Board, Piece) to handle the drawing of the respective objects. Polymorphism allows different objects to be treated uniformly through a common interface.

## 7. Object Interaction: 
    The objects interact with each other through method calls. For example, the Game class calls methods on the Board class to make moves, evaluate the state, and retrieve valid moves.

## 8. Object Composition: 
    The Board class contains a 2D list of Piece objects, representing the composition relationship between the board and its pieces.
&nbsp;
&nbsp;
### Overall, this code showcases how OOP concepts can be applied to model and implement a complex system like a checkers game, leading to modular, reusable, and maintainable code.
