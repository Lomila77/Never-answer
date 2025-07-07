const Chat = ({ messages }) => {
    return (
        <div className="min-h-0">
            {messages.map((msg, idx) => (
                <div
                    key={idx}
                    className={`chat ${msg.from === "ia" ? "chat-start" : "chat-end"}`}
                >
                    {msg.audio ? (
                        <audio controls className="bg-white text-[#333333] p-2 rounded-lg shadow-lg shadow-[#04A3A9]/20">
                            <source src={URL.createObjectURL(msg.audio)} type="audio/webm" />
                            Your browser does not support the audio element.
                        </audio>
                    ) :
                    <div className="bg-white text-[#333333] p-2 max-w-1/2 whitespace-pre-wrap text-wrap rounded-lg shadow-lg shadow-[#04A3A9]/20">{msg.text}</div>
}                </div>
            ))}
        </div>
    );
}

export default Chat;
