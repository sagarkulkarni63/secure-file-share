import React, { useState } from 'react';
import { apiFetch } from '../utils/api';

export default function Register({onRegisterSuccess}: {onRegisterSuccess: ()=>void}) {
  const [username,setUsername] = useState('');
  const [password,setPassword] = useState('');
  const [error,setError] = useState('');

  const handleRegister = async () => {
    try {
      await apiFetch('/register/', {
        method:'POST',
        body: JSON.stringify({username,password})
      });
      alert("Registered successfully. You can now login.");
      onRegisterSuccess();
    } catch(e:any) {
      setError(e.message);
    }
  };

  return (
    <div style={{marginTop:'20px'}}>
      <h2>Register</h2>
      {error && <p style={{color:'red'}}>{error}</p>}
      <input placeholder="Username (min 3 chars, no spaces)" value={username} onChange={e=>setUsername(e.target.value)}/>
      <input type="password" placeholder="Password (min 8 chars)" value={password} onChange={e=>setPassword(e.target.value)}/>
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}
