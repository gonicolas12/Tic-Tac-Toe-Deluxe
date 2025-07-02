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
# Si d'autres fichiers importent ces modules, ils n'auront pas d'effet secondaire
sys.modules['src.ui'] = None
sys.modules['src.menu'] = None

# Variables globales pour la gestion des fenêtres
app_running = False
current_window = None  # Référence à la fenêtre active actuelle

def start_game(game_mode='pvp', ai_level='medium'):
    """Lance le jeu avec le mode sélectionné"""
    global app_running
    global current_window
    
    # Marquer l'application comme en cours d'exécution
    app_running = True
    
    try:
        # Détruire toute fenêtre existante avant d'en créer une nouvelle
        if current_window is not None:
            try:
                if current_window.winfo_exists():
                    current_window.destroy()
            except:
                pass  # Ignorer les erreurs
            current_window = None  # Effacer la référence
        
        # Créer une nouvelle fenêtre Tk pour le jeu
        game_window = tk.Tk()
        current_window = game_window  # Stocker la référence globale
        
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
            
            # Indiquer que l'application n'est plus en cours d'exécution
            app_running = False
            
            # Enregistrer une référence locale
            local_window = game_window
            
            # Cacher la fenêtre pour feedback visuel immédiat
            try:
                if local_window.winfo_exists():
                    local_window.withdraw()
            except:
                pass
            
            # Utiliser after_idle pour différer le lancement du menu
            def safe_start_menu():
                global current_window  # Déclarer la variable comme globale
                
                # Lancer d'abord le menu
                start_menu()
                
                # Détruire la fenêtre précédente de façon différée
                def cleanup():
                    global current_window  # Déclarer la variable comme globale ici aussi
                    try:
                        if local_window.winfo_exists():
                            local_window.destroy()
                            print("✓ Fenêtre de jeu détruite avec succès après retour au menu")
                    except:
                        pass
                
                # Utiliser un timer pour destruction différée
                import threading
                threading.Timer(0.5, cleanup).start()
            
            # Lancer le menu via after_idle ou directement si la fenêtre n'existe plus
            try:
                if local_window and local_window.winfo_exists():
                    local_window.after_idle(safe_start_menu)
                else:
                    # Si la fenêtre n'existe plus, lancer directement
                    safe_start_menu()
            except Exception as e:
                print(f"⚠️ Fallback pour lancer le menu: {e}")
                # Appel direct en cas d'erreur
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
        game_window.mainloop()
    except Exception as e:
        print(f"❌ Erreur lors du lancement du jeu: {e}")
        app_running = False

def start_menu():
    """Lance le menu principal de façon robuste"""
    global app_running
    global current_window
    
    # Empêcher les lancements multiples
    if app_running:
        print("⚠️ Application déjà en cours d'exécution, menu ignoré")
        return
    
    app_running = True
    print("🚀 Démarrage du menu principal...")
    
    # Fermer proprement toute fenêtre existante
    if current_window is not None:
        try:
            if current_window.winfo_exists():
                print("🗑️ Fermeture d'une fenêtre existante...")
                current_window.destroy()
        except:
            pass  # Ignorer les erreurs
        current_window = None
    
    # Créer une nouvelle fenêtre pour le menu
    menu_window = tk.Tk()
    current_window = menu_window  # Mise à jour de la référence globale
    
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
        
        # Réinitialiser l'état global et cacher la fenêtre
        try:
            # Cacher la fenêtre immédiatement pour feedback visuel
            if local_window.winfo_exists():
                local_window.withdraw()
            
            # Réinitialiser l'état global 
            app_running = False
            
            # Fonction pour lancer le jeu de façon différée
            def safe_start_game():
                global current_window  # Déclarer la variable comme globale ici aussi
                try:
                    # Détruire la fenêtre du menu
                    if local_window.winfo_exists():
                        local_window.destroy()
                    
                    # Effacer la référence globale
                    if current_window == local_window:
                        current_window = None
                        
                    # Lancer le jeu
                    print("🔄 Lancement du jeu...")
                    start_game(game_mode_copy, ai_level_copy)
                except Exception as e:
                    print(f"❌ Erreur lors du lancement du jeu: {e}")
                    global app_running  # Déclarer app_running comme globale
                    app_running = False
                    
            # Utiliser after_idle pour attendre que Tk ait fini de traiter les événements
            local_window.after_idle(safe_start_game)
            
        except Exception as e:
            print(f"❌ Erreur pendant la transition menu -> jeu: {e}")
            app_running = False
    
    # Créer le menu avec callback vers start_game
    menu = EnhancedGameMenu(
        master=menu_window,
        on_game_start=start_game_callback
    )
    
    # Configurer et lancer le menu
    menu.setup_ui()
    menu_window.protocol("WM_DELETE_WINDOW", lambda: exit_app(menu_window))
    menu_window.mainloop()

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

if __name__ == "__main__":
    print("🎮 Lancement du jeu Tic Tac Toe Ultra-Moderne...")
    print("📁 Architecture modulaire chargée")
    print("🎨 Effets visuels et animations activés")
    print("🚀 Démarrage du menu principal avec drag & drop...")
    print("-" * 50)
    main()
