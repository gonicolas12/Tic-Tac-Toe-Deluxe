"""
Configuration du jeu Tic Tac Toe
"""

# Paramètres de la fenêtre
WINDOW_CONFIG = {
    'title': 'Jeu de Tic Tac Toe - Edition Deluxe',
    'min_width': 500,
    'min_height': 400,
    'default_width_ratio': 0.6,  # 60% de la largeur de l'écran
    'default_height_ratio': 0.7,  # 70% de la hauteur de l'écran
    'max_width': 1200,
    'max_height': 900,
    'resizable': True,
    'fullscreen': False
}

# Couleurs
COLORS = {
    'background': '#1a1a2e',
    'background_secondary': '#16213e',
    'background_tertiary': '#0f3460',
    'text_primary': '#eee6ff',
    'text_secondary': '#ff6b6b',
    'text_player_o': '#4ecdc4',
    'accent': '#e43f5a',
    'accent_secondary': '#f9ca24',
    'button_normal': '#16213e',
    'button_hover': '#0f3460',
    'button_active': '#533483',
    'button_restart': '#27ae60',
    'button_restart_hover': '#2ecc71',
    'button_replay': '#9b59b6',
    'button_replay_hover': '#8e44ad',
    'button_reset': '#e67e22',
    'button_reset_hover': '#f39c12',
    'button_quit': '#e74c3c',
    'button_quit_hover': '#c0392b',
    'button_fullscreen': '#3498db',
    'button_fullscreen_hover': '#2980b9',
    'winning_highlight': '#f39c12',
    'grid_line': '#533483',
    'shadow': '#000000'
}

# Paramètres de la grille (adaptatifs)
GRID_CONFIG = {
    'size': 3,
    'button_min_size': 70,    # Taille minimale réduite (80 -> 70)
    'button_max_size': 105,   # Taille maximale réduite (120 -> 105)
    'button_padding_ratio': 0.07,  # Padding légèrement réduit (0.08 -> 0.07)
    'border_width': 2,
    'relief_style': 'raised'
}

# Paramètres des joueurs
PLAYERS = {
    'player1': 'X',
    'player2': 'O',
    'starting_player': 'X'
}

# Messages
MESSAGES = {
    'victory': "Victoire!",
    'victory_text': "Le joueur {player} a gagné!",
    'draw': "Égalité!",
    'draw_text': "Match nul!",
    'current_player': "Tour du joueur: {player}",
    'score': "Score - X: {score_x}  |  O: {score_o}"
}

# Polices (adaptatives selon la taille d'écran)
FONTS = {
    'title': {
        'family': 'Segoe UI',
        'size_ratio': 0.045,  # Réduit de 0.06 à 0.045
        'weight': 'bold',
        'min_size': 16,
        'max_size': 36
    },
    'subtitle': {
        'family': 'Segoe UI',
        'size_ratio': 0.025,
        'weight': 'italic',
        'min_size': 10,
        'max_size': 20
    },
    'player_label': {
        'family': 'Segoe UI',
        'size_ratio': 0.03,  # Réduit de 0.035 à 0.03
        'weight': 'bold',
        'min_size': 11,
        'max_size': 20
    },
    'button_game': {
        'family': 'Segoe UI',
        'size_ratio': 0.08,  # Proportionnel à la taille des boutons
        'weight': 'bold',
        'min_size': 16,
        'max_size': 40
    },
    'button_control': {
        'family': 'Segoe UI',
        'size_ratio': 0.018,  # Légèrement réduit de 0.022 à 0.018
        'weight': 'bold',
        'min_size': 9,
        'max_size': 14
    },
    'score': {
        'family': 'Segoe UI',
        'size_ratio': 0.03,
        'weight': 'bold',
        'min_size': 11,
        'max_size': 18
    },
    'info': {
        'family': 'Segoe UI',
        'size_ratio': 0.02,
        'weight': 'normal',
        'min_size': 8,
        'max_size': 12
    }
}

# Paramètres d'animation et d'effets visuels
ANIMATION_CONFIG = {
    'particle_count': 50,
    'particle_speed_min': -1.0,
    'particle_speed_max': 1.0,
    'particle_size_min': 2,
    'particle_size_max': 5,
    'animation_fps': 20,  # Images par seconde
    'button_hover_scale': 1.05,
    'button_click_scale': 0.95,
    'pulse_duration': 200,  # ms
    'fade_duration': 300,   # ms
    'bounce_height': 10     # pixels
}

# Configuration de l'IA
AI_CONFIG = {
    'levels': {
        'easy': {
            'name': '🟢 FACILE',
            'description': 'IA basique avec mouvements aléatoires',
            'thinking_time': 0.5
        },
        'medium': {
            'name': '🟡 MOYEN', 
            'description': 'IA avec stratégie moyenne',
            'thinking_time': 1.0
        },
        'hard': {
            'name': '🔴 DIFFICILE',
            'description': 'IA experte avec algorithme minimax',
            'thinking_time': 2.0
        }
    },
    'default_level': 'medium'
}

# Configuration du menu
MENU_CONFIG = {
    'auto_fullscreen': True,
    'animation_enabled': True,
    'particle_background': True,
    'button_animations': True
}
