import React, { useState, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../utils/hooks';
import { shareFile } from '../store/shareSlice';
import { fetchFiles } from '../store/fileSlice';

export default function ShareFile() {
  const dispatch = useAppDispatch();
  const { list } = useAppSelector(state => state.files);
  const { shareUrl, error, loading } = useAppSelector(state=>state.share);

  const [selectedFileId, setSelectedFileId] = useState<number>(0);
  const [permission,setPermission] = useState('view');
  const [validity,setValidity] = useState(1);

  useEffect(()=>{
    dispatch(fetchFiles());
  },[dispatch]);

  const handleShare = () => {
    if(selectedFileId === 0) {
      alert("Please select a file.");
      return;
    }
    dispatch(shareFile({file_id:selectedFileId, permission, validity}));
  };

  return (
    <div style={{marginTop:'20px'}}>
      <h3>Share a File</h3>
      <div style={{display:'flex', gap:'10px', alignItems:'center', flexWrap:'wrap'}}>
        <div>
          <label>File:</label><br/>
          <select value={selectedFileId} onChange={e=>setSelectedFileId(Number(e.target.value))}>
            <option value={0}>-- Select a file --</option>
            {list.map(file => (
              <option key={file.id} value={file.id}>{file.filename}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Permission:</label><br/>
          <select value={permission} onChange={e=>setPermission(e.target.value)}>
            <option value="view">View</option>
            <option value="download">Download</option>
          </select>
        </div>
        <div>
          <label>Validity (hours):</label><br/>
          <input type="number" value={validity} onChange={e=>setValidity(Number(e.target.value))}/>
        </div>
        <button disabled={loading} onClick={handleShare}>Share</button>
      </div>
      {shareUrl && <p>Share URL: {shareUrl}</p>}
      {error && <p style={{color:'red'}}>Error: {error}</p>}
    </div>
  );
}
