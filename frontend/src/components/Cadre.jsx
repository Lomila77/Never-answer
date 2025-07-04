const Cadre = ({ size, componentChildren }) => {
    const classname = size === "small" ? "flex flex-col items-center justify-center bg-neutral size-16 rounded-full inset-shadow-sm box-border border-4 border-accent" :
        "flex flex-col bg-neutral justify-center w-100 m-5 rounded-lg shadow-neutral-900 overflow-y-auto max-h-[500px] p-4"

    return <div className={classname}>
            {componentChildren}
    </div>

}

export default Cadre;