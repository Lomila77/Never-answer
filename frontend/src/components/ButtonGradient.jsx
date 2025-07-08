import { ArrowRight } from "lucide-react";

const GradientButton = ({ children, onClick, className = '', style = {}, disabled }) => {
    return(
        <button
        className={` disabled:opacity-15 hover:shadow-emerald-400/40 hover:shadow-lg transiton-all duration-200 hover:scale-120 !text-white brightness-110 px-6 py-2 rounded-full bg-gradient-to-r from-[var(--primary)] to-emerald-400 transition-colors mt-4 ` + className}
        // onClick={() => handlesubmitSelection(choices[selectedIndex])}
        disabled={disabled}
        onClick={onClick}
    ><ArrowRight/></button>
    )
}
export default GradientButton;
