"""
Logique du jeu Tic Tac Toe avec support de l'IA
"""

from .utils import create_empty_board, check_winner, is_board_full, switch_player
from .ai import TicTacToeAI
from config.settings import PLAYERS

class GameLogic:
    """Classe gérant la logique du jeu Tic Tac Toe"""
    
    def __init__(self, game_mode='pvp', ai_difficulty='medium'):
        self.board = create_empty_board()
        self.current_player = PLAYERS['starting_player']
        self.game_over = False
        self.score_x = 0
        self.score_o = 0
        self.game_mode = game_mode  # 'pvp' ou 'ai'
        self.ai_difficulty = ai_difficulty
        
        # Initialiser l'IA si nécessaire
        if game_mode == 'ai':
            self.ai = TicTacToeAI(difficulty=ai_difficulty, player_symbol='O')
        else:
            self.ai = None
    
    def is_ai_turn(self):
        """Retourne True si c'est le tour de l'IA"""
        return self.game_mode == 'ai' and self.current_player == 'O'
    
    def get_ai_move(self):
        """Retourne le coup de l'IA"""
        if self.ai and self.is_ai_turn():
            return self.ai.get_move(self.board)
        return None
    
    def get_ai_thinking_time(self):
        """Retourne le temps de réflexion de l'IA"""
        if self.ai:
            return self.ai.get_thinking_time()
        return 0
        
    def make_move(self, row, col):
        """
        Effectue un mouvement sur la grille
        
        Args:
            row: Ligne de la case
            col: Colonne de la case
            
        Returns:
            dict: Résultat du mouvement avec les informations sur l'état du jeu
        """
        if self.game_over or self.board[row][col] != "":
            return {'valid': False}
            
        # Sauvegarder le joueur qui fait le coup avant de changer
        player_who_played = self.current_player
            
        # Effectuer le mouvement
        self.board[row][col] = self.current_player
        
        # Vérifier la victoire
        if check_winner(self.board):
            self.game_over = True
            winner = self.current_player
            if winner == 'X':
                self.score_x += 1
            else:
                self.score_o += 1
            return {
                'valid': True,
                'game_over': True,
                'winner': winner,
                'draw': False,
                'player_who_played': player_who_played
            }
            
        # Vérifier l'égalité
        if is_board_full(self.board):
            self.game_over = True
            return {
                'valid': True,
                'game_over': True,
                'winner': None,
                'draw': True,
                'player_who_played': player_who_played
            }
            
        # Changer de joueur
        self.current_player = switch_player(self.current_player)
        return {
            'valid': True,
            'game_over': False,
            'winner': None,
            'draw': False,
            'player_who_played': player_who_played
        }
        
    def restart_game(self):
        """Redémarre une nouvelle partie"""
        self.board = create_empty_board()
        self.current_player = PLAYERS['starting_player']
        self.game_over = False
        
    def reset_scores(self):
        """Remet les scores à zéro"""
        self.score_x = 0
        self.score_o = 0
        
    def get_board(self):
        """Retourne l'état actuel de la grille"""
        return self.board
        
    def get_current_player(self):
        """Retourne le joueur actuel"""
        return self.current_player
        
    def get_scores(self):
        """Retourne les scores actuels"""
        return {'X': self.score_x, 'O': self.score_o}
        
    def is_game_over(self):
        """Retourne True si le jeu est terminé"""
        return self.game_over
