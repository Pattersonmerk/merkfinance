import { useState } from 'react'
import { FaWhatsapp } from 'react-icons/fa';
import './ContactUs.css' // styles merged here

function ContactUs() {
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit(e) {
    e.preventDefault()
    setSubmitted(true) // just show confirmation, no backend call
  }

  return (
    <div className="contact-page">
      <h2>Nous Contacter</h2>
      <p>
        Agence de Canada (Toronto)<br />
        +1 (517) 225 3230<br />
        {' '}
        <a href="https://wa.me/15172253230" target="_blank" rel="noopener noreferrer">
          <FaWhatsapp size={32} color="white" />
        </a>
      </p>

      {!submitted ? (
        <form onSubmit={handleSubmit}>
          <label>
            Votre nom
            <input type="text" required />
          </label>

          <label>
            Email
            <input type="email" required />
          </label>

          <label>
            Message
            <textarea required />
          </label>

          <button type="submit">Envoyer</button>
        </form>
      ) : (
        <div className="confirmation">
          <h3>Merci pour votre message !</h3>
          <p>Nous vous répondrons sous peu.</p>
        </div>
      )}
    </div>
  )
}

export default ContactUs
