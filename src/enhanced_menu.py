"""
Menu principal ultra-moderne avec système de drag & drop
"""

import tkinter as tk
from tkinter import ttk
import math
import time
import random
from config.settings import COLORS, FONTS

class EnhancedGameMenu:
    """Menu principal avec drag & drop et animations avancées"""
    
    def __init__(self, master=None, on_game_start=None):
        self.master = master
        self.on_game_start = on_game_start
        self.selected_mode = None
        self.animation_running = False
        self.particles = []
        self.canvas = None
        
        # Variables pour le drag & drop
        self.dragging = False
        self.drag_item = None
        self.drag_data = {}
        self.mode_cards = {}
        self.drop_zone = None
        
        if self.master:
            self.master.title("TIC TAC TOE DELUXE - Menu Principal")
            self.master.attributes('-fullscreen', True)
            self.master.configure(bg=COLORS['background'])
            
            self.screen_width = self.master.winfo_screenwidth()
            self.screen_height = self.master.winfo_screenheight()
            
            # Raccourcis clavier
            self.master.bind('<Escape>', self._quit_app)
            self.master.bind('<Alt-F4>', self._quit_app)
            
            self.master.focus_set()
        
    def setup_ui(self):
        """Configure l'interface du menu avec drag & drop"""
        self.canvas = tk.Canvas(
            self.master,
            width=self.screen_width,
            height=self.screen_height,
            bg=COLORS['background'],
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        self._create_animated_background()
        self._create_title()
        self._create_drag_drop_interface()
        self._create_footer()
        
        self.master.after(100, self._start_animations)
        
    def _create_animated_background(self):
        """Crée un fond animé avec des particules"""
        for _ in range(20):
            x = random.randint(50, self.screen_width - 50)
            y = random.randint(50, self.screen_height - 50)
            size = random.randint(2, 4)
            speed_x = random.uniform(-0.5, 0.5)
            speed_y = random.uniform(-0.5, 0.5)
            
            particle = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=COLORS['accent_secondary'],
                outline='',
                stipple='gray25'
            )
            
            self.particles.append({
                'id': particle,
                'x': float(x),
                'y': float(y),
                'speed_x': speed_x,
                'speed_y': speed_y,
                'size': size
            })
            
    def _create_title(self):
        """Crée le titre principal avec effet lumineux"""
        # Titre principal
        title_y = self.screen_height * 0.15
        title_font_size = max(48, self.screen_height // 15)
        
        # Ombre du titre
        self.canvas.create_text(
            self.screen_width // 2 + 3,
            title_y + 3,
            text="✨ TIC TAC TOE DELUXE ✨",
            font=('Segoe UI', title_font_size, 'bold'),
            fill=COLORS['shadow'],
            anchor='center'
        )
        
        # Titre principal
        self.canvas.create_text(
            self.screen_width // 2,
            title_y,
            text="✨ TIC TAC TOE DELUXE ✨",
            font=('Segoe UI', title_font_size, 'bold'),
            fill=COLORS['text_primary'],
            anchor='center'
        )
        
        # Sous-titre
        subtitle_y = title_y + 80
        subtitle_font_size = max(18, self.screen_height // 40)
        
        self.canvas.create_text(
            self.screen_width // 2,
            subtitle_y,
            text="Glissez un mode de jeu dans la zone de démarrage",
            font=('Segoe UI', subtitle_font_size, 'italic'),
            fill=COLORS['accent_secondary'],
            anchor='center'
        )
        
    def _create_drag_drop_interface(self):
        """Crée l'interface avec drag & drop"""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Zone de drop (destination)
        drop_width = 400
        drop_height = 120
        drop_x = center_x - drop_width // 2
        drop_y = center_y + 100
        
        self.drop_zone = self.canvas.create_rectangle(
            drop_x, drop_y,
            drop_x + drop_width, drop_y + drop_height,
            fill=COLORS['background_secondary'],
            outline=COLORS['accent'],
            width=3,
            dash=(10, 5)
        )
        
        # Texte dans la zone de drop
        self.canvas.create_text(
            center_x, drop_y + drop_height // 2,
            text="🚀 GLISSEZ ICI POUR COMMENCER",
            font=('Segoe UI', 16, 'bold'),
            fill=COLORS['accent'],
            anchor='center'
        )
        
        # Cartes de mode de jeu (draggables)
        card_width = 280
        card_height = 100
        card_spacing = 350
        
        # Mode IA
        ai_x = center_x - card_spacing // 2 - card_width // 2
        ai_y = center_y - 50
        
        self._create_mode_card(
            ai_x, ai_y, card_width, card_height,
            "🤖 JOUEUR vs IA",
            "Affrontez l'intelligence artificielle",
            COLORS['button_restart'],
            'ai'
        )
        
        # Mode PvP  
        pvp_x = center_x + card_spacing // 2 - card_width // 2
        pvp_y = center_y - 50
        
        self._create_mode_card(
            pvp_x, pvp_y, card_width, card_height,
            "👥 JOUEUR vs JOUEUR",
            "Défiez vos amis",
            COLORS['button_fullscreen'],
            'pvp'
        )
        
    def _create_mode_card(self, x, y, width, height, title, subtitle, color, mode):
        """Crée une carte de mode draggable"""
        # Stocker les informations de la carte
        self.mode_cards[mode] = {
            'x': x, 'y': y, 'width': width, 'height': height,
            'original_x': x, 'original_y': y, 'color': color
        }
        
        # Rectangle de la carte
        card_rect = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=color,
            outline=COLORS['text_primary'],
            width=2,
            tags=f'card_{mode}'
        )
        
        # Titre de la carte
        title_text = self.canvas.create_text(
            x + width // 2, y + height // 3,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            fill='white',
            anchor='center',
            tags=f'card_{mode}'
        )
        
        # Sous-titre de la carte
        subtitle_text = self.canvas.create_text(
            x + width // 2, y + 2 * height // 3,
            text=subtitle,
            font=('Segoe UI', 12, 'normal'),
            fill='white',
            anchor='center',
            tags=f'card_{mode}'
        )
        
        # Ajouter les événements de drag & drop
        def start_drag(event):
            self._start_drag(event, mode)
        
        def drag_motion(event):
            self._drag_motion(event)
            
        def end_drag(event):
            self._end_drag(event)
            
        def card_hover_enter(event):
            self._card_hover_enter(mode)
            
        def card_hover_leave(event):
            self._card_hover_leave(mode)
        
        self.canvas.tag_bind(f'card_{mode}', '<Button-1>', start_drag)
        self.canvas.tag_bind(f'card_{mode}', '<B1-Motion>', drag_motion)
        self.canvas.tag_bind(f'card_{mode}', '<ButtonRelease-1>', end_drag)
        self.canvas.tag_bind(f'card_{mode}', '<Enter>', card_hover_enter)
        self.canvas.tag_bind(f'card_{mode}', '<Leave>', card_hover_leave)
        
    def _card_hover_enter(self, mode):
        """Effet hover sur les cartes"""
        if not self.dragging:
            items = self.canvas.find_withtag(f'card_{mode}')
            for item in items:
                if self.canvas.type(item) == 'rectangle':
                    self.canvas.itemconfig(item, width=4)
                    
    def _card_hover_leave(self, mode):
        """Fin de l'effet hover"""
        if not self.dragging:
            items = self.canvas.find_withtag(f'card_{mode}')
            for item in items:
                if self.canvas.type(item) == 'rectangle':
                    self.canvas.itemconfig(item, width=2)
                    
    def _start_drag(self, event, mode):
        """Commence le drag d'une carte"""
        self.dragging = True
        self.drag_item = mode
        
        # Convertir les coordonnées du canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        self.drag_data = {
            'start_x': canvas_x,
            'start_y': canvas_y,
            'mode': mode
        }
        
        # Mettre la carte au premier plan
        items = self.canvas.find_withtag(f'card_{mode}')
        for item in items:
            self.canvas.tag_raise(item)
            
        # Effet visuel de sélection
        items = self.canvas.find_withtag(f'card_{mode}')
        for item in items:
            if self.canvas.type(item) == 'rectangle':
                self.canvas.itemconfig(item, width=4, outline=COLORS['accent'])
                
    def _drag_motion(self, event):
        """Gère le mouvement pendant le drag"""
        if not self.dragging or not self.drag_item:
            return
            
        # Convertir les coordonnées du canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Calculer le déplacement
        dx = canvas_x - self.drag_data['start_x']
        dy = canvas_y - self.drag_data['start_y']
        
        # Déplacer tous les éléments de la carte
        items = self.canvas.find_withtag(f'card_{self.drag_item}')
        for item in items:
            self.canvas.move(item, dx, dy)
            
        # Mettre à jour les positions de départ
        self.drag_data['start_x'] = canvas_x
        self.drag_data['start_y'] = canvas_y
        
        # Vérifier si on survole la zone de drop
        self._check_drop_zone_hover(canvas_x, canvas_y)
            
    def _check_drop_zone_hover(self, x, y):
        """Vérifie si on survole la zone de drop"""
        if not self.drop_zone:
            return
            
        drop_coords = self.canvas.coords(self.drop_zone)
        if (drop_coords[0] <= x <= drop_coords[2] and 
            drop_coords[1] <= y <= drop_coords[3]):
            # Highlight de la zone de drop
            self.canvas.itemconfig(self.drop_zone, fill=COLORS['accent_secondary'], width=5)
        else:
            # Retour à la normale
            self.canvas.itemconfig(self.drop_zone, fill=COLORS['background_secondary'], width=3)
            
    def _end_drag(self, event):
        """Termine le drag"""
        if not self.dragging or not self.drag_item:
            return
            
        # Convertir les coordonnées du canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Vérifier si on a lâché dans la zone de drop
        drop_coords = self.canvas.coords(self.drop_zone)
        if (drop_coords[0] <= canvas_x <= drop_coords[2] and 
            drop_coords[1] <= canvas_y <= drop_coords[3]):
            # Succès ! Lancer le jeu
            self._launch_game_with_mode(self.drag_item)
        else:
            # Retourner à la position originale avec animation
            self._animate_card_return(self.drag_item)
                
        self.dragging = False
        self.drag_item = None
        
        # Remettre la zone de drop à la normale
        self.canvas.itemconfig(self.drop_zone, fill=COLORS['background_secondary'], width=3)
        
    def _animate_card_return(self, mode):
        """Anime le retour de la carte à sa position originale"""
        if mode not in self.mode_cards:
            return
            
        card_info = self.mode_cards[mode]
        target_x = card_info['original_x']
        target_y = card_info['original_y']
        
        # Obtenir la position actuelle du premier élément (rectangle)
        items = self.canvas.find_withtag(f'card_{mode}')
        if not items:
            return
            
        current_coords = self.canvas.coords(items[0])
        current_x = current_coords[0]
        current_y = current_coords[1]
        
        # Animation de retour
        steps = 15
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps
        
        def animate_step(step):
            if step < steps and items and self.master:
                try:
                    for item in items:
                        self.canvas.move(item, dx, dy)
                    self.master.after(20, lambda: animate_step(step + 1))
                except:
                    pass
            else:
                # Remettre les effets visuels normaux
                try:
                    for item in items:
                        if self.canvas.type(item) == 'rectangle':
                            self.canvas.itemconfig(item, width=2, outline=COLORS['text_primary'])
                except:
                    pass
                        
        animate_step(0)
        
    def _launch_game_with_mode(self, mode):
        """Lance le jeu avec le mode sélectionné"""
        # Animation de succès
        self._animate_success_feedback()
        
        # Arrêter toutes les animations en cours
        self.animation_running = False
        
        # Nettoyer toutes les tâches en attente sauf celle-ci
        if self.master:
            for task_id in self.master.tk.call('after', 'info'):
                try:
                    if task_id != self.master.tk.call('after', 'info', 'current'):
                        self.master.after_cancel(task_id)
                except:
                    pass
        
        # Lancer le jeu après l'animation
        def launch_delayed():
            try:
                if self.on_game_start:
                    print("✓ Mode sélectionné:", mode)
                    print("✓ Lancement du jeu...")
                    self.on_game_start(mode, 'hard')  # Un seul niveau d'IA
            except Exception as e:
                print(f"Erreur lors du lancement du jeu: {e}")
            
        # Attendre que l'animation soit terminée avant d'appeler le callback
        self.master.after(600, launch_delayed)
        
    def _animate_success_feedback(self):
        """Animation de feedback de succès"""
        # Faire clignoter la zone de drop
        colors = [COLORS['accent'], COLORS['accent_secondary']] * 3
        
        def flash_step(step):
            if step < len(colors) and self.drop_zone:
                try:
                    self.canvas.itemconfig(self.drop_zone, fill=colors[step])
                    self.master.after(150, lambda: flash_step(step + 1))
                except:
                    pass
                
        flash_step(0)
        
        # Pas d'animation supplémentaire - uniquement le clignotement de la zone de drop
        
    def _create_footer(self):
        """Crée le pied de page avec informations"""
        footer_y = self.screen_height - 100
        
        # Instructions
        self.canvas.create_text(
            self.screen_width // 2, footer_y,
            text="💡 Échap pour quitter • Glissez-déposez pour sélectionner un mode",
            font=('Segoe UI', 14, 'normal'),
            fill=COLORS['accent_secondary'],
            anchor='center'
        )
        
        # Bouton quitter
        quit_width = 120
        quit_height = 40
        quit_x = self.screen_width // 2 - quit_width // 2
        quit_y = footer_y + 30
        
        quit_button = self.canvas.create_rectangle(
            quit_x, quit_y,
            quit_x + quit_width, quit_y + quit_height,
            fill=COLORS['button_quit'],
            outline=COLORS['text_primary'],
            width=2,
            tags='quit_button'
        )
        
        quit_text = self.canvas.create_text(
            self.screen_width // 2, quit_y + quit_height // 2,
            text="❌ QUITTER",
            font=('Segoe UI', 12, 'bold'),
            fill='white',
            anchor='center',
            tags='quit_button'
        )
        
        def quit_click(event):
            self._quit_app()
            
        def quit_hover_enter(event):
            items = self.canvas.find_withtag('quit_button')
            for item in items:
                if self.canvas.type(item) == 'rectangle':
                    self.canvas.itemconfig(item, fill=COLORS['button_quit_hover'], width=4)
                    
        def quit_hover_leave(event):
            items = self.canvas.find_withtag('quit_button')
            for item in items:
                if self.canvas.type(item) == 'rectangle':
                    self.canvas.itemconfig(item, fill=COLORS['button_quit'], width=2)
        
        self.canvas.tag_bind('quit_button', '<Button-1>', quit_click)
        self.canvas.tag_bind('quit_button', '<Enter>', quit_hover_enter)
        self.canvas.tag_bind('quit_button', '<Leave>', quit_hover_leave)
        
    def _start_animations(self):
        """Démarre toutes les animations"""
        self.animation_running = True
        self._animate_particles()
        
    def _animate_particles(self):
        """Anime les particules d'arrière-plan"""
        if not self.animation_running:
            return
            
        # Mettre à jour chaque particule
        particles_to_remove = []
        for particle in self.particles:
            try:
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
                self.canvas.coords(
                    particle['id'],
                    particle['x'], particle['y'],
                    particle['x'] + particle['size'], particle['y'] + particle['size']
                )
            except:
                # Marquer la particule pour suppression
                particles_to_remove.append(particle)
        
        # Supprimer les particules problématiques
        for particle in particles_to_remove:
            if particle in self.particles:
                self.particles.remove(particle)
        
        # Planifier la prochaine frame
        if self.animation_running and self.master:
            self.master.after(100, self._animate_particles)
            
    def _quit_app(self, event=None):
        """Quitte l'application"""
        # Arrêter toutes les animations
        self.animation_running = False
        
        # Supprimer toutes les tâches en attente
        if self.master:
            for task_id in self.master.tk.call('after', 'info'):
                try:
                    self.master.after_cancel(task_id)
                except:
                    pass
        
        # Fermer la fenêtre proprement
        try:
            if self.master and self.master.winfo_exists():
                self.master.quit()
                self.master.destroy()
        except Exception as e:
            print(f"Erreur lors de la fermeture du menu: {e}")
