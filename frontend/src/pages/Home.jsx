import React from 'react';
import 'chessboard-element';
import './style.css';
// import { isLoggedIn } from '../utils/isLoggedIn';
import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';
import { hasJWT } from '../utils/hasJWT';
import { updateColor } from '../utils/updateColor';

// const importAll = (requireContext) => requireContext.keys().map(requireContext);
// const images = importAll(require.context('../assets/chesspieces/celtic', false, /\.(png|jpe?g|svg)$/));

// function importAll(r) {
//     let images = {};
//     r.keys().map((item) =>  { images[item.replace('./', '')] = r(item); });
//     return images;
// }

// const images = importAll(require.context('../assets/chesspieces/celtic', false, /\.svg$/));

function Home() {
    hasJWT();
    onlyAllowLegalMoves();

    return (
        <div className='center'>
            {/* <h1><img src={images['bN.svg']} /></h1>
            <h1><img src={images['wN.svg']} /></h1> */}
            <h2>Jesteś nie zalogowany
            <button type="button" className="btn btn-warning" onClick={() => React.board.flip()}>Flip Board</button>
            <button type="button" className="btn btn-warning dropdown-toggle" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Styl</button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <p className="dropdown-item" href="#" onClick={() => updateColor('#f0d9b5', '#b58863')}>Basic</p>
                    <p className="dropdown-item" href="#" onClick={() => updateColor('#ffffff', '#ff0000')}>Polska</p>
                    <p className="dropdown-item" href="#" onClick={() => updateColor('#00ff00', '#a020f0')}>Joker moment</p>
                </div>
            </h2>
            <h3>
            <chess-board
                position="start"
                orientation={React.flipped ? 'black' : 'white'}
                draggable-pieces
                ref={(e) => React.board = e}
                // piece-theme="../assets/chesspieces/alpha/{piece}.svg">
                // piece-theme={images['wN.svg']}
                // piece-theme={`${images['{piece}.svg']}`}
                // piece-theme={images[piece]}
            >
            </chess-board>
            </h3>            
        </div>
    );
}

export default Home;