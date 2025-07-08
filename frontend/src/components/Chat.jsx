const Chat = ({ messages }) => {
    return (
        <div className="min-h-0">
            {messages.map((msg, idx) => (
                <div
                    key={idx}
                    className={`chat ${msg.from === "ia" ? "chat-start" : "chat-end"}`}
                >
                    {msg.audio ? (
                        <>
                        {console.log("AUDIO TYPE:", msg.audio.arrayBuffer().then(buffer => {
                        const bytes = new Uint8Array(buffer.slice(0, 12));
                        const header = String.fromCharCode(...bytes);
                        console.log("Header:", header); // Doit contenir "RIFF....WAVE"
                        }))}
                        <audio controls className="bg-white text-[#333333] p-2 rounded-lg shadow-lg shadow-[#04A3A9]/20">
                            <source src={URL.createObjectURL(msg.audio)} type="audio/wav" />
                            Your browser does not support the audio element.
                        </audio></>
                    ) :
                    <div className="bg-white text-[#333333] p-2 rounded-lg shadow-lg shadow-[#04A3A9]/20">{msg.text}</div>
}                </div>
            ))}
        </div>
    );
}

export default Chat;
