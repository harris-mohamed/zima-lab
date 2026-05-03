import { useRef } from 'react'

interface CameraFeedProps {
  src: string
  label: string
}

export function CameraFeed({ src, label }: CameraFeedProps) {
  const imgRef = useRef<HTMLImageElement>(null)

  const handleError = () => {
    // Reload the MJPEG stream after a short delay on error.
    setTimeout(() => {
      if (imgRef.current) {
        imgRef.current.src = `${src}?t=${Date.now()}`
      }
    }, 2000)
  }

  return (
    <div className="camera-card">
      <h3 className="camera-card__label">{label}</h3>
      <img
        ref={imgRef}
        src={src}
        alt={label}
        className="camera-card__img"
        onError={handleError}
      />
    </div>
  )
}
