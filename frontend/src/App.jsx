import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import Bd_Noticia from '../components/Bd_Noticia.jsx'

function App() {
  const [noti, setNots] = useState([])

  useEffect(() => {
    fetch('http://localhost:8000/api/noticias/')
    .then(res => res.json())
    .then(res => setNots(res))
  })
  
  return (
    <Bd_Noticia/>
  )
}

export default App
