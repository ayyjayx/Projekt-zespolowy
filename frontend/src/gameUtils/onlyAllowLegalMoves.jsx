import React, { useEffect, useState } from "react";
import { Chess } from 'chess.js';
import 'chessboard-element';
// import axios from "axios";
import { hasJWT } from "../utils/hasJWT";
// import Cookies from 'universal-cookie';
import { io } from 'socket.io-client';

const game = new Chess();
// let socket;
const socket = io("http://localhost:5000");

export function getFenPosition(gameId) {
    const [position, setPosition] = useState(null);

    useEffect(() => {
        socket.emit("get_position", gameId)
        socket.on("FEN", (fen) => {
            setPosition(fen);
            console.log('position' + position);
        });
    }, [position]);

    return position;
}

export function onlyAllowLegalMoves(gameId) {
    hasJWT();
    // const cookies = new Cookies();
    const position = getFenPosition(gameId);


    if (position !== null) {
        game.load(position)
    }

    useEffect(() => {
        React.board.addEventListener('drag-start', (e) => {
            const { piece } = e.detail;
            // do not pick up pieces if the game is over
            if (game.isGameOver()) {
                updateStatus();
                socket.emit("game_pvp", {'move':''})
                socket.on("response", (response) =>{
                    console.log('gameover' + response);
                })
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

                if (move !== null && 'promotion' in move) {
                    console.log("promotion at: " + target + " into: " + move.promotion);
                }

                if (game.isGameOver()) {
                    socket.emit("game_pvp", {'move':''})
                    socket.on("response", (response) =>{
                        console.log('gameover' + response);
                })
                }

                else {
                    socket.emit("game_pvp", {'move': move.lan})
                    socket.on("response", (response) =>{
                        console.log('move made' + response);
                })
                }
            } catch {
                setAction('snapback');
            }
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
        console.log("status", status)
    }

    updateStatus();
}