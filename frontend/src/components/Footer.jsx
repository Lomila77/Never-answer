import Book from '../assets/book.png'
import Evaluation from '../assets/evaluation.png'
import Message from '../assets/chat.png'

const Footer = ( {setRoute} ) => {
    return (
        <footer className="footer footer-horizontal footer-center p-10 bg-neutral text-primary-content">
            <div className="dock flex flex-row items-center gap-6">
                <button onClick={() => setRoute("ws://localhost:8000/ws")}>
                    <img src={Message} alt="Message" className="size-[2em]" />
                    <span className="dock-label">Chat</span>
                </button>
                
                <button onClick={() => setRoute("ws://localhost:8000/ws")}>
                    <img src={Book} alt="Book" className="size-[2em]" />
                    <span className="dock-label">Course</span>
                </button>
                
                <button onClick={() => setRoute("ws://localhost:8000/ws/evaluation")}>
                    <img src={Evaluation} alt="Evaluation" className="size-[2em]" />
                    <span className="dock-label">Evaluation</span>
                </button>
            </div>
        </footer>
    )
}

export default Footer;