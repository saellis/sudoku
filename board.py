
class Board(object):
    """
    Represents a sudoku board to be solved
    """
    def __init__(self, **kwargs):
        """
        :param kwargs:
            filename -> name of the file to read board data from (see game.txt for example)
            board -> 2d list containing board data
        """
        if kwargs.get('filename'):
            self.board = self.readfile(kwargs['filename'])
        else:
            self.board = kwargs['board']
        self.answer = [[0 for _ in range(9)] for _ in range(9)]

    def row(self, r, c, coords=False):
        if coords:
            return [(i, r) for i in range(9)]
        return [x for x in self.board[r] if x != 0]

    def column(self, r, c, coords=False):
        if coords:
            return [(c, i) for i in range(9)]
        return [row[c] for row in self.board if row[c] != 0]

    def square(self, row, col):
        row, col = row - row % 3, col - col % 3
        return [self.board[row + rx][col + cx] for rx in range(3) for cx in range(3)]

    def possible_values(self, r, c):
        taken = set(self.row(r, c) + self.column(r, c) + self.square(r, c))
        return list(set(range(1, 10)).difference(taken))

    @property
    def complete(self):
        return 0 not in [num for sublist in self.board for num in sublist]

    @property
    def valid(self):
        for r in self.board:
            if set(r) != set(range(1, 10)):
                return False
        for c in range(9):
            col = set([row[c] for row in self.board])
            if col != set(range(1, 10)):
                return False
        for r, c in [(r, c) for r in [0, 3, 6] for c in [0, 3, 6]]:
            if set(self.square(r, c)) != set(range(1, 10)):
                return False
        return True

    @staticmethod
    def readfile(filename):
        g = []
        with open(filename, 'r') as f:
            for line in f:
                g.append([int(x) for x in line.split(' ')])
        return g

    def next_empty(self):
        for r, row in enumerate(self.board):
            for c, value in enumerate(row):
                if value == 0:
                    return r, c
        return -1, -1

    def __str__(self):
        res = ''
        for r in self.board:
            for val in r:
                res += str(val) + ' '
            res += '\n'
        return res

    def solve(self):
        if (-1, -1) == self.next_empty():
            print self.board
        solved = self.rec_solve(*self.next_empty())
        if solved:
            print self
        else:
            print 'Unsolvable board'
            exit()

    def rec_solve(self, r, c):
        if r == c == -1:
            return self
        for digit in self.possible_values(r, c):
            self.board[r][c] = digit
            self.answer[r][c] = digit
            att = self.rec_solve(*self.next_empty())
            if att:
                return att
            self.board[r][c] = 0
            self.answer[r][c] = 0
        return False


def main(b):
    b.solve()


if __name__ == '__main__':
    board = Board(filename='game.txt')
    main(board)
