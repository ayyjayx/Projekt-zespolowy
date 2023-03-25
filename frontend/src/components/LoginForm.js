import React, {useState} from 'react';
import './style.css'
function RegistrationForm() {
    return(
      <div className="form">
          <div className="form-body">
              <div className="login">
                  <label className="form_label" for="firstName">Login </label>
              </div>
              <div className="username">
                  <input className="form_input" type="text" id="userName" placeholder="Nazwa użytkownika"/>
              </div>
              <div className="password">
                  <input className="form_input" type="password"  id="password" placeholder="Hasło"/>
              </div>
          </div>
          <div class="footer">
              <button type="submit" class="btn">Zaloguj</button>
          </div>
      </div>      
    )       
}
export default RegistrationForm;