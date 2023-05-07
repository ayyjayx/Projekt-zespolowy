import React from 'react';
import 'chessboard-element';
import './style.css';
// import { isLoggedIn } from '../utils/isLoggedIn';
import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';
import { hasJWT } from '../utils/hasJWT';


function Home() {
    hasJWT();
    onlyAllowLegalMoves();

    return (
        <div className='center'>
            <h2>Jesteś nie zalogowany</h2>
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

export default Home;