import React, { useEffect, useState } from 'react';
// import { isLoggedIn } from '../utils/isLoggedIn';
import { hasJWT } from '../utils/hasJWT.jsx';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import './style.css';
import { io } from 'socket.io-client';
// import Cookies from 'universal-cookie';

// const cookies = new Cookies();
const socket = io("http://localhost:5000");

function LoggedHome() {

    const [playerId, setPlayerId] = useState(null);
    // const [playerColor, setPlayerColor] = useState(null);
    hasJWT();
    const [gameId, setGameId] = useState();

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
                console.log("res.data: ", response.data)
                setPlayerId(response.data)
                console.log("pId: ", playerId)
            }).catch(err => console.log(err));

        if (playerId !== null) {
            socket.on("newgame", (room) => {
                setGameId(room);
                console.log("creating a new game in room: " + room);
                socket.emit("newgame_pvp", { 'room': room, 'playerId': playerId })
            });
        }

        // if (gameId) {
        //     window.location.href = `/game/${gameId}`;
        // }

    }, [playerId, gameId])

    socket.on("redirect_to_game", (response) => {
        window.location.href = `/game/${response.id}`;
    })

    function joinRoom() {
        console.log("ask server to join room");
        socket.emit("join", { "user": playerId, "room": "Notifications" });
    }

    return (
        <div className='center'>
            <h2>Jesteś zalogowany</h2>
            <Button onClick={joinRoom}> Zagraj tu! </Button>
        </div>
    );
}

export default LoggedHome;