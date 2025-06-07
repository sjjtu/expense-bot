## ExpenseBot: Your Telegram Expense Tracker

**ExpenseBot** is a simple Telegram bot that helps you track your expenses using natural language.

**Features:**

* **Easy Expense Logging:** Simply tell the bot "I spent $10 on groceries" or "Bought coffee for $5", and it will record the expense in your database.
* **Natural Language Processing:**  No need to memorize commands, just speak naturally!
* **SQLite Database Storage:** Your expense data is securely stored locally in a SQLite database.

**Getting Started:**

1. **Clone the Repository:** `git clone https://github.com/sjjtu/expense-bot`
2. **Install Dependencies:** `uv init`

3. **Get a Telegram Bot Token:** Follow these instructions: [https://core.telegram.org/bots#6-botfather](https://core.telegram.org/bots#6-botfather)
4. **Configure the Bot:**
   * Replace `YOUR_TELEGRAM_BOT_TOKEN` in `main.py` with your bot token.

5. **Run the Bot:** `python main.py`

**Usage:**

Start a conversation with your bot in Telegram and start adding expenses! For example:

* "Spent $12 on lunch"
* "Bought movie tickets for $20"
* "Paid $5 for coffee yesterday"


 **Future Improvements:**

- [ ] data validation
- [ ] categorization e. g. food, rent, travel etc.
- [ ] get records
- [ ] voice to text


**Contributing:**

Contributions are welcome! Feel free to submit pull requests or open issues on GitHub.
