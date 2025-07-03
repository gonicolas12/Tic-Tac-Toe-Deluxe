"""
Point d'entrée principal du jeu Tic Tac Toe Ultra-Moderne avec Drag & Drop
"""

import sys
import os
import tkinter as tk

# Ajouter le répertoire du projet au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.game import GameLogic
from src.modern_ui import ModernGameUI
from src.enhanced_menu import EnhancedGameMenu
from config.settings import COLORS

# Désactiver les anciens modules qui pourraient causer des conflits
sys.modules['src.ui'] = None
sys.modules['src.menu'] = None

# Variables globales pour la gestion des fenêtres
app_running = False
current_window = None
transition_window = None
root = None

def create_transition_window():
    """Crée une fenêtre de transition couvrant tout l'écran pour des transitions fluides"""
    global transition_window
    global root
    
    print("🔄 Création d'une fenêtre de transition...")
    
    # Nettoyer toute ancienne fenêtre de transition
    if transition_window is not None:
        try:
            if transition_window.winfo_exists():
                transition_window.destroy()
                print("✓ Ancienne fenêtre de transition fermée")
        except Exception as e:
            print(f"Note: Erreur lors de la fermeture de l'ancienne fenêtre de transition: {e}")
    
    try:
        # Utiliser toujours la fenêtre racine comme parent si disponible
        if root and root.winfo_exists():
            transition_window = tk.Toplevel(root)
            print("✓ Fenêtre de transition créée à partir de la racine")
        else:
            print("⚠️ Fenêtre racine non disponible pour la transition")
            # Créer une fenêtre de transition indépendante
            transition_window = tk.Toplevel()
        
        # Configurer la fenêtre de transition pour une couverture totale
        transition_window.title("TIC TAC TOE DELUXE - Transition")
        transition_window.attributes('-fullscreen', True)
        transition_window.attributes('-topmost', True)
        transition_window.configure(bg=COLORS['background'])
        transition_window.overrideredirect(True)  # Enlever la barre de titre pour plus de fluidité
        
        # Forcer la fenêtre à couvrir tout l'écran immédiatement
        transition_window.geometry(f"{transition_window.winfo_screenwidth()}x{transition_window.winfo_screenheight()}+0+0")
        
        # Ne pas permettre de fermer avec le bouton X
        transition_window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Ajouter un effet visuel simple
        canvas = tk.Canvas(
            transition_window,
            bg=COLORS['background'],
            highlightthickness=0,
            width=transition_window.winfo_screenwidth(),
            height=transition_window.winfo_screenheight()
        )
        canvas.pack(fill='both', expand=True)
        
        # Texte principal
        canvas.create_text(
            transition_window.winfo_screenwidth() // 2,
            transition_window.winfo_screenheight() // 2,
            text="✨ TIC TAC TOE DELUXE ✨",
            font=('Segoe UI', 36, 'bold'),
            fill=COLORS['accent'],
            anchor='center'
        )
        
        # Texte de chargement
        canvas.create_text(
            transition_window.winfo_screenwidth() // 2,
            transition_window.winfo_screenheight() // 2 + 60,
            text="Chargement...",
            font=('Segoe UI', 16, 'italic'),
            fill=COLORS['accent_secondary'],
            anchor='center'
        )
        
        # Mettre à jour plusieurs fois pour s'assurer que la fenêtre est bien affichée
        transition_window.update_idletasks()
        transition_window.update()
        transition_window.focus_force()  # S'assurer que la fenêtre a le focus
        transition_window.lift()  # S'assurer qu'elle est au premier plan
        
        # Double vérification que la fenêtre couvre bien tout l'écran
        transition_window.attributes('-topmost', True)
        transition_window.update()
        
        print("✓ Fenêtre de transition affichée et optimisée")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la création de la fenêtre de transition: {e}")
        return None
    
    return transition_window

def close_transition_window(delay=500):
    """Ferme la fenêtre de transition après un délai"""
    global transition_window
    
    if transition_window is not None:
        try:
            if transition_window.winfo_exists():
                print(f"🔄 Préparation de la fermeture de la fenêtre de transition (délai: {delay}ms)")
                
                # S'assurer que la fenêtre de transition n'est plus au premier plan
                transition_window.attributes('-topmost', False)
                transition_window.lower()  # Mettre la fenêtre en arrière-plan
                
                # Fonction de nettoyage avec transition fluide
                def close_window():
                    global transition_window
                    try:
                        if transition_window and transition_window.winfo_exists():
                            # Transition douce : d'abord perdre le focus topmost
                            transition_window.attributes('-topmost', False)
                            transition_window.update_idletasks()
                            
                            # Ensuite la cacher progressivement
                            transition_window.withdraw()
                            transition_window.update_idletasks()
                            
                            # Finalement la détruire
                            transition_window.destroy()
                            print("✓ Fenêtre de transition fermée avec transition fluide")
                    except Exception as e:
                        print(f"⚠️ Erreur lors de la fermeture de la transition: {e}")
                    finally:
                        # Toujours réinitialiser la référence
                        transition_window = None
                
                # Programmer la fermeture après le délai
                transition_window.after(delay, close_window)
            else:
                # La fenêtre n'existe plus
                transition_window = None
        except Exception as e:
            print(f"⚠️ Erreur lors de la fermeture de la fenêtre de transition: {e}")
            transition_window = None

# Variables globales pour la gestion des fenêtres
app_running = False
current_window = None  # Référence à la fenêtre active actuelle

def start_game(game_mode='pvp', ai_level='medium'):
    """Lance le jeu avec le mode sélectionné"""
    global app_running
    global current_window
    global root
    global transition_window
    
    # Marquer l'application comme en cours d'exécution
    app_running = True
    print(f"⚙️ Démarrage du jeu en mode {game_mode}, niveau IA: {ai_level}")
    
    try:
        # Ne pas créer une nouvelle transition si une transition existe déjà
        if transition_window is None:
            # Créer une transition visuelle seulement si aucune n'existe
            create_transition_window()
            print("🔄 Nouvelle transition créée pour le jeu")
        else:
            print("♻️ Réutilisation de la transition existante pour le jeu")
        
        # Utiliser la fenêtre racine globale qui a été créée au démarrage de l'application
        game_window = root
        
        # Vérifier que la fenêtre existe encore
        if not game_window or not game_window.winfo_exists():
            print("⚠️ Fenêtre racine perdue, création d'une nouvelle fenêtre")
            # Recréer une fenêtre racine si elle a été détruite
            game_window = tk.Tk()
            root = game_window
        else:
            # Nettoyer tous les widgets existants
            print("♻️ Réutilisation de la fenêtre racine pour le jeu")
            for widget in game_window.winfo_children():
                try:
                    # Exclure la fenêtre de transition si elle existe
                    if transition_window is not None and widget != transition_window:
                        widget.destroy()
                except Exception as e:
                    print(f"Note: Erreur lors du nettoyage d'un widget: {e}")
        
        # S'assurer que la fenêtre est visible et au premier plan
        game_window.deiconify()
        current_window = game_window
        
        # Configurer la fenêtre
        game_window.title("TIC TAC TOE DELUXE - Jeu")
        game_window.attributes('-fullscreen', True)
        game_window.configure(bg=COLORS['background'])
        
        # Créer une nouvelle instance de logique de jeu
        game_logic = GameLogic()
        
        # Fonction pour retourner au menu de façon robuste
        def back_to_menu():
            print("↩️ Retour au menu principal...")
            global app_running
            global current_window
            global transition_window
            
            # Afficher la transition AVANT de masquer le jeu
            create_transition_window()
            
            # Attendre que la transition soit bien affichée avant de masquer le jeu
            def hide_game_after_transition():
                # Réinitialiser l'état de l'application
                global app_running
                app_running = False
                
                # Masquer la fenêtre de jeu mais NE PAS LA DÉTRUIRE
                try:
                    # Masquer le contenu actuel
                    for widget in game_window.winfo_children():
                        if transition_window is None or widget != transition_window:
                            widget.pack_forget()
                    
                    # Ne pas fermer la fenêtre, juste la masquer temporairement
                    game_window.withdraw()
                    print("✓ Interface de jeu masquée après transition")
                except Exception as e:
                    print(f"Note: {e}")
            
            # Attendre un petit délai pour que la transition soit bien visible
            root.after(150, hide_game_after_transition)
            
            # Lancement différé du menu pour laisser le temps à la transition
            def safe_start_menu():
                # Lancer le menu qui réutilisera la même fenêtre racine
                try:
                    print("🔄 Chargement du menu principal...")
                    start_menu()
                    
                    # La fenêtre de transition sera fermée par start_menu
                except Exception as e:
                    print(f"⚠️ Erreur lors du retour au menu: {e}")
                    # En cas d'erreur, fermer au moins la transition
                    close_transition_window(100)

            if root and root.winfo_exists():
                root.after(500, safe_start_menu)
            else:
                # Si la racine n'existe plus (cas improbable), appel direct
                safe_start_menu()
        
        # Créer l'interface moderne
        game_ui = ModernGameUI(
            master=game_window,
            game_logic=game_logic, 
            game_mode=game_mode,
            ai_level=ai_level,
            on_return_menu=back_to_menu
        )
        
        # Configurer et lancer le jeu
        print("🎮 Configuration de l'interface de jeu...")
        game_ui.setup_ui()
        print("✅ Jeu prêt - Mode:", "JOUEUR vs IA" if game_mode == "ai" else "JOUEUR vs JOUEUR")
        print("-" * 50)
        
        # Amener la fenêtre du jeu au premier plan, mais pas encore visible
        game_window.update()
        
        # Fermer la transition APRÈS que le jeu soit prêt
        def show_game_window():
            # S'assurer que la fenêtre de jeu est au premier plan
            game_window.lift()
            game_window.attributes('-topmost', True)
            game_window.after(10, lambda: game_window.attributes('-topmost', False))
            game_window.focus_force()  # Donner le focus au jeu
            print("✓ Fenêtre de jeu au premier plan")
        
        # Fermer la transition ET montrer le jeu après avec timing optimisé
        if transition_window and transition_window.winfo_exists():
            # D'abord programmer l'affichage du jeu avec un délai suffisant
            transition_window.after(800, show_game_window)
            # Puis fermer la transition avec un délai encore plus long
            close_transition_window(1200)
        else:
            # Si pas de transition, montrer le jeu directement
            show_game_window()
            
        print("✓ Interface de jeu configurée et affichée")
    except Exception as e:
        print(f"❌ Erreur lors du lancement du jeu: {e}")
        app_running = False

def start_menu():
    """Lance le menu principal de façon robuste"""
    global app_running
    global current_window
    global root
    global transition_window
    
    # Empêcher les lancements multiples
    if app_running:
        print("⚠️ Application déjà en cours d'exécution, menu ignoré")
        return
    
    app_running = True
    print("🚀 Démarrage du menu principal...")
    
    # Utiliser toujours la fenêtre racine globale
    menu_window = root
    
    # Vérifier que la fenêtre root existe bien
    if not menu_window or not menu_window.winfo_exists():
        print("⚠️ Fenêtre racine non disponible, création d'une nouvelle fenêtre")
        menu_window = tk.Tk()
        root = menu_window  # Mettre à jour la référence globale
    
    # Nettoyer tous les widgets existants
    for widget in menu_window.winfo_children():
        # Ne pas supprimer la fenêtre de transition si elle existe
        if transition_window is None or widget != transition_window:
            try:
                widget.destroy()
            except Exception as e:
                print(f"Note lors du nettoyage: {e}")
    
    # Configurer la fenêtre
    menu_window.deiconify()  # S'assurer que la fenêtre est visible
    menu_window.title("TIC TAC TOE DELUXE - Menu Principal")
    menu_window.attributes('-fullscreen', True)
    menu_window.configure(bg=COLORS['background'])
    
    # Mettre à jour la référence à la fenêtre courante
    current_window = menu_window
    print("✓ Fenêtre du menu principal préparée")
    
    # Définir un gestionnaire d'exception pour capturer les erreurs Tk
    def handle_tk_error(exc, val, tb):
        print(f"❌ Erreur Tkinter: {val}")
        sys.__excepthook__(exc, val, tb)
    
    # Installer le gestionnaire d'erreurs
    sys.excepthook = handle_tk_error
    
    # Fonction de callback pour lancer le jeu de façon robuste
    def start_game_callback(game_mode, ai_level):
        global app_running
        global current_window
        
        print(f"⚙️ Préparation du jeu en mode {game_mode.upper()}...")
        
        # Important: stocker les paramètres dans des variables locales
        game_mode_copy = game_mode
        ai_level_copy = ai_level
        
        # Enregistrer une référence locale à la fenêtre
        local_window = menu_window
        
        # Réinitialiser l'état global et préparer la transition
        try:
            # Afficher la fenêtre de transition AVANT de cacher le menu
            create_transition_window()
            
            # Attendre que la transition soit bien affichée avant de continuer
            def hide_menu_after_transition():
                # Maintenant on peut cacher la fenêtre du menu
                if local_window.winfo_exists():
                    local_window.withdraw()
                print("✓ Menu masqué après affichage de la transition")
                
                # Réinitialiser l'état global 
                global app_running
                app_running = False
            
            # Attendre un petit délai pour que la transition soit bien visible
            root.after(100, hide_menu_after_transition)
            
            # Fonction pour lancer le jeu de façon différée
            def safe_start_game():
                global current_window, app_running  # Déclarer les variables comme globales
                try:
                    print("✓ Mode sélectionné: " + game_mode_copy)
                    print("✓ Lancement du jeu...")
                    
                    # Ne pas détruire la fenêtre, juste nettoyer son contenu
                    if local_window.winfo_exists():
                        # Cacher les widgets existants au lieu de détruire la fenêtre
                        for widget in local_window.winfo_children():
                            # Ne pas détruire la fenêtre de transition
                            if transition_window is None or widget != transition_window:
                                widget.destroy()
                    
                    # Lancer le jeu, on réutilise la même fenêtre
                    start_game(game_mode_copy, ai_level_copy)
                except Exception as e:
                    print(f"❌ Erreur lors du lancement du jeu: {e}")
                    app_running = False
                    
            # Utiliser un délai plus long pour laisser voir la transition
            root.after(1000, safe_start_game)
            
        except Exception as e:
            print(f"❌ Erreur pendant la transition menu -> jeu: {e}")
            app_running = False
    
    # Créer le menu avec callback vers start_game
    menu = EnhancedGameMenu(
        master=menu_window,
        on_game_start=start_game_callback
    )
    
    # Configurer le menu
    menu.setup_ui()
    menu_window.protocol("WM_DELETE_WINDOW", lambda: exit_app(menu_window))
    menu_window.update()
    
    # Fonction pour afficher le menu après la transition
    def show_menu_window():
        # S'assurer que la fenêtre de menu est au premier plan
        menu_window.lift()
        menu_window.attributes('-topmost', True)
        menu_window.after(10, lambda: menu_window.attributes('-topmost', False))
        menu_window.focus_force()  # Donner le focus au menu
        print("✓ Menu principal au premier plan")
    
    # Fermer la transition ET montrer le menu après avec timing optimisé
    if transition_window and transition_window.winfo_exists():
        # D'abord programmer l'affichage du menu après un délai
        transition_window.after(400, show_menu_window)
        # Puis fermer la transition avec un délai plus long
        close_transition_window(700)
    else:
        # Si pas de transition, montrer le menu directement
        show_menu_window()
    
    print("✓ Interface de menu configurée et affichée")

def exit_app(window):
    """Quitte l'application proprement"""
    global app_running
    global current_window
    
    print("🚪 Fermeture de l'application...")
    app_running = False
    
    # Capture de toutes les fenêtres Tkinter actives
    all_windows = []
    if window:
        all_windows.append(window)
    if current_window and current_window != window:
        all_windows.append(current_window)
        
    # Fermeture propre de toutes les fenêtres
    for win in all_windows:
        try:
            if win and win.winfo_exists():
                print(f"Fermeture de la fenêtre {win}")
                win.withdraw()  # Cacher d'abord
                win.update()    # Mettre à jour pour appliquer withdraw
                win.destroy()   # Puis détruire
        except Exception as e:
            print(f"Note lors de la fermeture: {e}")
    
    # Réinitialiser l'état global
    current_window = None
    
    # Forcer le nettoyage des ressources
    import gc
    gc.collect()
    
    # Quitter l'application
    print("Au revoir! 👋")
    sys.exit(0)
        
def main():
    """Fonction principale du jeu avec gestion d'erreurs robuste"""
    # Configurer un gestionnaire d'exception global
    def global_exception_handler(exc_type, exc_val, exc_tb):
        global app_running, current_window  # Déclarer les variables globales
        print(f"❌ ERREUR CRITIQUE: {exc_type.__name__}: {exc_val}")
        import traceback
        traceback.print_exception(exc_type, exc_val, exc_tb)
        
        # Nettoyage des ressources
        app_running = False
        if current_window:
            try:
                if current_window.winfo_exists():
                    current_window.destroy()
            except:
                pass
            current_window = None
            
        sys.exit(1)
    
    # Installer le gestionnaire d'exceptions
    sys.excepthook = global_exception_handler
    
    try:
        # Lancer le menu principal
        start_menu()
    except Exception as e:
        print(f"❌ Erreur lors du lancement du jeu: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def init_app():
    """Initialisation complète de l'application avec gestion améliorée du démarrage"""
    global current_window, app_running, transition_window, root
    
    print("🎮 Lancement du jeu Tic Tac Toe Ultra-Moderne...")
    print("📁 Architecture modulaire chargée")
    print("🎨 Effets visuels et animations activés")
    print("-" * 50)
    
    # Réinitialiser les variables globales
    app_running = False
    current_window = None
    transition_window = None
    
    try:
        print("🔄 Création de la fenêtre principale...")
        # Créer une fenêtre racine unique pour toute l'application
        root = tk.Tk()
        root.withdraw()  # Masquer temporairement
        current_window = root  # Définir comme fenêtre courante
        
        # Configurer la gestion des erreurs Tkinter
        def handle_tk_error(exc_type, exc_val, exc_tb):
            print(f"❌ Erreur Tkinter: {exc_val}")
            import traceback
            traceback.print_exception(exc_type, exc_val, exc_tb)
        
        # Installer le gestionnaire d'erreurs
        root.report_callback_exception = handle_tk_error
        
        # Créer le splash screen
        print("🎨 Création du splash screen...")
        splash_window = tk.Toplevel(root)
        splash_window.title("TIC TAC TOE DELUXE - Chargement")
        splash_window.attributes('-fullscreen', True)
        splash_window.attributes('-topmost', True)
        splash_window.configure(bg=COLORS['background'])
        splash_window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Créer le contenu du splash screen
        splash_canvas = tk.Canvas(
            splash_window,
            bg=COLORS['background'],
            highlightthickness=0,
            width=splash_window.winfo_screenwidth(),
            height=splash_window.winfo_screenheight()
        )
        splash_canvas.pack(fill='both', expand=True)
        
        # Texte principal
        splash_canvas.create_text(
            splash_window.winfo_screenwidth() // 2,
            splash_window.winfo_screenheight() // 2,
            text="✨ TIC TAC TOE DELUXE ✨",
            font=('Segoe UI', 36, 'bold'),
            fill=COLORS['accent'],
            anchor='center'
        )
        
        # Texte de chargement
        loading_text = splash_canvas.create_text(
            splash_window.winfo_screenwidth() // 2,
            splash_window.winfo_screenheight() // 2 + 60,
            text="Chargement...",
            font=('Segoe UI', 16, 'italic'),
            fill=COLORS['accent_secondary'],
            anchor='center'
        )
        
        # Afficher immédiatement
        splash_window.update()
        print("✓ Splash screen affiché")
        
        # Planifier le démarrage du menu principal de façon fluide
        def launch_menu():
            try:
                print("🚀 Lancement du menu principal...")
                
                # Stocker le splash screen comme fenêtre de transition pour une transition fluide
                global transition_window
                transition_window = splash_window
                
                # Lancer le menu qui fermera lui-même la fenêtre de transition
                # et assurera l'affichage fluide
                start_menu()
                
            except Exception as e:
                print(f"❌ Erreur au démarrage du menu: {e}")
                # En cas d'erreur, détruire le splash screen
                try:
                    splash_window.destroy()
                except:
                    pass
                import traceback
                traceback.print_exc()
        
        # Lancer le menu après un délai
        root.after(1000, launch_menu)
        print("✓ Démarrage planifié avec succès")
        
        # Démarrer la boucle principale
        print("⏳ Démarrage de la boucle principale Tkinter")
        root.mainloop()
        print("✓ Fin de l'application")
        
    except Exception as e:
        print(f"❌ ERREUR FATALE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_app()
