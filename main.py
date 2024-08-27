#####################
# Welcome to Cursor #
#####################

import random

# HTML template for the game
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic-Tac-Toe</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        #game {
            text-align: center;
        }
        #board {
            display: grid;
            grid-template-columns: repeat(3, 100px);
            grid-gap: 5px;
            margin-bottom: 20px;
        }
        .cell {
            width: 100px;
            height: 100px;
            background-color: #fff;
            border: 1px solid #ccc;
            font-size: 2em;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
        }
        #message {
            font-size: 1.5em;
            margin-bottom: 20px;
        }
        #reset {
            font-size: 1em;
            padding: 10px 20px;
        }
        #ai-credit {
            font-size: 0.8em;
            margin-top: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div id="game">
        <div id="board"></div>
        <div id="message"></div>
        <button id="reset">Play Again</button>
        <div id="ai-credit">Created using AI</div>
    </div>
    <script>
        const board = document.getElementById('board');
        const message = document.getElementById('message');
        const resetButton = document.getElementById('reset');
        let currentPlayer = 'X';
        let gameBoard = ['', '', '', '', '', '', '', '', ''];
        let gameActive = true;

        function createBoard() {
            for (let i = 0; i < 9; i++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.setAttribute('data-index', i);
                cell.addEventListener('click', handleCellClick);
                board.appendChild(cell);
            }
        }

        function handleCellClick(e) {
            const index = e.target.getAttribute('data-index');
            if (gameBoard[index] === '' && gameActive) {
                gameBoard[index] = currentPlayer;
                e.target.textContent = currentPlayer;
                if (checkWinner()) {
                    message.textContent = `${currentPlayer} wins!`;
                    gameActive = false;
                } else if (gameBoard.every(cell => cell !== '')) {
                    message.textContent = "It's a tie!";
                    gameActive = false;
                } else {
                    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
                    if (currentPlayer === 'O') {
                        setTimeout(computerMove, 500);
                    }
                }
            }
        }

        function computerMove() {
            if (!gameActive) return;
            let move = getComputerMove();
            gameBoard[move] = 'O';
            document.querySelector(`[data-index="${move}"]`).textContent = 'O';
            if (checkWinner()) {
                message.textContent = 'O wins!';
                gameActive = false;
            } else if (gameBoard.every(cell => cell !== '')) {
                message.textContent = "It's a tie!";
                gameActive = false;
            } else {
                currentPlayer = 'X';
            }
        }

        function getComputerMove() {
            const winPatterns = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
                [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
                [0, 4, 8], [2, 4, 6] // Diagonals
            ];

            // Try to win
            for (let pattern of winPatterns) {
                const [a, b, c] = pattern;
                if (gameBoard[a] === 'O' && gameBoard[b] === 'O' && gameBoard[c] === '') return c;
                if (gameBoard[a] === 'O' && gameBoard[c] === 'O' && gameBoard[b] === '') return b;
                if (gameBoard[b] === 'O' && gameBoard[c] === 'O' && gameBoard[a] === '') return a;
            }

            // Block player's win
            for (let pattern of winPatterns) {
                const [a, b, c] = pattern;
                if (gameBoard[a] === 'X' && gameBoard[b] === 'X' && gameBoard[c] === '') return c;
                if (gameBoard[a] === 'X' && gameBoard[c] === 'X' && gameBoard[b] === '') return b;
                if (gameBoard[b] === 'X' && gameBoard[c] === 'X' && gameBoard[a] === '') return a;
            }

            // Create a fork (two winning moves)
            for (let i = 0; i < 9; i++) {
                if (gameBoard[i] === '') {
                    gameBoard[i] = 'O';
                    let winningMoves = 0;
                    for (let j = 0; j < 9; j++) {
                        if (gameBoard[j] === '') {
                            gameBoard[j] = 'O';
                            if (checkWinner()) winningMoves++;
                            gameBoard[j] = '';
                        }
                    }
                    gameBoard[i] = '';
                    if (winningMoves >= 2) return i;
                }
            }

            // Choose center if available
            if (gameBoard[4] === '') return 4;
            
            // Choose a corner
            const corners = [0, 2, 6, 8];
            const availableCorners = corners.filter(i => gameBoard[i] === '');
            if (availableCorners.length > 0) {
                return availableCorners[Math.floor(Math.random() * availableCorners.length)];
            }
            
            // Choose any available cell
            const emptyCells = gameBoard.reduce((acc, cell, index) => {
                if (cell === '') acc.push(index);
                return acc;
            }, []);
            return emptyCells[Math.floor(Math.random() * emptyCells.length)];
        }

        function checkWinner() {
            const winPatterns = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
                [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
                [0, 4, 8], [2, 4, 6] // Diagonals
            ];
            return winPatterns.some(pattern => {
                return pattern.every(index => gameBoard[index] === currentPlayer);
            });
        }

        function resetGame() {
            gameBoard = ['', '', '', '', '', '', '', '', ''];
            gameActive = true;
            currentPlayer = 'X';
            message.textContent = '';
            document.querySelectorAll('.cell').forEach(cell => {
                cell.textContent = '';
            });
        }

        resetButton.addEventListener('click', resetGame);
        createBoard();
    </script>
</body>
</html>
"""

def create_html_file():
    with open('tic_tac_toe.html', 'w') as f:
        f.write(HTML_TEMPLATE)

if __name__ == "__main__":
    create_html_file()
    print("Tic-Tac-Toe game has been created. Open 'tic_tac_toe.html' in your web browser to play.")
