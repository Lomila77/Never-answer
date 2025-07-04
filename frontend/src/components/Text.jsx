const Text = ({ theme, content }) => {
    const classname = theme === "dark" ? "text-lg mb-3 font-semibold font-sans" :
        "text-lg mb-3 text-neutral font-semibold font-sans"
    return <p className={classname}>
        {content}
    </p>
}

export default Text;