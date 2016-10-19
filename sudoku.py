import copy


class Game(object):
    def __init__(self, **kwargs):
        self.board = self.readfile(kwargs.get('filename', 'game.txt'))

    def row(self, r, c, coords=False):
        if coords:
            return [(i, r) or i in range(9)]
        return [x for x in self.board[r] if x != 0]

    def column(self, r, c, coords=False):
        if coords:
            return [(c, i) or i in range(9)]
        return [row[c] for row in self.board if row[c] != 0]

    def square(self, row, col, coords=False):
        '''Returns a list of the 9 digits in this coordinate's square
           will be less than 9 if there are blanks
           coords: return list of all coordinates in square'''
        if not 0 <= row <= 8 or not 0 <= col <= 8:
            return None
        result = {}
        key = 0
        for rx in range(3):
            for cx in range(3):
                result[key] = [(r, c) for r in range(rx * 3, rx * 3 + 3)
                                for c in range(cx * 3, cx * 3 + 3)]
                key += 1
        for k in range(9):
            if (row, col) in result[k]:
                if coords:
                    return result[k]
                curr = result[k]
        return [self.board[r][c] for r, c in curr if self.board[r][c] != 0]

    def possible_values(self, r, c):
        taken = set(self.row(r, c) + self.column(r, c) + self.square(r ,c))
        return list(set(range(1, 10)).difference(taken))

    @property
    def complete(self):
        flat = [num for sublist in self.board for num in sublist]
        return 0 not in flat

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

    def solve(self):
        if (-1, -1) == self.next_empty():
            print self.board
        solved = self.rec_solve(*self.next_empty())
        print solved.board

    def rec_solve(self, r, c):
        if r == c == -1:
            return self
        for digit in self.possible_values(r, c):
            new = copy.deepcopy(self)
            new.board[r][c] = digit
            att = new.rec_solve(*new.next_empty())
            if att:
                return att
        return False


def main(g):
    g.solve()



if __name__ == '__main__':
    game = Game(filename='game.txt')
    main(game)
