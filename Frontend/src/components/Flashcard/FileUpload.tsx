import React from 'react';

interface FileUploadProps {
  onFileChange: (file: File) => void;
  onUpload: () => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileChange, onUpload }) => {
  return (
    <div className="file-upload">
  <label className="upload-button">
    <input type="file" onChange={(e) => {
      if (e.target.files?.[0]) onFileChange(e.target.files[0]);
    }} />
    📤 Click here to upload a file
  </label>
  <button className="generate-btn" onClick={onUpload}>Generate Flashcards</button>
</div>

  );
};

export default FileUpload;
