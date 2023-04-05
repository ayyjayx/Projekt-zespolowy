import React from "react";
import { Link } from "react-router-dom";
// import { hasJWT } from '../utils/hasJWT.jsx';
import test from "./assets/test.png";
import info from "./assets/info.png";

function Navbar() {
    var isLoggedin = false;
    return (
      <div className="sidenav">  
        <nav className="navbar navbar-expand-lg navbar-light">
          <ul className="nav flex-column">
            <li className="nav-item">  
              <Link to="/">
                <a className="navbar-brand">
                  <img src={test} width="80" height="80" alt=""></img>
                </a>
              </Link>
            </li>
            <li className="nav-item">
              <div className="dropdown-container">
                <button type="button" className="btn nav-btn btn-warning btn-block mb-1 dropdown-toggle" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Graj</button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <Link to="/">
                    <a className="dropdown-item">Gracz</a>
                  </Link>
                  <Link to="/">
                    <a className="dropdown-item">Komputer</a>
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
            {!isLoggedin && (
            <li className="nav-item">  
              <Link to="/registration">
                <button type="button" className="btn nav-btn btn-info btn-block mb-1">Rejestracja</button>
              </Link>
            </li>
            )}
            {!isLoggedin && (
            <li className="nav-item">
              <Link to="/login">
                  <button type="button" className="btn nav-btn btn-info btn-block mb-1">Logowanie</button>
              </Link>
            </li>
            )}
            {isLoggedin && (
              <li className="nav-item">
                <Link to="/">
                  <button type="button" className="btn nav-btn btn-info btn-block mb-1">Profil</button>
                </Link>
              </li>
            )}
            {isLoggedin && (
              <li className="nav-item">
                <Link to="/">
                  <button type="button" className="btn nav-btn btn-danger btn-block mb-1">Wyloguj</button>
                </Link>
              </li>
            )}
            <li className="nav-item">  
              <Link to="/about">
                <a className="navbar-brand-two">
                  <img src={info} width="40" height="40" alt=""></img>
                </a>
              </Link>
            </li>
          </ul>
        </nav>
      </div>  
    );
}

export default Navbar;