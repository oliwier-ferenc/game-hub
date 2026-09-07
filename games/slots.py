import random 
import asyncio
import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from nicegui import ui
from theme import ACCENT_COLOR, ACCENT_LIGHT, ACCENT_ICON

# --- global variables ---
SYMBOLS = ["🍒", "🍋", "🍉", "⭐", "💎"]

# Determine how comomn each symbol is. More common symbols should have a higher count.
SYMBOL_COUNT = {
    "🍒": 6,
    "🍋": 5,
    "🍉": 4,
    "⭐": 3,
    "💎": 2,
}

# Determine the payout for each symbol. Higher value symbols should have a higher payout.
SYMBOL_VALUE = {
    "🍒": 2,
    "🍋": 3,
    "🍉": 4,
    "⭐": 6,
    "💎": 20
}


def get_random_symbol():
    all_symbols = []
    for symbol, count in SYMBOL_COUNT.items():
        all_symbols.extend([symbol] * count)
    return random.choice(all_symbols)


def spin_reels():
    return [get_random_symbol() for _ in range(3)]

# Payout calculation: If all three symbols match, the payout is the bet multiplied by the symbol's value.
# If two symbols match, the payout is the bet. Otherwise, the payout is 0.
def get_payout(reels, bet):
    if reels[0] == reels[1] == reels[2]:
        multiplier = SYMBOL_VALUE[reels[0]]
        return bet * multiplier
    elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
        return bet 
    return 0

@ui.page("/slots")
def slots_page():
    balance = 250
    current_reels = ["🍒", "🍒", "🍒"]

    def validate_bet():
        value = bet_input.value

        # Check if the value is None or empty
        if value is None or value == "":
            return False

        try:
            bet = int(value)
        except(ValueError, TypeError):
            result_label.text = "Please enter a valid number."
            return False

        # Check if the bet is less than or equal to zero
        if bet <= 0:
            return False 

        # Check if the bet is greater than the balance
        if bet > balance:
            result_label.text = "Insufficient balance!"
            return False

        return True

    def update_spin_button_state():
        if validate_bet():
            spin_button.enable()
        else:
            spin_button.disable()

    async def spin():
        nonlocal balance, current_reels

        try:
            bet = int(bet_input.value)
        except (ValueError, TypeError): 
            result_label.text = "Please enter a valid number."
            update_spin_button_state()
            return

        # Extra validation for bet amount
        if bet <= 0:
            result_label.text = "Bet must be greater than 0!"
            update_spin_button_state()
            return

        if bet > balance:
            result_label.text = "Insufficient balance!"
            update_spin_button_state()
            return

        # Deduct bet and lock controls during spin
        spin_button.disable()
        bet_input.disable()
        balance -= bet
        balance_label.text = f"Balance: ${balance}"

        # Generate results for the spin
        final_reels = spin_reels()

        # Run roll animation with staggered stops
        for i in range(20):  # Number of animation frames
            if i < 10:
                reel_1.text = random.choice(SYMBOLS)
            else:
                reel_1.text = final_reels[0]

            if i < 15:
                reel_2.text = random.choice(SYMBOLS)
            else:
                reel_2.text = final_reels[1]

            reel_3.text = random.choice(SYMBOLS) if i < 18 else final_reels[2]

            await asyncio.sleep(0.08)  # Delay for animation effect

        # Set final reels and update UI
        current_reels = final_reels
        reel_1.text = current_reels[0]
        reel_2.text = current_reels[1]
        reel_3.text = current_reels[2]

        # Calculate payout and update balance
        payout = get_payout(current_reels, bet)
        balance += payout

        if payout > 0:
            if current_reels[0] == current_reels[1] == current_reels[2]:
                multiplier = SYMBOL_VALUE[current_reels[0]]
                result_label.text = f"Jackpot! You won ${payout}!"
                result_label.classes(replace="text-2xl font-bold text-green-500")
            else:
                result_label.text = f"Two of a kind! You won ${payout}!"
                result_label.classes(replace="text-2xl font-bold text-yellow-500")
        else:
            result_label.text = "No win this time. Try again!"

        # Automatic bankrupt reset
        if balance <= 0:
            balance = 250
            result_label.text = "Bankrupt! Auto-reset back to $250."
            result_label.classes(replace="text-2xl font-bold text-red-500")

        # Reset UI state
        balance_label.text = f"Balance: ${balance}"

        # Clear and reenable input
        bet_input.set_value(0) 
        spin_button.enable()
        bet_input.enable()

        # Refresh button state for next turn
        update_spin_button_state() 
        
        
    # --- page layout ---
    ui.query(".nicegui-content").classes("p-0")

    with ui.column().classes(
        f"items-center justify-center gap-4 p-4 w-full h-screen bg-{ACCENT_LIGHT}"
    ):
        ui.label("Slot Machine").classes(f"text-4xl font-bold mb-2 text-{ACCENT_COLOR}")

        balance_label = ui.label(f"Balance: ${balance}").classes("text-lg font-bold")

        with ui.row().classes("gap-4"):
            reel_1 = ui.label(current_reels[0]).classes("text-6xl")
            reel_2 = ui.label(current_reels[1]).classes("text-6xl")
            reel_3 = ui.label(current_reels[2]).classes("text-6xl")

        result_label = ui.label("").classes("text-lg font-semibold text-center")

        bet_input = ui.number(
            label = "Bet amount ($)",
            placeholder = "Enter your bet",
            min = 1,
            step = 1,
            format = "%.0f",
            on_change = update_spin_button_state,
        ).props("outlined")

        spin_button = ui.button("Spin", on_click=spin).props("size=lg")

        # Start disabled until a valid bet is entered
        spin_button.disable()

        # Back to home link
        ui.link("<- Back to Game Hub", "/").classes("text-base text-blue-500 hover:underline mt-2")


# --- run the app ---
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Slots")