import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import './App.css';
import OIP from './assets/OIP.webp';

function App() {
  const [identifier, setIdentifier] = useState('');
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [payment, setPayment] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    const path = window.location.pathname || '';
    const m = path.match(/^\/payment\/(.+)$/);
    if (m) {
      const swift = decodeURIComponent(m[1]);
      fetchPayment(swift);
    }
  }, []);

  async function fetchPayment(swift) {
    setLoading(true);
    setError(null);
    try {
      const backendBase = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";
      const url = `${backendBase.replace(/\/$/, "")}/api/payments/${encodeURIComponent(swift)}/`;
      const res = await fetch(url, { headers: { "Accept": "application/json" } });
      if (!res.ok) throw new Error('SWIFT code introuvable');
      const data = await res.json();
      setPayment(data);
      navigate(`/payment/${encodeURIComponent(swift)}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleBack() {
    setPayment(null);
    setError(null);
    navigate('/');
  }

  function handleLogout() {
    setPayment(null);
    setError(null);
    navigate('/');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    if (!identifier) return setError('Veuillez entrer un SWIFT');
    await fetchPayment(identifier.trim());
  }

  function formatDate(dateString) {
    if (!dateString) return '';
    return new Date(dateString).toLocaleString('fr-FR', {
      dateStyle: 'medium',
      timeStyle: 'short',
    });
  }

  return (
    <div className="page-wrapper">
      <div className="center-block">
        {payment && (
          <div className="navbar-wrapper">
            <Navbar username={payment?.username} onLogout={handleLogout} />
          </div>
        )}

        {payment ? (
          <div className="login-card details" role="main">
            <button className="back" onClick={handleBack}>&larr; Retour</button>
            <h2>Détail du virement</h2>

            <div className="detail-grid">
              <div className="detail-item"><span className="label">ID transfert :</span><span className="detail-val">{payment.id_transfert}</span></div>
              <div className="detail-item"><span className="label">Banque :</span><span className="detail-val">{payment.banque_name}</span></div>
              <div className="detail-item"><span className="label">Numéro de compte :</span><span className="detail-val">{payment.beneficiaire_compte}</span></div>
              <div className="detail-item"><span className="label">Montant ($):</span><span className="detail-val">{payment.montant}</span></div>
              <div className="detail-item"><span className="label">Date d'échéance :</span><span className="detail-val">{formatDate(payment.echeance_date)}</span></div>
              <div className="detail-item"><span className="label">Date d'expiration :</span><span className="detail-val">{formatDate(payment.expiration_date)}</span></div>
              <div className="detail-item"><span className="label">Bénéficiaire :</span><span className="detail-val">{payment.beneficiaire_nom}</span></div>
              <div className="detail-item"><span className="label">Téléphone :</span><span className="detail-val">{payment.beneficiaire_telephone}</span></div>
              <div className="detail-item"><span className="label">Email du récepteur :</span><span className="detail-val">{payment.beneficiaire_email}</span></div>
              <div className="detail-item"><span className="label">Motif :</span><span className="detail-val">{payment.motif}</span></div>
            </div>

            <h3 className="moving-label">Entrez votre code de validation</h3>
            <input type="text" className="disabled-input" disabled />

            <form onSubmit={(e) => { e.preventDefault(); alert('Code soumis'); }}>
              <button type="submit">Soumettre</button>
            </form>

            <div className="support-section">
              <p>Un problème rencontré ?<br />Notre service d'assistance vous aide pour tout problème rencontré lié aux virements.</p>
              <button className="contact-button" onClick={() => navigate('/contact')}>Contactez nous</button>
            </div>

            <footer className="legal">Copyright © 2025 Merck Finance.</footer>
          </div>
        ) : (
          <div className="login-card" role="main">
            <header className="brand">
              <h1><img src={OIP} alt="Merck Finance Logo" className="logo"/>Finances</h1>
            </header>

            <section className="intro">
              <h2>Bienvenue!</h2>
              <p>Connectez-vous</p>
            </section>

            <form className="login-form" onSubmit={handleSubmit}>
              <label className="field">
                <span className="label-text">Code SWIFT</span>
                <input
                  type="text"
                  placeholder="Entrez votre code SWIFT"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  required
                />
              </label>

              <div className="form-row">
                <label className="remember">
                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                  />
                  <span>Se souvenir de moi</span>
                </label>
              </div>

              <button className="submit" type="submit" disabled={loading}>
                {loading ? 'Chargement...' : 'Se connecter'}
              </button>

              {error && <p className="error">{error}</p>}
            </form>

            <footer className="legal">Copyright © 2025 Merck Finance.</footer>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
