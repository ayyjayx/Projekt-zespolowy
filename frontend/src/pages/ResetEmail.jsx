import React, { useState }from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button'
import './style.css'


 export const getPost = (funcParamURL) => {
        return axios.get(`${funcParamURL}`);
      }

function ResetEmail() {

    const [email, setEmail] = useState('');

    
    const handleSubmit = (e) => {
        e.preventDefault();
        const registerPayload = {
            email: email
        }

        axios.post("http://localhost:5000/reset_send_email", {
            headers: {
                "Content-Type": "application/json"
            },
            registerPayload})
            .then(response => {
                console.log(response)
                setEmail('');
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
                            <label className="form_label" htmlFor="firstName">Rejestracja </label>
                        </div>
                        <div className="email">
                            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" id="email" className="form_input" placeholder="Email" />
                        </div>
                    </div>
                    <div className="footer">
                        <Button variant="Primary" type="submit" className="btn">Wyślij Link do Reset</Button>
                    </div>
                </form>
            </div></>
    );
}

export default ResetEmail;