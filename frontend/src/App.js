/* eslint-disable react/react-in-jsx-scope */
import './App.css';
import Header from './components/header';
import { setAuthToken } from './pages/Login';

const token = localStorage.getItem("token");
 if (token) {
     setAuthToken(token);
 }

function App() {
  return (
  <div className="App">
      <Header />
    </div>
  );
}

export default App;
