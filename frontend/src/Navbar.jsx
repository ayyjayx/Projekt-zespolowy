import React from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { hasJWT } from '../src/utils/hasJWT.jsx';
import test from "./assets/test.png";
import info from "./assets/info.png";
// import Cookies from 'universal-cookie';



// const cookies = new Cookies();
axios.defaults.withCredentials = true;
let isLoggedIn;

function LogOut() {
    axios.post("http://localhost:5000/logout")
        .then(response => {
            console.log(response)
        }).catch(err => console.log(err));
    window.location.reload(true)
}

function Navbar() {
    hasJWT() ? isLoggedIn = true : isLoggedIn = false;
    return (
        <div className="sidenav">
            <nav className="navbar navbar-expand-lg navbar-light">
                <ul className="nav flex-column">
                    <li className="nav-item">
                        <Link to="/">
                            <p className="navbar-brand">
                                <img src={test} width="80" height="80" alt=""></img>
                            </p>
                        </Link>
                    </li>
                    <li className="nav-item">
                        <div className="dropdown-container">
                            <button type="button" className="btn nav-btn btn-warning btn-block mb-1 dropdown-toggle" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Graj</button>
                            <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                <Link to="/">
                                    <p className="dropdown-item">Gracz</p>
                                </Link>
                                <Link to="/">
                                    <p className="dropdown-item">Komputer</p>
                                </Link>
                            </div>
                        </div>
                    </li>
                    <li className="nav-item">
                        <Link to="/">
                            <button type="button" className="btn nav-btn btn-warning btn-block mb-1">Puzzle</button>
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to="/">
                            <button type="button" className="btn nav-btn btn-warning btn-block mb-1">Samouczek</button>
                        </Link>
                    </li>
                    {isLoggedIn === false && (
                        <li className="nav-item">
                            <Link to="/login">
                                <button type="button" className="btn nav-btn btn-info btn-block mb-1">Logowanie</button>
                            </Link>
                        </li>
                    )}
                    {isLoggedIn === false &&
                        <li className="nav-item">
                            <Link to="/registration">
                                <button type="button" className="btn nav-btn btn-info btn-block mb-1">Rejestracja</button>
                            </Link>
                        </li>
                    }
                    {isLoggedIn === true && (
                        <li className="nav-item">
                            <Link to="/profile">
                                <button type="button" className="btn nav-btn btn-info btn-block mb-1">Profil</button>
                            </Link>
                        </li>
                    )}
                    {isLoggedIn === true && (
                        <li className="nav-item">
                            <Link to="/">
                                <button type="button" className="btn nav-btn btn-danger btn-block mb-1"
                                    onClick={LogOut}>Wyloguj</button>
                            </Link>
                        </li>
                    )}
                    <li className="nav-item">
                        <Link to="/about">
                            <p className="navbar-brand-two">
                                <img src={info} width="40" height="40" alt=""></img>
                            </p>
                        </Link>
                    </li>
                </ul>
            </nav>
        </div>
    );
}

export default Navbar;