import random
from nicegui import ui
from theme import ACCENT_COLOR, ACCENT_LIGHT, ACCENT_ICON

# --- global variables ---
choices = ["r", "p", "s"]
labels = {"r": "Rock", "p": "Paper", "s": "Scissors"}

# --- page layout ---
@ui.page("/rock-paper-scissors")
def rps_page():
    score = {"wins": 0, "losses": 0, "ties": 0} 

    # --- game logic ---
    def play(user_choice: str):
        computer_choice = random.choice(choices)
        choice_label.text = f"You chose {labels[user_choice]} — Computer chose {labels[computer_choice]}"

        if user_choice == computer_choice:
            result_label.text = "It's a tie!"
            result_label.classes(replace="text-2xl font-bold text-yellow-500")
            score["ties"] += 1
        elif (
            (user_choice == "r" and computer_choice == "s")
            or (user_choice == "p" and computer_choice == "r")
            or (user_choice == "s" and computer_choice == "p")
        ):
            result_label.text = "You win!"
            result_label.classes(replace="text-2xl font-bold text-green-500")
            score["wins"] += 1
        else:
            result_label.text = "Computer wins!"
            result_label.classes(replace="text-2xl font-bold text-red-500")
            score["losses"] += 1

        score_label.text = f"Wins: {score['wins']}  |  Losses: {score['losses']}  |  Ties: {score['ties']}"

    ui.query(".nicegui-content").classes("p-0")

    with ui.column().classes(
        f"items-center justify-center gap-4 p-4 w-full h-screen bg-{ACCENT_LIGHT}"
    ):
        ui.label("Rock Paper Scissors").classes(f"text-4xl font-bold mb-2 text-{ACCENT_COLOR}")

        with ui.row().classes("gap-4"):
            ui.button("Rock", on_click=lambda: play("r")).props("size=lg")
            ui.button("Paper", on_click=lambda: play("p")).props("size=lg")
            ui.button("Scissors", on_click=lambda: play("s")).props("size=lg")

        choice_label = ui.label("").classes("text-lg")
        result_label = ui.label("").classes("text-2xl font-bold")
        score_label = ui.label("Wins: 0  |  Losses: 0  |  Ties: 0").classes("text-base text-gray-500")

        # Back to home link
        ui.link("<- Back to Game Hub", "/").classes("text-base text-blue-500 hover:underline mt-2")


# --- run the app ---
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Rock Paper Scissors")