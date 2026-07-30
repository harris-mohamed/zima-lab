import { useCallback, useEffect, useState } from 'react'

const RECONNECT_INTERVAL_MS = 5 * 60 * 1000
const ERROR_RETRY_DELAY_MS = 5 * 1000

interface CameraFeedProps {
  src: string
  label: string
}

export function CameraFeed({ src, label }: CameraFeedProps) {
  const [connection, setConnection] = useState<'connecting' | 'live' | 'offline'>('connecting')
  const [attempt, setAttempt] = useState(() => Date.now())
  const streamUrl = `${src}?attempt=${attempt}`

  const reconnect = useCallback(() => {
    setConnection('connecting')
    setAttempt(Date.now())
  }, [])

  useEffect(() => {
    const reconnectIfVisible = () => {
      if (document.visibilityState === 'visible') {
        reconnect()
      }
    }

    const interval = window.setInterval(reconnectIfVisible, RECONNECT_INTERVAL_MS)
    window.addEventListener('focus', reconnect)
    window.addEventListener('online', reconnect)
    document.addEventListener('visibilitychange', reconnectIfVisible)

    return () => {
      window.clearInterval(interval)
      window.removeEventListener('focus', reconnect)
      window.removeEventListener('online', reconnect)
      document.removeEventListener('visibilitychange', reconnectIfVisible)
    }
  }, [reconnect])

  useEffect(() => {
    if (connection !== 'offline') {
      return
    }

    const timeout = window.setTimeout(reconnect, ERROR_RETRY_DELAY_MS)
    return () => window.clearTimeout(timeout)
  }, [connection, reconnect])

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
                onClick={reconnect}
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
