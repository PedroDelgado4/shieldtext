import { useState, useRef, useEffect } from "react"
import "../styles/floating.css"
import PDLogo from "../assets/PDLogo.svg"

function FloatingProfileButton() {
    const [open, setOpen] = useState(false)
    const containerRef = useRef(null)

    // Cerrar si haces click fuera
    useEffect(() => {
        function handleClickOutside(event) {
            if (
                containerRef.current &&
                !containerRef.current.contains(event.target)
            ) {
                setOpen(false)
            }
        }

        document.addEventListener("mousedown", handleClickOutside)

        return () => {
            document.removeEventListener("mousedown", handleClickOutside)
        }
    }, [])

    return (
        <div className="floating-container" ref={containerRef}>
            {open && (
                <div className="floating-popup">
                    <p>¡Visita mi perfil de GitHub para ver todos mis proyectos!</p>
                    <a
                        href="https://github.com/PedroDelgado4/"
                        target="_blank"
                        rel="noreferrer"
                    >
                        Ver GitHub →
                    </a>
                </div>
            )}

            <button
                className="floating-btn"
                onClick={() => setOpen(!open)}
            >
                <img src={PDLogo} alt="Logo de Pedro Delgado" className="floating-logo" />
            </button>
        </div>
    )
}

export default FloatingProfileButton