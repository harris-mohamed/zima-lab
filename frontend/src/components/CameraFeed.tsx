import { useEffect, useRef, useState } from 'react'

interface CameraFeedProps {
  src: string
  label: string
}

export function CameraFeed({ src, label }: CameraFeedProps) {
  const imgRef = useRef<HTMLImageElement>(null)
  const retryRef = useRef<number | null>(null)
  const backoffRef = useRef(2_000)
  const [offline, setOffline] = useState(false)

  const handleError = () => {
    setOffline(true)
    if (retryRef.current !== null) return

    retryRef.current = window.setTimeout(() => {
      retryRef.current = null
      if (imgRef.current) {
        imgRef.current.src = `${src}?t=${Date.now()}`
      }
      backoffRef.current = Math.min(backoffRef.current * 2, 60_000)
    }, backoffRef.current)
  }

  const handleLoad = () => {
    setOffline(false)
    backoffRef.current = 2_000
  }

  useEffect(() => {
    return () => {
      if (retryRef.current !== null) window.clearTimeout(retryRef.current)
    }
  }, [])

  return (
    <div className={`camera-card${offline ? ' camera-card--offline' : ''}`}>
      <h3 className="camera-card__label">{label}</h3>
      <img
        ref={imgRef}
        src={src}
        alt={label}
        className="camera-card__img"
        onError={handleError}
        onLoad={handleLoad}
      />
      {offline && <div className="camera-card__status">Camera unavailable</div>}
    </div>
  )
}
