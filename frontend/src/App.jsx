import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './styles/style.css'
import Home from './pages/Home'
import Background from './components/Background'
import Header from './components/Header'

function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <div>
        <Header />
        <Background componentChildren={
          <Routes>
            <Route path="/" element={<Home />} />
          </Routes>
        } />
      </div>
    </BrowserRouter>
  )
}

export default App
