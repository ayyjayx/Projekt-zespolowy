import React, { useEffect, useState } from 'react';
import 'chessboard-element';
import { useParams } from 'react-router-dom';
import './style.css';
import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';
import { hasJWT } from '../utils/hasJWT';
import axios from 'axios';


export function getFenPosition(gameId) {
    const [position, setPosition] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/game?gameId=${gameId}`, {
                    withCredentials: true,
                    headers: {
                      "Content-Type": "application/json"
                    }
                  });
                setPosition(response.data.FEN);
            } catch (error) {
                console.error(error);
            }
        };
        fetchData();
    }, [position]);

    return position;
  }


function Game() {
    hasJWT();
<<<<<<< HEAD
=======
    console.log(hasJWT());

    // nie działa bo pierwszy leci undefined
>>>>>>> d8aa1a19dd7426b2e77297cd713640f1ac517a75
    // hasJWT() ? '' : window.location.href = '/';
    const { gameId } = useParams();
    onlyAllowLegalMoves(gameId);
    


    return (
        <div className='center'>
            <h2>Zalogowany</h2>
            <chess-board
                position={getFenPosition(gameId)}
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