class GameOverError(Exception):
    # thrown when the game ends for the input/output program to know the
    # game ended and to display an error message
    pass




class Game:
    def __init__(self, rows: int, columns: int, start: list[str]):
        # start is a list passed in that will have "EMPTY" or "CONTENTS"
        # as its first element. If "EMPTY", the list has no more elements,
        # but if "CONTENTS", it will include a new element for each row
        # of the game, specifying what the user wants to have the game
        # board look like at the start.
        self._rows = rows
        self._columns = columns
        # state is the game board
        self._state = []
        # jtop, jmid, and jbot represent the top, middle, and bottom jewels,
        # respectively
        self._jtop = None
        self._jmid = None
        self._jbot = None
        # faller will become a list that holds the 3 jewels in order
        self._faller = None
        # faller state will indicate whether its falling, landed, or frozen
        self._faller_state = None
        if start[0] == 'EMPTY':
            # create an empty list of lists
            for i in range(self._rows):
                row = []
                for j in range(self._columns):
                    row.append(self._empty())
                self._state.append(row)
        elif start[0] == 'CONTENTS':
            # deletes the user command  from the list after its been
            # processed to reduce confusion
            del start[0]
            for i in range(self._rows):
                row = []
                # turn every character, including spaces, from the user
                # commands into a list of those characters.
                initial = [*start[i]]
                for j in range(self._columns):
                    # each element in the game is represented by a list,
                    # in the format [jewel/empty, state]. In this case,
                    # all the initial elements are frozen and added to
                    # the game board
                    row.append([initial[j], 'FROZEN'])
                self._state.append(row)
            # processes the spaces between jewels and shifts them all down
            self._shift_all_down()
            # check if there are any jewels matching
            self._check_for_matches()

    def _shift_all_down(self) -> None:
        # shifts all of the jewels to the bottom, going through any spaces
        # in between
        while True:
            check = 0
            for i in range(self._rows):
                for j in range(self._columns):
                    try:
                        if self._state[i][j][0] != ' ' and self._state[i + 1][j][0] == ' ':
                            piece = self._state[i][j]
                            self._state[i + 1][j] = piece
                            self._state[i][j] = self._empty()
                            check += 1
                    except IndexError:
                        pass
            if check == 0:
                break



    def add_faller(self, faller: str) -> None:
        # creates a list of three jewels, representing a faller
        if self._faller != None:
            pass
        else:
            jewel = faller.split(' ')
            self._jtop = Jewel(jewel[1], -3, int(jewel[0]) - 1)
            self._jmid = Jewel(jewel[2], -2, int(jewel[0]) - 1)
            self._jbot = Jewel(jewel[3], -1, int(jewel[0]) - 1)
            self._faller = [self._jbot, self._jmid, self._jtop]
            # first check if the top spot in the column specified
            # by the user is clear
            if self._check_below_clear():
                # if it is clear, move the faller down, showing the
                # bottomost jewel in the first row
                for jewel in self._faller:
                    jewel.down()
                # if the row below the new location of the faller is 
                # also open, the state of the faller becomes "FALL",
                # otherwise, it becomes "landed"
                if self._check_below_clear():
                    self._faller_state = 'FALL'
                    for jewel in self._faller:
                        if jewel.row() >= 0:
                            self._state[jewel.row()][jewel.col()] = [jewel.color(), self._faller_state]
                else:
                    self._faller_state = 'LANDED'
                    for jewel in self._faller:
                        if jewel.row() >= 0:
                            self._state[jewel.row()][jewel.col()] = [jewel.color(), self._faller_state]                
            # if the top spot in the column specified by the user is
            # occupied, the game ends
            else:
                raise GameOverError

    def clear(self) -> None:
        while self._check_for_matches():
            self._clear_matches()
            self._shift_all_down()

    def faller_exists(self) -> bool:
        if self._faller == None:
            return False
        else:
            return True
    
    def _check_for_matches(self) -> bool:
        # checks if there are any matches and changes the state of the
        # jewels to "MATCH" if they match either vertically, horizontally,
        # or diagonally. Returns true if there are any matches, false
        # otherwise.
        matches = False
        for row in range(self._rows):
            for col in range(1, self._columns - 1):
                # skip empty tiles
                if self._state[row][col][0] != ' ':
                    # check horizontal matches
                    center = self._state[row][col][0]
                    left = self._state[row][col - 1][0]
                    right = self._state[row][col + 1][0]
                    if center == left and center == right:
                        self._state[row][col][1] = 'MATCH'
                        self._state[row][col - 1][1] = 'MATCH'
                        self._state[row][col + 1][1] = 'MATCH'
                        matches = True          
        for row in range(1, self._rows - 1):
            for col in range(self._columns):
                if self._state[row][col][0] != ' ':
                    # check vertical matches
                    center = self._state[row][col][0]
                    above = self._state[row - 1][col][0]
                    below = self._state[row + 1][col][0]
                    if center == above and center == below:
                        self._state[row][col][1] = 'MATCH'
                        self._state[row - 1][col][1] = 'MATCH'
                        self._state[row + 1][col][1] = 'MATCH'
                        matches = True  
        for row in range(1, self._rows - 1):
            for col in range(1, self._columns - 1):
                if self._state[row][col][0] != ' ':
                    # check diagonal matches
                    center = self._state[row][col][0]
                    top_left = self._state[row - 1][col - 1][0]
                    top_right = self._state[row - 1][col + 1][0]
                    bot_left = self._state[row + 1][col - 1][0]
                    bot_right = self._state[row + 1][col + 1][0]
                    if center == top_left and center == bot_right:
                        self._state[row][col][1] = 'MATCH'
                        self._state[row - 1][col - 1][1] = 'MATCH'
                        self._state[row + 1][col + 1][1] = 'MATCH'
                        matches = True
                    if center == top_right and center == bot_left:
                        self._state[row][col][1] = 'MATCH'
                        self._state[row - 1][col + 1][1] = 'MATCH'
                        self._state[row + 1][col - 1][1] = 'MATCH'
                        matches = True      
        return matches

        

    def _clear_matches(self) -> None:
        # looks for any jewels that have been marked as having been
        # matched, and removes them from the game board
        for row in range(self._rows):
            for col in range(self._columns):
                if self._state[row][col][1] == 'MATCH':
                    self._state[row][col] = self._empty()

    def _check_below_clear(self) -> bool:
        # Returns true if the tile below the faller is empty, false otherwise.
        if self._faller != None:
            if self._rows - 1 > self._jbot.row():
                if self._state[self._jbot.row() + 1][self._jbot.col()] == [' ', 'FROZEN']:
                    return True
                else:
                    return False
            else:
                return False


            
    def move(self) -> None:
        # processes a blank input by the user.
        # if there are no fallers, and there are matches, clear the
        # matches and shift all jewels down and marks any new matches
        if self._faller == None:
            if self._check_for_matches():
                self._clear_matches()
                self._shift_all_down()
                self._check_for_matches()
        else:
            # if the faller is in fall state, move the faller down and
            # adjust the state/other tiles accordingly
            if self._faller_state == 'FALL':
                for jewel in self._faller:
                    if jewel.row() >= 0:
                        self._state[jewel.row()][jewel.col()] = self._empty()
                    jewel.down()
                    if not self._check_below_clear():
                        self._faller_state = 'LANDED'
                    if jewel.row() >= 0:
                        self._state[jewel.row()][jewel.col()] = [jewel.color(), self._faller_state] 
            # if faller is in landed state, freeze it. Check if any part of
            # faller did not make it onto the board, and if so, end the game.
            elif self._faller_state == 'LANDED':
                self._faller_state = 'FROZEN'
                for jewel in self._faller:
                    if jewel.row() < 0:
                        raise GameOverError
                    else:
                        self._state[jewel.row()][jewel.col()] = [jewel.color(), self._faller_state]                   
                # after faller freezes, if the game is still going,
                # check if any matches have been resulted from the faller,
                # then reset the faller variables
                self._check_for_matches()
                self._jtop = None
                self._jmid = None
                self._jbot = None
                self._faller = None
                self._faller_state = None



    def move_faller_left(self) -> None:
        # moves visible parts of the faller one tile to the left if
        # vacant and possible
        if self._faller == None:
            pass
        else:
            if self._check_left_is_clear():
                for jewel in self._faller:
                    if jewel.row() >= 0:
                        self._state[jewel.row()][jewel.col()] = self._empty()
                    jewel.left()
                    if self._check_below_clear():
                        self._faller_state = 'FALL'
                    else:
                        self._faller_state = 'LANDED'
                    if jewel.row() >= 0:
                        self._state[jewel.row()][jewel.col()] = [jewel.color(), self._faller_state]            
    def _check_left_is_clear(self) -> bool:
        # verifies the left of the faller is empty
        if self._jbot.col() > 0:
            if self._state[self._jbot.row()][self._jbot.col() - 1][0] == ' ':
                return True
        return False



    def move_faller_right(self) -> None:
        # moves visible parts of the faller one tile to the right if
        # vacant and possible
        if self._faller == None:
            pass
        else:
            if self._check_right_is_clear():
                for jewel in self._faller:
                    if jewel.row() >= 0:
                        self._state[jewel.row()][jewel.col()] = self._empty()
                    jewel.right()
                    if self._check_below_clear():
                        self._faller_state = 'FALL'
                    else:
                        self._faller_state = 'LANDED'
                    if jewel.row() >= 0:
                        self._state[jewel.row()][jewel.col()] = [jewel.color(), self._faller_state]  
    def _check_right_is_clear(self) -> bool:
        # verifies the right of the faller is empty
        if self._jbot.col() < self.columns() - 1:
            if self._state[self._jbot.row()][self._jbot.col() + 1][0] == ' ':
                return True
        return False
    
    def _empty(self) -> list[' ', 'FROZEN']:
        # Returns the representation of an empty tile
        return [' ', 'FROZEN']                

    def rotate_faller(self) -> None:
        # rotates the colors of the fallers as specified in the instructions
        b_color = self._jbot.color()
        m_color = self._jmid.color()
        t_color = self._jtop.color()
        self._jbot.set_color(m_color)
        self._jmid.set_color(t_color)
        self._jtop.set_color(b_color)
        # update them on the board if they are visible
        for jewel in self._faller:
            if jewel.row() >= 0:
                self._state[jewel.row()][jewel.col()][0] = jewel.color()
                
    def rows(self) -> int:
        return self._rows
    def columns(self) -> int:
        return self._columns
    def state(self) -> list[list['Jems']]:
        return self._state
        


class Jewel:
    # Jewel objects contain their color and the row/column they exist in
    def __init__(self, color: str, row: int, col: int):
        self._color = color
        self._row = row
        self._col = col

    def down(self) -> None:
        self._row += 1

    def right(self) -> None:
        self._col += 1

    def left(self) -> None:
        self._col -= 1

    def set_row_col(self, row: int, col: int) -> None:
        self._row = row
        self._col = col

    def set_color(self, color: str) -> None:
        self._color = color
        
    def color(self) -> str:
        return self._color

    def row(self) -> int | None:
        return self._row

    def col(self) -> int | None:
        return self._col










