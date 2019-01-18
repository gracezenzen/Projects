#Grace Zenzen zenze007

# I understand this is a graded, individual examination that may not be
# discussed with anyone.  I also understand that obtaining solutions or
# partial solutions from outside sources, or discussing
# any aspect of the examination with anyone will result in failing the course.
# I further certify that this program represents my own work and that none of
# it was obtained from any source other than material presented as part of the
# course.

import turtle
import random

#Takes input of nested list and uses it to draw the gameboard (initial board only)
def drawboard(board):
    turtle.setworldcoordinates(-248,-248,0,0)
    numbers=('1','2','3','4','5','6','7','8')
    turtle.hideturtle()
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-223,-10)
    turtle.shape("square")
    turtle.color("blue")
    turtle.resizemode("user")
    turtle.shapesize(25,25,10)
    for i in range(0,8):
        turtle.color("black")
        turtle.write(numbers[i], font=("Arial",15,"normal"))
        turtle.goto(turtle.xcor()+25, turtle.ycor())
    turtle.goto(-240, turtle.ycor()-15)
    for i, row in enumerate(board):
        turtle.color("black")
        turtle.write(numbers[i], font=("Arial",15,"normal"))
        turtle.goto(turtle.xcor()+19,turtle.ycor())
        for column in row:
            turtle.shape('square')
            turtle.color("blue")
            turtle.shapesize(2,2)
            turtle.stamp()
            if column==1:
                turtle.shape("circle")
                turtle.color("white")
                turtle.shapesize(1,1)
                turtle.stamp()
                turtle.goto(turtle.xcor()+25,turtle.ycor())
            elif column==2:
                turtle.shape("circle")
                turtle.color("black")
                turtle.shapesize(1,1)
                turtle.stamp()
                turtle.goto(turtle.xcor()+25,turtle.ycor())
            else:
                turtle.goto(turtle.xcor()+25,turtle.ycor())
        turtle.goto(-240, turtle.ycor()-25)

#cleans up player input into a list of two number/coordinates. Detects if player wants to exit and basic errors in input form.
def cleanup(string):
    row=False
    col=False
    done=False
    if string=='':
        done=True
        return done, row, col
    elif string==None:
        done=True
        return done, row, col
    else:
        string=string.replace('(','')
        string=string.replace(')','')
        string=string.replace(',','')
        string=string.replace(' ','')
        if not string.isdigit() or len(string)>2:
            return done, row, col
        else:
            for letter in string:
                if letter.isalpha():
                    return done, row, col
            row=int(string[0])
            col=int(string[1])
    return done, row, col

#Converts matrix/board coordinates to turtle coordinates
def findcoordinates(row, col):
    dict_xcors={1:-221, 2:-196, 3:-171, 4:-146, 5:-121, 6:-96, 7:-71, 8:-46}
    dict_ycors={1:-25, 2:-50, 3:-75, 4:-100, 5:-125, 6:-150, 7:-175, 8:-200}
    turtle_xcor=dict_xcors[col]
    turtle_ycor=dict_ycors[row]
    return turtle_xcor, turtle_ycor

#updates board by stamping "tile" onto a space. Does one at a time.
def update_board(turtle_xcor,turtle_ycor, color):
    turtle.goto(turtle_xcor, turtle_ycor)
    turtle.shape('circle')
    turtle.shapesize(1,1)
    if color==1:
        turtle.color("white")
    else:
        turtle.color("black")
    turtle.stamp()

#returns counter of neighbors of opposite color and a list of the coordinates of the neighbors
def neighbors(board, row, col, color):
    counter=0
    neighborsList=[]
    #Find coordinate in terms of matrix (matrix starts at zero and board starts at 1)
    r_index=int(row)-1
    c_index=int(col)-1
    for i, row in enumerate(board):
        if i==r_index-1 or i==r_index+1 or i==r_index:
            for j, value in enumerate(row):
                if j==c_index or j==c_index-1 or j==c_index+1:
                    if value!=color and value!=0:
                        counter+=1
                        neighborsList.append((i+1,j+1))
    return counter, neighborsList

#Takes coordinates of neighbor of opposite color (in terms of board) and goes along the "line" (uses operations) to see if there is a white tile in the line (making it a valid move)
def final_stop_batman(row_matrix, column_matrix, operations, board, color):
    done=False
    validLine=False
    while done==False:
        if row_matrix>7 or column_matrix>7:
            done=True
        elif row_matrix<0 or column_matrix<0:
            done=True
        elif board[row_matrix][column_matrix]==color:
            done=True
            validLine=True
        elif board[row_matrix][column_matrix]==0:
            done=True
        else:
            row_matrix=row_matrix+operations[0]
            column_matrix=column_matrix+operations[1]
    return validLine

#checks if the player move is valid, first calls neighbors to find neighbors of opposite color. Then calls final_stop_batman to see if there's another white tile along that line
#Returns list of valid tiles tiles next to the move, and operations to move along that line.
def isValidMove(board, row, col, color):
    validity=False
    validNeighbors=[]
    operations_list=[]
    counter, neighborsList=neighbors(board, row, col, color)
    if counter==0:
        return validity, neighborsList, (0,0)
    for coordinates in neighborsList:
        operations=(coordinates[0]-row,coordinates[1]-col) #(neighbor row minus move row, neighbor column minus move column)- returns operations necessary to move to next place in line
        final_value=final_stop_batman(coordinates[0]-1+operations[0], coordinates[1]-1+operations[1], operations, board, color)
        if final_value==True:
            validity=True
            validNeighbors.append(coordinates)
            operations_list.append(operations)
    return validity, validNeighbors, operations_list

#Updates board/matrix by 'flipping' all tiles of opposite color IN ONE LINE
def flip(board, color, neighbor, operations):
    flipped_tiles=[]
    r_index=neighbor[0]-1
    c_index=neighbor[1]-1
    done=False
    while done==False:
        if r_index<=7 and c_index<=7:
            if board[r_index][c_index]!=color and board[r_index][c_index]!=0:
                flipped_tiles.append((r_index+1,c_index+1))
                r_index=r_index+operations[0]
                c_index=c_index+operations[1]
            else:
                done=True
        else:
            done=True
    return flipped_tiles

#Uses isValidMove and iteration to find all possible moves in the board for a given color.
def getValidMoves(board, color):
    possible_moves=[]
    r_index=0
    c_index=0
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column==0:
                validity, validNeighbors, operations_list=isValidMove(board, i+1, j+1, color)
                if validNeighbors!=[]:
                    possible_moves.append((i, j))
    return possible_moves

#Uses possible moves from getValidMoves to select the next computer play.
def selectNextPlay(board):
    possible_moves=getValidMoves(board, 1)
    computer_move=random.choice(possible_moves)
    rowC=computer_move[0]+1
    colC=computer_move[1]+1
    return rowC, colC

#Uses another turtle to clear previous message and write new message.
def turtleMessage(message, alfred):
    alfred.clear()
    alfred.hideturtle()
    alfred.penup()
    alfred.goto(-124,-248)
    alfred.shapesize(1,1)
    alfred.color('black')
    alfred.write(message, align="center", font=("Arial", 18, 'bold'))
    return alfred

#Brings functions together to update matrix and display for computer moves.
def updateBoardComp(board, alfred):
    rowC, colC=selectNextPlay(board)
    turtleMessage("Computer moves to " + str(rowC)+', '+ str(colC), alfred)
    validity, validNeighbors, operations_list=isValidMove(board, rowC, colC, 1)
    board[rowC-1][colC-1]=1
    all_dose_flips=[]
    for i, coordinates in enumerate(validNeighbors):
        doseCoordinates=flip(board, 1, coordinates, operations_list[i])
        all_dose_flips+=doseCoordinates
    all_dose_flips.append((rowC, colC))
    for things in all_dose_flips:
        board[things[0]-1][things[1]-1]=1
    for coordinates in all_dose_flips:
        turtle_xcor, turtle_ycor=findcoordinates(coordinates[0], coordinates[1])
        update_board(turtle_xcor, turtle_ycor, 1)
    return board

#Brings functions together to update matrix and display for player moves.
def updateBoardPlayer(board, validNeighbors, row, col, operations_list):
    board[row-1][col-1]=2
    total_flips_player=[]
    for i, coordinates in enumerate(validNeighbors):
        flipped_tiles=flip(board, 2, coordinates, operations_list[i])
        total_flips_player+=flipped_tiles
    total_flips_player.append((row, col))
    for things in total_flips_player:
        board[things[0]-1][things[1]-1]=2
    #Update board with new tile and flipped tiles
    for coordinates in total_flips_player:
        turtle_xcor, turtle_ycor=findcoordinates(coordinates[0], coordinates[1])
        update_board(turtle_xcor,turtle_ycor, 2)
    return board

#Counts the amount of each tile in board/matrix.
def final_count(board):
    white_counter=0
    black_counter=0
    for row in board:
        for column in row:
            if column==1:
                white_counter+=1
            elif column==2:
                black_counter+=1
            else:
                pass
    return white_counter, black_counter

def main():
    alfred=turtle.Turtle()
    alfred.hideturtle()
    board=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,2,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    drawboard(board)
    done=False
    while done==False:
        #Finds the valid moves for each player and the combined valid moves.
        validmovesH=getValidMoves(board, 2)
        validmovesC=getValidMoves(board, 1)
        validmovesA=validmovesH+validmovesC
        #If there are no valid moves exit loop.
        if validmovesA==[]:
            done=True
        #Human doesn't have any valid moves.
        elif validmovesH==[]:
            turtleMessage("You have no valid moves. Computer goes again.", alfred)
            board=updateBoardComp(board, alfred)
        #Computer doesn't have any valid moves.
        elif validmovesC==[]:
            turtleMessage("Computer has no valid moves. You go again.", alfred)
            done2=False
            while done2==False:
                player_move=turtle.textinput("move now please","Where do you want to move (row, column)? ")
                done_detect, row, col=cleanup(player_move)
                #If player wants to quit game or the input is wrong game will quit or display message.
                if done_detect==True:
                    done2=True
                    done=True
                elif row==False and col==False:
                    turtleMessage("That input is not in the correct form (row, column). Please try again.", alfred)
                elif board[row-1][col-1]!=0:
                    turtleMessage("That input is not a valid move. Please review the rules and try again.", alfred)
                else:
                    validity, validNeighbors, operations_list=isValidMove(board, row, col, 2)
                    #If there are no valid neighbors/lines/the move is invalid
                    if validNeighbors==[]:
                        turtleMessage("That input is not a valid move. Please review the rules and try again.", alfred)
                    #Past all input checks. Goes on to update matrix, and display.
                    else:
                        done2=True
                        board=updateBoardPlayer(board, validNeighbors, row, col, operations_list)
        #Both have valid moves.
        else:
            done2=False
            while done2==False:
                player_move=turtle.textinput("move now please","Where do you want to move (row, column)? ")
                done_detect, row, col=cleanup(player_move)
                #If player wants to quit game or the input is wrong game will quit or display message.
                if done_detect==True:
                    done2=True
                    done=True
                elif row==False and col==False:
                    turtleMessage("That input is not in the correct form (row, column). Please try again.", alfred)
                elif board[row-1][col-1]!=0:
                    turtleMessage("That input is not a valid move. Please review the rules and try again.", alfred)
                else:
                    validity, validNeighbors, operations_list=isValidMove(board, row, col, 2)
                    #If there are no valid neighbors/lines/the move is invalid
                    if validNeighbors==[] or board[row-1][col-1]!=0:
                        turtleMessage("That input is not a valid move. Please review the rules and try again.", alfred)
                    else:
                        #Past all input checks. Goes on to update matrix, and display.
                        done2=True
                        board=updateBoardPlayer(board, validNeighbors, row, col, operations_list)
                        #Check if computer has valid moves
                        validmovesC=getValidMoves(board,1)
                        if validmovesC==[]:
                            #If computer doesn't have valid moves.
                            done2=True
                        else:
                            #Computer still has valid moves.
                            board=updateBoardComp(board, alfred)
    #Game is done. Count tiles and display appropriate message.
    white_counter, black_counter=final_count(board)
    if white_counter>black_counter:
        turtleMessage("The computer has won. Feel free to shed your tears in the shower. Score: " + str(white_counter) + ', ' + str(black_counter), alfred)
    elif black_counter>white_counter:
        turtleMessage("Congrats, you won against a machine. You're amazing. Score: " + str(black_counter) + ', ' + str(white_counter), alfred)
    else:
        turtleMessage("You tied. Wow. Score: " + str(white_counter) + ', ' + str(black_counter), alfred)

if __name__ == '__main__':
    main()
