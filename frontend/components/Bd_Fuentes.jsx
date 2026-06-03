export default function Bd_Noticia({id,title }){
    return(
        <article>
            <h3>{id} : {title}</h3>
            <p>Descripcion de la noticia</p>
        </article>
    )
}