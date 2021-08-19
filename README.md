# Othello-ai

This rep uses Monte Carlo to play the game Othello. Play [here](https://othello-ai-dhorne.herokuapp.com/). The main code is in [app/main.py](https://github.com/ki0apa/Othello-ai/blob/main/app/main.py).

## How it Works

Othello AI uses Monte Carlo Tree Search (MCTS) to play the game. Essentially, MCTS searches a large game tree of a two-player deterministic game to choose the optimal move of a given game state.

### What is a Game Tree

Most games can be represented by a directed tree. A node represents a game state (eg, a given arrangement of pieces in an Othello board and whether it's black's or white's turn). An edge between a node A and a node B represents a possible move at the game state A such that after the move, the game state is B. A node has no children when there is no possible moves, i.e. the game is over. 

Game trees can be useful to find a winner in a game and find the optimal move. You can assign every node in the game tree a winner. For leaf nodes, it is easy to find the winner since the game is over at that point. The winner of a non-leaf node is the player of that node's game state if there is a child such that the current player wins. The optimal move is then an edge that connects this node to its child. If there is no child where the player of the node wins, then the winner is the opponent and there is no optimal move. You can recur to find the winner of the game and the optimal first move. Unfortunately, this is impossible to do with the game Othello, because the game tree is estimated to have 10^58 nodes. This is far too many to compute on a household computer. Luckily, Monte Carlo Tree Search works well in the game Othello. 

### What is Monte Carlo Tree Search

To summarize, MCTS runs many random simulations of the game at a given game state. MCTS maintains a partial version of the entire game tree. For a given iteration, MCTS performs 4 steps. First, MCTS performs the _selection_ step by recursively selecting nodes on the partial game tree based on two factors 

1. MCTS is more likely to select nodes that have a higher win lose ratio.
2. MCTS is more likely to select nodes that have been explored less than other nodes. 

After MCTS reaches a node where not all possible moves have been explored, a new node is created. This is the _expansion_ step. Then MCTS runs a simulation from the game state represented by the new node. This is the _simulation_ step. Finally, it updates the win-lose ratio and the number of times a node has been explored on the partial game tree. This is the _back propagation_ step. After many iterations, the node which has been explored the most is the optimal move. The [wikipedia page](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) on MCTS explains the algorithm in more detail. 

![](https://upload.wikimedia.org/wikipedia/commons/2/21/MCTS-steps.svg)

## Modifications Made for Othello

When I initially programmed MCTS for Otehllo, the bot would make many mistakes. For instance, it would make moves that made it easier for me to put a piece on the corner. This is not an optimal move. To account for that, I added a heuristic in the _selection_ step. A third factor rates a move based purely on the position in the board a piece is placed. For instance, corners and edges have a high rating. While positions around the corner have a low rating because it makes it easier for the opponent to place a piece in a corner. This made the bot very good at Othello. 


