import React, { useState, useEffect } from 'react';
import { apiFetch } from '../utils/api';

export default function MFASetup() {
  const [secret,setSecret] = useState('');

  useEffect(()=>{
    apiFetch('/mfa-setup/')
      .then(res=>setSecret(res.secret))
      .catch(console.error);
  },[]);

  return (
    <div style={{marginTop:'20px'}}>
      <h2>MFA Setup</h2>
      {secret && (
        <p>
          Your TOTP secret: <b>{secret}</b><br/>
          <span style={{color:'blue'}}>Please save this secret in your authenticator app (e.g., Google Authenticator) to complete MFA login.</span>
        </p>
      )}
    </div>
  );
}
