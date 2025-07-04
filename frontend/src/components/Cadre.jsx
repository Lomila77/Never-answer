const Cadre = ({ size, componentChildren }) => {
    const classname = size === "small" ? "flex flex-col items-center justify-center bg-neutral size-16 rounded-full inset-shadow-sm box-border border-4 border-accent" :
        "flex flex-col items-center bg-neutral justify-center size-32 m-5 rounded-full inner-shadow-neutral box-border border-4 border-accent"

    return <div className={classname}>
            {componentChildren}
    </div>

}

export default Cadre;