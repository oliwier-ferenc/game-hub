# Game Hub 

A small collection of browser-based games built with [NiceGUI](https://nicegui.io/), a python framework for building web UIs without writing HTML/CSS/JS.

**[Play it live here](https://game-hub-56g8.onrender.com)**

> Note: the free hosting tier sleeps after periods of inactivity - the first load after a while may take a minute to wake up.

## About this project:

This started as a way to learn Python and NiceGUI from scratch by building small, complete games one at a time, then combining them into a single hub with shared navigation and styling. It's a learning project, not a production app, but everything here works end to end.

## Games

- **Rock Paper Scissors:** The classic game against a random computer opponent, with win/loss/tie tracking.
- **Tic-Tac-Toe:** Play against a computer opponent that tries to win or block you, with a scoreboard and reset button.
- **Slots:** Play an animated fruit slot machine with variable symbol payouts and bankruptcy protection.

**More features are in progress.**

## Tech stack

- Python
- [NiceGUI](https://nicegui.io/) for the UI
- Hosted on [Render](https://render.com/)

## Running it locally

```bash
git clone https://github.com/oliwier-ferenc/game-hub.git
cd game-hub
pip install -r requirements.txt
python main.py
```

Then open `http://localhost:8080` in your browser.
