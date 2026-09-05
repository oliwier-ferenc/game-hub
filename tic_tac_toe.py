import random
from nicegui import ui
from theme import ACCENT_COLOR, ACCENT_LIGHT, ACCENT_ICON

# --- global variables ---
board = [None] * 9          
human_symbol = "X"          
computer_symbol = "O"              
score = {"wins": 0, "losses": 0, "ties": 0}

# --- game logic ---
WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def check_winner(board):
    for a, b, c in WIN_COMBOS:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_tie(board):
    return all(cell is not None for cell in board)

def find_winning_move(board, symbol):
    for a, b, c in WIN_COMBOS:
        cells = [board[a], board[b], board[c]]
        indices = [a, b, c]
        # A winning move exists in this combo if two cells already have our symbol and the third is still empty.
        if cells.count(symbol) == 2 and cells.count(None) == 1:
            empty_index = indices[cells.index(None)]
            return empty_index
    return None

def end_of_turn():
    winner = check_winner(board)
    if winner:
        status_label.text = f"{winner} wins!"
        for btn in cell_buttons:
            btn.disable()
        if winner == human_symbol:
            score["wins"] += 1
        else:
            score["losses"] += 1
        update_score_label()
        return True
 
    if is_tie(board):
        status_label.text = "It's a tie!"
        for btn in cell_buttons:
            btn.disable()
        score["ties"] += 1
        update_score_label()
        return True
 
    return False

def update_score_label():
    score_label.text = f"Wins: {score['wins']} | Losses: {score['losses']} | Ties: {score['ties']}"

def reset_board():
    global board
    board = [None] * 9
    for btn in cell_buttons:
        btn.text = ""
        btn.enable()
    status_label.text = f"Your turn ({human_symbol})"

def make_move(index):
    if board[index] is not None:
        return  # Reject click on cells which are already taken

    # Human's move 
    board[index] = human_symbol
    cell_buttons[index].text = human_symbol
    cell_buttons[index].disable() # can't click it again

    if end_of_turn():
        return # If Human's move ended the game, don't let the computer play
    
    # Computer's turn
    # Priority: 1. Winning move, 2. Blocking move, 3. Center, 4. Random empty cell
    empty_cells = [i for i, cell in enumerate(board) if cell is None]

    winning_move = find_winning_move(board, computer_symbol)
    blocking_move = find_winning_move(board, human_symbol)

    if winning_move is not None:
        computer_choice = winning_move
    elif blocking_move is not None:
        computer_choice = blocking_move
    elif 4 in empty_cells:
        computer_choice = 4
    else:
        computer_choice = random.choice(empty_cells)

    board[computer_choice] = computer_symbol
    cell_buttons[computer_choice].text = computer_symbol
    cell_buttons[computer_choice].disable()

    if end_of_turn():
        return # If Computer's move ended the game, don't update the status for human's turn    

    # if neither move ended the game, let the player know it's their turn again
    status_label.text = f"Your turn ({human_symbol})"

# --- page layout ---
@ui.page("/tic-tac-toe")
def tic_tac_toe_page():
    global cell_buttons, status_label, score_label

    cell_buttons = []

    ui.query(".nicegui-content").classes("p-0")

    with ui.column().classes(
        f"items-center justify-center gap-4 p-4 w-full min-h-screen bg-{ACCENT_LIGHT}"
    ):
        ui.label("Tic-Tac-Toe").classes(f"text-4xl font-bold mb-2 text-{ACCENT_COLOR}")

        status_label = ui.label(f"Your turn ({human_symbol})").classes("text-lg font-semibold")

        # the tic-tac-toe grid
        with ui.grid(columns=3).classes("gap-2"):
            for index in range(9):
                btn = ui.button("", on_click=lambda i=index: make_move(i)).classes("w-16 h-16 text-2xl").props("size=lg square")
                cell_buttons.append(btn)

        score_label = ui.label(
            f"Wins: {score['wins']} | Losses: {score['losses']} | Ties: {score['ties']}"
        ).classes("text-lg font-semibold")

        ui.button("Reset Game", on_click=reset_board).props("outline").classes("mt-4")

        # Back to home link
        ui.link("<- Back to Game Hub", "/").classes("text-base text-blue-500 hover:underline mt-2")

# --- run the app ---
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Tic-Tac-Toe")