const Plank = ({ componentChildren }) => {
    return (
        <div className="card bg-primary flex flex-col items-center justify-center p-10 rounded-3xl shadow-xl inset-shadow-sm">
            <div className="card-body">
                {componentChildren}
            </div>
        </div>
    )
}

export default Plank;