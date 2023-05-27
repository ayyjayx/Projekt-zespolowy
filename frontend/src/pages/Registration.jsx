import React, { useState } from 'react';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button'
import axios from 'axios';
import './style.css'

function Registration() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [passwordRepeat, setPasswordRepeat] = useState('');
    const [registrationStatus, setRegistrationStatus] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const registerPayload = {
            username: username,
            email: email,
            password: password,
            passwordRepeat: passwordRepeat
        }

        axios.post("http://localhost:5000/registration", registerPayload)
            .then(response => {
                setRegistrationStatus(response.data)
                setUsername('');
                setEmail('');
                setPassword('');
                setPasswordRepeat('');
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
                <form onSubmit={handleSubmit}>
                    <div className="form-body">
                        <div className="register">
                            <label className="form_label" htmlFor="firstName">Rejestracja </label>
                        </div>
                        <div className="username">
                            <input value={username} onChange={(e) => setUsername(e.target.value)} className="form_input" type="text" id="userName" placeholder="Nazwa użytkownika" />
                        </div>
                        <div className="email">
                            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" id="email" className="form_input" placeholder="Email" />
                        </div>
                        <div className="password">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Hasło" />
                        </div>
                        <div className="confirm-password">
                            <input value={passwordRepeat} onChange={(e) => setPasswordRepeat(e.target.value)} className="form_input" type="password" id="confirmPassword" placeholder="Powtórz hasło" />
                        </div>
                    </div>
                    <div className="footer">
                        <Link to='/login'>
                            <Button variant="Primary" className="btn">Masz konto?</Button>
                        </Link>
                        <Button variant="Primary" type="submit" className="btn float-right">Zarejestruj</Button>
                    </div>
                    <p>{registrationStatus}</p>
                </form>
            </div></>
    );
}

export default Registration;