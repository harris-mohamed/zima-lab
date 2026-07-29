import { useState } from 'react'

interface CameraFeedProps {
  src: string
  label: string
}

export function CameraFeed({ src, label }: CameraFeedProps) {
  const [connection, setConnection] = useState<'connecting' | 'live' | 'offline'>('connecting')
  const [attempt, setAttempt] = useState(0)
  const streamUrl = `${src}?attempt=${attempt}`

  return (
    <article className="camera-card">
      <div className="camera-card__header">
        <h3>{label}</h3>
        <span className={`camera-state camera-state--${connection}`}>
          <span aria-hidden="true" />
          {connection === 'live' ? 'Live' : connection === 'offline' ? 'Unavailable' : 'Connecting'}
        </span>
      </div>
      <div className="camera-card__viewport">
        <img
          key={streamUrl}
          src={streamUrl}
          alt={`${label} live feed`}
          onLoad={() => setConnection('live')}
          onError={() => setConnection('offline')}
        />
        {connection !== 'live' && (
          <div className="camera-card__fallback">
            <p>{connection === 'offline' ? 'Camera feed is unavailable' : 'Opening camera feed…'}</p>
            {connection === 'offline' && (
              <button
                className="button"
                type="button"
                onClick={() => {
                  setConnection('connecting')
                  setAttempt((current) => current + 1)
                }}
              >
                Reconnect
              </button>
            )}
          </div>
        )}
      </div>
    </article>
  )
}
