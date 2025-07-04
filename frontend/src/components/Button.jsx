import { Link } from "react-router-dom";

const Button = ({ theme, text, to, submit, disabled }) => {
    const classname = theme === "dark" ? "btn btn-accent hover:border-black rounded-xl text-xl text-white inset-shadow-sm font-sans font-extrabold" :
    "btn btn-neutral hover:border-primary rounded-xl text-xl text-accent inset-shadow-sm shadow-xl font-sans font-bold"

    
    return <div className="flex-1">
        {to ? (
            <Link to={to}>
                <button disabled={disabled} className={classname}>
                    {text}
                </button>
            </Link>
        ) : submit ? (
                <button disabled={disabled} className={classname}>
                    {text}
                </button>
        ) : null
        }
    </div>
}

export default Button;