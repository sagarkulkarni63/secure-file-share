import React from 'react';
import { useAppDispatch, useAppSelector } from '../utils/hooks';
import { fetchFiles } from '../store/fileSlice';
import { useEffect } from 'react';
import { apiFetch } from '../utils/api';

export default function FileList() {
  const dispatch = useAppDispatch();
  const { list, loading, error } = useAppSelector(state=>state.files);

  useEffect(()=>{
    dispatch(fetchFiles());
  },[dispatch]);

  if(loading) return <p>Loading files...</p>;
  if(error) return <p style={{color:'red'}}>Error: {error}</p>;

  const handleDownload = async (fileId: number, filename: string) => {
    const res = await fetch(`${process.env.REACT_APP_API_URL}/files/${fileId}/download/`, {
      credentials: 'include'
    });
    if(res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      window.URL.revokeObjectURL(url);
    } else {
      alert("Could not download file. Please make sure you're logged in.");
    }
  };

  return (
    <div style={{marginTop:'20px'}}>
      <h3>Your Files</h3>
      <ul style={{listStyle:'none', padding:0}}>
        {list.map(file => (
          <li key={file.id} style={{marginBottom:'10px'}}>
            {file.filename} 
            <button style={{marginLeft:'10px'}} onClick={()=>handleDownload(file.id, file.filename)}>Download</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
