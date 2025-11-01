import './VideoPlayer.css'

function VideoPlayer({ videoUrl }) {
  const handleDownload = () => {
    const a = document.createElement('a')
    a.href = videoUrl
    a.download = 'hiresong-pitch.mp4'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  return (
    <div className="video-player">
      <div className="success-message">
        <h2>🎉 Your Video Pitch is Ready!</h2>
        <p>Watch your personalized 30-second pitch below</p>
      </div>
      
      <div className="video-container">
        <video
          controls
          className="video"
        >
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
      
      <div className="video-actions">
        <button className="btn btn-download" onClick={handleDownload}>
          ⬇️ Download Video
        </button>
      </div>
    </div>
  )
}

export default VideoPlayer
