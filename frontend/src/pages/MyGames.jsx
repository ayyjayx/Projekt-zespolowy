import React, { useEffect, useState } from "react";
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Button'
import axios from 'axios';
import { hasJWT } from '../utils/hasJWT.jsx';


function MyGames() {
    hasJWT();
    const [account, setAccount] = useState('');
    const [games, setGames] = useState([]);

    useEffect(() => {
        axios.get("http://uwmchess.herokuapp.com/api/profile", {
            withCredentials: true,
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
        axios.get("http://uwmchess.herokuapp.com/api/profile/games", {
            withCredentials: true,
            headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => {
                console.log(response.data);
                setGames(response.data.games);
            })
            .catch(err => {
                console.log(err);
            });
    },
        []);

  const handleBack = () => {
    window.location.href = '/profile'
  }

    // console.log(games)
    return (
        <div className="center">
          <h1>{account.username} : Rozegrane gry</h1>
          <Table striped bordered responsive>
            <thead>
              <tr>
                <th>Game ID</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Result</th>
                <th>SAN</th>
                {/* <th>FEN</th> */}
              </tr>
            </thead>
            <tbody>
              {games.map((game) => (
                <tr key={game.id}>
                  <td>{game.id}</td>
                  <td>{game.start_time}</td>
                  <td>{game.end_time}</td>
                  <td>{game.result}</td>
                  <td>{game.san}</td>
                  {/* <td>{game.fen}</td> */}
                </tr>
              ))}
            </tbody>
          </Table>
          <Button onClick={handleBack}>Powrót do Profilu</Button>
        </div>
      );
}

export default MyGames;