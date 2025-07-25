from .KamisadoLogic import board_colours, start_positions
import numpy as np
from numba import njit
import numba


# ############################ BOARD DESCRIPTION ##############################
# Board is described by a 9x8 array
# Colours are always in this order: 0: Brown 1: Green, 2: Red 3: Yellow
# 4: Pink, 5: Purple, 6: Blue, 7: Orange
# Second player pieces have 1 in front, eg 12 for second player red piece
# Here is the description of each line of the board. For readibility, we defined
# "shortcuts" that actually are views (numpy name) of overal board.
# ### Index  Shortcut                Meaning
# ###  0-8   self.board              Board
# ###  8-9   self.info               Colour to move, Move_num, ..., 0
# Any line follow by a 0 (or n 0s) means the last (or last n) columns is always 0


# ############################ ACTION DESCRIPTION #############################
# There are 8 * 7 * 3 = 169 actions
# To get action number do piece_colour * 21 + direction * 7 + num_steps - 1
# Directions = {Left Diagonal: 0, Up: 1, Right Diagonal: 2}
# If there are no possible moves then 168 is chosen
# To further demonstrate:
# ### Index  Meaning
# ###   0    Brown, Left, 1
# ###   1    Brown, Left, 2
# ###  ...
# ###   7    Brown, Up, 1
# ###   8    Brown, Up, 2
# ###  ...
# ###   21   Green, Left, 1
# ###   22   Green, Left, 2
# ###  ...
# ###   167  Orange, Right, 7
# ###   168  Pass

@njit(cache=True, fastmath=True, nogil=True)
def observation_size(_num_players):
    return (9, 8)


@njit(cache=True, fastmath=True, nogil=True)
def action_size():
    return 169


@njit(cache=True, fastmath=True, nogil=True)
def my_random_choice(prob):
    result = np.searchsorted(np.cumsum(prob), np.random.random(), side="right")
    return result


spec = [
    ('state', numba.int8[:, :]),
    ('board', numba.int8[:, :]),
    ('info', numba.int8[:, :]),
]


@numba.experimental.jitclass(spec)
class Board():
    def __init__(self):
        self.state = np.zeros((9, 8), dtype=np.int8)

    def init_game(self):
        self.copy_state(np.zeros((9, 8), dtype=np.int8), copy_or_not=False)
        self.board[:] = -np.ones((8, 8), dtype=np.int8)
        self.choose_initial_board_states()
        self.info[0, 0] = -1
        return

    def choose_initial_board_states(self):
        choose_from = np.ones(12)
        first_idx = my_random_choice(choose_from / choose_from.sum())
        choose_from[first_idx] = 0
        second_idx = my_random_choice(choose_from / choose_from.sum())
        idxes = np.sort([first_idx, second_idx])
        self.board[7, :] = start_positions[idxes[0]]
        self.board[0, :] = start_positions[idxes[1]][::-1] + 10
        return

    def get_state(self):
        return self.state

    def valid_moves(self, player):
        result = np.zeros(169, dtype=np.bool_)
        colour_to_move = self.info[0, 0]
        if colour_to_move == -1:
            for colour in range(8):
                token = 10 * player + colour
                position = np.argwhere(self.board == token)[0]
                player_direction = 2 * player - 1
                max_distance = 2
                for direction in range(3):
                    for distance in range(1, max_distance):
                        new_placement = (
                            position[0] + player_direction * distance,
                            position[1] - player_direction * (direction - 1) * distance
                        )

                        if 0 <= new_placement[0] <= 7 and 0 <= new_placement[1] <= 7:
                            if self.board[new_placement] == -1:
                                result[colour * 21 + direction * 7 + distance - 1] = True
                            else:
                                break
                        else:
                            break
        else:
            token = 10 * player + colour_to_move
            position = np.argwhere(self.board == token)[0]
            player_direction = 2 * player - 1
            if self.info[0, 1] < 3:
                max_distance = self.info[0, 1] * 2 + 2
            else:
                max_distance = 8
            for direction in range(3):
                for distance in range(1, max_distance):
                    new_placement = (
                        position[0] + player_direction * distance,
                        position[1] - player_direction * (direction - 1) * distance
                    )

                    if 0 <= new_placement[0] <= 7 and 0 <= new_placement[1] <= 7:
                        if self.board[new_placement] == -1:
                            result[colour_to_move * 21 + direction * 7 + distance - 1] = True
                        else:
                            break
                    else:
                        break
        if np.sum(result) == 0:
            result[-1] = True
        return result

    def make_move(self, move, player, random_seed):
        if move != 168:
            colour = move // 21
            token = 10 * player + colour
            position = np.argwhere(self.board == token)[0]
            direction = (move % 21) // 7
            distance = (move % 7) + 1
            player_direction = 2 * player - 1
            new_placement = (position[0] + player_direction * distance, position[1] - player_direction * (direction - 1) * distance)
            self.board[position[0], position[1]] = -1
            self.board[new_placement] = token
            self.info[0, 0] = board_colours[new_placement]
            self.info[0, 2] = 0
        else:
            colour = self.info[0, 0]
            token = 10 * player + colour
            position = np.argwhere(self.board == token)[0]
            self.info[0, 0] = board_colours[position[0], position[1]]
            self.info[0, 2] += 1
        next_player = (player + 1) % 2
        self.info[0, 1] += 1
        return next_player

    def copy_state(self, state, copy_or_not):
        if self.state is state and not copy_or_not:
            return
        self.state = state.copy() if copy_or_not else state
        self.board = self.state[0:8, :]  # 8
        self.info = self.state[8:9, :]  # 1

    def check_end_game(self, next_player):
        if (np.any((self.board[0] >= 0) & (self.board[0] < 10))):
            out = np.array([1.0, -1.0], dtype=np.float32)
        elif np.any(self.board[7] >= 10):
            out = np.array([-1.0, 1.0], dtype=np.float32)
        elif self.info[0, 2] > 10:
            out = np.array([1.0, 1.0], dtype=np.float32)
            out[next_player] = -1.0
        else:
            out = np.array([0.0, 0.0], dtype=np.float32)
        return out

    def swap_players(self, _player):
        self.board[:] = np.flip(self.board)
        p0_rows = []
        p0_cols = []
        p1_rows = []
        p1_cols = []

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                val = self.board[i, j]
                if 0 <= val <= 8:
                    p0_rows.append(i)
                    p0_cols.append(j)
                elif 10 <= val <= 18:
                    p1_rows.append(i)
                    p1_cols.append(j)

        for k in range(len(p0_rows)):
            self.board[p0_rows[k], p0_cols[k]] += 10

        for k in range(len(p1_rows)):
            self.board[p1_rows[k], p1_cols[k]] -= 10

    def get_symmetries(self, policy, valid_actions):
        symmetries = [(self.state.copy(), policy, valid_actions)]
        return symmetries

    def get_round(self):
        return self.info[0, 1]
