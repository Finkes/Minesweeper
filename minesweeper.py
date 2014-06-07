import random

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class MineSweeperGame(object):
    """docstring for MineSweeperGame"""
    def __init__(self,grid_width,grid_height,num_of_mines):
        super(MineSweeperGame, self).__init__()
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = self._generate_grid(self.grid_width, self.grid_height, num_of_mines)

        self._calculate_numbers()

    def run(self):
        while True:
            self._render_grid()
            x = int(raw_input("X:\t"))
            y = int(raw_input("Y:\t"))

            if not (0 <= x < self.grid_width) or not (0 <= y < self.grid_height):
                print "invalid input (target is out of grid)"
                continue

            selected_cell = self.grid[y][x]

            if selected_cell.is_unvealed():
                continue

            selected_cell.unveal()

            if isinstance(selected_cell, MineCell):
                print "BOOM"
                break

            else:
                if selected_cell.is_zero():
                    self._unveal_neighbours_of_cell(x,y)

    def _unveal_neighbours_of_cell(self,x,y):
        neighbours = self._get_neighbours_of_cell(x,y)

        for n in neighbours:
            cell = self.grid[n[1]][n[0]]

            if not isinstance(cell, MineCell) and not cell.is_unvealed():
                cell.unveal()

                if cell.is_zero():
                    self._unveal_neighbours_of_cell(n[0],n[1])


    def _render_grid(self):

        print " ",

        for i in xrange(0,self.grid_width):
            print i,
        print ""

        for y in xrange(0,self.grid_height):
            print y,
            for x in xrange(0, self.grid_width):
                print self.grid[y][x].get_visible_symbol(),
            print ""


    def _generate_grid(self,width, height, num_of_mines):
        grid = []

        for y in xrange(0,height):
            grid.append([])
            for x in xrange(0,width):
                grid[y].append(Cell())

        while num_of_mines > 0:
            x,y = random.randint(0,width-1), random.randint(0,height-1)

            if not isinstance(grid[y][x], MineCell):
                num_of_mines-=1
                grid[y][x] = MineCell()

        return grid


    def _calculate_numbers(self):
        for y in xrange(0,self.grid_height):
            for x in xrange(0, self.grid_width):
                if not isinstance(self.grid[y][x], MineCell):
                    self.grid[y][x].set_front_side_symbol(str(self._calculate_number(x,y)))


    def _calculate_number(self, x, y):
        neighbours = self._get_neighbours_of_cell(x,y)
        count = 0

        for n in neighbours:
            if isinstance(self.grid[n[1]][n[0]], MineCell):
                count += 1

        return count


    def _get_neighbours_of_cell(self, x ,y):
        
        neighbours = []

        if x < self.grid_width-1: #check right neighbour
            neighbours.append((x+1,y))

        if x > 0: #check left neighbour
            neighbours.append((x-1,y))

        if y < self.grid_height-1: #check below neighbour
            neighbours.append((x,y+1))

        if y > 0: #check above neighbour
            neighbours.append((x,y-1))

        if x < self.grid_width-1 and y < self.grid_height-1:
            neighbours.append((x+1,y+1))

        if x > 0 and y < self.grid_height-1:
            neighbours.append((x-1,y+1))

        if x < self.grid_width-1 and y > 0:
            neighbours.append((x+1,y-1))

        if x > 0 and y > 0:
            neighbours.append((x-1,y-1))

        return neighbours



class Cell(object):
    """docstring for Cell"""
    def __init__(self):
        super(Cell, self).__init__()
        self.unvealed = False
        self.front_side = "?"
        self.back_side = "#"

    def get_visible_symbol(self):
        if self.unvealed:
            if self.is_zero():
                return Colors.OKGREEN + self.front_side + Colors.ENDC    
            return Colors.OKBLUE + self.front_side + Colors.ENDC
        return Colors.WARNING + self.back_side + Colors.ENDC

    def is_unvealed(self):
        return self.unvealed

    def is_zero(self):
        if int(self.front_side) == 0:
            return True
        return False


    def set_front_side_symbol(self, front_side_symbol):
        self.front_side = front_side_symbol

    def unveal(self):
        self.unvealed = True
        

class MineCell(Cell):
    """docstring for MineCell"""
    def __init__(self):
        super(MineCell, self).__init__()
        self.front_side = "X"


        
if __name__ == "__main__":
    game = MineSweeperGame(10,10,10)
    game.run()
