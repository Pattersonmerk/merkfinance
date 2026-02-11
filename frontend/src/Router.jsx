import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import App from './App'
import ContactUs from './ContactUs'
import Navbar from './Navbar'

function AppRouter() {
  return (
    <Router>
      <Routes>
        {/* Login + Payment page */}
        <Route path="/" element={<App />} />

        {/* Payment details page (same App component handles it) */}
        <Route path="/payment/:swift" element={<App />} />

        {/* Contact page always shows Navbar */}
        <Route path="/contact" element={
          <>
            <Navbar />
            <ContactUs />
          </>
        } />
      </Routes>
    </Router>
  )
}

export default AppRouter
