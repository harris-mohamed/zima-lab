import { useCallback, useEffect, useMemo, useState } from 'react'
import { CameraFeed } from './components/CameraFeed'
import './styles/App.css'

type CameraSource = 'picam' | 'usb'

interface Snapshot {
  filename: string
  source: CameraSource
  taken_at: string | null
}

const CAMERA_NAMES: Record<CameraSource, string> = {
  picam: 'Pi Camera',
  usb: 'USB Camera',
}

function formatTimestamp(value: string | null) {
  if (!value) return 'Unknown time'
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

async function fetchSnapshots() {
  const response = await fetch('/api/cameras/snapshots')
  if (!response.ok) throw new Error(`Archive request failed: ${response.status}`)
  return (await response.json()) as Snapshot[]
}

export default function App() {
  const [snapshots, setSnapshots] = useState<Snapshot[]>([])
  const [archiveStatus, setArchiveStatus] = useState<'loading' | 'ready' | 'error'>('loading')
  const [activeSource, setActiveSource] = useState<CameraSource | 'all'>('all')
  const [selected, setSelected] = useState<Snapshot | null>(null)

  const loadSnapshots = useCallback(async () => {
    try {
      setSnapshots(await fetchSnapshots())
      setArchiveStatus('ready')
    } catch {
      setArchiveStatus('error')
    }
  }, [])

  useEffect(() => {
    fetchSnapshots()
      .then((data) => {
        setSnapshots(data)
        setArchiveStatus('ready')
      })
      .catch(() => setArchiveStatus('error'))
  }, [])

  const visibleSnapshots = useMemo(
    () => snapshots.filter((snapshot) => activeSource === 'all' || snapshot.source === activeSource),
    [activeSource, snapshots],
  )

  return (
    <main className="site-shell">
      <header className="site-header">
        <div>
          <p className="eyebrow">Camera monitor</p>
          <h1>Zima Lab</h1>
        </div>
        <span className="system-badge">
          <span aria-hidden="true" />
          Local system
        </span>
      </header>

      <section aria-labelledby="live-heading">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Now</p>
            <h2 id="live-heading">Live cameras</h2>
          </div>
        </div>
        <div className="live-grid">
          <CameraFeed src="/api/cameras/picam" label="Pi Camera" />
          <CameraFeed src="/api/cameras/usb" label="USB Camera" />
        </div>
      </section>

      <section aria-labelledby="archive-heading">
        <div className="section-heading archive-heading">
          <div>
            <p className="eyebrow">Last 24 hours</p>
            <h2 id="archive-heading">Archive</h2>
          </div>
          <button className="button button--secondary" type="button" onClick={() => void loadSnapshots()}>
            Refresh archive
          </button>
        </div>

        <div className="archive-controls" aria-label="Filter archive">
          {(['all', 'picam', 'usb'] as const).map((source) => (
            <button
              className={`filter${activeSource === source ? ' filter--active' : ''}`}
              type="button"
              key={source}
              onClick={() => setActiveSource(source)}
            >
              {source === 'all' ? 'All cameras' : CAMERA_NAMES[source]}
            </button>
          ))}
          {archiveStatus === 'ready' && (
            <span className="archive-count">{visibleSnapshots.length} images</span>
          )}
        </div>

        {archiveStatus === 'loading' && <p className="archive-message">Loading archive…</p>}
        {archiveStatus === 'error' && (
          <div className="archive-message archive-message--error">
            <p>The archive could not be loaded.</p>
            <button className="button button--secondary" type="button" onClick={() => void loadSnapshots()}>
              Try again
            </button>
          </div>
        )}
        {archiveStatus === 'ready' && visibleSnapshots.length === 0 && (
          <p className="archive-message">No archived images yet. The first images appear after capture starts.</p>
        )}
        {archiveStatus === 'ready' && visibleSnapshots.length > 0 && (
          <div className="archive-grid">
            {visibleSnapshots.map((snapshot) => (
              <button
                className="snapshot"
                type="button"
                key={snapshot.filename}
                onClick={() => setSelected(snapshot)}
              >
                <img
                  src={`/api/cameras/snapshots/${encodeURIComponent(snapshot.filename)}`}
                  alt={`${CAMERA_NAMES[snapshot.source]} at ${formatTimestamp(snapshot.taken_at)}`}
                  loading="lazy"
                />
                <span>
                  <strong>{CAMERA_NAMES[snapshot.source]}</strong>
                  <time dateTime={snapshot.taken_at ?? undefined}>{formatTimestamp(snapshot.taken_at)}</time>
                </span>
              </button>
            ))}
          </div>
        )}
      </section>

      {selected && (
        <div className="lightbox" role="dialog" aria-modal="true" aria-label="Archived camera image">
          <button className="lightbox__backdrop" type="button" onClick={() => setSelected(null)} aria-label="Close" />
          <div className="lightbox__panel">
            <div className="lightbox__header">
              <div>
                <strong>{CAMERA_NAMES[selected.source]}</strong>
                <time dateTime={selected.taken_at ?? undefined}>{formatTimestamp(selected.taken_at)}</time>
              </div>
              <button className="button button--secondary" type="button" onClick={() => setSelected(null)}>
                Close
              </button>
            </div>
            <img
              src={`/api/cameras/snapshots/${encodeURIComponent(selected.filename)}`}
              alt={`${CAMERA_NAMES[selected.source]} at ${formatTimestamp(selected.taken_at)}`}
            />
          </div>
        </div>
      )}
    </main>
  )
}
