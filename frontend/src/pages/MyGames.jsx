import React, { useEffect, useState } from "react";
import Button from 'react-bootstrap/Button'
import axios from 'axios';
import { hasJWT } from '../utils/hasJWT.jsx';


function MyGames() {
    hasJWT();
    const [account, setAccount] = useState('');
    const [games, setGames] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:5000/profile", {
            withCredentials: true
        },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => {
                console.log(response.data);
                setAccount(response.data);
            })
            .catch(err => {
                console.log(err);
            });
    },
        []);
    
    useEffect(() => {
        axios.get("http://localhost:5000/profile/games", {
            withCredentials: true
        },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => {
                console.log(response.data);
                setGames(response.data);
            })
            .catch(err => {
                console.log(err);
            });
    },
        []);

    const handleBack = () => {
        window.location.href = '/profile'
    }

    return (
        <div className="center">
            <h1>{account.username} : Rozegrane gry</h1>
            <ul>
                {games.map((game) => (
                    <li key={game.id}>
                        <p>Game ID: {game.id}</p>
                        <p>Start Time: {game.start_time}</p>
                        <p>End Time: {game.end_time}</p>
                        <p>Result: {game.result}</p>
                        <p>FEN: {game.fen}</p>
                    </li>
                ))}
            </ul>
            <Button onClick={handleBack}>Powrót do Profilu</Button>
        </div>
    );
}

export default MyGames;
