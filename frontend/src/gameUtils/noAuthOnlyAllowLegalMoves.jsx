import React, { useEffect } from "react";
import { Chess } from 'chess.js';
import 'chessboard-element';
import axios from "axios";

export function noAuthOnlyAllowLegalMoves() {
    const game = new Chess();
    const saved_fen = localStorage.getItem("FEN");
    if (saved_fen) {
        game.load(saved_fen)
    }
    else {
        localStorage.setItem("FEN", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    }

    useEffect(() => {
        React.board.addEventListener('drag-start', (e) => {
            const { piece } = e.detail;
            if (game.isGameOver()) {
                updateStatus();
                localStorage.removeItem("FEN");
                e.preventDefault();
                return;
            }

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

            try {
                const move = game.move({
                    from: source,
                    to: target,
                    promotion: 'q'
                });

                if (game.isGameOver()) {
                    updateStatus();
                    axios.post(`http://uwmchess.herokuapp.com/api/game_noauth`, {
                        fen: game.fen(),
                        move: move.lan,
                        over: true,
                    });
                    localStorage.removeItem("FEN");
                    return;
                }

                else {
                    console.log(move);
                    localStorage.setItem("FEN", game.fen())
                    axios.post(`http://uwmchess.herokuapp.com/api/game_noauth`, {
                        fen: game.fen(),
                        move: move.lan,
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
            status = `Game over, ${moveColor} is in checkmate.`;
        } else if (game.isDraw()) {
            status = 'Game over, drawn position';
        } else {
            status = `${moveColor} to move`;
            if (game.inCheck()) {
                status += `, ${moveColor} is in check`;
            }
        }



        React.statusElement = status;
        React.fenElement = game.fen();
        React.pgnElement = game.pgn();
        console.log("status", status)
    }

    updateStatus();
}