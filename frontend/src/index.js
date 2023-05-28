import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReactDOMClient from 'react-dom/client';
import Layout from "./pages/Layout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Registration from "./pages/Registration";
import LoggedHome from "./pages/LoggedHome";
import Profile from './pages/Profile';
import About from './pages/About';
import ProfileUpdate from './pages/ProfileUpdate';
import ProfileDelete from './pages/ProfileDelete';
import PasswordReset from './pages/PasswordReset';
import ResetEmail from './pages/ResetEmail';
import Game from './pages/Game';
import NotAuthGame from './pages/NotAuthGame';
import MyGames from './pages/MyGames';
import ComingSoon from './pages/ComingSoon';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path='login' element={<Login />} />
          <Route path='registration' element={<Registration />} />
          <Route path='loggedhome' element={<LoggedHome />} />
          <Route path='profile' element={<Profile />} />
          <Route path='about' element={<About />} />
          <Route path='profile/update' element={<ProfileUpdate />} />
          <Route path='profile/delete' element={<ProfileDelete />} />
          <Route path='reset_password' element={<PasswordReset />} />
          <Route path='reset_send_email' element={<ResetEmail />} />
          <Route path='game/:gameId' element={<Game />} />
          <Route path='game_noauth' element={<NotAuthGame />} />
          <Route path='profile/games' element={<MyGames />} />
          <Route path='comingsoon' element={<ComingSoon />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

ReactDOMClient.createRoot(document.getElementById("root")).render(<App />);