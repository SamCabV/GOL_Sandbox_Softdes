import functions
def main():
    """
    Main function

    Ties all the the funcitons together, 
    prompting user for input game mode,
    then for user to draw, 
    then for user to scrub through game boards
    """
    dimx = 75
    dimy = 75
    while True:
        # Take Input Conditions
        outputs = functions.user_inputs()


        # depeding on inputs appropriately
        # instantiates functions
        # Play Original GOL
        if outputs[0] == 0:
            if outputs[3] == 0:
                grid = functions.draw(dimx,dimy)
                functions.game(dimx,dimy, 8,grid)
            if outputs[3] == 1:
                grid = functions.draw_rand(dimx,dimy)
                functions.game(dimx,dimy, 8,grid)
        #int(tuple(outputs[1])[1])

        # Play GORB
        if outputs[0] == 1:
            if outputs[3] == 0:
                grid = functions.draw(dimx,dimy)
                functions.game(dimx,dimy, 8,grid,[],[],1)
            if outputs[3] == 1:
                grid = functions.draw_rand(100,100)
                functions.game(dimx,dimy, 8,grid,[],[],1)
    

        # Play Custom Game
        if outputs[0] == 2:
            # Parse string of custom rules
            alpha_str = outputs[1].split(",")
            delta_str = outputs[2].split(",")
            alpha = []
            delta = []
            for i in alpha_str:
                alpha.append(int(i))
            for i in delta_str:
                delta.append(int(i))
            if outputs[3] == 0:
                grid = functions.draw(dimx,dimy)
                functions.game(dimx,dimy, 8,grid,alpha,delta)
            if outputs[3] == 1:
                grid = functions.draw_rand(100,100)
                functions.game(dimx,dimy, 8,grid,alpha,delta)
            
if __name__ == "__main__":
    main()
    pygame.quit
    