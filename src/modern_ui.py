"""
Interface utilisateur ultra-moderne avec animations et effets visuels
"""

import tkinter as tk
from tkinter import messagebox
import math
import time
import threading
import sys
from config.settings import (WINDOW_CONFIG, COLORS, GRID_CONFIG, 
                           MESSAGES, FONTS)
from .utils import get_winning_positions

class ModernGameUI:
    """Interface de jeu ultra-moderne avec effets visuels avancés"""
    
    def __init__(self, master=None, game_logic=None, game_mode='pvp', ai_level='medium', on_return_menu=None):
        self.master = master
        self.game_logic = game_logic
        self.game_mode = game_mode
        self.ai_level = ai_level
        self.on_return_menu = on_return_menu
        self.buttons = []
        self.player_label = None
        self.score_label = None
        self.game_frame = None
        self.canvas = None
        
        # Variables pour les animations et effets
        self.particles = []
        self.animation_running = False
        self.thinking_indicator = None
        self.ai_thinking = False
        self.button_effects = {}
        
        if self.game_mode == 'ai':
            from .ai import TicTacToeAI
            self.ai_player = TicTacToeAI(difficulty=self.ai_level)
        else:
            self.ai_player = None
            
        if self.master:
            self.master.title("TIC TAC TOE DELUXE - Jeu")
            self.master.attributes('-fullscreen', True)
            self.master.configure(bg=COLORS['background'])
            
            self.screen_width = self.master.winfo_screenwidth()
            self.screen_height = self.master.winfo_screenheight()
            
            # Raccourcis clavier
            self.master.bind('<Escape>', self._return_to_menu)
            self.master.bind('<F11>', self._toggle_fullscreen)
            
            self.master.focus_set()
            
            self.is_fullscreen = True
        
    def setup_ui(self):
        """Configure l'interface ultra-moderne"""
        # Canvas de fond pour les effets
        self.canvas = tk.Canvas(
            self.master,
            width=self.screen_width,
            height=self.screen_height,
            bg=COLORS['background'],
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Frame principal
        self.main_frame = tk.Frame(
            self.canvas,
            bg=COLORS['background']
        )
        
        # Configuration du frame principal
        frame_width = min(self.screen_width * 0.9, 1000)
        frame_height = min(self.screen_height * 0.75, 700)
        
        # Ajuster la position verticale selon le mode de jeu
        vertical_offset = 30 if self.game_mode == 'pvp' else 50
        
        self.canvas.create_window(
            self.screen_width // 2,
            self.screen_height // 2 - vertical_offset,
            window=self.main_frame,
            anchor='center',
            width=frame_width,
            height=frame_height
        )
        
        self._create_background_effects()
        self._create_modern_header()
        self._create_ultra_grid()
        self._create_enhanced_controls()
        
        self._create_bottom_control_panel()
        self._create_animated_footer()
        self._start_all_animations()
        self._update_player_display()
    
    def _create_background_effects(self):
        """Crée des effets d'arrière-plan animés"""
        for _ in range(30):
            x = hash(str(_)) % self.screen_width
            y = hash(str(_ * 2)) % self.screen_height
            size = 3 + (_ % 5)
            speed_x = ((_ % 20) - 10) / 15
            speed_y = ((_ % 15) - 7) / 12
            
            particle = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=COLORS['accent_secondary'],
                outline='',
                stipple='gray12'
            )
            
            self.particles.append({
                'id': particle,
                'x': x,
                'y': y,
                'speed_x': speed_x,
                'speed_y': speed_y,
                'size': size
            })
        
        # Lignes de grille subtiles en arrière-plan
        grid_spacing = 50
        for x in range(0, self.screen_width, grid_spacing):
            self.canvas.create_line(
                x, 0, x, self.screen_height,
                fill=COLORS['grid_line'],
                width=1,
                stipple='gray25'
            )
        for y in range(0, self.screen_height, grid_spacing):
            self.canvas.create_line(
                0, y, self.screen_width, y,
                fill=COLORS['grid_line'],
                width=1,
                stipple='gray25'
            )
    
    def _create_modern_header(self):
        """Crée un en-tête moderne avec animations"""
        header_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        header_frame.pack(fill='x', pady=(10, 20))
        
        # Titre avec effet néon - taille plus adaptée
        title_font_size = min(28, max(22, self.screen_height // 35))
        title_font = ('Segoe UI', title_font_size, 'bold')
        
        self.title_label = tk.Label(
            header_frame,
            text="✨ TIC TAC TOE DELUXE ✨",
            font=title_font,
            bg=COLORS['background'],
            fg=COLORS['text_primary']
        )
        self.title_label.pack(pady=(0, 10))
        
        # Mode de jeu - plus compact
        mode_text = "🤖 Mode: Joueur vs IA" if self.game_mode == 'ai' else "👥 Mode: Joueur vs Joueur"
        mode_font_size = min(14, max(12, self.screen_height // 70))
        mode_font = ('Segoe UI', mode_font_size, 'italic')
        
        self.mode_label = tk.Label(
            header_frame,
            text=mode_text,
            font=mode_font,
            bg=COLORS['background'],
            fg=COLORS['accent_secondary']
        )
        self.mode_label.pack(pady=(0, 10))
        
        # Indicateur de joueur actuel avec animation
        player_frame = tk.Frame(
            header_frame,
            bg=COLORS['background_secondary'],
            relief='solid',
            bd=2
        )
        player_frame.pack(pady=10)
        
        player_font = ('Segoe UI', max(16, self.screen_height // 40), 'bold')
        self.player_label = tk.Label(
            player_frame,
            text=f"🔴 Tour du joueur: {self.game_logic.get_current_player()} 🔴",
            font=player_font,
            bg=COLORS['background_secondary'],
            fg=COLORS['text_secondary'],
            padx=20,
            pady=10
        )
        self.player_label.pack()
        
        # Indicateur de réflexion IA
        if self.game_mode == 'ai':
            self.thinking_frame = tk.Frame(header_frame, bg=COLORS['background'])
            self.thinking_frame.pack(pady=(10, 0))
            
            thinking_font = ('Segoe UI', max(12, self.screen_height // 60), 'italic')
            self.thinking_label = tk.Label(
                self.thinking_frame,
                text="",
                font=thinking_font,
                bg=COLORS['background'],
                fg=COLORS['accent']
            )
            self.thinking_label.pack()
    
    def _create_ultra_grid(self):
        """Crée une grille de jeu ultra-moderne avec effets"""
        # Container avec effet de halo et taille adaptée
        grid_container = tk.Frame(
            self.main_frame,
            bg=COLORS['background'],
            relief='solid',
            bd=1
        )
        # Limiter la proportion que prend la grille pour laisser de l'espace aux contrôles
        # Utiliser un pady plus grand en bas pour réserver plus d'espace pour les contrôles
        # Ajuster le centrage vertical selon le mode de jeu pour garantir un alignement identique
        top_padding = 40 if self.game_mode == 'pvp' else 10  # Plus d'espace en haut pour PvP
        grid_container.pack(expand=True, fill='both', pady=(top_padding, 50), padx=20)
        
        # Configuration de la taille de la grille
        grid_size = min(self.screen_width // 4, self.screen_height // 4)
        if self.game_mode == 'pvp':
            grid_size = int(grid_size * 1.05)
            
        square_container = tk.Frame(
            grid_container,
            bg=COLORS['background'],
            width=grid_size,
            height=grid_size
        )
        square_container.pack(expand=True, padx=20, pady=20)
        
        square_container.pack_propagate(False)
        
        self.game_frame = tk.Frame(
            square_container,
            bg=COLORS['background_tertiary'],
            relief='solid',
            bd=4
        )
        self.game_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Calcul des dimensions adaptatives
        screen_min_dimension = min(self.screen_width, self.screen_height)
        base_size = screen_min_dimension // 12
        button_size = min(120, max(60, base_size))
        padding = max(4, button_size // 15)
        
        font_size = max(20, button_size // 4)
        game_font = ('Segoe UI', font_size, 'bold')
        
        # Créer les boutons avec effets avancés
        self.buttons = []
        for i in range(3):
            button_row = []
            for j in range(3):
                button = self._create_ultra_button(
                    self.game_frame, i, j, game_font, button_size, padding
                )
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Configuration responsive
        for i in range(3):
            self.game_frame.grid_rowconfigure(i, weight=1)
            self.game_frame.grid_columnconfigure(i, weight=1)
    
    def _create_ultra_button(self, parent, row, col, font, size, padding):
        """Crée un bouton ultra-moderne avec effets visuels"""
        char_width = min(7, max(3, size // 12))
        char_height = min(3, max(1, size // 25))
        
        button = tk.Button(
            parent,
            text="",
            font=font,
            width=char_width,
            height=char_height,
            bg=COLORS['button_normal'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['button_active'],
            relief='raised',
            bd=3,
            cursor='hand2',
            command=lambda: self._on_ultra_button_click(row, col)
        )
        
        button.grid(row=row, column=col, padx=padding, pady=padding, sticky='nsew')
        
        # Effets visuels avancés
        self._add_ultra_button_effects(button, row, col)
        
        return button
    
    def _add_ultra_button_effects(self, button, row, col):
        """Ajoute des effets visuels avancés aux boutons"""
        original_bg = COLORS['button_normal']
        hover_bg = COLORS['button_hover']
        
        def on_enter(e):
            if button['state'] != 'disabled':
                button.config(
                    bg=hover_bg,
                    relief='solid',
                    bd=4
                )
                self._animate_button_glow(button, True)
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button.config(
                    bg=original_bg,
                    relief='raised',
                    bd=3
                )
                self._animate_button_glow(button, False)
        
        def on_click(e):
            if button['state'] != 'disabled':
                self._animate_button_click(button)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        button.bind('<Button-1>', on_click)
        
        # Stocker l'état du bouton pour les animations
        self.button_effects[f"{row},{col}"] = {
            'button': button,
            'glowing': False,
            'original_bg': original_bg,
            'hover_bg': hover_bg
        }
    
    def _animate_button_glow(self, button, glow_on):
        """Anime un effet de halo sur le bouton"""
        if glow_on:
            # Simuler un effet de halo avec changement de relief
            button.config(relief='solid', bd=4)
        else:
            button.config(relief='raised', bd=3)
    
    def _animate_button_click(self, button):
        """Anime le clic du bouton"""
        original_relief = button['relief']
        button.config(relief='sunken')
        self.master.after(100, lambda: button.config(relief=original_relief))
    
    def _create_enhanced_controls(self):
        """Crée des contrôles améliorés avec animations - seulement le tableau de score"""
        # Frame principal des contrôles
        control_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        control_frame.pack(side='bottom', fill='x', pady=(10, 30))
        
        # Tableau des scores avec effet visuel attractif
        score_container = tk.Frame(
            control_frame,
            bg=COLORS['background_secondary'],
            relief='ridge',
            bd=2,
            # Assurer une largeur minimale pour éviter la compression
            width=max(300, self.screen_width * 0.25)
        )
        # Empêcher le redimensionnement pour maintenir la largeur minimale
        score_container.pack_propagate(False)
        score_container.pack(pady=10, padx=20)
        
        # Titre pour le score
        score_title = tk.Label(
            score_container,
            text="🏆 TABLEAU DES SCORES 🏆",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['background_secondary'],
            fg=COLORS['text_primary']
        )
        score_title.pack(pady=5)
        
        # Créer un conteneur pour les scores avec espacement fixe
        score_display = tk.Frame(score_container, bg=COLORS['background_secondary'])
        score_display.pack(pady=5, fill='x', expand=True)
        
        # Ajuster la taille de la police
        scores = self.game_logic.get_scores()
        score_font_size = min(18, max(14, self.screen_height // 60))
        score_font = ('Segoe UI', score_font_size, 'bold')
        
        # Zone X
        x_frame = tk.Frame(score_display, bg="#FF5555", padx=10, pady=5)
        # Utiliser un conteneur flexible pour bien positionner les frames X et O
        x_frame.pack(side=tk.LEFT, padx=15, fill='both')
        
        self.x_label = tk.Label(
            x_frame,
            text=f"X: {scores['X']}",
            font=score_font,
            bg="#FF5555",
            fg="white",
            width=5,  # Largeur fixe pour éviter la compression
            padx=10
        )
        self.x_label.pack()
        
        # Séparateur
        separator = tk.Label(
            score_display,
            text="|",
            font=score_font,
            bg=COLORS['background_secondary'],
            fg=COLORS['text_primary'],
            padx=10
        )
        separator.pack(side=tk.LEFT)
        
        # Zone O
        o_frame = tk.Frame(score_display, bg="#5555FF", padx=10, pady=5)
        o_frame.pack(side=tk.LEFT, padx=15, fill='both')
        
        self.o_label = tk.Label(
            o_frame,
            text=f"O: {scores['O']}",
            font=score_font,
            bg="#5555FF",
            fg="white",
            width=5,  # Largeur fixe pour éviter la compression
            padx=10
        )
        self.o_label.pack()
        
        # Les références sont déjà stockées en tant que self.x_label et self.o_label
        
        # Stocker aussi une référence compatible avec le code existant
        self.score_label = score_title  # Fallback uniquement
        
        # Les boutons de contrôle ne sont plus créés ici - uniquement dans le panneau inférieur
    
    def _create_ultra_control_buttons(self, parent):
        """Crée des boutons de contrôle ultra-modernes - FONCTION CONSERVÉE UNIQUEMENT POUR COMPATIBILITÉ"""
        # Cette fonction n'est plus utilisée activement pour éviter les boutons en double
        # Les boutons sont maintenant uniquement dans le panneau de contrôle inférieur
        pass
    
    def _create_modern_control_button(self, parent, text, command, font, bg_color, hover_color):
        """Crée un bouton de contrôle moderne avec effets"""
        button = tk.Button(
            parent,
            text=text,
            font=font,
            bg=bg_color,
            fg='white',
            activebackground=hover_color,
            activeforeground='white',
            relief='raised',
            bd=2,
            cursor='hand2',
            command=command,
            padx=10,
            pady=5,
            width=8  # Largeur réduite pour tous les boutons
        )
        
        # Effets de survol
        def on_enter(e):
            button.config(bg=hover_color, relief='solid', bd=4)
        
        def on_leave(e):
            button.config(bg=bg_color, relief='raised', bd=3)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button
    
    
    def _on_ultra_button_click(self, row, col):
        """Gestionnaire de clic avec effets visuels"""
        if self.ai_thinking:
            return  # Empêcher les clics pendant que l'IA réfléchit
            
        result = self.game_logic.make_move(row, col)
        
        if not result['valid']:
            self._animate_invalid_move(self.buttons[row][col])
            return
        
        # Animation de placement du symbole
        self._animate_symbol_placement(row, col, result['player_who_played'])
        
        if result['game_over']:
            if result['winner']:
                self._handle_victory(result['winner'])
            else:
                self._handle_draw()
        else:
            self._update_player_display()
            
            # Si c'est le tour de l'IA
            if self.game_logic.is_ai_turn():
                self.master.after(500, self._handle_ai_turn)
    
    def _animate_symbol_placement(self, row, col, symbol):
        """Anime le placement d'un symbole"""
        button = self.buttons[row][col]
        
        # Effet de flash
        original_bg = button['bg']
        flash_color = COLORS['winning_highlight']
        
        def flash_sequence():
            colors = [flash_color, original_bg, flash_color, original_bg]
            for i, color in enumerate(colors):
                self.master.after(i * 100, lambda c=color: button.config(bg=c))
        
        flash_sequence()
        
        # Placer le symbole avec style
        symbol_color = COLORS['text_secondary'] if symbol == 'X' else COLORS['text_player_o']
        self.master.after(400, lambda: button.config(
            text=symbol,
            fg=symbol_color,
            state='disabled',
            bg=COLORS['button_active']
        ))
    
    def _animate_invalid_move(self, button):
        """Anime un mouvement invalide"""
        original_bg = button['bg']
        error_color = COLORS['button_quit']
        
        def shake_effect():
            positions = [2, -2, 1, -1, 0]
            for i, offset in enumerate(positions):
                self.master.after(i * 50, lambda: None)  # Simpler shake
        
        # Flash rouge
        button.config(bg=error_color)
        self.master.after(200, lambda: button.config(bg=original_bg))
        shake_effect()
    
    def _handle_ai_turn(self):
        """Gère le tour de l'IA avec animations"""
        if self.game_mode != 'ai' or self.game_logic.is_game_over():
            return
            
        # Vérifier si c'est le tour de l'IA (joueur O)
        if self.game_logic.current_player != 'O':
            return
        
        self.ai_thinking = True
        self._start_thinking_animation()
        
        # Obtenir le temps de réflexion selon le niveau
        thinking_times = {'easy': 0.5, 'medium': 1.0, 'hard': 2.0}
        thinking_time = thinking_times.get(self.ai_level, 1.0)
        
        def make_ai_move():
            self._stop_thinking_animation()
            self.ai_thinking = False
            
            # Obtenir le coup de l'IA
            board_state = [['', '', ''], ['', '', ''], ['', '', '']]
            for i in range(3):
                for j in range(3):
                    if hasattr(self, 'buttons') and len(self.buttons) > i and len(self.buttons[i]) > j:
                        button_text = self.buttons[i][j]['text']
                        if button_text in ['X', 'O']:
                            board_state[i][j] = button_text
            
            if hasattr(self, 'ai_player'):
                move = self.ai_player.get_move(board_state)
                if move:
                    row, col = move
                    self._on_ultra_button_click(row, col)
        
        # Attendre le temps de réflexion
        self.master.after(int(thinking_time * 1000), make_ai_move)
    
    def _start_thinking_animation(self):
        """Démarre l'animation de réflexion de l'IA"""
        if hasattr(self, 'thinking_label'):
            self.thinking_label.config(text="🤖 L'IA réfléchit...")
            self._animate_thinking_dots()
    
    def _animate_thinking_dots(self):
        """Anime les points de réflexion"""
        if not self.ai_thinking or not hasattr(self, 'thinking_label'):
            return
        
        dots = [".", "..", "...", ""]
        current_time = int(time.time() * 2) % len(dots)
        
        if self.thinking_label.winfo_exists():
            self.thinking_label.config(text=f"🤖 L'IA réfléchit{dots[current_time]}")
            self.master.after(250, self._animate_thinking_dots)
    
    def _stop_thinking_animation(self):
        """Arrête l'animation de réflexion"""
        if hasattr(self, 'thinking_label') and self.thinking_label.winfo_exists():
            self.thinking_label.config(text="")
    
    def _update_player_display(self):
        """Met à jour l'affichage du joueur actuel avec animation"""
        current_player = self.game_logic.get_current_player()
        
        # Vérifier si c'est au tour de l'IA
        if self.game_mode == 'ai' and current_player == 'O':
            # Mettre à jour l'affichage pour indiquer que c'est au tour de l'IA
            player_text = "🤖 Tour de l'IA (O)"
            player_color = COLORS['text_player_o']
            
            # Désactiver tous les boutons pendant que l'IA réfléchit
            self._disable_all_buttons()
            
            # Lancer automatiquement le tour de l'IA après un court délai
            # si le jeu n'est pas terminé et que l'IA ne réfléchit pas déjà
            if not self.game_logic.is_game_over() and not self.ai_thinking:
                self.master.after(500, self._handle_ai_turn)
        else:
            # Réactiver les boutons pour le joueur humain
            self._enable_valid_buttons()
            
            player_symbol = "🔴" if current_player == 'X' else "🔵"
            player_text = f"{player_symbol} Tour du joueur: {current_player} {player_symbol}"
            player_color = COLORS['text_secondary'] if current_player == 'X' else COLORS['text_player_o']
        
        # Animation de changement
        self._animate_label_change(self.player_label, player_text, player_color)
    
    def _animate_label_change(self, label, new_text, new_color):
        """Anime le changement d'un label"""
        def fade_out():
            label.config(fg=COLORS['background'])
        
        def fade_in():
            label.config(text=new_text, fg=new_color)
        
        fade_out()
        self.master.after(150, fade_in)
    
    def _handle_victory(self, winner):
        """Gère une victoire avec effets spéciaux"""
        self._highlight_winning_line()
        self._animate_victory_celebration()
        self._update_score_display()
        
        # Message de victoire personnalisé
        if self.game_mode == 'ai':
            if winner == 'X':
                message = "🎉 Félicitations ! Vous avez battu l'IA !"
            else:
                message = "🤖 L'IA a gagné ! Essayez encore !"
        else:
            message = f"🎉 Victoire du joueur {winner} !"
        
        self.master.after(1500, lambda: messagebox.showinfo("Victoire !", message))
    
    def _animate_victory_celebration(self):
        """Anime une célébration de victoire"""
        # Faire clignoter le titre
        original_color = self.title_label['fg']
        celebration_color = COLORS['winning_highlight']
        
        def flash_title():
            colors = [celebration_color, original_color] * 5
            for i, color in enumerate(colors):
                self.master.after(i * 200, lambda c=color: self.title_label.config(fg=c))
        
        flash_title()
    
    def _highlight_winning_line(self):
        """Met en surbrillance la ligne gagnante avec animation"""
        winning_positions = get_winning_positions(self.game_logic.get_board())
        if winning_positions:
            for row, col in winning_positions:
                button = self.buttons[row][col]
                self._animate_winning_cell(button)
    
    def _animate_winning_cell(self, button):
        """Anime une cellule gagnante"""
        original_bg = button['bg']
        highlight_color = COLORS['winning_highlight']
        
        def pulse_effect():
            colors = [highlight_color, original_bg] * 8
            for i, color in enumerate(colors):
                self.master.after(i * 150, lambda c=color: button.config(bg=c) if button.winfo_exists() else None)
        
        pulse_effect()
    
    def _handle_draw(self):
        """Gère une égalité"""
        messagebox.showinfo("Égalité", "Match nul ! Bien joué à tous les deux !")
    
    def _update_score_display(self):
        """Met à jour l'affichage des scores avec animation"""
        scores = self.game_logic.get_scores()
        
        # Mettre à jour les labels X et O du tableau principal
        if hasattr(self, 'x_label') and hasattr(self, 'o_label'):
            def blink_main_labels(count=0):
                if count >= 6:  # 3 clignotements complets
                    if hasattr(self, 'x_label'):
                        self.x_label.config(text=f"X: {scores['X']}", fg="white")
                    if hasattr(self, 'o_label'):
                        self.o_label.config(text=f"O: {scores['O']}", fg="white")
                    return
                
                # Alterner entre normal et highlight
                if count % 2 == 0:
                    if hasattr(self, 'x_label'):
                        self.x_label.config(fg="yellow")
                    if hasattr(self, 'o_label'):
                        self.o_label.config(fg="yellow")
                else:
                    if hasattr(self, 'x_label'):
                        self.x_label.config(fg="white")
                    if hasattr(self, 'o_label'):
                        self.o_label.config(fg="white")
                
                self.master.after(200, lambda: blink_main_labels(count + 1))
            
            # Mettre à jour les labels principaux
            self.x_label.config(text=f"X: {scores['X']}")
            self.o_label.config(text=f"O: {scores['O']}")
            blink_main_labels()
            
        # Mettre à jour les scores X et O du panneau du bas avec animation
        def update_bottom_scores():
            if hasattr(self, 'bottom_score_x_label') and hasattr(self, 'bottom_score_o_label'):
                def blink_bottom_score(count=0):
                    if count >= 6:  # 3 clignotements complets
                        if hasattr(self, 'bottom_score_x_label'):
                            self.bottom_score_x_label.config(text=f"X: {scores['X']}", fg="white")
                        if hasattr(self, 'bottom_score_o_label'):
                            self.bottom_score_o_label.config(text=f"O: {scores['O']}", fg="white")
                        return
                    
                    # Alterner entre normal et highlight pour les deux labels
                    if count % 2 == 0:
                        if hasattr(self, 'bottom_score_x_label'):
                            self.bottom_score_x_label.config(fg="yellow")
                        if hasattr(self, 'bottom_score_o_label'):
                            self.bottom_score_o_label.config(fg="yellow")
                    else:
                        if hasattr(self, 'bottom_score_x_label'):
                            self.bottom_score_x_label.config(fg="white")
                        if hasattr(self, 'bottom_score_o_label'):
                            self.bottom_score_o_label.config(fg="white")
                    
                    # Continuer l'animation
                    if self.master:
                        self.master.after(200, lambda: blink_bottom_score(count + 1))
                
                # Mettre à jour les textes
                if hasattr(self, 'bottom_score_x_label'):
                    self.bottom_score_x_label.config(text=f"X: {scores['X']}")
                if hasattr(self, 'bottom_score_o_label'):
                    self.bottom_score_o_label.config(text=f"O: {scores['O']}")
                
                # Lancer l'animation
                blink_bottom_score()
        
        # Lancer la mise à jour du panneau du bas
        update_bottom_scores()
    
    def _start_all_animations(self):
        """Démarre toutes les animations d'arrière-plan"""
        self.animation_running = True
        self._animate_background_particles()
        self._animate_title_glow()
    
    def _animate_background_particles(self):
        """Anime les particules d'arrière-plan"""
        if not self.animation_running or not self.canvas.winfo_exists():
            return
        
        for particle in self.particles:
            # Déplacer
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Rebonds
            if particle['x'] <= 0 or particle['x'] >= self.screen_width:
                particle['speed_x'] *= -1
            if particle['y'] <= 0 or particle['y'] >= self.screen_height:
                particle['speed_y'] *= -1
            
            # Limites
            particle['x'] = max(0, min(self.screen_width, particle['x']))
            particle['y'] = max(0, min(self.screen_height, particle['y']))
            
            # Mettre à jour
            try:
                self.canvas.coords(
                    particle['id'],
                    particle['x'], particle['y'],
                    particle['x'] + particle['size'], particle['y'] + particle['size']
                )
            except:
                pass
        
        self.master.after(50, self._animate_background_particles)
    
    def _animate_title_glow(self):
        """Anime un effet de lueur sur le titre"""
        if not self.animation_running:
            return
        
        # Effet subtil de pulsation
        current_time = time.time()
        # Pas d'effet visible pour ne pas être distrayant
        
        self.master.after(500, self._animate_title_glow)
    
    def _on_restart_click(self):
        """Redémarre le jeu avec animation"""
        self.game_logic.restart_game()
        self._reset_ui_with_animation()
        
        # Si l'IA commence
        if self.game_logic.is_ai_turn():
            self.master.after(1000, self._handle_ai_turn)
    
    def _reset_ui_with_animation(self):
        """Remet l'interface à zéro avec animation"""
        # Animation de nettoyage
        for i in range(3):
            for j in range(3):
                button = self.buttons[i][j]
                self._animate_button_reset(button, i * 3 + j)
        
        # Mettre à jour l'affichage du joueur
        self.master.after(500, self._update_player_display)
    
    def _animate_button_reset(self, button, delay_index):
        """Anime la remise à zéro d'un bouton"""
        def reset_button():
            button.config(
                text="",
                state='normal',
                bg=COLORS['button_normal'],
                fg=COLORS['text_primary'],
                relief='raised'
            )
            
            # Réactiver les effets
            if button.winfo_exists():
                # Flash de reset
                flash_color = COLORS['accent_secondary']
                button.config(bg=flash_color)
                self.master.after(100, lambda: button.config(bg=COLORS['button_normal']))
        
        # Délai échelonné pour un effet en cascade
        self.master.after(delay_index * 100, reset_button)
    
    def _on_reset_score_click(self):
        """Remet les scores à zéro avec animation"""
        self.game_logic.reset_scores()
        self._update_score_display()
    
    def _return_to_menu(self, event=None):
        """Retourne au menu principal de manière robuste"""
        print("↩️ Retour au menu principal (ModernUI)...")
        
        # Vérifier qu'on a un callback valide
        if not hasattr(self, 'on_return_menu') or self.on_return_menu is None:
            print("❌ Aucun callback de retour au menu n'est défini!")
            return
        
        # Désactiver les boutons pour éviter les doubles clics
        if hasattr(self, 'bottom_menu_button'):
            self.bottom_menu_button.config(state='disabled')
            
        # Arrêter toutes les animations immédiatement
        self.animation_running = False
        
        # Annuler toutes les tâches en attente pour éviter les conflits
        if self.master:
            try:
                for task_id in self.master.tk.call('after', 'info'):
                    try:
                        self.master.after_cancel(task_id)
                    except:
                        pass
            except:
                pass  # Ignorer les erreurs potentielles
        
        # Capturer les références nécessaires
        callback = self.on_return_menu
        master = self.master
        
        # Vérification de sécurité
        if not master:
            print("⚠️ Master est None, appel direct du callback...")
            callback()
            return
            
        print("✓ Préparation du retour au menu...")
        
        # Méthode de retour au menu optimisée
        def execute_return():
            # 1. Cacher la fenêtre immédiatement pour feedback visuel
            try:
                if master and master.winfo_exists():
                    master.withdraw()
            except:
                pass
                
            # 2. Appeler le callback pour créer le menu
            print("✓ Appel du callback de menu...")
            callback()
            
            # 3. Détruire la fenêtre de jeu après un court délai
            def final_cleanup():
                try:
                    if master and master.winfo_exists():
                        master.destroy()
                        print("✓ Fenêtre de jeu détruite avec succès")
                except Exception as e:
                    print(f"Note: Fenêtre déjà fermée: {e}")
            
            # Utiliser un timer indépendant pour la destruction finale
            import threading
            threading.Timer(0.5, final_cleanup).start()
        
        # Utiliser after_idle pour s'assurer que les événements Tk en cours sont traités
        if master:
            master.after_idle(execute_return)
    
    def _toggle_fullscreen(self, event=None):
        """Bascule le plein écran (bien que déjà en plein écran)"""
        self.is_fullscreen = not self.is_fullscreen
        self.master.attributes('-fullscreen', self.is_fullscreen)
    
    def _quit_game(self):
        """Quitte le jeu proprement"""
        print("🚪 Fermeture du jeu...")
        
        # Arrêter les animations
        self.animation_running = False
        
        # Annuler toutes les tâches en attente
        if self.master:
            for task_id in self.master.tk.call('after', 'info'):
                try:
                    self.master.after_cancel(task_id)
                except:
                    pass
        
        # Fermer la fenêtre
        try:
            if self.master and self.master.winfo_exists():
                self.master.destroy()
                sys.exit(0)  # Assurer la fermeture complète
        except Exception as e:
            print(f"Erreur lors de la fermeture: {e}")
            sys.exit(1)  # Forcer la fermeture
    
    def _disable_all_buttons(self):
        """Désactive tous les boutons de la grille pour empêcher le joueur de jouer pendant le tour de l'IA"""
        for i in range(3):
            for j in range(3):
                if hasattr(self, 'buttons') and len(self.buttons) > i and len(self.buttons[i]) > j:
                    self.buttons[i][j].config(state='disabled')
    
    def _enable_valid_buttons(self):
        """Active uniquement les boutons correspondant à des cases vides"""
        for i in range(3):
            for j in range(3):
                if hasattr(self, 'buttons') and len(self.buttons) > i and len(self.buttons[i]) > j:
                    button = self.buttons[i][j]
                    # N'activer que les boutons vides
                    if button['text'] not in ['X', 'O']:
                        button.config(state='normal')
    
    def _create_bottom_control_panel(self):
        """Crée un panneau de contrôle fixe en bas de l'écran, toujours visible"""
        # Frame pour le panneau de contrôle en position absolue
        bottom_panel = tk.Frame(
            self.master,  # Attaché directement à la fenêtre principale
            bg=COLORS['background_secondary'],
            relief='raised',
            bd=2,
            height=60  # Hauteur fixe
        )
        # Positionner le panneau en bas de l'écran
        bottom_panel.place(x=0, y=self.screen_height-60, width=self.screen_width, height=60)
        
        # S'assurer que le panneau est au premier plan
        bottom_panel.lift()
        
        # Ajouter un raccourci texte au centre
        shortcuts_label = tk.Label(
            bottom_panel,
            text="💡 Échap: Menu • F11: Plein écran • Interface moderne",
            font=('Segoe UI', 10, 'normal'),
            bg=COLORS['background_secondary'],
            fg=COLORS['accent']
        )
        shortcuts_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Zone des scores
        score_frame = tk.Frame(bottom_panel, bg=COLORS['background_secondary'], width=250)
        score_frame.pack_propagate(False)  # Empêcher le redimensionnement 
        score_frame.pack(side=tk.LEFT, padx=20, fill='y')
        
        scores = self.game_logic.get_scores()
        score_text = f"Score  X: {scores['X']}  |  O: {scores['O']}"
        
        # Labels de score séparés et plus visibles
        score_prefix = tk.Label(
            score_frame,
            text="Score",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['background_secondary'],
            fg=COLORS['text_primary'],
            padx=5,
            pady=5
        )
        score_prefix.pack(side=tk.LEFT)
        
        # X avec couleur distinctive
        score_x_frame = tk.Frame(score_frame, bg="#FF5555", padx=5, pady=3)
        score_x_frame.pack(side=tk.LEFT, padx=10)
        
        score_x_label = tk.Label(
            score_x_frame,
            text=f"X: {scores['X']}",
            font=('Segoe UI', 14, 'bold'),
            bg="#FF5555",
            fg='white',
            padx=8
        )
        score_x_label.pack()
        
        # Séparateur
        separator = tk.Label(
            score_frame,
            text="|",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['background_secondary'],
            fg=COLORS['text_primary'],
            padx=5
        )
        separator.pack(side=tk.LEFT)
        
        # O avec couleur distinctive
        score_o_frame = tk.Frame(score_frame, bg="#5555FF", padx=5, pady=3)
        score_o_frame.pack(side=tk.LEFT, padx=10)
        
        score_o_label = tk.Label(
            score_o_frame,
            text=f"O: {scores['O']}",
            font=('Segoe UI', 14, 'bold'),
            bg="#5555FF",
            fg='white',
            padx=8
        )
        score_o_label.pack()
        
        # Stocker les références aux labels pour mise à jour future
        self.bottom_score_x_label = score_x_label
        self.bottom_score_o_label = score_o_label
        
        # Nous avons déjà stocké les références aux labels X et O
        
        # Zone des boutons centrés
        button_frame = tk.Frame(bottom_panel, bg=COLORS['background_secondary'])
        button_frame.pack(side=tk.RIGHT, padx=20, fill='y')
        
        # Taille de police adaptée
        button_font = ('Segoe UI', 11, 'bold')
        
        # Boutons avec espacement uniforme
        self.bottom_replay_button = tk.Button(
            button_frame,
            text="🔄 REJOUER",
            font=button_font,
            bg=COLORS['button_replay'],
            fg='white',
            activebackground=COLORS['button_replay_hover'],
            command=self._on_restart_click,
            padx=8,
            pady=3,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.bottom_replay_button.pack(side=tk.LEFT, padx=5)
        
        self.bottom_reset_button = tk.Button(
            button_frame,
            text="🔄 RESET",
            font=button_font,
            bg=COLORS['button_reset'],
            fg='white',
            activebackground=COLORS['button_reset_hover'],
            command=self._on_reset_score_click,
            padx=8,
            pady=3,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.bottom_reset_button.pack(side=tk.LEFT, padx=5)
        
        self.bottom_menu_button = tk.Button(
            button_frame,
            text="🏠 MENU",
            font=button_font,
            bg=COLORS['button_fullscreen'],
            fg='white',
            activebackground=COLORS['button_fullscreen_hover'],
            command=self._return_to_menu,
            padx=8,
            pady=3,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.bottom_menu_button.pack(side=tk.LEFT, padx=5)
        
        self.bottom_quit_button = tk.Button(
            button_frame,
            text="❌ QUITTER",
            font=button_font,
            bg=COLORS['button_quit'],
            fg='white',
            activebackground=COLORS['button_quit_hover'],
            command=self._quit_game,
            padx=8,
            pady=3,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.bottom_quit_button.pack(side=tk.LEFT, padx=5)
