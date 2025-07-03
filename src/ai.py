"""
Intelligence artificielle pour le jeu Tic Tac Toe
IA difficile mais battable avec stratégie adaptative
"""

import random
import time
from .utils import check_winner, is_board_full

class TicTacToeAI:
    """IA difficile mais battable pour le jeu Tic Tac Toe"""
    
    def __init__(self, difficulty='hard', player_symbol='O'):
        # Le paramètre difficulty est conservé pour compatibilité mais ignoré
        self.player_symbol = player_symbol
        self.human_symbol = 'X' if player_symbol == 'O' else 'O'
        self.move_count = 0  # Compteur de coups pour adapter la stratégie
        
    def get_move(self, board):
        """
        Retourne le meilleur coup pour l'IA difficile mais battable
        
        Args:
            board: État actuel de la grille (3x3)
            
        Returns:
            tuple: (row, col) du meilleur coup
        """
        self.move_count += 1
        return self._get_challenging_move(board)
    
    def _get_challenging_move(self, board):
        """
        IA difficile mais battable : utilise une stratégie adaptative
        - Premier coup : évite le centre (plus humain)
        - Privilégie la stratégie défensive/offensive
        - Introduit parfois des coups suboptimaux calculés
        """
        # Premier coup de l'IA : stratégie variable et plus humaine
        if self.move_count == 1:
            return self._get_opening_move(board)
        
        # Toujours vérifier si l'IA peut gagner immédiatement
        win_move = self._find_winning_move(board, self.player_symbol)
        if win_move:
            return win_move
        
        # Toujours bloquer si le joueur peut gagner
        block_move = self._find_winning_move(board, self.human_symbol)
        if block_move:
            return block_move
        
        # Vérifier les fourchettes (double menace) - priorité élevée
        fork_move = self._find_fork_move(board, self.player_symbol)
        if fork_move:
            # 85% de chance de jouer la fourchette (laisse 15% d'opportunité)
            if random.random() < 0.85:
                return fork_move
        
        # Bloquer les fourchettes adverses
        opponent_fork = self._find_fork_move(board, self.human_symbol)
        if opponent_fork:
            # Chercher un coup qui bloque la fourchette ou crée une contre-menace
            counter_move = self._find_counter_fork(board, opponent_fork)
            if counter_move:
                return counter_move
            return opponent_fork  # Bloquer directement si pas de contre-jeu
        
        # Stratégie adaptative selon la phase de jeu
        if self.move_count <= 3:
            # Début de partie : stratégie positionnelle avec un peu d'aléatoire
            return self._get_positional_move(board)
        else:
            # Fin de partie : jeu plus précis mais pas parfait
            return self._get_endgame_move(board)
    
    def _get_opening_move(self, board):
        """Premier coup de l'IA - stratégie variée et moins prévisible"""
        # Si le joueur a pris le centre, prendre un coin (stratégie classique)
        if board[1][1] == self.human_symbol:
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            available_corners = [(r, c) for r, c in corners if board[r][c] == ""]
            if available_corners:
                return random.choice(available_corners)
        
        # Si le joueur a pris un coin, ne pas toujours prendre le centre
        corners_taken = sum(1 for r, c in [(0, 0), (0, 2), (2, 0), (2, 2)] if board[r][c] == self.human_symbol)
        
        if corners_taken > 0:
            # 60% de chance de prendre le centre, 40% de prendre un autre coin ou côté
            if random.random() < 0.6 and board[1][1] == "":
                return (1, 1)
            else:
                # Prendre un coin libre ou un côté
                good_moves = []
                corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
                
                for r, c in corners + sides:
                    if board[r][c] == "":
                        good_moves.append((r, c))
                
                if good_moves:
                    return random.choice(good_moves)
        
        # Première ouverture : variation entre centre et coins
        if board[1][1] == "":
            # 70% centre, 30% coin (plus imprévisible que toujours centre)
            if random.random() < 0.7:
                return (1, 1)
        
        # Prendre un coin si disponible
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [(r, c) for r, c in corners if board[r][c] == ""]
        if available_corners:
            return random.choice(available_corners)
        
        # Fallback sur un mouvement aléatoire
        return self._get_random_move(board)
    
    def _find_fork_move(self, board, symbol):
        """Trouve un coup qui crée une fourchette (double menace de victoire)"""
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    # Tester ce coup
                    board[i][j] = symbol
                    winning_moves = []
                    
                    # Compter combien de coups gagnants ce coup créerait
                    for x in range(3):
                        for y in range(3):
                            if board[x][y] == "":
                                board[x][y] = symbol
                                if check_winner(board):
                                    winning_moves.append((x, y))
                                board[x][y] = ""
                    
                    board[i][j] = ""  # Annuler le coup test
                    
                    # C'est une fourchette si on a au moins 2 coups gagnants
                    if len(winning_moves) >= 2:
                        return (i, j)
        
        return None
    
    def _find_counter_fork(self, board, fork_position):
        """Trouve un coup qui bloque une fourchette ou crée une contre-menace"""
        # D'abord essayer de créer une menace qui force l'adversaire à défendre
        for i in range(3):
            for j in range(3):
                if board[i][j] == "" and (i, j) != fork_position:
                    board[i][j] = self.player_symbol
                    
                    # Vérifier si ce coup crée une menace immédiate
                    threats = 0
                    for x in range(3):
                        for y in range(3):
                            if board[x][y] == "":
                                board[x][y] = self.player_symbol
                                if check_winner(board):
                                    threats += 1
                                board[x][y] = ""
                    
                    board[i][j] = ""  # Annuler le coup test
                    
                    # Si ce coup crée une menace, c'est un bon contre-jeu
                    if threats > 0:
                        return (i, j)
        
        return None
    
    def _get_positional_move(self, board):
        """Stratégie positionnelle avec un peu d'aléatoire"""
        # Prendre le centre si disponible (70% de chance)
        if board[1][1] == "" and random.random() < 0.7:
            return (1, 1)
        
        # Prendre un coin si disponible
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [(r, c) for r, c in corners if board[r][c] == ""]
        if available_corners:
            # 80% de chance de prendre un coin, 20% de faire autre chose
            if random.random() < 0.8:
                return random.choice(available_corners)
        
        # Stratégie alternative : côtés ou mouvement aléatoire
        return self._get_fallback_move(board)
    
    def _get_endgame_move(self, board):
        """Stratégie de fin de partie - plus précise mais pas parfaite"""
        # Utiliser minimax avec une probabilité réduite (90%)
        if random.random() < 0.9:
            _, move = self._minimax(board, True, -float('inf'), float('inf'))
            if move:
                return move
        
        # 10% du temps, utiliser une stratégie simple (moins optimale)
        return self._get_fallback_move(board)
    
    def _get_fallback_move(self, board):
        """Stratégie de fallback simple pour remplacer les anciens niveaux"""
        # Prendre le centre si disponible
        if board[1][1] == "":
            return (1, 1)
        
        # Prendre un coin si disponible
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [(r, c) for r, c in corners if board[r][c] == ""]
        if available_corners:
            return random.choice(available_corners)
        
        # Prendre un côté
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_sides = [(r, c) for r, c in sides if board[r][c] == ""]
        if available_sides:
            return random.choice(available_sides)
        
        # Mouvement aléatoire en dernier recours
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    empty_cells.append((i, j))
        
        return random.choice(empty_cells) if empty_cells else None
    
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
    
    def reset_game(self):
        """Réinitialise l'état de l'IA pour une nouvelle partie"""
        self.move_count = 0
    
    def get_thinking_time(self):
        """Retourne un temps de réflexion pour rendre l'IA plus humaine"""
        # Temps de réflexion variable selon la phase de jeu
        if self.move_count == 1:
            return random.uniform(0.8, 1.5)  # Premier coup plus rapide
        elif self.move_count <= 3:
            return random.uniform(1.2, 2.3)  # Début de partie
        else:
            return random.uniform(1.8, 3.2)  # Fin de partie plus réfléchie
