import React, { useEffect, board } from 'react';
import 'chessboard-element';
import { useParams } from 'react-router-dom';
import './style.css';
import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';
import { getFenPosition } from '../gameUtils/onlyAllowLegalMoves';
// import { hasJWT } from '../utils/hasJWT';

function importAll(r) {
    let images = {};
    r.keys().map((item) => { images[item.replace('./', '')] = r(item); });
    return images;
}

const images = importAll(require.context('../assets/pieces', false, /\.svg$/));

function Game() {
    // hasJWT() ? '' : window.location.href = '/home';
    const { gameId } = useParams();
    useEffect(() => {
        if (!board) return;
        board.pieceTheme = (piece) => {
            return images[`${piece}.svg`];
        }
    }, [board])


    onlyAllowLegalMoves(gameId);
    const position = getFenPosition(gameId);

    return (
        <div className='center'>
            <h2>Zalogowany</h2>
            <chess-board
                position={position}
                orientation={React.flipped ? 'black' : 'white'}
                draggable-pieces
                ref={(e) => React.board = e}
            >
            </chess-board>
            <button onClick={() => board.flip()}>Flip Board</button>
        </div>
    );
}

export default Game;