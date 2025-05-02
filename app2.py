# Jeu de Morpion (Tic Tac Toe) avec un Agent IA utilisant l'algorithme Minimax
# Ce code implémente un jeu de Morpion (Tic Tac Toe) où un joueur humain joue contre un Agent intelligent .
# L'Agent utilise l'algorithme Minimax pour déterminer le meilleur coup à jouer.

import tkinter as tk
import random

"""Cette classe représente le jeu de Morpion
   Elle gère l'état du jeu, les mouvements des joueurs et l'algorithme Minimax.
"""
class Morpion:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Jeu de morpion avec IA")
        self.largeur = 400
        self.hauteur = 500

        self.fenetre.geometry(f"{self.largeur}x{self.hauteur}")
        self.tableau = [['-' for _ in range(3)] for _ in range(3)]
        self.joueur_humain = 'X'
        self.joueur_ia = 'O'
        self.current_joueur = random.choice([self.joueur_humain, self.joueur_ia])
        self.jeu_en_cours = True

        self.label_message = tk.Label(self.fenetre, text="Jouez votre tour !", font=("Arial", 14))
        self.label_message.pack(pady=10)

        self.cadre_grille = tk.Frame(self.fenetre)
        self.cadre_grille.pack(pady=20)

        self.boutons = [[None for _ in range(3)] for _ in range(3)]
        self.creer_interface()

        self.bouton_rejouer = tk.Button(self.fenetre, text="Jouer encore", font=("Arial", 12), command=self.reinitialiser_jeu)
        self.bouton_rejouer.pack(pady=10)
        self.bouton_rejouer.config(state=tk.DISABLED)

    def creer_interface(self):
        for i in range(3):
            for j in range(3):
                bouton = tk.Button(self.cadre_grille, text=" ", font=("Arial", 16), width=5, height=2,
                                   command=lambda i=i, j=j: self.jouer(i, j))
                bouton.grid(row=i, column=j)
                self.boutons[i][j] = bouton

    def verifier_si_a_gagne(self, joueur):
        for i in range(3):
            if all(self.tableau[i][j] == joueur for j in range(3)) or all(self.tableau[j][i] == joueur for j in range(3)):
                return True
        if all(self.tableau[i][i] == joueur for i in range(3)) or all(self.tableau[i][2 - i] == joueur for i in range(3)):
            return True
        return False

    def est_rempli(self):
        return all(case != '-' for ligne in self.tableau for case in ligne)

    def algorithme_minimax(self, profondeur, est_max):
        if self.verifier_si_a_gagne(self.joueur_ia):
            return 10 - profondeur
        if self.verifier_si_a_gagne(self.joueur_humain):
            return -10 + profondeur
        if self.est_rempli():
            return 0

        if est_max:
            meilleur_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.tableau[i][j] == "-":
                        self.tableau[i][j] = self.joueur_ia
                        score = self.algorithme_minimax(profondeur + 1, False)
                        self.tableau[i][j] = "-"
                        meilleur_score = max(meilleur_score, score)
            return meilleur_score
        else:
            meilleur_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.tableau[i][j] == "-":
                        self.tableau[i][j] = self.joueur_humain
                        score = self.algorithme_minimax(profondeur + 1, True)
                        self.tableau[i][j] = "-"
                        meilleur_score = min(meilleur_score, score)
            return meilleur_score

    def meilleur_coup(self):
        meilleur_score = -float('inf')
        coup = (-1, -1)

        # Vérifier si l'adversaire peut gagner et bloquer (faire un coup défensif : fonctionnalité demandé dans l'énoncé)
        for i in range(3):
            for j in range(3):
                if self.tableau[i][j] == '-':
                    self.tableau[i][j] = self.joueur_humain
                    if self.verifier_si_a_gagne(self.joueur_humain):
                        self.tableau[i][j] = self.joueur_ia
                        return (i, j)
                    self.tableau[i][j] = '-'

        # Si pas besoin de bloquer, utiliser Minimax
        for i in range(3):
            for j in range(3):
                if self.tableau[i][j] == '-':
                    self.tableau[i][j] = self.joueur_ia
                    score = self.algorithme_minimax(0, False)
                    self.tableau[i][j] = '-'
                    if score > meilleur_score:
                        meilleur_score = score
                        coup = (i, j)
        return coup

    def jouer(self, i, j):
        if self.jeu_en_cours and self.tableau[i][j] == '-':
            self.tableau[i][j] = self.joueur_humain
            self.boutons[i][j].config(text=self.joueur_humain)

            if self.verifier_si_a_gagne(self.joueur_humain):
                self.fin_partie("Vous avez gagné !")
                return
            elif self.est_rempli():
                self.fin_partie("Match nul !")
                return

            self.current_joueur = self.joueur_ia
            self.fenetre.after(500, self.tour_ia)

    def tour_ia(self):
        if self.jeu_en_cours:
            i, j = self.meilleur_coup()
            self.tableau[i][j] = self.joueur_ia
            self.boutons[i][j].config(text=self.joueur_ia)

            if self.verifier_si_a_gagne(self.joueur_ia):
                self.fin_partie("L'agent a gagné !")
            elif self.est_rempli():
                self.fin_partie("Match nul !")

            self.current_joueur = self.joueur_humain

    def fin_partie(self, message):
        self.label_message.config(text=message)
        self.jeu_en_cours = False
        self.bouton_rejouer.config(state=tk.NORMAL)

    def reinitialiser_jeu(self):
        self.tableau = [['-' for _ in range(3)] for _ in range(3)]
        self.jeu_en_cours = True
        self.label_message.config(text="Jouez votre tour !")
        self.bouton_rejouer.config(state=tk.DISABLED)
        for i in range(3):
            for j in range(3):
                self.boutons[i][j].config(text=" ")

    def demarrer_jeu(self):
        self.fenetre.mainloop()

# Lancer le jeu en création une instance de la classe morpion
morpion = Morpion()
morpion.demarrer_jeu()

