import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
    return (
        <nav>
            <ul>
                <li>
                    <Link to="/">Strona domowa</Link>
                </li>
                <li>
                    <Link to="/login">Logowanie</Link>
                </li>
                <li>
                    <Link to="/registration">Rejestracja</Link>
                </li>

            </ul>
        </nav>
    );
}

export default Navbar;