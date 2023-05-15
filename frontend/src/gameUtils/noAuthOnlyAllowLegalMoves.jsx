import React, { useEffect } from "react";
import { Chess } from 'chess.js';
import 'chessboard-element';
import axios from "axios";

// add saving FEN to localStorage
// and send fen with each request? 
export function onlyAllowLegalMoves() {
    const game = new Chess();

    useEffect(() => {
        React.board.addEventListener('drag-start', (e) => {
            const { piece } = e.detail;
            // do not pick up pieces if the game is over
            if (game.isGameOver()) {
                updateStatus();
                axios.post(`http://localhost:5000/game_noauth`, {
                        over: true,
                    });
                e.preventDefault();
                return;
            }

            // only pick up pieces for the side to move
            if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
                (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
                e.preventDefault();
                return;
            }
        });

    }, []);

    useEffect(() => {
        React.board.addEventListener('drop', (e) => {
            const { source, target, setAction } = e.detail;

            // see if the move is legal
            try {
                const move = game.move({
                    from: source,
                    to: target,
                    promotion: 'q' // always promote to a queen for simplicity
                });
                
                if (game.isGameOver()) {
                    updateStatus();
                    axios.post(`http://localhost:5000/game_noauth`, {
                        fen: game.fen(),
                        move: source + target,
                        over: true,
                    });
                    e.preventDefault();
                    return;
                }

                else {
                    console.log(move);
                    axios.post(`http://localhost:5000/game_noauth`, {
                        fen: game.fen(),
                        move: source + target,
                    });
                }
                
                
            } catch {
                setAction('snapback');
            }
            console.log("Dostępne ruchy: ", game.moves())
            updateStatus();
        });
    }, []);

    useEffect(() => {
        // update the board position after the piece snap
        // for castling, en passant, pawn promotion
        React.board.addEventListener('snap-end', () => {
            React.board.setPosition(game.fen());
        });
    }, []);

    function updateStatus() {
        let status = '';
        let moveColor = 'White';
        if (game.turn() === 'b') {
            moveColor = 'Black';
        }

        if (game.isCheckmate()) {
            // checkmate?
            status = `Game over, ${moveColor} is in checkmate.`;
        } else if (game.isDraw()) {
            // draw?
            status = 'Game over, drawn position';
        } else {
            // game still on
            status = `${moveColor} to move`;

            // check?
            if (game.inCheck()) {
                status += `, ${moveColor} is in check`;
            }
        }
        
        

        React.statusElement = status;
        React.fenElement = game.fen();
        React.pgnElement = game.pgn();
        console.log(status)
    }

    updateStatus();
}