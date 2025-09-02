# 🎮 Discord Game & Party Bot

This Discord bot is designed for:
- 🎲 Searching games in a database (`Excel`)
- 👥 Organizing temporary voice channels for parties (party system)
- 🛠️ A set of useful commands (spam, change status, help)

## 📦 Features

### 🔹 Main Commands
- `.help` – shows a list of commands with descriptions.
- `.game {name / year / developer / genre}` – searches a game in the database (`db.xlsx`) and shows a description with an image, developer, and system requirements.
- `.party @user` – creates a temporary voice channel for the author and the invited user.
- `.party_accept` – join the party after being invited.
- `.spam {amount}, {phrase}` – sends a message multiple times (for fun).
- `.change_status` – change the bot’s status (**admin only**).

### 🔹 Party System
- The author can invite another user to their private voice channel.
- The invited user confirms the invitation via `.party_accept`.
- The channel is automatically deleted when participants leave.

### 🔹 Games
- The bot pulls information from an **Excel file `db.xlsx`**.
- Search can be done by:
  - game title
  - release year
  - developer
  - genre
- Returns an embed with:
  - title and year
  - developer
  - image
  - system requirements (minimum and maximum)
  - download link
