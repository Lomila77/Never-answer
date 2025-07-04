import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './styles/style.css'
import Home from './pages/Home'
import Background from './components/Background'
import Header from './components/Header'
import Footer from './components/Footer'

function App() {
  const [route, setRoute] = useState("ws://localhost:8000/ws")

  return (
    <BrowserRouter>
      <div>
        <Header />
        <Background componentChildren={
          <Routes>
            <Route path="/" element={<Home route={route} />} />
          </Routes>
        } />
        <Footer setRoute={setRoute} />
      </div>
    </BrowserRouter>
  )
}

export default App
