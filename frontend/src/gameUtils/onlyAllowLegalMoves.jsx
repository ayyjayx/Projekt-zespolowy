import React, { useEffect } from "react";
import { Chess } from 'chess.js';
import 'chessboard-element';
import axios from "axios";
import { getFenPosition } from "../pages/Game";
import Cookies from 'universal-cookie';


const game = new Chess();
const cookies = new Cookies();

export function onlyAllowLegalMoves(gameId) {
    const position = getFenPosition(gameId);
    if (position !== null) {
        game.load(position);
    }

    useEffect(() => {
        React.board.addEventListener('drag-start', (e) => {
        const { piece } = e.detail;
        // do not pick up pieces if the game is over
        if (game.isGameOver()) {
            updateStatus();
            axios.post(`http://localhost:5000/game?gameId=${gameId}`, {
                    over: true,
                }, {
                    withCredentials: true,
                    headers: {
                        "X-CSRF-TOKEN": `${cookies.get("csrf_access_token")}`,
                    }
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
        // React.board.setPosition(game.fen());
        React.board.addEventListener('drop', (e) => {
        const { source, target, setAction } = e.detail;

        // see if the move is legal
        try {
            const move = game.move({
                from: source,
                to: target,
                promotion: 'q' // always promote to a queen for simplicity
            });

            if (move !== null && 'promotion' in move){
                console.log("promotion at: " + target + " into: " + move.promotion);
            }
            updateStatus();

            if (game.isGameOver()) {
                axios.post(`http://localhost:5000/game?gameId=${gameId}`, {
                    move: move.lan,
                    over: true,
                }, {
                    withCredentials: true,
                    headers: {
                        "X-CSRF-TOKEN": `${cookies.get("csrf_access_token")}`,
                    }
                });
                e.preventDefault();
                return;
            }
            else {
                // console.log(move);
                axios.post(`http://localhost:5000/game?gameId=${gameId}`, {
                    move: move.lan,
                }, {
                    withCredentials: true,
                    headers: {
                        "X-CSRF-TOKEN": `${cookies.get("csrf_access_token")}`,
                    }
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
}

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
