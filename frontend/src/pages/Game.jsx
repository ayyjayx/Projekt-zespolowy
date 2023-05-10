import React from 'react';
import 'chessboard-element';
import './style.css';
import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';

function Game() {
    onlyAllowLegalMoves();

    return (
        <div className='center'>
            <h2>Nie zalogowany</h2>
            <chess-board
                position="start"
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