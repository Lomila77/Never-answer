import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './styles/style.css'
import Home from './pages/Home'
import Background from './components/Background'
import Header from './components/Header'

import SideBar from './components/SideBar'

function App() {
  const [route, setRoute] = useState("ws://localhost:8000/ws")
  const [welcomeDisplayed, setWelcomeDisplayed] = useState(false)

  return (
    <BrowserRouter>

        <div className='flex flex-row gap-0 h-full w-full overflow-hidden'>
        {/* <Header /> */}
            <SideBar setRoute={setRoute} />
            <Background componentChildren={
            <Routes>
                <Route path="/" element={<Home route={route} />} />
            </Routes>
            } />
      </div>
    </BrowserRouter>
  )
}

export default App
