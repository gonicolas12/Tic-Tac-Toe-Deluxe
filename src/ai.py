"""
Intelligence artificielle pour le jeu Tic Tac Toe
"""

import random
import time
from .utils import check_winner, is_board_full

class TicTacToeAI:
    """IA pour le jeu Tic Tac Toe avec différents niveaux de difficulté"""
    
    def __init__(self, difficulty='medium', player_symbol='O'):
        self.difficulty = difficulty  # 'easy', 'medium', 'hard'
        self.player_symbol = player_symbol
        self.human_symbol = 'X' if player_symbol == 'O' else 'O'
        
    def get_move(self, board):
        """
        Retourne le meilleur coup pour l'IA
        
        Args:
            board: État actuel de la grille (3x3)
            
        Returns:
            tuple: (row, col) du meilleur coup
        """
        if self.difficulty == 'easy':
            return self._get_random_move(board)
        elif self.difficulty == 'medium':
            return self._get_medium_move(board)
        else:  # hard
            return self._get_hard_move(board)
    
    def _get_random_move(self, board):
        """Coup aléatoire (IA facile)"""
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    empty_cells.append((i, j))
        
        return random.choice(empty_cells) if empty_cells else None
    
    def _get_medium_move(self, board):
        """IA moyenne : bloque le joueur et cherche à gagner"""
        # 1. Vérifier si l'IA peut gagner
        win_move = self._find_winning_move(board, self.player_symbol)
        if win_move:
            return win_move
        
        # 2. Vérifier si il faut bloquer le joueur
        block_move = self._find_winning_move(board, self.human_symbol)
        if block_move:
            return block_move
        
        # 3. Prendre le centre si disponible
        if board[1][1] == "":
            return (1, 1)
        
        # 4. Prendre un coin si disponible
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [(r, c) for r, c in corners if board[r][c] == ""]
        if available_corners:
            return random.choice(available_corners)
        
        # 5. Mouvement aléatoire sinon
        return self._get_random_move(board)
    
    def _get_hard_move(self, board):
        """IA difficile : utilise l'algorithme minimax"""
        _, move = self._minimax(board, True, -float('inf'), float('inf'))
        return move
    
    def _find_winning_move(self, board, symbol):
        """Trouve un coup gagnant pour le symbole donné"""
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    # Tester ce coup
                    board[i][j] = symbol
                    if check_winner(board):
                        board[i][j] = ""  # Annuler le coup
                        return (i, j)
                    board[i][j] = ""  # Annuler le coup
        return None
    
    def _minimax(self, board, is_maximizing, alpha, beta, depth=0):
        """
        Algorithme minimax avec élagage alpha-beta
        
        Args:
            board: État de la grille
            is_maximizing: True si c'est le tour de l'IA
            alpha: Valeur alpha pour l'élagage
            beta: Valeur beta pour l'élagage
            depth: Profondeur actuelle
            
        Returns:
            tuple: (score, meilleur_coup)
        """
        # Vérifier les conditions de fin
        if check_winner(board):
            winner = self._get_winner(board)
            if winner == self.player_symbol:
                return 10 - depth, None
            elif winner == self.human_symbol:
                return depth - 10, None
        
        if is_board_full(board):
            return 0, None
        
        if is_maximizing:
            max_eval = -float('inf')
            best_move = None
            
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.player_symbol
                        eval_score, _ = self._minimax(board, False, alpha, beta, depth + 1)
                        board[i][j] = ""
                        
                        if eval_score > max_eval:
                            max_eval = eval_score
                            best_move = (i, j)
                        
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # Élagage alpha-beta
            
            return max_eval, best_move
        
        else:
            min_eval = float('inf')
            best_move = None
            
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.human_symbol
                        eval_score, _ = self._minimax(board, True, alpha, beta, depth + 1)
                        board[i][j] = ""
                        
                        if eval_score < min_eval:
                            min_eval = eval_score
                            best_move = (i, j)
                        
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # Élagage alpha-beta
            
            return min_eval, best_move
    
    def _get_winner(self, board):
        """Retourne le gagnant de la grille actuelle"""
        # Vérifier les lignes
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]
        
        # Vérifier les colonnes
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return board[0][col]
        
        # Vérifier les diagonales
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        
        return None
    
    def get_thinking_time(self):
        """Retourne un temps de réflexion pour rendre l'IA plus humaine"""
        if self.difficulty == 'easy':
            return random.uniform(0.5, 1.5)
        elif self.difficulty == 'medium':
            return random.uniform(1.0, 2.5)
        else:  # hard
            return random.uniform(1.5, 3.0)
