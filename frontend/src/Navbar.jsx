import OIP from './assets/OIP.webp'
import './App.css'

function Navbar({ username, onLogout }) {
  return (
    <div className="navbar-wrapper">
      <nav className="navbar">
        {/* Left side: Logo + Title */}
        <div className="navbar-left">
          <img src={OIP} alt="Merck Finance logo" className="navbar-logo" />
          <span className="navbar-title">Finances</span>
        </div>

        {/* Right side: Username + Logout */}
        <div className="navbar-actions">
          {username && (
            <span className="navbar-username">{username}</span>
          )}
          <button className="btn-logout" onClick={onLogout}>
            Déconnexion
          </button>
        </div>
      </nav>
    </div>
  )
}

export default Navbar
