"""
Program for solving 9x9 Sudoku Puzzles.
Uses "Simple" algorithm to solve the puzzle - Involves scanning each row, column and subgrid of the sudoku
puzzle until finds the appropriate number to place in the unit square

23-06-2020
By: Luka Djukic
"""

from typing import List


class SudokuPuzzle:
    """
        A Class which represents a Sudoku Puzzle.

        === Attributes ===
        - puzzle: The grid of numbers
        - complete: Whether the board is complete or not

        === Representation Invariant ===
        - Sudoku cell):
            In each cell the numbers must be between 0-9. Where,
                - 0 represents the cell being empty
                - (1 - 9) are the only possible values that the user can input to complete the puzzle
    """
    puzzle: List[List[int]]
    complete: bool

    def __init__(self, puzzle: List[List[int]]) -> None:
        """
        Initializes an SudokuPuzzle object.

        **NOTE**
            - Changes are made to the given puzzle to ensure that the starting values which make up the puzzle cannot
              be altered.
            - Values which were originally on the board have +10 added to them to differentiate them from values entered
              by the user or program

        """
        for row in range(9):
            for column in range(9):
                if puzzle[row][column] != 0:
                    puzzle[row][column] = puzzle[row][column] + 10  # This is done to differentiate from user entries
        self.puzzle = puzzle
        self.complete = False

    def input_number(self, num: int, row: int, column: int) -> bool:
        """
        Inputs the number, num, into the puzzle at selected row and column
        :param num: The number to input into the board (1-9)
        :param row: The row where the number is being placed (1-9)
        :param column: The column where the number is being placed (1-9)
        :return: True or False depending on whether the input succeeded
        """
        # First we check to make sure the user isn't trying to alter a set number
        if self.puzzle[row][column] > 9:
            return False
        else:
            self.puzzle[row][column] = num
            return True

    def check_subgrid(self, row: int, column: int) -> List[int]:
        """
        Returns a list of numbers used in 3x3 subgrid where the requested unit resides
        """
        used_numbers = []

        # lists which store which rows and columns will be checked - certain combinations correspond to specific
        # subgrids ex: row = [0, 1, 2] x column = [3, 4, 5] Is the top middle subgrid
        row_check = []
        column_check = []

        # First to find which rows will need to be analyzed
        if row < 3:
            row_check.extend([0, 1, 2])
        elif 3 <= row < 6:
            row_check.extend([3, 4, 5])
        else:
            row_check.extend([6, 7, 8])

        # Next to find which columns need to be analyzed
        if column < 3:
            column_check.extend([0, 1, 2])
        elif 3 <= column < 6:
            column_check.extend([3, 4, 5])
        else:
            column_check.extend([6, 7, 8])

        # Loop through subgrid to find used numbers
        for rowiter in row_check:
            for columniter in column_check:
                if self.puzzle[rowiter][columniter] != 0:
                    number = self.puzzle[rowiter][columniter] % 10
                    used_numbers.append(number)

        return used_numbers

    def check_unit_options(self, row: int, column: int) -> List[int]:
        """
        Returns a list of integers that are able to be placed in the selected unit
        """
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Check the numbers used in the row of unit
        for number in self.puzzle[row]:
            if (number % 10) in options:
                options.remove((number % 10))

        # Check the numbers used in the column of the unit
        for rowiter in range(9):
            if (self.puzzle[rowiter][column] % 10) in options:
                options.remove((self.puzzle[rowiter][column] % 10))

        # Check the numbers used in the subgrid of the unit
        nums_in_subgrid = self.check_subgrid(row, column)
        for num in nums_in_subgrid:
            if num in options:
                options.remove(num)

        return options

    def complete_puzzle(self) -> None:
        """
        Scans through the puzzle and completes it by narrowing down the options available for each entry unit until
        only one remains.
        """

        while not self.complete:
            completed_squares = 0
            for row in range(9):
                for column in range(9):
                    if self.puzzle[row][column] != 0:
                        completed_squares += 1
                    else:
                        options = self.check_unit_options(row, column)
                        if len(options) == 1:
                            self.input_number(options[0], row, column)
                            completed_squares += 1
            if completed_squares == 81:
                self.complete = True

    def __str__(self) -> str:
        """
        Return a string representation of this Sudoku Puzzle
        """
        stringed_puzzle = " "
        for row in self.puzzle:
            string_list_of_row = []
            for num in row:
                string_list_of_row.append(str(num % 10))
            stringed_row = ' | '.join(string_list_of_row)
            stringed_puzzle = stringed_puzzle + stringed_row + ' |\n---------------------------------------\n '
        return stringed_puzzle


if __name__ == "__main__":
    sudokuboard = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0],
                   [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
                   [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    sudoku = SudokuPuzzle(sudokuboard)
    print(sudoku)
    print("\n\n\n Now starting process to complete puzzle... \n\n\n")
    sudoku.complete_puzzle()
    print(sudoku)