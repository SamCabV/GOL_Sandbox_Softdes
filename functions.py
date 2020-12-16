import random
import numpy as np
import string
import copy
import pygame

pygame.font.init()
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


def user_inputs():
    '''
    Draws UI to prompt user to input intial model parameters and
    game mode

    Args:
        None
    Returns:
        output: List containing three values,
            index 0: Game Mode Int from 0-2
            index 1: String number list for Alpha Val
            index 2: String Number list for Delta Val
    '''
    pygame.init()
    surface = pygame.display.set_mode((1150, 600))
    diagram = pygame.image.load(r'data/diagram.jpg')  # Moore Diagram Image
    text = pygame.image.load(r'data/text.jpg')  # Wall of text image
    clock = pygame.time.Clock()
    game_mode = 0  # 0 = GOL, 1 = GORB, 2 = Custom

    # Starts up a bunch of the text boxes and buttons
    input_box1 = InputBox(450, 500, 160, 32)
    input_box2 = InputBox(450, 550, 160, 32)
    text_box1 = TextBox(360, 500, 90, 32, "Input α:")
    text_box2 = TextBox(360, 550, 90, 32, "Input δ:")
    gol_switch = button(COLOR_ACTIVE, 50, 400, 160, 60, "Play GOL")
    gorb_switch = button(COLOR_INACTIVE, 250, 400, 160, 60, "Play GORB")
    custom_switch = button(COLOR_INACTIVE, 450, 400, 160, 60, "Play Custom")
    finish_switch = button(COLOR_INACTIVE, 50, 500, 130, 80, "Start Draw")
    soup_switch = button(COLOR_INACTIVE, 200, 500, 130, 80, "Start Soup")

    # Put all the text boxes and buttons into lists for
    # easy drasurfaceg
    input_boxes = [input_box1, input_box2]
    boxes = [input_box1, input_box2, text_box1, text_box2]
    switches = [
        gol_switch,
        gorb_switch,
        custom_switch,
        finish_switch,
        soup_switch]
    done = False

    # Input Loop Runs until closed or
    # Game Start Button Clicked
    while not done:
        # Handle Quiting
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                done = True

            # Handle Mouse Dection in Text Boxes
            # and Buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gol_switch.isOver(pos):
                    if game_mode == 0:
                        pass
                    else:
                        game_mode = 0

                if gorb_switch.isOver(pos):
                    if game_mode == 1:
                        pass
                    else:
                        game_mode = 1

                if custom_switch.isOver(pos):
                    if game_mode == 2:
                        pass
                    else:
                        game_mode = 2

                if finish_switch.isOver(pos):
                    output = [game_mode, input_box1.text, input_box2.text, 0]
                    pygame.quit()
                    return output
                if soup_switch.isOver(pos):
                    output = [game_mode, input_box1.text, input_box2.text, 1]
                    pygame.quit()
                    return output
                if game_mode == 0:
                    gol_switch.color = COLOR_ACTIVE
                    gorb_switch.color = COLOR_INACTIVE
                    custom_switch.color = COLOR_INACTIVE
                if game_mode == 1:
                    gol_switch.color = COLOR_INACTIVE
                    gorb_switch.color = COLOR_ACTIVE
                    custom_switch.color = COLOR_INACTIVE
                if game_mode == 2:
                    gol_switch.color = COLOR_INACTIVE
                    gorb_switch.color = COLOR_INACTIVE
                    custom_switch.color = COLOR_ACTIVE

            # Little Color animation when hovering over
            # Finish Button
            if finish_switch.isOver(pos):
                finish_switch.color = COLOR_ACTIVE
            else:
                finish_switch.color = COLOR_INACTIVE
            if soup_switch.isOver(pos):
                soup_switch.color = COLOR_ACTIVE
            else:
                soup_switch.color = COLOR_INACTIVE

            # Handle events in boxes
            for box in input_boxes:
                box.handle_event(event)

        # Draw Everything
        surface.fill((30, 30, 30))
        for box in boxes:
            box.draw(surface)
        for switch in switches:
            switch.draw(surface)
        surface.blit(pygame.transform.rotozoom(diagram, 0, .83), (0, 0))
        surface.blit(pygame.transform.rotozoom(text, 0, .95), (640, 0))
        pygame.display.flip()
        clock.tick(30)


class button():
    """
    Defines buttons for user input

    Class has a number of methods for user interaction
    with buttons, including drasurfaceg and mouse detection

    Code adapted from: https://bit.ly/37NRA7S

    Attributes:
        Color: RGB values to set color of button drawn
        x: int X position of button
        y: int Y position of button
        width: int width of button
        height: int height of button
        text: string text button holds
    """

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface):
        """
        Draws button

        Takes in a surface and draws a button
        on that surface

        Args:
            surface: pygame surface in which to draw button
        """
        pygame.draw.rect(
            surface,
            self.color,
            (self.x,
             self.y,
             self.width,
             self.height),
            0)

        # Draw text on button
        if self.text != '':
            font = pygame.font.Font(None, 32)
            text = font.render(self.text, 1, (0, 0, 0))
            surface.blit(text,
                         (self.x + (self.width / 2 - text.get_width() / 2),
                          self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        """
        Checks if the mouse is over a
        button and returns True if it is

        Args:
            pos: current mouse position as a tuple
                of (x,y) coordinates using pygame's
                mouse button down feature
        Returns:
            if the mouse is in the same bounding box as
            the button, returns true
        """
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class InputBox:
    """
    Defines a text input box class

    Class has a number of methods for user interaction
    with text iput, such as being clicked and typed on

    Code adapted from: https://bit.ly/3m5Nq03

    Attributes:
        rect: defines as a rectangle
        x: int X position of text box
        y: int Y position of text box
        width: int width of text box
        height: int height of text box
        text: string input text the text box holds
        rect: Defines as text box as a
            rectangle using x, y, width & height
        color: Color of button
        active = state of button
        txt_surface = renders text directly on
            text box
    """

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        Defines a text input box class

        Class has a number of methods for user interaction
        with text iput, such as being clicked and typed on

        Attributes:
            event: takes in pygame event
        """

        # Handle getting clicked on by setting
        # Button to active and changing color
        if event.type == pygame.MOUSEBUTTONDOWN:

            # as long as it is selected change color
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        # Handle typing once button is clicked
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):

        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, surface):

        # Blit the text.
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Draw the rect.
        pygame.draw.rect(surface, self.color, self.rect, 2)


class TextBox:
    """
    Defines a Static Text Box

    Class works similar to the InputBox class but
    simply displays given text and has no user
    interaction

    Code adapted from: https://bit.ly/3m5Nq03

    Attributes:
        rect: defines as a rectangle
        x: int X position of text box
        y: int Y position of text box
        width: int width of text box
        height: int height of text box
        text: string input text the text box holds
        rect: Defines as text box as a
            rectangle using x, y, width & height
        color: Color of button
        txt_surface = renders text directly on
            text box
    """

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, surface):
        # Blit the text.
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Draw the rect.
        pygame.draw.rect(surface, self.color, self.rect, 2)


def draw_rand(dimx, dimy):
    '''
    Populates a grid with a random starting
    Cell arragement also known as a "soup"

    Args:
        dimx: int for x size of game grid
        dimy: int for y size of game grid
    Returns:
        grid: an np array with randomized 0's
        and 1's representing a cell layout
    '''
    grid = np.random.randint(0, 2, (dimx, dimy))
    return grid


def draw(dimx, dimy):
    '''
    Creates and displays a drawable grid

    Creates an array-backed grid that can be
    clicked on to "draw" cells, drawn cells
    can also be clicked on to get deleted.
    Sets up initial conditions for calcualting
    board states in given cellular automaton algorithm.

    Args:
        dimx: int for x size of game grid
        dimy: int for y size of game grid
    Returns:
        grid: np array contating initial
            parameters for automaton simulation
    '''

    sz = 8  # Global Cell Size

    # Adjust actually dispalyed grid to be
    # smaller to ignore edge-cases which are
    # permanatantly dead cells
    vdimx = dimx - 2
    vdimy = dimy - 2

    # Starts up np array as grid
    grid = make_grid(dimx, dimy)

    # Initialize pygame
    pygame.init()

    # Display parameters of surface adjusted
    surface = pygame.display.set_mode((vdimx * sz, vdimy * sz))

    # Set Title of surface to instructions
    pygame.display.set_caption(
        "Please Draw Your Initial Conditions, Press Space when done")

    # Loop until the user clicks the close button
    done = False

    # set clock to not go faster than its supposed to
    clock = pygame.time.Clock()

    # input loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle closing surface
                done = True  # break loop when done

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Handle Space quit
                    done = True  # break loop when done
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Change the x/y surface coordinates to grid descrete
                # grid areas
                column = pos[0] // (sz)
                row = pos[1] // (sz)

                # Set that location to one or alive
                if grid[row][column] == 0:
                    grid[row][column] = 1

                # or delete a cell that's already alive
                else:
                    grid[row][column] = 0

                # DEBUG CODE:
                # print("Click ", pos, "Grid coordinates: ", row, column)

        # Set the surface background
        surface.fill(col_background)

        # Draw and update board state as its drawn
        draw_board(surface, grid)

        # Draw the grid
        draw_grid(surface, dimx, dimy)

        # Limit to 60 frames per second
        clock.tick(60)

        # Display Changes in surface
        pygame.display.flip()

    # Make sure we actually quit if we break the loop
    pygame.quit()

    # Output Drawn State
    return grid


def draw_grid(surface, dimy, dimx):
    '''
    Draws the actual grid lines

    Draws grid lines to make drasurfaceg initial coniditions
    a bit easier for the user

    Args:
        surface: pygame surface in which to draw the grid
        dimx: int for x size of game grid
        dimy: int for y size of game grid
    '''
    sz = 8  # Global Cell Size
    for i in range(dimx):
        new_height = round(i * sz)
        new_width = round(i * sz)

        # Lines were being buggy so just draw them to impossibly
        # long lengths to assure they reach from one side of the screen to the
        # other
        pygame.draw.line(surface, col_alive, (0, new_height),
                         (10000, new_height), 1)
        pygame.draw.line(surface, col_alive, (new_width, 0),
                         (new_width, 10000), 1)


def game(dimx, dimy, sz, grid, alpha=[2, 3], delta=[3], GORB=0):
    '''
    Maing game loop function, Simulates the
    cellular automata behavior using desired
    rule-set and initial conditions

    Takes in all the nessasary inputs to simulate desired
    automaton setup and enables a user to interact with
    which each "generation" of the simulation by playing
    forward and backward using corresponding keyboard
    arrows or using space to let simulation run. For GOL
    and custom rulesets pre-calculates first 150 moves,
    for GORB calculates only 100 for because pre-caluclating
    too many more would crash and take longer to boot up program.


    Args:
        dimx: int for x size of game grid
        dimy: int for y size of game grid
        sz: int cell size, TODO: GLOBALIZE
        grid: np array with initial conditions
            for sim
        alpha: tuple representing how many live cell
            neighbors a live cell must have to
            survive to the next generation
        delta: tuple representing how many live cell
            neighbors a dead cell must have to be
            born next generation
        GORB: int, are we playing GORB??? :^)
    '''
    # Set up a bunch of variables
    pygame.init()
    loading = pygame.image.load(r'data/loading.jpg')
    # Crop Display
    vdimx = dimx - 2
    vdimy = dimy - 2
    surface = pygame.display.set_mode((vdimx * sz, vdimy * sz))

    pygame.display.set_caption(
        "Cellular Automaton Simulation, Space to Pause or Play,\
            Left and Right Arrow Keys to Step")

    counter = 0  # current position of sim in list of positions
    auto_play = 0  # flag for "auto-play" of sim
    clock = pygame.time.Clock()

    # Set loading Screen
    surface.fill((30, 30, 48))
    surface.blit(pygame.transform.rotozoom(loading, 0, .6), (0, 0))
    pygame.display.update()
    # list that holds all game states calulcated
    # done this way so player can step back in time
    game_grids = []
    game_grids.append(grid)

    # Pre-generate boardstates to make game
    # experience more smooth
    if GORB == 0:
        for i in range(200):
            game_grids.append(play_round(game_grids[-1], alpha, delta))

    # because GORB is unpredictable, generate less states to prevent crashes
    else:
        alpha = random.sample(range(0, 8), random.randint(0, 8))
        delta = random.sample(range(0, 8), random.randint(0, 8))
        for i in range(150):
            game_grids.append(play_round(game_grids[-1], alpha, delta))

    # Debug code for probing crashes:
    # print("ready to go")

    draw_board(surface, game_grids[0])  # Draw first board state
    clock.tick(60)
    pygame.display.update()

    # Handles all keyboard inputs to navigate
    # Through board-states
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                # Scrub through states forward
                # and backward with arrow keys
                if event.key == pygame.K_RIGHT:
                    counter += 1
                    # Protect inputs to get more descrete movement
                    pygame.time.delay(5)
                if event.key == pygame.K_LEFT:
                    counter -= 1
                    pygame.time.delay(5)

                # Set outplay on and off
                if event.key == pygame.K_SPACE:
                    auto_play = not(auto_play)

        # If outplay, scrub forward a step at a
        # time with 5ms breaks
        if auto_play == 1:
            counter += 1
            pygame.time.delay(5)

        # Generate next state if it hasn't been generated yet
        if counter + 10 > len(game_grids):
            game_grids.append(play_round(game_grids[-1], alpha, delta))

        # Prevent player from going into negative indexes to
        # protect from breaking program
        if counter < 0:
            counter = 0

        # Draws current board state
        # Prevents player from drawing states that
        # Haven't been computed
        if counter < len(game_grids):
            surface.fill(col_grid)
            draw_board(surface, game_grids[counter])
            clock.tick(60)
            pygame.display.update()


def draw_board(surface, new_grid):
    '''
    Draws board for automaton

    Takes in a surface and np array and
    draws on to the surface

    Args:
        surface: pygame surface in which to the grid
        new_grid: np array that represents a board state
    '''

    sz = 8  # Global Cell Size

    # Sweep through every cell, take its information
    # Draw an appropriate square representing each cell
    for j, tile in enumerate(new_grid):
        for i, tile_contents in enumerate(tile):
            myrect = pygame.Rect(i * sz, j * sz, sz, sz)
            pygame.draw.rect(surface, map_color(tile_contents), myrect)

    # Uncomment if you want to see a grid in final sim
    # draw_grid(surface,size[0],size[1])
    return


def map_color(cell):
    '''
    Map cell state to color

    Takes in a cell state and outputs its
    appropriate color

    Args:
        cell: int/boolean representing cell state
    Returns:
        col: RGB value for setting cell color
    '''

    if cell == 0:
        col = col_background
    if cell == 1:
        col = col_alive
    return col


def play_round(grid, alpha=[2, 3], delta=[3]):
    '''
    Calculates following board state by applying
    state-machine function

    Takes in nessasary variables to calculate the next
    board state, and outputs it as an np array

    Args:
        grid: np grid to use for calculations
        alpha: tuple representing how many live cell
            neighbors a live cell must have to
            survive to the next generation
        delta: tuple representing how many live cell
            neighbors a dead cell must have to be
            born next generation
    Returns:
        new_grid: np array representing next board state
    '''
    size = grid.shape
    new_grid = make_grid(size[0], size[1])  # Make a whole new grid

    # Sweep through grid and evaluate it cell by cell
    for i in range(size[0] - 2):
        for j in range(size[1] - 2):
            new_grid[i + 1][j + 1] = evaluate(i + 1, j + 1, grid, alpha, delta)
    return new_grid


def evaluate(an, am, grid, alpha, delta):
    '''
    Takes in a grid and evaluates a single cell
    by looking at the cells around it

    Evaluates a cell by turning the current cell into
    an object that sums its count of neighbors and
    applying checking for alpha and delta conditions.

    Args:
        an: int representing rows index in cell grid
            being evaluated
        am: int representing columns index in cell grid
            being evaluated
        grid: np grid being evaluated
        alpha: tuple representing how many live cell
            neighbors a live cell must have to
            survive to the next generation
        delta: tuple representing how many live cell
            neighbors a dead cell must have to be
            born next generation
    Returns:
        next_state: int representing next cell state
    '''

    # Make arrays to check each condition with flexibility
    alpha_check = []
    delta_check = []

    # Create a cell object based on the current
    # grid index being evaluated and each of its
    # neighbors to calculate next state
    new_cell = cell(grid[an][am],
                    grid[an + 1][am],
                    grid[an + 1][am + 1],
                    grid[an][am + 1],
                    grid[an - 1][am],
                    grid[an][am - 1],
                    grid[an - 1][am - 1],
                    grid[an + 1][am - 1],
                    grid[an - 1][am + 1])

    # Check Delta if dead
    # and alpha if alive
    if new_cell._state == 0:
        for i in delta:

            # check all delta values as neighbors sum
            # OR all of them to check if any of the states
            # are represented
            delta_check.append(new_cell.check_n(i))
        next_state = any(delta_check)
    if new_cell._state == 1:
        for i in alpha:

            # check all alpha values as neighbors sum
            # OR all of them to check if any of the states
            # are represented
            alpha_check.append(new_cell.check_n(i))
        next_state = any(alpha_check)
    return next_state


class cell:
    """
    Creates a cell object that has convinient methods
    for calculating the cell's next state

    Attributes:
        state: Cell being evaluated
        TL: Cell Top-Left to Cell being evaluated
        T: Cell Top to Cell being evaluated
        TR: Cell Top-Right to Cell being evaluated
        L: Cell Left to Cell being evaluated
        R: Cell Right to Cell being evaluated
        BL: Cell Bottom-Left to Cell being evaluated
        B: Cell Bottom to Cell being evaluated
        BR: Cell Bottom-Right to Cell being evaluated
        _num_n: Sum of all neighbors
    """

    def __init__(self, state, TL, T, TR, L, R, BL, B, BR):
        self._state = state
        self._num_n = TL + T + TR + L + R + BL + B + BR

    def check_n(self, n):
        """
        Check if a cell has n neighbors

        Args:
            n: value to check if cell has that
                many neighbors
        returns:
            boolean value representing a cell
            having that many neighbors
        """

        if self._num_n == n:
            return 1
        else:
            return 0


def make_grid(n, m):
    """
    Makes a "blank grid" of size nxm
    represented by an np array

    Args:
        n: number of rows in grid
        m: number of columns in grid
    returns:
        grid: np array representing
            game board

    """

    # Make grid bigger to account for edge cases
    grid = np.zeros((n + 2, m + 2), dtype=int)
    return grid


def populate_grid(keyn, keym, grid):
    """
    Populates grid adjusted for edge-cases

    Used for bug testing and to populate the
    grid before GUI implementation was made

    Args:
        keyn: row index of cell
        keym: column index of cell
        grid: np array representing game board
    returns:
        grid: np array representing game board

    """
    grid[keyn + 2, keym + 2] = 1
    return grid
