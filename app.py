from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize empty board
def create_board():
    return [["" for _ in range(3)] for _ in range(3)]

# Check for a winner
def check_winner(board, player):
    for i in range(3):
        if all(cell == player for cell in board[i]):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Check if the board is full
def is_draw(board):
    return all(cell != "" for row in board for cell in row)

@app.route("/", methods=["GET", "POST"])
def index():
    if "board" not in session:
        session["board"] = create_board()
        session["player"] = "X"
        session["message"] = ""

    board = session["board"]
    current_player = session["player"]
    message = session["message"]

    if request.method == "POST":
        row = int(request.form["row"])
        col = int(request.form["col"])

        if board[row][col] == "":
            board[row][col] = current_player
            if check_winner(board, current_player):
                message = f"Player {current_player} wins!"
            elif is_draw(board):
                message = "It's a draw!"
            else:
                current_player = "O" if current_player == "X" else "X"

        session["board"] = board
        session["player"] = current_player
        session["message"] = message

    return render_template("index.html", board=board, message=message, player=current_player)

@app.route("/reset")
def reset():
    session.pop("board", None)
    session.pop("player", None)
    session.pop("message", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
