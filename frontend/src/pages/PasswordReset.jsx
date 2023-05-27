import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button'
import './style.css'

function PasswordReset() {

    const [password, setPassword] = useState('');
    const [passwordRepeat, setPasswordRepeat] = useState('');
    const [resetStatus, setResetStatus] = useState('');

    const emailMatch = window.location.href.match(/email=([^&]+)/);
    const email = emailMatch ? emailMatch[1] : '';
    const tokenMatch = window.location.href.match(/token=([^&]+)/);
    const token = tokenMatch ? tokenMatch[1] : '';

    const url = `http://localhost:5000/reset_password?token=${token}&email=${email}`;

    useEffect(() => {
        axios.get(url)
            .then(response => {
                console.log(response.data)
            })
            .catch(err => { console.log(err) });
    },
        []);

    const handleSubmit = (e) => {
        e.preventDefault();
        const resetPayload = {
            email: email,
            password: password,
            passwordRepeat: passwordRepeat,
            token: token
        }
        axios.post("http://localhost:5000/reset_password", resetPayload)
            .then(response => {
                console.log(email);
                console.log(token);
                setPassword('');
                setPasswordRepeat('');
                setResetStatus(response.data.msg);
                console.log(response.data);
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
                        <div className="reset password">
                            <label className="form_label" htmlFor="firstName">Reset Hasła </label>
                        </div>
                        <p>Email: {email}</p>
                        <div className="password">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Hasło" />
                        </div>
                        <div className="confirm-password">
                            <input value={passwordRepeat} onChange={(e) => setPasswordRepeat(e.target.value)} className="form_input" type="password" id="confirmPassword" placeholder="Powtórz hasło" />
                        </div>
                    </div>
                    <div className="footer">
                        <Button variant="Primary" type="submit" className="btn">Zmień dane</Button>
                        <Link to='/login'>
                            <Button variant="Primary" className="btn float-right">Powrót do logowania</Button>
                        </Link>
                    </div>
                    <p>{resetStatus}</p>
                </form>
            </div></>
    );
}

export default PasswordReset;