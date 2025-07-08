import React from "react";
import { useState } from "react";
import { ArrowRight } from "lucide-react";

const Mbti = ({ setShowMbti, setMbtiSelection }) => {
    const [answers, setAnswers] = useState([]);
    const questions = [
        {
          question: "When you meet new people, you prefer to:",
          options: [
            "Talk to many people and get to know them quickly",
            "Talk to only a few people and prefer deep conversations",
          ],
        },
        {
          question: "To recharge your energy, you prefer to:",
          options: [
            "Go out and be active with others",
            "Spend time alone or in a quiet environment",
          ],
        },
        {
          question: "When making decisions, you tend to rely on:",
          options: [
            "Logic and concrete facts",
            "Your feelings and personal values",
          ],
        },
        {
          question: "You prefer to organize your day:",
          options: [
            "With a clear plan and specific schedule",
            "By leaving room for spontaneity and flexibility",
          ],
        },
        {
          question: "You learn best when:",
          options: [
            "You have clear and concrete instructions",
            "You can explore ideas, concepts, and possibilities",
          ],
        },
      ];
      console.log("Questions:", questions.length);


    const handleChange = (question, value) => {
        if (!value) return;
        if (!answers[question]) {
          setAnswers((prev) => ({ ...prev, [question]: value }));
          console.log("in", answers)
        }
        else {
            setAnswers((prev) => ({ ...prev, [question]: value }));
            console.log("else", answers)
        }
      console.log("ANSWERS:", answers.length, answers);
    };

    const handleSubmit = (e) => {
      e.preventDefault();
        setShowMbti(false)
        setMbtiSelection(answers);
      console.log("Réponses:", answers);
    };
    return (
        <>
        <h3 className="font-bold text-lg text-center">I’d love to learn a little more about you! Take a moment to answer these questions so I can get to know you better.</h3>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {questions.map((q, index) => (
                <div key={index} className="flex flex-col">
                    <label className="font-semibold mb-2">{q.question}</label>
                    {q.options.map((option, i) => (
                        <label key={i} className="flex items-center text-gray-400 gap-2">
                            <input
                                type="radio"
                                name={q.question}
                                value={option}
                                checked={answers[q.question] === option}
                                onChange={() => handleChange(q.question, option)}
                                className="cursor-pointer checked:bg-[var(--primary)] checked:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)] focus:ring-opacity-50 rounded-full border-gray-300"
                            />
                            {option}
                        </label>
                    ))}
                </div>
            ))}
            <button
                className=' disabled:opacity-15 w-fit self-center hover:shadow-emerald-400/40 hover:shadow-lg transiton-all duration-200 hover:scale-105 !text-white brightness-110 px-6 py-2 rounded-full bg-gradient-to-r from-[var(--primary)] to-emerald-400 transition-colors mt-4'
                type="submit"
                disabled={Object.keys(answers).length < 5}
            ><ArrowRight/>
            <p>{questions.lenght}</p>
            </button>

        </form>
        </>
    );
}
export default Mbti;
