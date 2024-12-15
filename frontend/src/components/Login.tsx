// Login.tsx
import React, { useState } from 'react';
import { useAppDispatch } from '../utils/hooks';
import { login } from '../store/authSlice';

export default function Login() {
  const [username,setUsername] = useState('');
  const [password,setPassword] = useState('');
  const [error,setError] = useState('');
  const dispatch = useAppDispatch();

  const handleLogin = async () => {
    try {
      await dispatch(login({username,password})).unwrap();
    } catch(e:any) {
      setError(e);
    }
  };

  return (
    <div style={{marginTop:'20px'}}>
      <h2>Login</h2>
      {error && <p style={{color:'red'}}>{error}</p>}
      <input placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)}/>
      <input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)}/>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
