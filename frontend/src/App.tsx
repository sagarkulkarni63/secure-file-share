import React, { useState } from 'react';
import { useAppSelector, useAppDispatch } from './utils/hooks';
import Login from './components/Login';
import Register from './components/Register';
import MFAConfirm from './components/MFAConfirm';
import MFASetup from './components/MFASetup';
import UploadFile from './components/UploadFile';
import FileList from './components/FileList';
import ShareFile from './components/ShareFile';
import './styles/app.css';
import { apiFetch } from './utils/api';
import { logout } from './store/authSlice';
function App() {
  const { isLoggedIn, mfaRequired } = useAppSelector(state => state.auth);
  const [showRegister, setShowRegister] = useState(false);
  const dispatch = useAppDispatch();
  const handleRegisterSuccess = () => {
    setShowRegister(false);
  };

  const handleLogout = async () => {
    await apiFetch('/logout/', { method:'POST' });
    dispatch(logout());
  };
  return (
    <div style={{maxWidth:'600px', margin:'auto', padding:'20px', fontFamily:'Arial'}}>
      <h1>Secure File Sharing App</h1>

      {!isLoggedIn && (
        <>
          {!showRegister ? (
            <>
              <Login />
              <p style={{marginTop:'10px'}}>Don't have an account? <a href="#" onClick={()=>setShowRegister(true)}>Register here</a></p>
            </>
          ) : (
            <Register onRegisterSuccess={handleRegisterSuccess}/>
          )}
        </>
      )}

      {isLoggedIn && (
        <>
          {/* <MFASetup /> */}
          <button onClick={handleLogout} style={{marginBottom:'20px'}}>Logout</button>
          <h2>Your Files</h2>
          <UploadFile />
          <FileList />
          <ShareFile />
        </>
      )}
    </div>
  );
}

export default App;
