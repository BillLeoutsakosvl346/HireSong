import { useRef, useState } from 'react'
import './FileUpload.css'

function FileUpload({ label, accept, onFileSelect, file, fileType }) {
  const inputRef = useRef(null)
  const [judgeComment, setJudgeComment] = useState('')

  const handleClick = () => {
    inputRef.current?.click()
  }

  const handleChange = (e) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      onFileSelect(selectedFile)
      // Judge the file
      judgeFile(selectedFile)
    }
  }

  const judgeFile = (file) => {
    const sizeInMB = file.size / 1024 / 1024
    
    if (fileType === 'pdf') {
      const comments = [
        sizeInMB > 5 ? "Wow, that's a THICC CV! 📚" : "Nice and compact CV! 📄",
        "I bet this CV is full of lies... 😏",
        "Hope there are no typos in there! 🤞",
        "Did you really graduate from there? 🤔",
        "Your CV looks... interesting... 👀"
      ]
      setJudgeComment(comments[Math.floor(Math.random() * comments.length)])
    } else {
      const comments = [
        "You look... unique! 📸",
        "Is that really your best angle? 🤨",
        "Professional! (kind of) 👔",
        "I've seen worse selfies! 😅",
        "Camera loves you! (or does it?) 📷"
      ]
      setJudgeComment(comments[Math.floor(Math.random() * comments.length)])
    }

    // Clear comment after a few seconds
    setTimeout(() => setJudgeComment(''), 4000)
  }

  const handleRemove = (e) => {
    e.stopPropagation()
    onFileSelect(null)
    if (inputRef.current) {
      inputRef.current.value = ''
    }
  }

  return (
    <div className="file-upload">
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleChange}
        style={{ display: 'none' }}
      />
      
      {!file ? (
        <button
          type="button"
          className="upload-button"
          onClick={handleClick}
        >
          {label}
        </button>
      ) : (
        <>
          <div className="file-preview">
            <div className="file-info">
              {fileType === 'image' ? (
                <img
                  src={URL.createObjectURL(file)}
                  alt="Preview"
                  className="file-thumbnail"
                />
              ) : (
                <div className="file-icon">📄</div>
              )}
              <div className="file-details">
                <span className="file-name">{file.name}</span>
                <span className="file-size">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </span>
              </div>
            </div>
            <button
              type="button"
              className="remove-button"
              onClick={handleRemove}
            >
              ✕
            </button>
          </div>
          {judgeComment && (
            <div className="judge-comment">
              💭 {judgeComment}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default FileUpload
