const Background = ({ componentChildren }) => {
    return <div className="flex w-full flex-col items-center justify-center bg-[var(--primary)]/10  h-full">
            {componentChildren}
        </div>
}

export default Background;
