import React, { useState } from 'react';
import { apiFetch } from '../utils/api';
import { useAppDispatch } from '../utils/hooks';
import { fetchFiles } from '../store/fileSlice';

export default function UploadFile() {
  const [selectedFile,setSelectedFile] = useState<File|null>(null);
  const dispatch = useAppDispatch();

  const handleUpload = async () => {
    if(!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);
    try {
      await apiFetch('/files/upload/', {
        method:'POST',
        body: formData,
        isForm:true,
      });
      alert("File uploaded successfully!");
      // Fetch updated file list
      dispatch(fetchFiles());
    } catch(e:any) {
      alert(e.message);
    }
  };

  return (
    <div style={{marginTop:'20px'}}>
      <h3>Upload a File</h3>
      <input type="file" onChange={e=>setSelectedFile(e.target.files?.[0]||null)}/>
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}
