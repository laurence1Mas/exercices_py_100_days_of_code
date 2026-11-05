# c'est que fait la variable WINNING_LINES, elle contient toutes les combinaisons gagnantes possibles 
# pour le jeu du morpion (tic-tac-toe). Chaque tuple représente une ligne gagnante sur le plateau de jeu, 
# en utilisant les indices des cases du plateau (de 0 à 8).
WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

def display_board(board):
    """Affiche le plateau de jeu actuel."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_win(board, player):
    """Vérifie si un joueur a gagné."""
    for line in WINNING_LINES:
        if all(board[position] == player for position in line):
            return True
    return False

def check_draw(board):
    """Vérifie si le jeu est terminé sans gagnant."""
    return " " not in board

def get_player_move(board, player):
    """Demande au joueur de choisir une position valide sur le plateau."""
    while True:
        try:
            # On demande au joueur de choisir une position entre 1 et 9, puis on soustrait 
            # 1 pour obtenir l'indice correspondant dans la liste du plateau.
            move = int(input(f"Player {player}, choose a position (1-9): ")) - 1
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")
            continue
        # On vérifie si le mouvement est valide : il doit être compris entre 0 et 8 (indices du plateau)
        # et la case correspondante doit être vide (représentée par un espace "    
        if 0 <= move < 9 and board[move] == " ":
            return move

        print("Invalid move! That spot is taken or out of range. Try again.")

def play_game():
    """Fonction principale pour jouer au jeu du morpion."""
    board = [" "] * 9
    current_player = "X"

    print("--- Welcome to Python Tic-Tac-Toe ---")
    print("Positions are numbered from 1 to 9 as follows:")
    print(" 1 | 2 | 3 ")
    print("---|---|---")
    print(" 4 | 5 | 6 ")
    print("---|---|---")
    print(" 7 | 8 | 9 ")
    # On entre dans une boucle infinie pour le déroulement du jeu. À chaque itération, 
    # on affiche le plateau, on demande au joueur courant de faire un mouvement, 
    # puis on vérifie si ce joueur a gagné ou si le jeu est terminé par un match nul. 
    # Si aucune de ces conditions n'est remplie, on change de joueur et on continue.
    while True:
        display_board(board)
        move = get_player_move(board, current_player)
        board[move] = current_player
        # On vérifie si le joueur courant a gagné après son mouvement. Si c'est le cas, on affiche le plateau,
        # on annonce le gagnant et on sort de la boucle pour terminer le jeu.
        if check_win(board, current_player):
            display_board(board)
            print(f" Player {current_player} wins!")
            break
        # On vérifie si le plateau est plein et qu'aucun joueur n'a gagné, ce qui signifie 
        # que le jeu est terminé par un match nul.
        if check_draw(board):
            display_board(board)
            print(" It's a draw! Well played both.")
            break
        # On change de joueur pour le prochain tour. Si le joueur courant est "X", on passe à "O",
        # sinon on passe à "X".
        current_player = "O" if current_player == "X" else "X"
# On vérifie si le script est exécuté directement (et non importé comme module).
if __name__ == "__main__":
    play_game()
