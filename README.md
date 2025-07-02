# 🎮 Jeu de Tic Tac Toe Deluxe Ultra-Moderne

Un jeu de Tic Tac Toe (Morpion) sophistiqué avec interface graphique ultra-moderne développé en Python avec tkinter.

## ✨ Nouvelles fonctionnalités révolutionnaires

- 🎮 **Menu interactif avec drag & drop** : Glissez-déposez les modes de jeu pour une expérience unique
- 🤖 **Intelligence artificielle avancée** : Affrontez une IA avec 3 niveaux de difficulté (Facile, Moyen, Difficile)
- 🖥️ **Mode plein écran automatique** : Expérience immersive dès le lancement
- 🎨 **Effets visuels spectaculaires** : Animations de particules, transitions fluides, effets hover
- 🎯 **Interface ultra-réactive** : Boutons qui réagissent au survol avec des animations
- 📱 **Design responsive** : S'adapte parfaitement à toutes les tailles d'écran
- ✨ **Animations partout** : Chaque interaction est accompagnée d'effets visuels

## 📁 Structure du projet

```
tic_tac_toe/
├── main.py                # Point d'entrée principal avec gestionnaire d'application
├── README.md              # Documentation du projet
├── src/                   # Code source principal
│   ├── __init__.py        # Initialisation du package
│   ├── game.py            # Logique du jeu
│   ├── modern_ui.py       # Interface de jeu ultra-moderne
│   ├── enhanced_menu.py   # Menu principal avec drag & drop
│   ├── ai.py              # Intelligence artificielle pour le jeu
│   ├── ui.py              # Interface utilisateur classique
│   └── utils.py           # Fonctions utilitaires
└── config/                # Configuration
    └── settings.py        # Paramètres du jeu, couleurs, animations
```

## 🚀 Comment jouer

1. **Lancez le jeu** en exécutant `python main.py`
2. **Menu interactif** : 
   - Glissez une carte de mode (🤖 JOUEUR vs IA ou 👥 JOUEUR vs JOUEUR) 
   - Déposez-la dans la zone "🚀 GLISSEZ ICI POUR COMMENCER"
   - Le jeu se lance automatiquement avec le mode choisi !
3. **Mode Joueur vs IA** :
   - Vous jouez les X, l'IA joue les O
   - L'IA adapte son temps de réflexion selon le niveau choisi
   - Animations spéciales quand l'IA réfléchit
4. **Mode Joueur vs Joueur** :
   - Deux joueurs s'affrontent alternativement (X et O)
   - Cliquez sur une case vide pour placer votre symbole
5. **Objectif** : Le premier à aligner 3 symboles (horizontalement, verticalement ou diagonalement) gagne
6. **Commandes** :
   - **Échap** : Retourner au menu principal
   - **🏠 MENU** : Bouton pour revenir au menu
   - **🔄 Rejouer** : Recommencer une partie
   - **🔄 Reset Score** : Remettre les scores à zéro

## 🛠️ Fonctionnalités

- ✅ **Menu interactif avec drag & drop** : Sélection des modes par glisser-déposer
- ✅ **Intelligence artificielle multicouche** : 3 niveaux de difficulté avec algorithmes adaptatifs
- ✅ **Plein écran automatique** : Expérience immersive dès le lancement
- ✅ **Effets visuels spectaculaires** : Particules animées, transitions fluides, feedback visuel
- ✅ **Interface ultra-moderne** : Design sophistiqué avec palette de couleurs avancée
- ✅ **Animations de boutons** : Effets hover, scale, glow et pulsation
- ✅ **Interface responsive** : Adaptation automatique à toutes les résolutions
- ✅ **Système de scores** : Persistant pendant la session avec affichage dynamique
- ✅ **Détection intelligente** : Victoires et égalités avec mise en surbrillance
- ✅ **Architecture modulaire** : Code extensible et maintenable
- ✅ **Configuration centralisée** : Personnalisation facile des couleurs et paramètres
- ✅ **Navigation fluide** : Transitions entre menu et jeu avec animations

## 🎨 Personnalisation

Vous pouvez personnaliser l'apparence du jeu en modifiant le fichier `config/settings.py` :
- **Couleurs de l'interface** : Palette complète personnalisable
- **Animations** : Vitesse des particules, effets de boutons
- **IA** : Temps de réflexion par niveau, noms des niveaux
- **Menu** : Configuration du drag & drop, animations
- **Polices de caractères** : Tailles adaptatives selon la résolution
- **Messages affichés** : Textes de victoire, égalité, etc.

## 🤖 Intelligence Artificielle

L'IA propose 3 niveaux de difficulté :

- **🟢 FACILE** : Mouvements principalement aléatoires (0.5s de réflexion)
- **🟡 MOYEN** : Stratégie équilibrée avec blocage basique (1.0s de réflexion)  
- **🔴 DIFFICILE** : Algorithme minimax imbattable (2.0s de réflexion)

L'IA affiche des indicateurs visuels de réflexion et adapte son comportement selon le niveau choisi.

## 📋 Prérequis

- Python 3.6 ou supérieur
- tkinter (inclus par défaut avec Python)

## 🔧 Lancement

```bash
python main.py
```

## 👨‍💻 Architecture

Le projet suit une architecture modulaire avancée :

- **main.py** : Point d'entrée avec gestionnaire d'application et navigation entre menu/jeu
- **src/enhanced_menu.py** : Menu principal avec système de drag & drop et animations
- **src/modern_ui.py** : Interface de jeu ultra-moderne avec effets visuels avancés
- **src/ai.py** : Intelligence artificielle avec algorithme minimax et niveaux de difficulté
- **src/game.py** : Logique du jeu et détection des victoires
- **src/utils.py** : Fonctions utilitaires réutilisables
- **config/settings.py** : Configuration centralisée (couleurs, animations, IA, menu)

Cette architecture permet une **maintenance facile**, une **extensibilité maximale** et une **séparation claire des responsabilités**.

## 🎯 Expérience Utilisateur

- **Démarrage** : Plein écran automatique pour une immersion totale
- **Navigation** : Drag & drop intuitif pour la sélection des modes
- **Feedback** : Chaque action a un retour visuel (hover, clic, animations)
- **Transitions** : Passages fluides entre le menu et le jeu
- **Responsivité** : Interface qui s'adapte à toutes les tailles d'écran
- **Performance** : Animations optimisées pour une fluidité parfaite
