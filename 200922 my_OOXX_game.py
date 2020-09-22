'''
demo_project_Python/200922 OOXXgame
Author: Elie-Yen
Python version: 3.6
'''
  
import numpy as np
import random as rd
def MyGame():
    P, C = 'X', 'O'
    level, board, order, R = 0, np.full((3,3), '_'), [], {'C': 0, 'P': 0, 'draw': 0}
    deco = '\n' + '=' * 25 + '\n'
    welcome = ('\nWelcome! Please choose game level\n(type [ end ] to end at anytime)\n' +
                'type [ easy / mid / master ]\n')
    ask_next = '\nWhere do you wanna put {0}?\n(valid number range: 0,1,2 ex: 2, 2 )'
    c_rep = "I'm done! I put {0} at ({1}, {2})\n"
    playend = 'Would you wanna play again?\ntype [ play / end ]\n'
    
    def Err_(res, msg): #invalid input
        print("\nSorry, invalid input: '", res,"' please type again!")
        return 'type [ {0} ]'.format(msg)
    
    def Winner_(row, col):  
        h, v = set(board[row]), set(board.T[col])
        d1, d2 = set(board.flat[[0,4,8]]), set(board.flat[[2,4,6]])
        for x in [{P}, {C}]:  # someone won
            if x in (h, v, d1, d2):
                if x == {P}: #player won
                    R['P'] += 1
                    print('\n ====Congrats! you won====\n', board, deco)
                else: # computer won
                    R['C'] += 1
                    print( '\n =======Good  Game!=======\n', board, deco) 
                order.append('end')
                return playend
        if '_' not in board:  # a draw
            R['draw'] += 1
            order.append('end')  
            print( "\n =========A draw!=========\n", board, deco)
            return playend
        # keep playing
        elif order[-1] == P:  # player's turn end 
            print("\nYou put {0} at ({1}, {2})\n".format(P, row, col),
                  board,"\n\nnow it's my turn!\n")
            return C_(board)
        else: # computer's turn end
            print(ask_next.format(P))
            return 'type [ row, column ]'
    
    
    def C_(board): # calculate the best position.... the most difficult part
        order.append(C)
        d1, d2 = board.flat[[0,4,8]], board.flat[[2,4,6]]
        vacancy = set()
        # test if anyone is about to connect in his next turn
        for x in [C,P]:
            line = []
            for i in range(3): 
                if d1[i] == '_' and set(sorted(d1)[:2]) == {x}:
                    line.append((i,i))
                if d2[i] == '_' and set(sorted(d2)[:2]) == {x}:
                    line.append((i, 2-i))
                for j in range(3):
                    if board[i,j] == '_':
                        vacancy.add((i,j))
                        if set(sorted(board[i])[:2]) == {x}:
                            line.append((i,j))
                    if board[j,i] == '_' and set(sorted(board.T[i])[:2]) == {x}:
                        line.append((j,i))
            if line: # some one is about to connect
                row, col = rd.choice(line)
                board[row, col] = C
                print(c_rep.format(C, row, col), board)
                return Winner_(row, col)
        
        # no one is about to connect
        corner = {(0,0), (2,0), (0,2), (2,2)}
        row, col = rd.choice(list(vacancy)) # default for not-included & easy
        if corner & vacancy and level in ['mid', 'master']:
            row, col = rd.choice(list(corner & vacancy))
            if board[1,1] == '_':
                row, col = rd.choice([(1, 1), (row, col)])
            d = {0: [1, 3, 2], 2: [1, 5, 0], 6: [7, 3, 8], 8: [7, 5, 6]}
            
            '''
            P _ _
            _ C *
            _ _ P
            '''
            d6 = list(filter(lambda x: ( # defend with 6 empty
                set(board.flat[[ abs(x-4) - 1, 9 - abs(x-4) ]]) == {P} 
                and board[1,1] == C and len(vacancy) == 6), [1,3,5,7]))
            
            '''
            _ ? _    _ P _
            C C P    ? C ?
            * ? _    * C _
            '''
            bsT_4 = list(filter(lambda x: ( # big slope Triangle with 4 available corner
                (set(board.flat[[ 4, d[x][1] ]]) in ({C}, {P})
                 and set(board.flat[[ x, 8 - x, 8 -d[x][2] ]]) == {'_'} )
                or (set(board.flat[[ 4, d[x][0] ]]) in ({C}, {P})
                    and set(board.flat[[ x, 8 - x, d[x][2] ]]) == {'_'} )), [0,2,6,8]))
                      
            '''
            * C _
            C ? ?
            _ ? ?
            
            '''
            sL_3 = list(filter(lambda x: ( # small L with 3 available corner
                (set(board.flat[[ d[x][0], d[x][1] ]]) in ({C}, {P}) 
                and set(board.flat[[ x, d[x][2], 8 - d[x][2] ]]) == {'_'} )), [0,2,6,8]))
            
            '''
            * C _   * _ C 
            _ ? ?   C ? ?
            C ? ?   _ ? ?
            '''
            sL_2 = list(filter(lambda x: ( # small L with 2 available corner
                (set(board.flat[[ d[x][2], d[x][1] ]]) in ({C}, {P})
                 and set(board.flat[[ x, 8 - d[x][2], d[x][0] ]]) == {'_'} )
                or (set(board.flat[[ 8 - d[x][2], d[x][0] ]]) in ({C}, {P})
                    and set(board.flat[[ x, d[x][2], d[x][1] ]]) == {'_'} )), [0,2,6,8]))
            
            '''
             C P _   P ? _
             _ C ?   ? C P
             * ? P   * _ C
            '''
            bsT_2 = list(filter(lambda x: ( # big slope Triangle with 2 available corner
                (set(board.flat[[ 4, 8 - d[x][2] ]]) in ({C}, {P})
                 and set(board.flat[[ x, 8 - x, d[x][1] ]]) == {'_'} )
                or (set(board.flat[[ 4, d[x][2] ]]) in ({C}, {P})
                    and set(board.flat[[ x, 8 - x, d[x][0] ]]) == {'_'} )), [0,2,6,8]))
            
            '''
            ? ? C    C P C
            ? _ P    _ _ ?
            * _ C    * ? ?
            '''
            bsT_1  = list(filter(lambda x: ( # big slope Triangle with 1 available corner
                (set(board.flat[[ 8 - x, 8 - d[x][2] ]]) in ({C}, {P})
                 and set(board.flat[[ x, 4, d[x][1] ]]) == {'_'} )
                or (set(board.flat[[ 8 - x, d[x][2] ]]) in ({C}, {P})
                    and set(board.flat[[ x, 4, d[x][0] ]]) == {'_'} )), [0,2,6,8]))
            
            '''
            C ? ?
            _ P ?
            * _ C
            '''
            bL_1 = list(filter(lambda x: ( # big L with 1 available corner
                set(board.flat[[ d[x][2], 8 - d[x][2] ]]) == {C}
                and set(board.flat[[ x, d[x][0], d[x][1] ]]) == {'_'} ), [0,2,6,8]))
                      
            if level == 'master' and (d6 or bsT_4 or sL_3 or sL_2):
                x = 0
                if d6:
                    x = rd.choice(d6)
                elif bsT_4:
                    x = rd.choice(bsT_4)
                elif sL_3:
                    x = rd.choice(sL_3)    
                else:
                    x = rd.choice(sL_2)
                row, col = x // 3, x % 3
            
            # master & mid
            elif bsT_2 or bsT_1 or bL_1: 
                x = 0
                if bsT_2:
                    x = rd.choice(bsT_2)
                elif bsT_1:
                    x = rd.choice(bsT_1)    
                else:
                    x = rd.choice(bL_1)
                row, col = x // 3, x % 3                         
            elif len(corner & vacancy) == 3:
                if board[1,1] == '_':
                    row, col = 1, 1
                else:
                    x = list(corner - vacancy) 
                    row, col = 2 - x[0][0], 2 - x[0][1] 
        board[row, col] = C
        print (c_rep.format(C, row, col), board)
        return Winner_(row, col)


    # main processing of player
    print(welcome)
    res = input().replace(' ','').lower()
    while res != 'end': 
        res_s = res.split(',')
        if not order: #choose level
            if res in  ('easy', 'mid', 'master'):
                level = res
                order.append(level)
                print('\nYou choose [ {0} ] level'.format(level),
                     '\nWould you wanna start first?\ntype [ y / n ]\n')
            else:
                print(Err_(res, 'easy / mid / master')) 
        elif order == [level]: #game start
            if res == 'y':
                order.append(P)
                print (ask_next.format(P),'\ntype [ row, column ]')
            elif res == 'n':
                P, C = 'O', 'X'
                order.append(C)
                print("\nTHX, you're a nice guy! I'll start first!\n\n")
                print(C_(board), '\n')
            else:
                print( Err_(res, 'y / n') ) 
        elif (order[-1] !=  'end' and len(res_s)== 2   #player's turn
               and set(res_s).issubset({'0','1','2'})): 
                row, col = int(res_s[0]), int(res_s[1])
                if board[row, col] == '_':
                    board[row, col] = P
                    order.append(P)
                    print(Winner_(row, col))   
                else: # valid input but it's occupied
                    print( '\nSorry, {0},{1} is occupied!'.format(row, col),
                          'please type again!\ntype [ row, column ]\n')
        else: 
            if order[-1] == 'end':  # game over
                if res.lower() == 'play': # play again
                    board, order = np.full((3,3), '_'), []
                    P, C = 'X', 'O'
                    print(welcome)
                else: 
                    print( Err_(res, 'play, end'))
            else:
                print( Err_(res, 'row, column') )  
        res = input()
    
    result = '\ntotal: {0}\nPlayer: {1} %\nComputer: {2} %\nDraw: {3} %'
    if sum(R.values()):
        s = sum(R.values())
        print(result.format(s), round(100 * R['P'] / s, 2), 
                           round(100 * R['C'] / s, 2),
                           round(100 * R['draw'] / s, 2)))
    print(deco, " End the game\n THX for playing MyGame!!!", deco) #end game
    R['P'], R['C'], R['draw'] = 0, 0, 0
    return 'The program ends successfully'
