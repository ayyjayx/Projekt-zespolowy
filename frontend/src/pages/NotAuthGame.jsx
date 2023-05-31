import React, { useEffect } from 'react';
import 'chessboard-element';
import './style.css';
import { noAuthOnlyAllowLegalMoves } from '../gameUtils/noAuthOnlyAllowLegalMoves';
import { updateColor } from '../utils/updateColor';

function importAll(r) {
    let images = {};
    r.keys().map((item) => { images[item.replace('./', '')] = r(item); });
    return images;
}

const images = importAll(require.context('../assets/pieces', false, /\.svg$/));

function NotAuthGame() {
    noAuthOnlyAllowLegalMoves();

    useEffect(() => {
        if (!React.board) return;
        React.board.pieceTheme = (piece) => {
            return images[`${piece}.svg`];
        }
    }, [React.board])

    return (
        <div className='center'>
            <h2>Jesteś niezalogowany</h2>
            <button type="button" className="btn btn-warning" onClick={() => {
                React.board.start();
                localStorage.setItem("FEN", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
                location.reload();
            }}>Nowa gra</button>
            <button type="button" className="btn btn-warning" onClick={() => React.board.flip()}>Flip Board</button>
            <button type="button" className="btn btn-warning dropdown-toggle" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Styl</button>
            <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <p className="dropdown-item" href="#" onClick={() => updateColor('#f0d9b5', '#b58863')}>Basic</p>
                <p className="dropdown-item" href="#" onClick={() => updateColor('#ffffff', '#ff0000')}>Polska</p>
                <p className="dropdown-item" href="#" onClick={() => updateColor('#00ff00', '#a020f0')}>Joker moment</p>
            </div>
            <h3>
                <chess-board
                    position={localStorage.getItem("FEN")}
                    orientation={React.flipped ? 'black' : 'white'}
                    draggable-pieces
                    ref={(e) => React.board = e}
                >
                </chess-board>
            </h3>
        </div>
    );
}

export default NotAuthGame;