import React, { useState } from 'react';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button'
import axios from 'axios';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginStatus, setLoginStatus] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const loginPayload = {
            username: username,
            password: password,
        }

        axios.post("http://localhost:5000/login", loginPayload, {
            withCredentials: true,
        })
            .then(response => {
                if (response.status === 201) {
                    setLoginStatus(response.data.login);
                }
                else {
                    console.log(response.headers);
                    window.location.href = '/loggedhome';
                }
            }).catch(err => console.log(err));
    };

    const handleReset = () => {
        window.location.href = 'reset_send_email'
    };

    return (
        <><header className="App-header">
            szaszki.pl
        </header>
            <div className="form">
                <form onSubmit={handleSubmit}>
                    <div className="form-body">
                        <div className="login">
                            <label className="form_label" htmlFor="firstName">Logowanie</label>
                        </div>
                        <div className="username">
                            <input value={username} onChange={(e) => setUsername(e.target.value)} className="form_input" type="text" id="userName" placeholder="Nazwa użytkownika" />
                        </div>
                        <div className="password">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Hasło" />
                        </div>
                    </div>
                    <div className="footer">
                        <Link to='/registration'>
                            <Button variant="Primary" className="btn">Nie masz konta? Zarejestruj się!</Button>
                        </Link>
                        <Button variant="Primary" type="submit" className="btn">Zaloguj</Button>
                        <Button onClick={handleReset}>Zapomniane Hasło</Button>
                    </div>
                    <p>{loginStatus}</p>
                </form>
            </div>
        </>
    );
}

export default Login;