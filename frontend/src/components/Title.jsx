const Title = ({ size, content }) => {
    const classname = size === "large" ? "text-4xl font-bold mb-5 text-neutral inner-text-shadow-lg font-sans" :
        "text-2xl font-bold mb-5 text-neutral inner-text-shadow-lg font-sans"
    return <h1 className={classname}>
        {content}
    </h1>
}

export default Title;