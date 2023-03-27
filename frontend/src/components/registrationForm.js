import React, {useState} from 'react';
import './style.css'
function RegistrationForm() {
    return(
      <div className="form">
          <div className="form-body">
              <div className="register">
                  <label className="form_label" for="firstName">Rejestracja </label>
              </div>
              <div className="username">
                  <input className="form_input" type="text" id="userName" placeholder="Nazwa użytkownika"/>
              </div>
              <div className="email">
                  <input  type="email" id="email" className="form_input" placeholder="Email"/>
              </div>
              <div className="password">
                  <input className="form_input" type="password"  id="password" placeholder="Hasło"/>
              </div>
              <div className="confirm-password">
                  <input className="form_input" type="password" id="confirmPassword" placeholder="Powtórz hasło"/>
              </div>
          </div>
          <div class="footer">
              <button type="submit" class="btn">Zarejestruj</button>
          </div>
      </div>      
    )       
}
export default RegistrationForm;