const Chat = ({ messages }) => {
    return (
        <div>
            {messages.map((msg, idx) => (
                <div
                    key={idx}
                    className={`chat ${msg.from === "ia" ? "chat-start" : "chat-end"}`}
                >
                    <div className="chat-bubble">{msg.text}</div>
                </div>
            ))}
        </div>
    );
}

export default Chat;