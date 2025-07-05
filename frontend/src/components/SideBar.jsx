import Book from '../assets/book.png'
import Evaluation from '../assets/evaluation.png'
import Message from '../assets/chat.png'

const SideBar = ( {setRoute} ) => {
    return (
        <drawer className="drawer drawer-open bg-emerald-50 shadow-2xl text-primary-content w-14 md:w-20 py-2">
            <div className="flex flex-col items-center gap-6">
                <button onClick={() => setRoute("ws://localhost:8000/ws")}>
                    <img src={Message} alt="Message" className="size-[2em]" />
                    <span className="dock-label">Chat</span>
                </button>

                <button onClick={() => setRoute("ws://localhost:8000/ws/course")}>
                    <img src={Book} alt="Book" className="size-[2em]" />
                    <span className="dock-label">Course</span>
                </button>

                <button onClick={() => setRoute("ws://localhost:8000/ws/evaluation")}>
                    <img src={Evaluation} alt="Evaluation" className="size-[2em]" />
                    <span className="dock-label">Evaluation</span>
                </button>
            </div>
        </drawer>
    )
}

export default SideBar;
