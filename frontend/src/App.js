import './App.css';
import Header from './components/header';
import RegistrationForm from './components/registrationForm';
import LoginForm from './components/LoginForm';


function App() {
  return (
    <><div className="App">
      <Header />
    </div>
    
    <div className="Forms">
      <RegistrationForm />
      <LoginForm />
    </div>
    <div className="Login-link">
      <a className="Register-link">
        <button style={{backgroundColor: '#CBECF7'}}>Zarejestruj się</button>
      </a>
      <a className="Register-link">
        <button style={{backgroundColor: '#CBECF7'}}>Zaloguj się</button>
      </a>
    </div>
    </>
  );
}

export default App;
