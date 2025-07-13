// // import React, { useState } from 'react'
// // import { uploadMeeting } from '../api/meetings'
// // import { useNavigate } from 'react-router-dom'

// // export default function UploadMeeting() {
// //   const [url, setUrl] = useState('')
// //   const [title, setTitle] = useState('')
// //   const [error, setError] = useState(null)
// //   const navigate = useNavigate()

// //   const handleSubmit = async (e) => {
// //     e.preventDefault()
// //     setError(null)
// //     try {
// //       await uploadMeeting({ title, file_url: url })
// //       navigate('/')
// //     } catch (err) {
// //       setError(err.message)
// //     }
// //   }

// //   return (
// //     <form onSubmit={handleSubmit}>
// //       <h1>Upload Meeting</h1>
// //       {error && <p style={{color:'red'}}>{error}</p>}
// //       <div>
// //         <label>Title: </label>
// //         <input value={title} onChange={e => setTitle(e.target.value)} required />
// //       </div>
// //       <div>
// //         <label>File URL: </label>
// //         <input value={url} onChange={e => setUrl(e.target.value)} required />
// //       </div>
// //       <button type="submit">Upload</button>
// //     </form>
// //   )
// // }
// import React, { useState, useRef } from 'react';
// import { uploadMeeting } from '../api/meetings';
// import { useNavigate } from 'react-router-dom';
// import '/UploadMeeting.css';
// import axios from 'axios';


// export default function UploadMeeting() {
//   const [url, setUrl] = useState('');
//   const [title, setTitle] = useState('');
//   const [file, setFile] = useState(null);
//   const [error, setError] = useState(null);
//   const [isUploading, setIsUploading] = useState(false);
//   const fileInputRef = useRef(null);
//   const navigate = useNavigate();

//   const handleFileClick = () => {
//     fileInputRef.current.click();
//   };

//   const handleFileChange = (e) => {
//     const selectedFile = e.target.files[0];
//     if (selectedFile) {
//       setFile(selectedFile);
//       setUrl(''); // Clear URL if file is selected
//     }
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError(null);
//     setIsUploading(true);
  
//     try {
//       const formData = new FormData();
//       formData.append('title', title);
//       if (file) {
//         formData.append('file', file);
//       } else if (url) {
//         formData.append('file_url', url);
//       } else {
//         throw new Error('Please provide either a file or a URL');
//       }
  
//       const response = await uploadMeeting(formData);
//       const meetingId = response.data?.meeting_id || response.meeting_id;
//       navigate(`/meeting/${meetingId}`);
//     } catch (err) {
//       console.error('Upload error:', err);
//       setError(err.response?.data?.detail || err.message);
//     } finally {
//       setIsUploading(false);
//     }
//   };
  

//   return (
//     <div className="upload-container">
//       <div className="upload-card">
//         <h1>Upload Meeting</h1>
        
//         {error && <div className="error-message">{error}</div>}

//         <form onSubmit={handleSubmit}>
//           <div className="form-group">
//             <label>Title</label>
//             <input
//               type="text"
//               value={title}
//               onChange={(e) => setTitle(e.target.value)}
//               required
//               placeholder="Enter meeting title"
//             />
//           </div>

//           <div className="upload-options">
//             <div className="file-upload">
//               <label>Upload File</label>
//               <div 
//                 className="file-drop-area" 
//                 onClick={handleFileClick}
//                 onDragOver={(e) => e.preventDefault()}
//                 onDrop={(e) => {
//                   e.preventDefault();
//                   const droppedFile = e.dataTransfer.files[0];
//                   if (droppedFile) {
//                     setFile(droppedFile);
//                     setUrl('');
//                   }
//                 }}
//               >
//                 <input 
//                   type="file" 
//                   ref={fileInputRef}
//                   onChange={handleFileChange}
//                   style={{ display: 'none' }}
//                 />
//                 <div className="file-drop-content">
//                   {file ? (
//                     <span>{file.name}</span>
//                   ) : (
//                     <>
//                       <span className="drop-icon">↑</span>
//                       <span>Drag & drop files or click to browse</span>
//                       <span className="file-types">MP3, MP4, or PDF (MAX. 50MB)</span>
//                     </>
//                   )}
//                 </div>
//               </div>
//             </div>

//             <div className="or-divider">
//               <span>OR</span>
//             </div>

//             <div className="form-group">
//               <label>File URL</label>
//               <input
//                 type="url"
//                 value={url}
//                 onChange={(e) => {
//                   setUrl(e.target.value);
//                   if (e.target.value) setFile(null);
//                 }}
//                 disabled={!!file}
//                 placeholder="Paste file URL here"
//               />
//             </div>
//           </div>

//           <button type="submit" disabled={isUploading}>
//             {isUploading ? 'Uploading...' : 'Transcribe Meeting'}
//           </button>
//         </form>
//       </div>
//     </div>
//   );
// }

import React, { useState, useRef } from 'react';
import { uploadMeeting } from '../api/meetings';
import { useNavigate } from 'react-router-dom';
import '../UploadMeeting.css';

export default function UploadMeeting() {
  const [url, setUrl] = useState('');
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUrl('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('title', title);
      if (file) {
        formData.append('file', file);
      } else if (url) {
        formData.append('file_url', url);
      } else {
        throw new Error('Please provide either a file or URL');
      }

      const response = await uploadMeeting(formData);
      const meetingId = response.data?.meeting_id || response.meeting_id;
      navigate(`/meeting/${meetingId}`);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.detail || err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-page-container">
      {/* Background Blobs */}
      <div className="blob blob-1"></div>
      <div className="blob blob-2"></div>
      <div className="blob blob-3"></div>

      {/* Main Content */}
      <div className="upload-container">
        <div className="upload-card">
          <h1 className="upload-title">Upload Meeting</h1>
          
          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit} className="upload-form">
            <div className="form-group">
              <label>Meeting Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                placeholder="Enter meeting title"
              />
            </div>

            <div className="upload-options">
              <div className="file-upload">
                <label>Upload File</label>
                <div 
                  className="file-drop-area" 
                  onClick={handleFileClick}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault();
                    const droppedFile = e.dataTransfer.files[0];
                    if (droppedFile) {
                      setFile(droppedFile);
                      setUrl('');
                    }
                  }}
                >
                  <input 
                    type="file" 
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                  />
                  <div className="file-drop-content">
                    {file ? (
                      <span className="file-name">{file.name}</span>
                    ) : (
                      <>
                        <span className="drop-icon">↑</span>
                        <span>Drag & drop files or click to browse</span>
                        <span className="file-types">MP3, MP4, or PDF (MAX. 50MB)</span>
                      </>
                    )}
                  </div>
                </div>
              </div>

              <div className="or-divider">
                <span>OR</span>
              </div>

              <div className="form-group">
                <label>File URL</label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => {
                    setUrl(e.target.value);
                    if (e.target.value) setFile(null);
                  }}
                  disabled={!!file}
                  placeholder="Paste file URL here"
                />
              </div>
            </div>

            <button type="submit" disabled={isUploading} className="submit-button">
              {isUploading ? (
                <>
                  <span className="spinner"></span>
                  Uploading...
                </>
              ) : (
                'Transcribe Meeting'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}