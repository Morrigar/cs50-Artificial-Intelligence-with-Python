import itertools
import random
import copy

#test


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells)==self.count:
            return cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells)==0:
            return cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=4, width=4):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            if not sentence.cells:
                self.knowledge.remove(sentence)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            if not sentence.cells:
                self.knowledge.remove(sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        print (f'Known Mines: {self.mines}')
        neighbors = set ()                                    # Create a set of the neighbors for the sentence.
        for i in range(cell[0] - 1, cell[0] + 2):             # Loop over all cells within one row and column of cell
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell or (i,j) in self.safes:     # Ignore the cell itself or if it is already in safe list.
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:  # Otherwise add cell to neighbors.
                    neighbors.add((i,j))

        if count == 0:                              # If there are no mines in the count, mark all cells
            for item in neighbors:
                print (f'In initial pass, markings {item} as safe.')
                self.mark_safe(item)
            return

        if len(neighbors) == count:
            for item in neighbors:
                print (f'In initial pass, marking {item} as a mine.')
                self.mark_mine(item)
            return

        if len(neighbors) == 0:
            return

        newKnowledge = Sentence(neighbors, count)  # Create the sentence.
        knowledgeCopy = copy.deepcopy(self.knowledge)           # Copy the knowledge

        for sentence in knowledgeCopy:
            if not sentence.cells:
                self.knowledge.remove(sentence)
            if sentence.cells.issubset(newKnowledge.cells) and sentence.cells != newKnowledge.cells:      # from existing sentences in the knowledge base.
                print (f'Subtracting {sentence} from {newKnowledge}.')
                derivedSentence = Sentence(newKnowledge.cells.difference(sentence.cells),
                                                                                    newKnowledge.count - sentence.count)
                print (f'Result {derivedSentence}')
                if derivedSentence.count == 0:
                    for item in derivedSentence.cells:
                        print (f'Adding {item} to safe cells.')
                        self.mark_safe(item)
                elif derivedSentence.count == len (derivedSentence.cells):
                    for item in derivedSentence.cells:
                        print (f'Adding {item} to mines.')
                        self.mark_mine(item)
                else:
                    print (f'Adding {derivedSentence} to Knowledge.')
                    self.knowledge.append(derivedSentence)
            if newKnowledge.cells.issubset(sentence.cells) and sentence.cells != newKnowledge.cells:
                print(f'Subtracting {newKnowledge} from {sentence}.')
                derivedSentence = Sentence(sentence.cells.difference(newKnowledge.cells),
                                                                                    sentence.count - newKnowledge.count)
                print (f'Result: {derivedSentence}')
                if derivedSentence.count == 0:
                    for item in derivedSentence.cells:
                        print(f'Adding {item} to safe cells.')
                        self.mark_safe(item)
                elif derivedSentence.count == len(derivedSentence.cells):
                    for item in derivedSentence.cells:
                        print(f'Adding {item} to mines.')
                        self.mark_mine(item)
                else:
                    print (f'Adding {derivedSentence} to Knowledge.')
                    self.knowledge.append(derivedSentence)

        if newKnowledge not in self.knowledge:
            self.knowledge.append(newKnowledge)

        for sentence in self.knowledge:
            if not sentence.cells:
                print ('In cleanup, removing empty sentence.')
                self.knowledge.remove(sentence)
            if len(sentence.cells)==sentence.count:
                eraser = []
                for item in sentence.cells:
                    eraser.append(item)
                for item in eraser:
                    print(f'In cleanup, marking {item} as mine.')
                    self.mark_mine(item)
            if sentence.count == 0:
                eraser = []
                for item in sentence.cells:
                    eraser.append(item)
                for item in eraser:
                    print (f'In cleanup, marking {item} as safe.')
                    self.mark_safe(item)






    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if not self.safes:
            return
        possibleMoves = self.safes.difference(self.moves_made)
        if not possibleMoves:
            return
        returnMove = possibleMoves.pop()
        print (f'Chose {returnMove} as a safe move.')
        return returnMove

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        i = random.randrange(self.height)
        j = random.randrange(self.width)
        move = (i,j)
        while move in self.mines or move in self.moves_made:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            move = (i, j)
        print(f'Chose {move} as a random move.')
        return move


game = Minesweeper()
for i in range(game.height):
    row = []
    for j in range(game.width):
        game.board[i][j] = False

game.board[1][3] = True
game.board[2][2] = True


hal = MinesweeperAI()



tset = {1,2,3,4,5}
tset2 = {2,3,4}

def makeAmove(AI, game):
    if AI.make_safe_move != None:
        move = AI.make_safe_move()
        AI.add_knowledge (move, game.nearby_mines(move))
    else:
        move = AI.make_random_move()
        AI.add_knowledge (move, game.nearby_mines(move))


#hal.add_knowledge((0,0),game.nearby_mines((0,0)))

#hal.add_knowledge((0,1), 1)
#hal.add_knowledge((0,2), 1)

#hal.add_knowledge((2,1), 2)

#makeAmove(hal, game)