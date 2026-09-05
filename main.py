from nicegui import ui
import os
from games.rps_game import rps_page
from games.tic_tac_toe import tic_tac_toe_page
from theme import ACCENT_COLOR, ACCENT_LIGHT, ACCENT_ICON

# browser icons: https://fonts.google.com/icons?icon.size=24&icon.color=%23e3e3e3

# --- home page ---
@ui.page("/")
def home_page():

    # --- page layout ---
    ui.query(".nicegui-content").classes("p-0")

    with ui.column().classes(
        f"items-center justify-center gap-4 p-4 w-full h-screen bg-{ACCENT_LIGHT} rounded-lg shadow-md"
    ):
        ui.label("Game Hub").classes(f"text-5xl font-bold mb-2 text-{ACCENT_COLOR}")
        ui.label("Welcome to the Game Hub! Choose a game to play.").classes("text-lg text-gray-600 mb-4")

        # --- game cards ---
        with ui.row().classes("justify-center gap-4"):

        ## Rock Paper Scissors card
            with ui.card().classes("cursor-pointer p-4 hover:shadow-lg").on("click", lambda: ui.navigate.to("/rock-paper-scissors")):
                with ui.column().classes("items-center gap-2"):
                    ui.icon("videogame_asset").classes(f"text-4xl text-{ACCENT_ICON}")
                    ui.label("Rock Paper Scissors")

        ## Tic Tac Toe card
            with ui.card().classes("cursor-pointer p-4 hover:shadow-lg").on("click", lambda: ui.navigate.to("/tic-tac-toe")):
                    with ui.column().classes("items-center gap-2"):
                        ui.icon("grid_on").classes(f"text-4xl text-{ACCENT_ICON}")  
                        ui.label("Tic Tac Toe") 

        ## Placeholder card
            #with ui.card().classes("cursor-pointer p-4 hover:shadow-lg").on("click", lambda: ui.navigate.to("/placeholder")):
             #       with ui.column().classes("items-center gap-2"):
              #          ui.icon("casino").classes(f"text-4xl text-{ACCENT_ICON}")  
               #         ui.label("Placeholder Game")


# --- run the app ---
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Game Hub", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))