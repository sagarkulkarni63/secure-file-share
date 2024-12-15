import React, { useState } from 'react';
import { useAppDispatch } from '../utils/hooks';
import { mfaConfirm } from '../store/authSlice';

export default function MFAConfirm() {
  const [token,setToken] = useState('');
  const dispatch = useAppDispatch();

  const handleMfa = () => {
    dispatch(mfaConfirm(token));
  };

  return (
    <div>
      <h2>MFA Required</h2>
      <input placeholder="MFA Token" value={token} onChange={e=>setToken(e.target.value)}/>
      <button onClick={handleMfa}>Confirm</button>
    </div>
  );
}
