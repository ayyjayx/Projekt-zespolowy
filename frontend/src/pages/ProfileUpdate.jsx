import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button'
import axios from 'axios';
import { Link } from "react-router-dom";
import { hasJWT } from '../utils/hasJWT.jsx';
// import jwt_decode from "jwt-decode";
import './style.css'
import Cookies from 'universal-cookie';


function ProfileUpdate() {
    hasJWT();
    const cookies = new Cookies();
    const [account, setAccount] = useState('');

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [updateStatus, setUpdateStatus] = useState('');

    axios.defaults.withCredentials = true;

    useEffect(() => {
        axios.get("http://uwmchess.herokuapp.com/api/profile",
            {
                withCredentials: true
            }, {
            headers: {
                "Content-Type": "application/json"
            },
        })
            .then(response => {
                setAccount(response.data);
            })
            .catch(err => { console.log(err); });
    },
        []);

    const handleSubmit = (e) => {
        e.preventDefault();
        const updatePayload = {
            id: account.id,
            username: username,
            email: email,
            password: password
        }

        axios.post("http://uwmchess.herokuapp.com/api/profile/update", updatePayload, {
            headers: {
                "X-CSRF-TOKEN": `${cookies.get("csrf_access_token")}`,
            },
        })
            .then(response => {
                setUpdateStatus(response.data.profile);
                setPassword('');
            })
            .catch(err => {
                console.log(err)
            }
            );
    };

    return (
        <><header className="App-header">
            szaszki.pl
        </header>
            <div className="form">
                <h1>Twoje obecne dane</h1>
                <p>Nazwa użytkownika: {account.username}</p>
                <p>Email: {account.email}</p>
            </div>
            <div className="form">
                <form onSubmit={handleSubmit}>
                    <div className="form-body">
                        <div className="register">
                            <label className="form_label" htmlFor="firstName">Edycja danych</label>
                        </div>
                        <div className="username">
                            <input value={username} onChange={(e) => setUsername(e.target.value)} className="form_input" type="text" id="userName" placeholder="Nowa nazwa użytkownika" />
                        </div>
                        <div className="email">
                            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" id="email" className="form_input" placeholder="Nowy email" />
                        </div>
                        <div className="password">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Podaj aktualne hasło" />
                        </div>
                    </div>
                    <p>
                        Wypełnij tylko te pola z danymi, które chcesz zmienić
                    </p>
                    <div className="footer">
                        <Button variant="Primary" type="submit" className="btn">Zmień dane</Button>
                        <Link to='/reset_send_email'>
                            <Button variant="Primary" className="btn float-right">Resetuj hasło</Button>
                        </Link>
                    </div>
                    <p>{updateStatus}</p>
                </form>
            </div></>
    );
}

export default ProfileUpdate;