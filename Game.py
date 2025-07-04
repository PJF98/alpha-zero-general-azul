class Game():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        pass

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """

    def getNextState(self, board, player, action, random_seed=0):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player
            random_seed: define seed for any random choice (MCTS exploration),
                         or 0 for true random (real move)

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """

    def getGameEnded(self, board, next_player):
        """
        Input:
            board: current board

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
        """

    def getScore(self, board, player):
        """
        Input:
            board: current board
            player: player you want to have score (may not be current player)

        Returns:
            score of such player
        """

    def getRound(self, board):
        """
        Input:
            board: current board

        Returns:
            number of played rounds so far
        """

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """

    def getSymmetries(self, board, pi, valid_actions):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """

    def getNumberOfPlayers(self):
        """
        Returns:
            number_players: Number of players that current game supports
        """

    def moveToString(self, move, current_player):
        """
        Input:
            move: int coding for an aciton
            current_player: index of current player

        Returns:
            string: a human representation of such move, as a printable string
        """

    def printBoard(self, numpy_board):
        """
        Input:
            numpy_board: a numpy representation of a board, may be different than self.board

        Print: a human representation of such board on stdout, used during pit involving a human
        """
