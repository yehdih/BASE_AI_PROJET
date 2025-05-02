import streamlit as st
import math
import time
import random

st.set_page_config(
    page_title="Morpion",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.board-button {
    width: 100%;
    height: 100px;
    font-size: 50px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #1e3a8a;
}
.stButton button {
    height: 100px;
    width: 100%;
    font-size: 40px !important;
    background-color: #f8fafc;
    border: 2px solid #cbd5e1;
    border-radius: 8px;
    transition: all 0.3s ease;
}
.stButton button:hover {
    background-color: #e2e8f0;
    transform: scale(1.02);
}
.game-status {
    font-size: 28px;
    font-weight: bold;
    margin: 20px 0;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.win {
    background-color: #d1fae5;
    color: #065f46;
    animation: pulse 1.5s infinite;
}
.draw {
    background-color: #fef3c7;
    color: #92400e;
}
.sidebar-content {
    padding: 20px 0;
}
.centered-text {
    text-align: center;
}
.score-display {
    font-size: 20px;
    margin-bottom: 25px;
    padding: 15px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-left: 5px solid #0ea5e9;
}
.header-container {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #e2e8f0;
}
.game-title {
    font-size: 42px;
    font-weight: bold;
    color: #1e3a8a;
    margin-bottom: 10px;
}
.game-subtitle {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 20px;
}
.player-x {
    color: #dc2626;
}
.player-o {
    color: #2563eb;
}
.game-board {
    background-color: #f8fafc;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    margin-bottom: 30px;
}
.info-section {
    background-color: #f8fafc;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    margin-top: 30px;
}
.info-header {
    font-size: 24px;
    color: #1e3a8a;
    margin-bottom: 15px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 10px;
}
.move-history {
    max-height: 250px;
    overflow-y: auto;
    padding: 10px;
    background-color: #f1f5f9;
    border-radius: 8px;
}
.move-history ul {
    margin-bottom: 0;
}
.move-history li {
    padding: 5px 0;
    border-bottom: 1px dashed #e2e8f0;
}
.move-history li:last-child {
    border-bottom: none;
}
.difficulty-badge {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    margin-left: 8px;
}
.difficulty-easy {
    background-color: #dcfce7;
    color: #166534;
}
.difficulty-medium {
    background-color: #fef3c7;
    color: #92400e;
}
.difficulty-hard {
    background-color: #fee2e2;
    color: #991b1b;
}
.settings-label {
    font-weight: bold;
    color: #475569;
    margin-bottom: 5px;
}
.action-button {
    width: 100%;
    margin-top: 10px;
}
@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.4);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(5, 150, 105, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(5, 150, 105, 0);
    }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.fade-in {
    animation: fadeIn 0.5s ease-in;
}
.x-mark {
    color: #dc2626;
    font-weight: bold;
}
.o-mark {
    color: #2563eb;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]

if 'game_over' not in st.session_state:
    st.session_state.game_over = False
    
if 'ai_thinking' not in st.session_state:
    st.session_state.ai_thinking = False
    
if 'winner' not in st.session_state:
    st.session_state.winner = None
    
if 'human_score' not in st.session_state:
    st.session_state.human_score = 0
    
if 'ai_score' not in st.session_state:
    st.session_state.ai_score = 0
    
if 'draws' not in st.session_state:
    st.session_state.draws = 0
    
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Difficile"
    
if 'player_mark' not in st.session_state:
    st.session_state.player_mark = "O"
    
if 'ai_goes_first' not in st.session_state:
    st.session_state.ai_goes_first = False
    
if 'move_history' not in st.session_state:
    st.session_state.move_history = []

def get_player_marks():
    if st.session_state.player_mark == "X":
        return {"HUMAIN": "X", "IA": "O"}
    else:
        return {"HUMAIN": "O", "IA": "X"}

def verifier_gagnant(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    
    return None

def est_plein(board):
    return all(cell != "" for row in board for cell in row)

def coups_disponibles(board):
    coups = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                coups.append((i, j))
    return coups

def minimax(board, depth, alpha, beta, is_maximizing):
    marks = get_player_marks()
    IA = marks["IA"]
    HUMAIN = marks["HUMAIN"]
    
    gagnant = verifier_gagnant(board)
    if gagnant == IA:
        return 10 - depth
    elif gagnant == HUMAIN:
        return depth - 10
    elif est_plein(board):
        return 0
        
    max_depth = 9
    if st.session_state.difficulty == "Facile":
        max_depth = 1
    elif st.session_state.difficulty == "Moyen":
        max_depth = 3
        
    if depth >= max_depth:
        return 0
        
    if is_maximizing:
        meilleur_score = -math.inf
        for i, j in coups_disponibles(board):
            board[i][j] = IA
            score = minimax(board, depth + 1, alpha, beta, False)
            board[i][j] = ""
            meilleur_score = max(score, meilleur_score)
            alpha = max(alpha, meilleur_score)
            if beta <= alpha:
                break
        return meilleur_score
    else:
        meilleur_score = math.inf
        for i, j in coups_disponibles(board):
            board[i][j] = HUMAIN
            score = minimax(board, depth + 1, alpha, beta, True)
            board[i][j] = ""
            meilleur_score = min(score, meilleur_score)
            beta = min(beta, meilleur_score)
            if beta <= alpha:
                break
        return meilleur_score

def meilleur_coup():
    marks = get_player_marks()
    IA = marks["IA"]
    
    if st.session_state.difficulty == "Facile":
        if random.random() < 0.5:
            coups = coups_disponibles(st.session_state.board)
            if coups:
                return random.choice(coups)
    elif st.session_state.difficulty == "Moyen":
        if random.random() < 0.2:
            coups = coups_disponibles(st.session_state.board)
            if coups:
                return random.choice(coups)
    
    meilleur_score = -math.inf
    coup = None
    
    for i, j in coups_disponibles(st.session_state.board):
        st.session_state.board[i][j] = IA
        score = minimax(st.session_state.board, 0, -math.inf, math.inf, False)
        st.session_state.board[i][j] = ""
        
        if st.session_state.difficulty != "Difficile":
            score += random.uniform(-0.1, 0.1)
            
        if score > meilleur_score:
            meilleur_score = score
            coup = (i, j)
    
    return coup

def faire_jouer_ia():
    if not st.session_state.game_over and not est_plein(st.session_state.board):
        st.session_state.ai_thinking = True

def executer_coup_ia():
    if st.session_state.ai_thinking:
        marks = get_player_marks()
        IA = marks["IA"]
        
        time.sleep(0.5)
        
        ia_coup = meilleur_coup()
        if ia_coup:
            i, j = ia_coup
            st.session_state.board[i][j] = IA
            st.session_state.move_history.append((i, j, IA))
        
        verifier_etat_jeu()
        st.session_state.ai_thinking = False
        st.rerun()

def verifier_etat_jeu():
    gagnant = verifier_gagnant(st.session_state.board)
    if gagnant:
        st.session_state.winner = gagnant
        st.session_state.game_over = True
        marks = get_player_marks()
        if gagnant == marks["HUMAIN"]:
            st.session_state.human_score += 1
        else:
            st.session_state.ai_score += 1
    elif est_plein(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.draws += 1

def redemarrer_jeu():
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.ai_thinking = False
    st.session_state.move_history = []
    
    if st.session_state.ai_goes_first:
        faire_jouer_ia()

def changer_premier_joueur():
    st.session_state.ai_goes_first = not st.session_state.ai_goes_first
    redemarrer_jeu()

def reinitialiser_scores():
    st.session_state.human_score = 0
    st.session_state.ai_score = 0
    st.session_state.draws = 0

def changer_symbole():
    st.session_state.player_mark = "X" if st.session_state.player_mark == "O" else "O"
    redemarrer_jeu()

with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>Paramètres du Jeu</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<p class='settings-label'>Difficulté</p>", unsafe_allow_html=True)
    difficulty_fr = {"Facile": "Facile", "Moyen": "Moyen", "Difficile": "Difficile"}
    difficulty_en = {"Facile": "Easy", "Moyen": "Medium", "Difficile": "Hard"}
    
    difficulte = st.selectbox(
        "",
        ["Facile", "Moyen", "Difficile"],
        index=["Facile", "Moyen", "Difficile"].index(st.session_state.difficulty if st.session_state.difficulty in difficulty_fr.values() else difficulty_fr[st.session_state.difficulty]),
        label_visibility="collapsed"
    )
    
    difficulty_colors = {
        "Facile": "difficulty-easy",
        "Moyen": "difficulty-medium",
        "Difficile": "difficulty-hard"
    }
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="difficulty-badge {difficulty_colors[difficulte]}">{difficulte}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if difficulte != st.session_state.difficulty:
        st.session_state.difficulty = difficulte
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<p class='settings-label'>Jouer en tant que</p>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    with cols[0]:
        x_selected = st.session_state.player_mark == "X"
        if st.button("X", use_container_width=True, type="primary" if x_selected else "secondary"):
            if not x_selected:
                st.session_state.player_mark = "X"
                redemarrer_jeu()
    with cols[1]:
        o_selected = st.session_state.player_mark == "O"
        if st.button("O", use_container_width=True, type="primary" if o_selected else "secondary"):
            if not o_selected:
                st.session_state.player_mark = "O"
                redemarrer_jeu()
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<p class='settings-label'>Qui commence</p>", unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        human_first = not st.session_state.ai_goes_first
        if st.button("Vous", use_container_width=True, type="primary" if human_first else "secondary"):
            if not human_first:
                st.session_state.ai_goes_first = False
                redemarrer_jeu()
    with cols[1]:
        ai_first = st.session_state.ai_goes_first
        if st.button("IA", use_container_width=True, type="primary" if ai_first else "secondary"):
            if not ai_first:
                st.session_state.ai_goes_first = True
                redemarrer_jeu()
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    if st.button("🔄 Réinitialiser Scores", use_container_width=True):
        reinitialiser_scores()
    
    if st.button("🎮 Nouvelle Partie", use_container_width=True, type="primary"):
        redemarrer_jeu()
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="header-container fade-in">
    <h1 class="game-title">🎮 Morpion</h1>
    <p class="game-subtitle">Défiez l'IA dans ce jeu classique de stratégie</p>
</div>
""", unsafe_allow_html=True)

player_mark_class = "player-x" if st.session_state.player_mark == "X" else "player-o"
ai_mark_class = "player-o" if st.session_state.player_mark == "X" else "player-x"
ai_mark = "O" if st.session_state.player_mark == "X" else "X"

st.markdown(f"""
<div class="score-display fade-in">
    <b>Vous (<span class="{player_mark_class}">{st.session_state.player_mark}</span>):</b> {st.session_state.human_score} &nbsp;|&nbsp;
    <b>IA (<span class="{ai_mark_class}">{ai_mark}</span>):</b> {st.session_state.ai_score} &nbsp;|&nbsp;
    <b>Égalités:</b> {st.session_state.draws}
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="game-board fade-in">', unsafe_allow_html=True)

for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        cell_value = st.session_state.board[i][j]
        
        if cell_value == "":
            if not st.session_state.game_over and not st.session_state.ai_thinking:
                if cols[j].button(" ", key=f"{i}-{j}", use_container_width=True):
                    marks = get_player_marks()
                    HUMAIN = marks["HUMAIN"]
                    
                    st.session_state.board[i][j] = HUMAIN
                    st.session_state.move_history.append((i, j, HUMAIN))
                    
                    verifier_etat_jeu()
                    
                    if not st.session_state.game_over:
                        faire_jouer_ia()
            else:
                cols[j].button(" ", key=f"{i}-{j}", disabled=True, use_container_width=True)
        else:
            mark_class = "x-mark" if cell_value == "X" else "o-mark"
            cols[j].markdown(f"""
            <div class="board-button">
                <span class="{mark_class}">{cell_value}</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.ai_thinking:
    executer_coup_ia()

if st.session_state.game_over:
    if st.session_state.winner:
        marks = get_player_marks()
        if st.session_state.winner == marks["HUMAIN"]:
            winner_text = "Vous avez gagné! 🎉"
            status_class = "win"
        else:
            winner_text = "L'IA a gagné! 🤖"
            status_class = "win"
        st.markdown(f"""
        <div class="game-status {status_class} fade-in">
            {winner_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="game-status draw fade-in">
            Match nul! 🤝
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Informations de Jeu")

if st.session_state.move_history:
    move_history_text = "<ul>"
    for idx, (row, col, mark) in enumerate(st.session_state.move_history):
        player = "Humain" if mark == st.session_state.player_mark else "IA"
        move_history_text += f"<li>Coup {idx+1}: {player} ({mark}) placé à la position ({row+1}, {col+1})</li>"
    move_history_text += "</ul>"
    
    with st.expander("Historique des Coups"):
        st.markdown(move_history_text, unsafe_allow_html=True)

difficulty_info = {
    "Facile": "L'IA fait parfois des coups aléatoires et a une anticipation limitée.",
    "Moyen": "L'IA fait moins d'erreurs et a une anticipation modérée.",
    "Difficile": "L'IA joue de façon optimale en utilisant l'algorithme minimax avec élagage alpha-bêta."
}

with st.expander("Comment Jouer"):
    st.markdown("""
    1. Le but et d'aligner trois de vos symboles (horizontalement, verticalement ou en diagonale).
    2. Vous et l'IA jouez à tour de rôle.
    3. Le premier joueur à aligner trois symboles gagne.
    4. Si toutes les cases sont remplies et personne n'a gagné, c'est un match nul.
    
    **Difficulté actuelle:** {} - {}
    
    Vous pouvez modifier les paramètres dans la barre latérale pour ajuster la difficulté, choisir votre symbole ou décider qui commence.
    """.format(st.session_state.difficulty, difficulty_info[st.session_state.difficulty]))

if st.session_state.ai_goes_first and len(st.session_state.move_history) == 0 and not st.session_state.game_over and not st.session_state.ai_thinking:
    faire_jouer_ia()
    st.rerun()
