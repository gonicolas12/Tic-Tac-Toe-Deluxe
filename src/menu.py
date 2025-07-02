"""
Menu principal du jeu Tic Tac Toe avec animations et effets
"""

import tkinter as tk
from tkinter import ttk
import math
import time
from config.settings import COLORS, FONTS, WINDOW_CONFIG

class GameMenu:
    """Classe gérant le menu principal avec animations"""
    
    def __init__(self, on_game_start=None):
        self.window = None
        self.on_game_start = on_game_start
        self.selected_mode = None
        self.animation_running = False
        self.particles = []
        self.canvas = None
        
    def setup_window(self):
        """Configure la fenêtre du menu en plein écran automatique"""
        self.window = tk.Tk()
        self.window.title("TIC TAC TOE DELUXE - Menu Principal")
        
        # Passer automatiquement en plein écran
        self.window.attributes('-fullscreen', True)
        self.window.configure(bg=COLORS['background'])
        
        # Obtenir les dimensions de l'écran
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        # Raccourcis pour quitter
        self.window.bind('<Escape>', self._quit_app)
        self.window.bind('<Alt-F4>', self._quit_app)
        
        self.window.focus_set()
        
    def setup_ui(self):
        """Configure l'interface du menu avec animations"""
        # Canvas pour les effets de fond animés
        self.canvas = tk.Canvas(
            self.window,
            width=self.screen_width,
            height=self.screen_height,
            bg=COLORS['background'],
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Frame principal centré
        self.main_frame = tk.Frame(
            self.canvas,
            bg=COLORS['background'],
            padx=50,
            pady=50
        )
        
        # Centrer le frame sur le canvas
        canvas_frame = self.canvas.create_window(
            self.screen_width // 2,
            self.screen_height // 2,
            window=self.main_frame,
            anchor='center'
        )
        
        self._create_animated_background()
        self._create_title()
        self._create_mode_selection()
        self._create_ai_level_selection()  # Ajouter la sélection de niveau
        self._create_footer()
        
        # Démarrer les animations
        self._start_animations()
        
    def _create_animated_background(self):
        """Crée un fond animé avec des particules"""
        # Créer des particules d'arrière-plan
        for _ in range(50):
            x = tk.IntVar(value=tk._default_root.tk.call('expr', f'int(rand() * {self.screen_width})') if hasattr(tk, '_default_root') else 100)
            y = tk.IntVar(value=tk._default_root.tk.call('expr', f'int(rand() * {self.screen_height})') if hasattr(tk, '_default_root') else 100)
            size = 2 + (hash(str(x.get() + y.get())) % 4)  # Taille 2-5
            speed_x = (hash(str(x.get())) % 20 - 10) / 10  # Vitesse -1 à 1
            speed_y = (hash(str(y.get())) % 20 - 10) / 10
            
            particle = self.canvas.create_oval(
                x.get(), y.get(), x.get() + size, y.get() + size,
                fill=COLORS['accent_secondary'],
                outline='',
                stipple='gray25'  # Effet de transparence
            )
            
            self.particles.append({
                'id': particle,
                'x': x.get(),
                'y': y.get(),
                'speed_x': speed_x,
                'speed_y': speed_y,
                'size': size
            })
    
    def _create_title(self):
        """Crée le titre principal avec effet lumineux"""
        # Titre principal avec ombre
        title_font_size = max(48, self.screen_height // 15)
        title_font = ('Segoe UI', title_font_size, 'bold')
        
        self.title_label = tk.Label(
            self.main_frame,
            text="✨ TIC TAC TOE DELUXE ✨",
            font=title_font,
            bg=COLORS['background'],
            fg=COLORS['text_primary'],
            pady=30
        )
        self.title_label.pack(pady=(0, 40))
        
        # Sous-titre animé
        subtitle_font = ('Segoe UI', max(18, self.screen_height // 40), 'italic')
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Expérience de jeu ultime avec IA et effets visuels",
            font=subtitle_font,
            bg=COLORS['background'],
            fg=COLORS['accent_secondary'],
            pady=10
        )
        self.subtitle_label.pack(pady=(0, 60))
        
    def _create_mode_selection(self):
        """Crée la sélection de mode avec boutons animés"""
        # Frame pour les modes
        modes_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        modes_frame.pack(pady=40)
        
        # Style pour les boutons de mode
        button_width = max(20, self.screen_width // 60)
        button_font = ('Segoe UI', max(16, self.screen_height // 50), 'bold')
        
        # Mode Joueur vs IA
        self.ai_button = self._create_animated_button(
            modes_frame,
            "🤖 JOUEUR vs IA",
            lambda: self._select_mode('ai'),
            button_font,
            COLORS['button_restart'],
            COLORS['button_restart_hover'],
            width=button_width
        )
        self.ai_button.pack(pady=15)
        
        # Mode Joueur vs Joueur
        self.pvp_button = self._create_animated_button(
            modes_frame,
            "👥 JOUEUR vs JOUEUR",
            lambda: self._select_mode('pvp'),
            button_font,
            COLORS['button_fullscreen'],
            COLORS['button_fullscreen_hover'],
            width=button_width
        )
        self.pvp_button.pack(pady=15)
        
        # Bouton démarrer (initialement désactivé)
        self.start_button = self._create_animated_button(
            modes_frame,
            "🚀 COMMENCER LA PARTIE",
            self._start_game,
            button_font,
            COLORS['accent'],
            COLORS['button_quit_hover'],
            width=button_width,
            state='disabled'
        )
        self.start_button.pack(pady=(40, 20))
        
    def _create_animated_button(self, parent, text, command, font, bg_color, hover_color, width=20, state='normal'):
        """Crée un bouton avec animations de survol"""
        button = tk.Button(
            parent,
            text=text,
            font=font,
            bg=bg_color,
            fg='white',
            activebackground=hover_color,
            relief='raised',
            bd=3,
            cursor='hand2',
            command=command,
            width=width,
            pady=15,
            state=state
        )
        
        # Ajouter les effets d'animation
        def on_enter(e):
            if button['state'] != 'disabled':
                button.config(
                    bg=hover_color,
                    relief='solid',
                    bd=4
                )
                self._animate_button_scale(button, 1.05)
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button.config(
                    bg=bg_color,
                    relief='raised',
                    bd=3
                )
                self._animate_button_scale(button, 1.0)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button
        
    def _animate_button_scale(self, button, target_scale):
        """Anime la mise à l'échelle d'un bouton"""
        # Simulation simple d'effet de scale via le padding
        if target_scale > 1.0:
            button.config(pady=18)
        else:
            button.config(pady=15)
    
    def _create_footer(self):
        """Crée le pied de page avec informations"""
        footer_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        footer_frame.pack(side='bottom', pady=(60, 20))
        
        # Instructions
        instructions_font = ('Segoe UI', max(12, self.screen_height // 60), 'normal')
        instructions = tk.Label(
            footer_frame,
            text="💡 Échap pour quitter • Les boutons réagissent au survol de la souris",
            font=instructions_font,
            bg=COLORS['background'],
            fg=COLORS['accent_secondary']
        )
        instructions.pack()
        
        # Bouton quitter
        quit_font = ('Segoe UI', max(14, self.screen_height // 55), 'bold')
        self.quit_button = self._create_animated_button(
            footer_frame,
            "❌ QUITTER",
            self._quit_app,
            quit_font,
            COLORS['button_quit'],
            COLORS['button_quit_hover'],
            width=15
        )
        self.quit_button.pack(pady=(20, 0))
    
    def _start_game(self):
        """Lance le jeu avec le mode sélectionné"""
        if self.selected_mode and self.on_game_start:
            self.animation_running = False
            
            # Obtenir le niveau d'IA si mode IA sélectionné
            ai_level = 'medium'  # Par défaut
            if hasattr(self, 'ai_level_var'):
                ai_level = self.ai_level_var.get()
            
            # Passer les paramètres au callback
            mode = 'ai' if self.selected_mode == 'ai' else 'pvp'
            self.on_game_start(mode, ai_level)
            
            # Fermer le menu
            self.window.destroy()
    
    def _create_ai_level_selection(self):
        """Crée la sélection du niveau d'IA"""
        self.ai_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        
        # Titre du niveau
        level_label = tk.Label(
            self.ai_frame,
            text="🎯 Niveau de difficulté de l'IA",
            font=('Segoe UI', max(14, self.screen_height // 55), 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text_primary']
        )
        level_label.pack(pady=(20, 10))
        
        # Variable pour stocker le niveau sélectionné
        self.ai_level_var = tk.StringVar(value='medium')
        
        # Boutons de niveau
        levels = [
            ('🟢 FACILE', 'easy', COLORS['accent_secondary']),
            ('🟡 MOYEN', 'medium', COLORS['accent']),
            ('🔴 DIFFICILE', 'hard', COLORS['button_quit'])
        ]
        
        for text, level, color in levels:
            btn = tk.Radiobutton(
                self.ai_frame,
                text=text,
                variable=self.ai_level_var,
                value=level,
                font=('Segoe UI', max(12, self.screen_height // 60), 'normal'),
                bg=COLORS['background'],
                fg=COLORS['text_primary'],
                selectcolor=color,
                activebackground=COLORS['background'],
                activeforeground=COLORS['text_primary'],
                relief='flat',
                bd=0
            )
            btn.pack(anchor='w', padx=20, pady=5)
    
    def _update_ui_for_mode(self, mode):
        """Met à jour l'interface selon le mode sélectionné"""
        if mode == 'ai':
            self.ai_frame.pack(pady=(20, 20))
        else:
            self.ai_frame.pack_forget()
    
    def _select_mode(self, mode):
        """Sélectionne le mode de jeu"""
        self.selected_mode = mode
        
        # Mettre à jour l'apparence des boutons
        if mode == 'ai':
            self.ai_button.config(
                bg=COLORS['winning_highlight'],
                relief='solid',
                bd=4
            )
            self.pvp_button.config(
                bg=COLORS['button_fullscreen'],
                relief='raised',
                bd=3
            )
        else:
            self.pvp_button.config(
                bg=COLORS['winning_highlight'],
                relief='solid',
                bd=4
            )
            self.ai_button.config(
                bg=COLORS['button_restart'],
                relief='raised',
                bd=3
            )
        
        # Mettre à jour l'interface selon le mode
        self._update_ui_for_mode(mode)
        
        # Activer le bouton démarrer avec animation
        self.start_button.config(
            state='normal',
            bg=COLORS['accent']
        )
        self._animate_button_activation()
    
    def _animate_button_activation(self):
        """Anime l'activation du bouton démarrer"""
        def pulse():
            if not hasattr(self, 'start_button') or not self.start_button.winfo_exists():
                return
            colors = [COLORS['accent'], COLORS['button_quit_hover']]
            for i, color in enumerate(colors * 3):  # 3 pulsations
                self.window.after(i * 200, lambda c=color: (
                    self.start_button.config(bg=c) 
                    if hasattr(self, 'start_button') and self.start_button.winfo_exists() 
                    else None
                ))
        
        pulse()
    
    def _start_animations(self):
        """Démarre toutes les animations"""
        self.animation_running = True
        self._animate_particles()
        self._animate_title()
    
    def _animate_particles(self):
        """Anime les particules d'arrière-plan"""
        if not self.animation_running:
            return
            
        # Mettre à jour chaque particule
        for particle in self.particles:
            # Nouvelle position
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Rebond sur les bords
            if particle['x'] <= 0 or particle['x'] >= self.screen_width:
                particle['speed_x'] *= -1
            if particle['y'] <= 0 or particle['y'] >= self.screen_height:
                particle['speed_y'] *= -1
            
            # Garder dans les limites
            particle['x'] = max(0, min(self.screen_width, particle['x']))
            particle['y'] = max(0, min(self.screen_height, particle['y']))
            
            # Mettre à jour la position
            try:
                self.canvas.coords(
                    particle['id'],
                    particle['x'], particle['y'],
                    particle['x'] + particle['size'], particle['y'] + particle['size']
                )
            except:
                pass
        
        # Planifier la prochaine frame
        if self.animation_running:
            self.window.after(50, self._animate_particles)
    
    def _animate_title(self):
        """Anime le titre avec effet de pulsation"""
        if not self.animation_running:
            return
            
        # Effet de pulsation sur le sous-titre
        try:
            current_time = time.time()
            # Simuler l'opacité en changeant la couleur - effet simple mais efficace
            
            if self.animation_running:
                self.window.after(100, self._animate_title)
        except:
            pass
    
    def _quit_app(self, event=None):
        """Quitte l'application"""
        self.animation_running = False
        self.window.quit()
        self.window.destroy()
    
    def run(self):
        """Lance le menu"""
        self.setup_window()
        self.setup_ui()
        self.window.mainloop()
