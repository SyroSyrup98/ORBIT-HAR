import { useState } from "react";
import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <div className={`app ${darkMode ? "dark" : "light"}`}>
      {/* Header */}
      <header className="topbar">
        <div>
          <h1>ORBIT-HAR</h1>
          <span>ONBOARD EXPERIMENT ASSISTANT</span>
        </div>

        <div className="header-actions">
          <button
            className="theme-toggle"
            onClick={() => setDarkMode(!darkMode)}
            aria-label="Toggle theme"
          >
            <span className="theme-icon">
              {darkMode ? "☀" : "☾"}
            </span>

            <span>
              {darkMode ? "LIGHT" : "DARK"}
            </span>
          </button>

          <div className="system-status">
            <span className="status-dot"></span>
            SYSTEM ONLINE
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="dashboard">

        {/* Camera */}
        <section className="camera-panel panel">
          <div className="panel-header">
            <span>LIVE CAMERA</span>
            <span className="muted">CAM-01</span>
          </div>

          <div className="camera-feed">
            <div className="camera-placeholder">
              CAMERA FEED
            </div>

            <div className="camera-overlay">
              <span>LOCAL INFERENCE</span>
            </div>
          </div>

          <div className="camera-info">
            <div>
              <span className="label">ACTIVITY</span>
              <strong>WAITING</strong>
            </div>

            <div>
              <span className="label">OBJECT</span>
              <strong>NONE</strong>
            </div>

            <div>
              <span className="label">CONFIDENCE</span>
              <strong>--</strong>
            </div>
          </div>
        </section>

        {/* Mission */}
        <aside className="mission-panel panel">
          <div className="panel-header">
            <span>MISSION</span>
            <span className="mission-id">EXP-01</span>
          </div>

          <div className="mission-section">
            <span className="label">EXPERIMENT</span>
            <h2>Sample Handling</h2>
          </div>

          <div className="mission-section">
            <span className="label">PROGRESS</span>

            <div className="progress-text">
              <strong>01</strong>
              <span>/ 04 STEPS</span>
            </div>

            <div className="progress-bar">
              <div className="progress-fill"></div>
            </div>
          </div>

          <div className="mission-section">
            <span className="label">EXPECTED ACTION</span>
            <strong className="action">WAITING</strong>
          </div>

          <div className="mission-section">
            <span className="label">SYSTEM STATE</span>

            <div className="state">
              <span className="state-dot"></span>
              PERCEPTION READY
            </div>
          </div>
        </aside>

        {/* Sequence */}
        <section className="sequence-panel panel">
          <div className="panel-header">
            <span>EXPERIMENT SEQUENCE</span>
            <span className="muted">EXP-01</span>
          </div>

          <div className="sequence-list">
            <SequenceStep
              number="01"
              action="Reach"
              object="Bottle"
              status="current"
            />

            <SequenceStep
              number="02"
              action="Pick Up"
              object="Bottle"
            />

            <SequenceStep
              number="03"
              action="Move"
              object="Bottle"
            />

            <SequenceStep
              number="04"
              action="Place"
              object="Bottle"
            />
          </div>
        </section>

        {/* Logs */}
        <section className="log-panel panel">
          <div className="panel-header">
            <span>SEQUENCE LOG</span>
            <span className="muted">LOCAL</span>
          </div>

          <div className="log-list">
            <Log
              time="--:--:--"
              message="Waiting for experiment input..."
            />
          </div>
        </section>

      </main>
    </div>
  );
}

function SequenceStep({ number, action, object, status = "" }) {
  return (
    <div className={`sequence-step ${status}`}>
      <span className="step-number">{number}</span>

      <div className="step-info">
        <strong>{action}</strong>
        <span>{object}</span>
      </div>

      <span className="step-status">
        {status === "current" ? "CURRENT" : "PENDING"}
      </span>
    </div>
  );
}

function Log({ time, message }) {
  return (
    <div className="log-entry">
      <span>{time}</span>
      <p>{message}</p>
    </div>
  );
}

export default App;