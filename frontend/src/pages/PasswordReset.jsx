import React, { useEffect, useState }from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button'
import './style.css'

function PasswordReset() {

    // const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [passwordRepeat, setPasswordRepeat] = useState('');


    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const email = params.get('email');

        axios.get("http://localhost:5000/reset_password?email=", {params: {email}})
            .then(response => {
                console.log(response.data);
                // setEmail(email);
            })
            .catch(err => { console.log(err) });
    },
        []);

    const handleSubmit = (e) => {
        const params = new URLSearchParams(window.location.search);
        const email = params.get('email');

        e.preventDefault();
        const registerPayload = {
            password: password,
            passwordRepeat: passwordRepeat
        }
        axios.post("http://localhost:5000/reset_password?email=" + email, registerPayload)
            .then(response => {
                console.log(response)
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
                        <div className="reset password">
                            <label className="form_label" htmlFor="firstName">Reset Hasła </label>
                        </div>
                        <div className="password">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Hasło" />
                        </div>
                        <div className="confirm-password">
                            <input value={passwordRepeat} onChange={(e) => setPasswordRepeat(e.target.value)} className="form_input" type="password" id="confirmPassword" placeholder="Powtórz hasło" />
                        </div>
                    </div>
                    <div className="footer">
                        <Button variant="Primary" type="submit" className="btn">Zmień dane</Button>
                    </div>
                </form>
            </div></>
    );
}

export default PasswordReset;