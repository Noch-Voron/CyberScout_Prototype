import { useEffect, useState } from 'react'

export default function Bd_Noticia(){
    const [noti, setNots] = useState([])
    useEffect(() => {
        fetch('http://localhost:8000/api/noticias/')
        .then(res => res.json())
        .then(res => setNots(res))
    })
  
    return(
        <main>
            <h1>FrontEnd</h1>
            <h2>Noticias en la base de datos</h2>
            {noti.map((noticia) => (
                <article key ={noticia.id}>
                    <h3>{noticia.id} : {noticia.title}</h3>
                    <p>Descripcion de la noticia</p>
                </article>
            ))}
        </main>
    )
}