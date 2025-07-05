const Chat = ({ messages }) => {
    return (
        <div>
            {messages.map((msg, idx) => (
                <div
                    key={idx}
                    className={`chat ${msg.from === "ia" ? "chat-start" : "chat-end"}`}
                >
                    <div className="bg-white p-2 rounded-lg shadow-lg shadow-emerald-100">{msg.text}</div>
                </div>
            ))}
        </div>
    );
}

export default Chat;
