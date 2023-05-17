import React from 'react';
import 'chessboard-element';
import './style.css';
import { noAuthOnlyAllowLegalMoves } from '../gameUtils/noAuthOnlyAllowLegalMoves';



function NotAuthGame() {
    noAuthOnlyAllowLegalMoves();

    return (
        <div className='center'>
            <h2>Nie zalogowany</h2>
            <chess-board
                position={localStorage.getItem("FEN")}
                orientation={React.flipped ? 'black' : 'white'}
                draggable-pieces
                ref={(e) => React.board = e}
            >
            </chess-board>
            <button onClick={() => React.board.flip()}>Flip Board</button>
            <button onClick={() => {
                React.board.start();
                localStorage.setItem("FEN", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
                location.reload();
            }}>Start new game</button>
        </div>
    );
}

export default NotAuthGame;