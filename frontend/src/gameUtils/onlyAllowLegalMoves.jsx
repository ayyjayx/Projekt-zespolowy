import React, { useEffect, useState } from "react";
import { Chess } from 'chess.js';
import 'chessboard-element';
import axios from "axios";
import { hasJWT } from "../utils/hasJWT";
// import Cookies from 'universal-cookie';
import { io } from 'socket.io-client';

const game = new Chess();
// let socket;
const socket = io("http://localhost:5000");

export function getFenPosition(gameId) {
    const [position, setPosition] = useState(null);
    const [playerColor, setPlayerColor] = useState(null);
    const [playerId, setPlayerId] = useState(null);

    useEffect(() => { // te dwa sockety to chyba jakoś razem, albo odwrotnie
        axios.get("http://localhost:5000/get_player", {
            withCredentials: true
        },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => {
                // console.log(response.data)
                setPlayerId(response.data)
            }).catch(err => console.log(err));
    }, []);

    if (playerId !== null) {
        socket.emit("get_position", { 'room': gameId, 'move': '', 'playerId': playerId })
        socket.on("FENandColor", (response) => {
            setPosition(response.fen);
            setPlayerColor(response.color);
        });
    }

    return [position, playerColor];
}

export function onlyAllowLegalMoves(gameId) {
    hasJWT();
    const position = getFenPosition(gameId)[0];
    const playerColor = getFenPosition(gameId)[1];
    console.log("playerColor poczatek funkcji: ", playerColor)

    if (position !== null) {
        game.load(position)
    }

    useEffect(() => {
        React.board.addEventListener('drag-start', (e) => {
            const { piece } = e.detail;
            // do not pick up pieces if the game is over
            if (game.isGameOver()) {
                updateStatus();
                socket.emit("game_pvp", { 'room': gameId, 'move': '' })
                socket.on("response", (response) => {
                    console.log('gameover' + response);
                })
            }
            // only pick up pieces for the side to move
            if ((game.turn() === 'w' && playerColor === 'b') ||
                (game.turn() === 'b' && playerColor === 'w') ||
                (game.turn() === 'w' && playerColor === 'w' && piece.search(/^b/) === 0) ||
                (game.turn() === 'b' && playerColor === 'b' && piece.search(/^w/) === 0)) {
                e.preventDefault();
                return;
            }
        });
    }, [playerColor]);

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
                    socket.emit("game_pvp", { 'room': gameId, 'move': '' })
                    socket.on("response", (response) => {
                        console.log('gameover' + response);
                    })
                }
                else {
                    socket.emit("game_pvp", { 'room': gameId, 'move': move.lan })
                }
            } catch {
                setAction('snapback');
            }
            updateStatus();
        });
    }, []);

    socket.on("fenResponse", (response) => {
        console.log('move made: ', response);
        game.load(response)
        React.board.setPosition(game.fen());
    })

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