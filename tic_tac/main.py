# Function to print the current state of the game board
def display_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def check_win(board, player):
    # All 8 possible winning line combinations (3 horizontal, 3 vertical, 2 diagonal)
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]
    
    for combo in win_combinations:
        # Check if all 3 positions in a combination contain the current player's mark
        if board[combo[0]] == player and board[combo[1]] == player and board[combo[2]] == player:
            return True
    return False

# Function to check if the board is completely full (Draw condition)
def check_draw(board):
    # If there are no empty spaces (' ') left, it's a draw
    return ' ' not in board

# Main game loop function
def play_game():
    # Represent the board as a list of 9 empty spaces
    board = [' '] * 9
    current_player = 'X'
    game_over = False

    print("--- Welcome to Python Tic-Tac-Toe ---")
    print("Positions are numbered from 1 to 9 as follows:")
    print(" 1 | 2 | 3 ")
    print("---|---|---")
    print(" 4 | 5 | 6 ")
    print("---|---|---")
    print(" 7 | 8 | 9 ")
    
    while not game_over:
        display_board(board)
        
        # Input loop to ensure valid user input
        while True:
            try:
                move = int(input(f"Player {current_player}, choose a position (1-9): ")) - 1
                
                # Check if move is within range and the spot is empty
                if 0 <= move <= 8 and board[move] == ' ':
                    board[move] = current_player
                    break
                else:
                    print("Invalid move! That spot is taken or out of range. Try again.")
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 9.")

        # Check if the current move resulted in a win
        if check_win(board, current_player):
            display_board(board)
            print(f" Player {current_player} wins!")
            game_over = True
        # Check if the move resulted in a tie
        elif check_draw(board):
            display_board(board)
            print(" It's a draw! Well played both.")
            game_over = True
        else:
            # Switch players: if 'X', change to 'O'; if 'O', change to 'X'
            current_player = 'O' if current_player == 'X' else 'X'

# Run the game
if __name__ == "__main__":
    play_game()