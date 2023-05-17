import React from 'react';
import 'chessboard-element';
import { useParams } from 'react-router-dom';
import './style.css';
import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';
import { getFenPosition } from '../gameUtils/onlyAllowLegalMoves';
// import { hasJWT } from '../utils/hasJWT';

function Game() {
    // hasJWT() ? '' : window.location.href = '/home';
    const { gameId } = useParams();
    onlyAllowLegalMoves(gameId);
    const position = getFenPosition(gameId)
    // console.log(posFen)

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
            <button onClick={() => React.board.flip()}>Flip Board</button>
        </div>
    );
}

export default Game;