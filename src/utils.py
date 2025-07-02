"""
Fonctions utilitaires pour le jeu Tic Tac Toe
"""

def create_empty_board(size=3):
    """Crée une grille de jeu vide"""
    return [["" for _ in range(size)] for _ in range(size)]

def check_winner(board):
    """
    Vérifie s'il y a un gagnant sur le plateau
    
    Args:
        board: La grille de jeu 3x3
        
    Returns:
        bool: True s'il y a un gagnant, False sinon
    """
    size = len(board)
    
    # Vérifier les lignes
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return True
            
    # Vérifier les colonnes
    for col in range(size):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return True
            
    # Vérifier les diagonales
    if board[0][0] == board[1][1] == board[2][2] != "":
        return True
    if board[0][2] == board[1][1] == board[2][0] != "":
        return True
        
    return False

def is_board_full(board):
    """
    Vérifie si la grille est pleine
    
    Args:
        board: La grille de jeu 3x3
        
    Returns:
        bool: True si la grille est pleine, False sinon
    """
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True

def get_winning_positions(board):
    """
    Retourne les positions de la ligne gagnante
    
    Args:
        board: La grille de jeu 3x3
        
    Returns:
        list: Liste des positions (row, col) de la ligne gagnante ou None
    """
    size = len(board)
    
    # Vérifier les lignes
    for i, row in enumerate(board):
        if row[0] == row[1] == row[2] != "":
            return [(i, 0), (i, 1), (i, 2)]
            
    # Vérifier les colonnes
    for col in range(size):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return [(0, col), (1, col), (2, col)]
            
    # Vérifier les diagonales
    if board[0][0] == board[1][1] == board[2][2] != "":
        return [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return [(0, 2), (1, 1), (2, 0)]
        
    return None

def switch_player(current_player):
    """
    Change de joueur
    
    Args:
        current_player: Le joueur actuel ('X' ou 'O')
        
    Returns:
        str: L'autre joueur
    """
    return "O" if current_player == "X" else "X"
