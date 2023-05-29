import React, { useEffect, useState } from 'react';
// import { isLoggedIn } from '../utils/isLoggedIn';
import { hasJWT } from '../utils/hasJWT.jsx';
// import axios from 'axios';
import Button from 'react-bootstrap/Button';
import './style.css';
import { io } from 'socket.io-client';


const socket = io("http://localhost:5000");
// let socket;
function LoggedHome() {
    hasJWT();
    const [ gameId, setGameId ] = useState('');

    useEffect(() => { // te dwa sockety to chyba jakoś razem, albo odwrotnie
        socket.on("newgame", (room) => {
            setGameId(room);
            console.log("creating a new game in room: " + room);
            socket.emit("newgame_pvp", {'room':room,'white':111,'black':112})       
        });
        if (gameId){
            window.location.href = `/game/${gameId}`;
        }
        // socket.on("redirect_to_game", (room, ids) => {
        //     window.location.href = `/game/${gameId}`;
        // })
    })
    
    function joinRoom() {
        console.log("ask server to join room");
        socket.emit("join", { "user": Date.now(), "room": "Notifications" });
    }

    return (
        <div className='center'>
            <h2>Jesteś zalogowany</h2>
            <Button onClick={joinRoom}> Zagraj tu! </Button>
        </div>
    );
}

export default LoggedHome;