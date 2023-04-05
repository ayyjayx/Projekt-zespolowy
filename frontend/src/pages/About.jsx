import React from 'react';
import alan from "../assets/Alan.png";
import basia from "../assets/Basia.png";
import karolina from "../assets/Karolina.png";
import konrad from "../assets/Konrad.png";
import kuba from "../assets/Kuba.png";

function About() {
    return (
    <>
    <header className="App-header">
            szaszki.pl
    </header>
    <div className="form-two">
        <form>
            <a className="center-text"><h1>Top 5 Inc.</h1></a>
            <div className="picture">
                <img src={alan} width="40" height="40" className="d-inline-block align-top"></img>
                Alan Janukiewicz: Leader/Frontend
            </div>
            <div className="picture">
                <img src={karolina} width="40" height="40" className="d-inline-block align-top"></img>
                Karolina Ryzińska: Backend
            </div>
            <div className='picture'>
                <img src={konrad} width="40" height="40" className='d-inline-block align-top'></img>
                Konrad Kisiel: Backend
            </div>
            <div className='picutre'>
                <img src={basia} width="40" height="40" className='d-inline-block align top'></img>
                Barbara Żurek: UX/UI
            </div>
            <div className='picture'>
                <img src={kuba} width="40" height="40" className='d-inline-block align top'></img>
                Jakub Kordowski: Database/Frontend
            </div>
        </form>
    </div>
    </>
    );
}

export default About;