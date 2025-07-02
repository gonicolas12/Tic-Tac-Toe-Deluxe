"""
Interface utilisateur pour le jeu Tic Tac Toe
"""

import tkinter as tk
from tkinter import messagebox
from config.settings import (WINDOW_CONFIG, COLORS, GRID_CONFIG, 
                           MESSAGES, FONTS)
from .utils import get_winning_positions

class GameUI:
    """Classe gérant l'interface utilisateur du jeu"""
    
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.window = None
        self.buttons = []
        self.player_label = None
        self.score_label = None
        self.game_frame = None
        
    def setup_window(self):
        """Configure la fenêtre principale de manière responsive"""
        self.window = tk.Tk()
        self.window.title(WINDOW_CONFIG['title'])
        
        # Obtenir les dimensions de l'écran
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculer la taille de la fenêtre en fonction de l'écran
        window_width = min(
            int(screen_width * WINDOW_CONFIG['default_width_ratio']),
            WINDOW_CONFIG['max_width']
        )
        window_height = min(
            int(screen_height * WINDOW_CONFIG['default_height_ratio']),
            WINDOW_CONFIG['max_height']
        )
        
        # S'assurer que la fenêtre n'est pas trop petite
        window_width = max(window_width, WINDOW_CONFIG['min_width'])
        window_height = max(window_height, WINDOW_CONFIG['min_height'])
        
        self.window.geometry(f"{window_width}x{window_height}")
        self.window.configure(bg=COLORS['background'])
        self.window.resizable(WINDOW_CONFIG['resizable'], WINDOW_CONFIG['resizable'])
        self.window.minsize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
        
        # Centrer la fenêtre sur l'écran
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Gestion simple et directe du plein écran
        self.window.bind('<Key>', self._on_key_event)
        self.window.bind('<KeyPress>', self._on_key_event)
        self.window.bind('<KeyRelease>', self._on_key_event)
        
        self.window.bind('<Configure>', self._on_window_resize)
        
        # S'assurer que la fenêtre peut recevoir les événements clavier
        self.window.focus_set()
        
        # Rendre la fenêtre focusable en permanence
        self.window.bind('<Button-1>', lambda e: self.window.focus_set())
        
        # Activer la capture universelle des touches
        self.window.bind_all('<Key>', self._on_universal_key)
        
        self.is_fullscreen = False
        
        # Stocker les dimensions pour les calculs responsives
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def setup_ui(self):
        """Configure tous les éléments de l'interface"""
        # Créer le frame principal avec gradient
        self.main_frame = tk.Frame(self.window, bg=COLORS['background'])
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self._create_header()
        self._create_game_grid()
        self._create_control_panel()
        self._create_footer()
        
        # S'assurer que le focus clavier est bien configuré après création de l'UI
        self.window.after(100, self._ensure_keyboard_focus)
        
    def _create_header(self):
        """Crée l'en-tête avec titre et informations du joueur"""
        header_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        header_frame.pack(fill='x', pady=(0, 15))  # Padding réduit
        
        # Titre principal (plus petit)
        self.title_label = tk.Label(
            header_frame,
            text="✨ TIC TAC TOE DELUXE ✨",
            font=self._get_font('title'),
            bg=COLORS['background'],
            fg=COLORS['text_primary']
        )
        self.title_label.pack(pady=(0, 15))  # Padding réduit, sous-titre supprimé
        
        # Informations du joueur actuel
        player_frame = tk.Frame(header_frame, bg=COLORS['background_secondary'], relief='raised', bd=2)
        player_frame.pack(pady=8)  # Padding réduit
        
        self.player_label = tk.Label(
            player_frame,
            text=f"🔴 Tour du joueur: {self.game_logic.get_current_player()} 🔴",
            font=self._get_font('player_label'),
            bg=COLORS['background_secondary'],
            fg=COLORS['text_secondary'],
            padx=16,  # Padding réduit
            pady=8   # Padding réduit
        )
        self.player_label.pack()
        
    def _create_game_grid(self):
        """Crée la grille de jeu avec style moderne et responsive"""
        # Container pour centrer la grille parfaitement
        self.grid_container = tk.Frame(self.main_frame, bg=COLORS['background'])
        self.grid_container.pack(expand=True, fill='both', pady=10)
        
        # Frame de la grille avec bordure stylée - centré avec pack
        self.game_frame = tk.Frame(
            self.grid_container, 
            bg=COLORS['background_tertiary'],
            relief='raised',
            bd=3
        )
        # Utiliser pack au lieu de grid pour le centrage
        self.game_frame.pack(expand=False, anchor='center')
        
        # Initialiser la liste des boutons
        self.buttons = []
        
        # Créer directement les boutons
        self._create_grid_buttons_simple()
        
    def _create_grid_buttons_simple(self):
        """Crée les boutons de la grille de manière simple et fiable"""
        # Calculer la taille des boutons
        button_size = self._calculate_button_size()
        padding = max(3, int(button_size * GRID_CONFIG['button_padding_ratio']))
        
        # Convertir en taille de caractères
        char_width = max(3, button_size // 12)
        char_height = max(2, button_size // 19)
        
        # Taille de police
        font_size = max(13, button_size // 5.5)
        game_font = ('Segoe UI', int(font_size), 'bold')
        
        # Vider la liste des boutons
        self.buttons = []
        
        # Créer les boutons ligne par ligne
        for i in range(3):  # 3 lignes
            button_row = []
            for j in range(3):  # 3 colonnes
                button = tk.Button(
                    self.game_frame,
                    text="",
                    font=game_font,
                    width=char_width,
                    height=char_height,
                    bg=COLORS['button_normal'],
                    fg=COLORS['text_primary'],
                    activebackground=COLORS['button_active'],
                    relief='raised',
                    bd=2,
                    command=lambda row=i, col=j: self._on_button_click(row, col),
                    cursor='hand2'
                )
                
                # Positionner le bouton dans la grille
                button.grid(row=i, column=j, padx=padding, pady=padding, sticky='nsew')
                
                # Ajouter les effets hover
                button.bind('<Enter>', lambda e, b=button: self._on_button_hover(b, True))
                button.bind('<Leave>', lambda e, b=button: self._on_button_hover(b, False))
                
                button_row.append(button)
            
            self.buttons.append(button_row)
        
        # Configurer le redimensionnement uniforme
        for i in range(3):
            self.game_frame.grid_rowconfigure(i, weight=1)
            self.game_frame.grid_columnconfigure(i, weight=1)
            
    def _create_control_panel(self):
        """Crée le panneau de contrôle avec scores et boutons"""
        control_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        control_frame.pack(side='bottom', fill='x', pady=(15, 0))
        
        # Affichage des scores dans un cadre stylé
        score_frame = tk.Frame(
            control_frame, 
            bg=COLORS['background_secondary'],
            relief='raised',
            bd=3
        )
        score_frame.pack(pady=10)
        
        scores = self.game_logic.get_scores()
        self.score_label = tk.Label(
            score_frame,
            text=MESSAGES['score'].format(score_x=scores['X'], score_o=scores['O']),
            font=self._get_font('score'),
            bg=COLORS['background_secondary'],
            fg=COLORS['text_primary'],
            padx=20,
            pady=8
        )
        self.score_label.pack()
        
        # Boutons de contrôle
        self._create_control_buttons(control_frame)
        
    def _create_control_buttons(self, parent):
        """Crée les boutons de contrôle avec taille adaptative et icônes centrées"""
        button_frame = tk.Frame(parent, bg=COLORS['background'])
        button_frame.pack(pady=10)
        
        button_font = self._get_font('button_control')
        button_padding_x = max(10, self.window.winfo_width() // 90)  # Padding réduit
        button_padding_y = max(4, self.window.winfo_height() // 140)  # Padding réduit
        
        # Bouton Rejouer (style principal) avec icône plus centrée
        self.replay_button = tk.Button(
            button_frame,
            text="🔄  Rejouer",  # Espacement ajouté entre icône et texte
            font=button_font,
            bg=COLORS['button_replay'],
            fg='white',
            activebackground=COLORS['button_replay_hover'],
            padx=button_padding_x,
            pady=button_padding_y,
            relief='raised',
            bd=3,
            cursor='hand2',
            command=self._on_restart_click
        )
        self.replay_button.pack(side=tk.LEFT, padx=6)
        
        # Bouton Reset Score avec icône plus centrée
        self.reset_score_button = tk.Button(
            button_frame,
            text="🔄  Reset Score",  # Espacement ajouté
            font=button_font,
            bg=COLORS['button_reset'],
            fg='white',
            activebackground=COLORS['button_reset_hover'],
            padx=button_padding_x,
            pady=button_padding_y,
            relief='raised',
            bd=3,
            cursor='hand2',
            command=self._on_reset_score_click
        )
        self.reset_score_button.pack(side=tk.LEFT, padx=6)
        
        # Bouton Plein écran avec icône plus grande et centrée
        self.fullscreen_button = tk.Button(
            button_frame,
            text="🖥️  Plein écran (F11)",  # Espacement ajouté
            font=button_font,
            bg=COLORS['button_fullscreen'],
            fg='white',
            activebackground=COLORS['button_fullscreen_hover'],
            padx=button_padding_x,
            pady=button_padding_y,
            relief='raised',
            bd=3,
            cursor='hand2',
            command=self._toggle_fullscreen
        )
        self.fullscreen_button.pack(side=tk.LEFT, padx=6)
        
        # Bouton Quitter avec icône plus centrée
        self.quit_button = tk.Button(
            button_frame,
            text="❌  Quitter",  # Espacement ajouté
            font=button_font,
            bg=COLORS['button_quit'],
            fg='white',
            activebackground=COLORS['button_quit_hover'],
            padx=button_padding_x,
            pady=button_padding_y,
            relief='raised',
            bd=3,
            cursor='hand2',
            command=self.window.quit
        )
        self.quit_button.pack(side=tk.LEFT, padx=6)
        
    def _create_footer(self):
        """Crée le pied de page avec informations"""
        footer_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        footer_frame.pack(side='bottom', fill='x')
        
        self.info_label = tk.Label(
            footer_frame,
            text="💡 Plein écran: F11 | Alt+Entrée | Ctrl+F • Quitter plein écran: Échap",
            font=self._get_font('info'),
            bg=COLORS['background'],
            fg=COLORS['accent_secondary']
        )
        self.info_label.pack(pady=3)
        
    def _on_button_click(self, row, col):
        """Gestionnaire de clic sur un bouton de la grille"""
        result = self.game_logic.make_move(row, col)
        
        if not result['valid']:
            return
            
        # Mettre à jour l'affichage du bouton avec le bon joueur
        player_who_played = result['player_who_played']
        
        self.buttons[row][col].config(
            text=player_who_played,
            fg=COLORS['text_secondary'] if player_who_played == 'X' else COLORS['text_player_o'],
            state='disabled'
        )
        
        if result['game_over']:
            if result['winner']:
                # Il y a un gagnant
                self._show_victory_message(result['winner'])
                self._highlight_winning_line()
                self._update_score_display()
            else:
                # Match nul
                self._show_draw_message()
        else:
            # Continuer le jeu
            self._update_player_label()
            
    def _show_victory_message(self, winner):
        """Affiche le message de victoire"""
        messagebox.showinfo(
            MESSAGES['victory'],
            MESSAGES['victory_text'].format(player=winner)
        )
        
    def _show_draw_message(self):
        """Affiche le message de match nul"""
        messagebox.showinfo(MESSAGES['draw'], MESSAGES['draw_text'])
        
    def _highlight_winning_line(self):
        """Met en surbrillance la ligne gagnante"""
        winning_positions = get_winning_positions(self.game_logic.get_board())
        if winning_positions:
            for row, col in winning_positions:
                self.buttons[row][col].config(bg=COLORS['winning_highlight'])
                
    def _update_player_label(self):
        """Met à jour l'affichage du joueur actuel avec animation"""
        current_player = self.game_logic.get_current_player()
        player_color = COLORS['text_player_o'] if current_player == 'O' else COLORS['text_secondary']
        player_symbol = "🔵" if current_player == 'O' else "🔴"
        
        self.player_label.config(
            text=f"{player_symbol} Tour du joueur: {current_player} {player_symbol}",
            fg=player_color,
            bg=COLORS['background_secondary']
        )
        
    def _update_score_display(self):
        """Met à jour l'affichage des scores"""
        scores = self.game_logic.get_scores()
        self.score_label.config(
            text=MESSAGES['score'].format(score_x=scores['X'], score_o=scores['O'])
        )
        
    def _on_restart_click(self):
        """Gestionnaire pour redémarrer le jeu"""
        self.game_logic.restart_game()
        self._reset_ui()
        
    def _on_reset_score_click(self):
        """Gestionnaire pour remettre les scores à zéro"""
        self.game_logic.reset_scores()
        self._update_score_display()
        
    def _reset_ui(self):
        """Remet l'interface à l'état initial avec effets"""
        # Réinitialiser les boutons avec animation
        for i in range(GRID_CONFIG['size']):
            for j in range(GRID_CONFIG['size']):
                button = self.buttons[i][j]
                button.config(
                    text="",
                    state='normal',
                    bg=COLORS['button_normal'],
                    fg=COLORS['text_primary']
                )
                # Réactiver les effets hover
                button.bind('<Enter>', lambda e, b=button: self._on_button_hover(b, True))
                button.bind('<Leave>', lambda e, b=button: self._on_button_hover(b, False))
                
        # Mettre à jour le label du joueur
        self._update_player_label()
        
    def _on_button_hover(self, button, entering):
        """Effet hover sur les boutons de la grille"""
        if button['state'] != 'disabled':
            if entering:
                button.config(bg=COLORS['button_hover'])
            else:
                button.config(bg=COLORS['button_normal'])
                
    def _ensure_keyboard_focus(self):
        """S'assurer que la fenêtre peut recevoir les événements clavier"""
        self.window.focus_set()
        self.window.update_idletasks()
        
    def _toggle_fullscreen(self, event=None):
        """Bascule entre plein écran et mode fenêtré"""
        self.is_fullscreen = not self.is_fullscreen
        self.window.attributes('-fullscreen', self.is_fullscreen)
        
        # Forcer la mise à jour après un délai
        self.window.after(200, self._force_complete_update)
        
    def _exit_fullscreen(self, event=None):
        """Quitte le mode plein écran"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.window.attributes('-fullscreen', False)
            
            # Forcer la mise à jour après un délai
            self.window.after(200, self._force_complete_update)
        
    def _force_complete_update(self):
        """Force une mise à jour complète de toute l'interface"""
        try:
            # Mettre à jour les polices
            self._update_fonts()
            
            # Forcer la mise à jour de la géométrie
            self.window.update_idletasks()
            
            # Mettre à jour seulement les propriétés de la grille existante
            if hasattr(self, 'buttons') and self.buttons:
                self._update_grid_size()
                
            # S'assurer du focus
            self.window.focus_set()
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")

    def _force_ui_update(self):
        """Force la mise à jour complète de l'interface"""
        # Mettre à jour les polices
        self._update_fonts()
        
        # Mettre à jour la grille si elle existe
        if hasattr(self, 'buttons') and self.buttons:
            self._update_grid_size()
            
        # S'assurer du focus clavier
        self._ensure_keyboard_focus()
        
    def _calculate_font_size(self, font_config):
        """Calcule la taille de police adaptative"""
        window_height = self.window.winfo_height()
        if window_height <= 1:  # Fenêtre pas encore initialisée
            window_height = WINDOW_CONFIG['min_height']
            
        calculated_size = int(window_height * font_config['size_ratio'])
        return max(font_config['min_size'], min(calculated_size, font_config['max_size']))
    
    def _get_font(self, font_key):
        """Retourne une police avec taille adaptative"""
        font_config = FONTS[font_key]
        size = self._calculate_font_size(font_config)
        return (font_config['family'], size, font_config['weight'])
    
    def _calculate_button_size(self):
        """Calcule la taille des boutons de la grille"""
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        
        if window_width <= 1 or window_height <= 1:
            return GRID_CONFIG['button_min_size']
            
        # Calculer la taille en fonction de l'espace disponible (équilibré)
        available_width = window_width * 0.55  # 55% de la largeur pour la grille (réduit de 60%)
        available_height = window_height * 0.4  # 40% de la hauteur pour la grille (réduit de 45%)
        
        # Taille basée sur l'espace disponible divisé par 3 (grille 3x3)
        size_from_width = available_width // 3
        size_from_height = available_height // 3
        
        # Prendre la plus petite des deux pour que ça rentre
        button_size = min(size_from_width, size_from_height)
        
        # Appliquer les limites min/max
        return max(GRID_CONFIG['button_min_size'], 
                  min(button_size, GRID_CONFIG['button_max_size']))
    
    def _on_window_resize(self, event=None):
        """Gestionnaire de redimensionnement de la fenêtre"""
        if event and event.widget != self.window:
            return
            
        # Utiliser un délai pour éviter les appels multiples rapides
        if hasattr(self, '_resize_timer'):
            self.window.after_cancel(self._resize_timer)
        
        self._resize_timer = self.window.after(100, self._delayed_resize_update)
    
    def _delayed_resize_update(self):
        """Mise à jour différée après redimensionnement"""
        try:
            # Mettre à jour les polices
            self._update_fonts()
            
            # Forcer la géométrie
            self.window.update_idletasks()
            
            # Mettre à jour la grille si elle existe
            if hasattr(self, 'buttons') and self.buttons:
                self._update_grid_size()
                
            # S'assurer du focus clavier
            self.window.focus_set()
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour différée: {e}")
    
    def _update_fonts(self):
        """Met à jour toutes les polices selon la nouvelle taille"""
        if hasattr(self, 'title_label'):
            self.title_label.config(font=self._get_font('title'))
        if hasattr(self, 'player_label'):
            self.player_label.config(font=self._get_font('player_label'))
        if hasattr(self, 'score_label'):
            self.score_label.config(font=self._get_font('score'))
        if hasattr(self, 'info_label'):
            self.info_label.config(font=self._get_font('info'))
            
        # Mettre à jour les boutons de contrôle
        button_font = self._get_font('button_control')
        if hasattr(self, 'replay_button'):
            self.replay_button.config(font=button_font)
        if hasattr(self, 'reset_score_button'):
            self.reset_score_button.config(font=button_font)
        if hasattr(self, 'fullscreen_button'):
            self.fullscreen_button.config(font=button_font)
        if hasattr(self, 'quit_button'):
            self.quit_button.config(font=button_font)
    
    def _update_grid_size(self):
        """Met à jour la taille de la grille existante sans la recréer"""
        if not hasattr(self, 'buttons') or not self.buttons:
            return
            
        # Calculer les nouvelles tailles
        button_size = self._calculate_button_size()
        padding = max(3, int(button_size * GRID_CONFIG['button_padding_ratio']))
        
        # Convertir en taille de caractères
        char_width = max(3, button_size // 12)
        char_height = max(2, button_size // 19)
        
        font_size = max(13, button_size // 5.5)
        game_font = ('Segoe UI', int(font_size), 'bold')
        
        # Mettre à jour chaque bouton existant
        try:
            for i in range(len(self.buttons)):
                for j in range(len(self.buttons[i])):
                    if self.buttons[i][j] and self.buttons[i][j].winfo_exists():
                        self.buttons[i][j].config(
                            width=char_width,
                            height=char_height,
                            font=game_font
                        )
                        # Mettre à jour le padding
                        self.buttons[i][j].grid_configure(padx=padding, pady=padding)
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la grille: {e}")
            # En cas d'erreur, ne pas recréer automatiquement pour éviter les boucles
    
    def run(self):
        """Lance l'application"""
        self.setup_window()
        self.setup_ui()
        self.window.mainloop()
        
    def _on_universal_key(self, event):
        """Gestionnaire universel des touches - capture tout"""
        # Debug désactivé
        # print(f"Touche détectée: {event.keysym} (code: {event.keycode})")
        
        # F11 - codes possibles selon le clavier
        if event.keysym in ['F11'] or event.keycode in [122, 95]:
            self._toggle_fullscreen()
            return "break"
            
        # Échap
        if event.keysym in ['Escape'] or event.keycode in [27]:
            if self.is_fullscreen:
                self._exit_fullscreen()
            return "break"
            
        return None
    
    def _on_key_event(self, event):
        """Gestionnaire secondaire des événements clavier"""
        # Alt + Entrée
        if event.state & 0x20000 and event.keysym == 'Return':  # Alt mask
            self._toggle_fullscreen()
            return "break"
            
        # Ctrl + F
        if event.state & 0x4 and event.keysym.lower() == 'f':  # Ctrl mask
            self._toggle_fullscreen()
            return "break"
            
        return None

    def _on_key_press(self, event):
        """Gestionnaire global des événements clavier pour déboggage et raccourcis"""
        # Debug: afficher la touche pressée (optionnel, à retirer en production)
        # print(f"Touche pressée: {event.keysym}, Code: {event.keycode}")
        
        # Gestion spéciale pour F11 selon le clavier
        if event.keysym == 'F11' or event.keycode == 122:  # F11 sur la plupart des claviers
            self._toggle_fullscreen(event)
            return "break"
            
        # Gestion de la touche Échap
        if event.keysym == 'Escape' or event.keycode == 27:
            if self.is_fullscreen:
                self._exit_fullscreen(event)
            return "break"
            
        # Raccourcis alternatifs
        if event.state & 0x8:  # Alt est pressé
            if event.keysym == 'Return':  # Alt + Entrée
                self._toggle_fullscreen(event)
                return "break"
                
        if event.state & 0x4:  # Ctrl est pressé
            if event.keysym.lower() == 'f':  # Ctrl + F
                self._toggle_fullscreen(event)
                return "break"
                
        return None
