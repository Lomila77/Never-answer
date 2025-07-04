const Background = ({ componentChildren }) => {
    return <div className="flex flex-col items-center justify-center p-8 bg-neutral shadow-lg w-full">
            {componentChildren}
        </div>
}

export default Background;