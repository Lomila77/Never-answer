import React from "react";
import { useState } from "react";
import { ArrowRight } from "lucide-react";

const Mbti = ({ setShowMbti, setMbtiSelection }) => {
    const [answers, setAnswers] = useState([]);
    const questions = [
        {
          question: "Quand tu rencontres de nouvelles personnes, tu préfères :",
          options: [
            "Parler avec beaucoup de gens, faire connaissance rapidement" ,
             "Parler avec quelques personnes seulement, préférer des conversations profondes",
          ],
        },
        {
          question: "Pour te ressourcer, tu préfères :",
          options: [
            "Sortir et être actif avec d’autres",
            "Passer du temps seul(e) ou dans un cadre calme",
          ],
        },
        {
          question: "Quand tu prends des décisions, tu te bases plutôt sur :",
          options: [
            "La logique et les faits concrets",
            "Tes sentiments et valeurs personnelles",
          ],
        },
        {
          question: "Tu préfères organiser ta journée :",
          options: [
            "Avec un plan clair et des horaires précis",
            "En laissant place à l’improvisation et la flexibilité",
          ],
        },
        {
          question: "Tu apprends mieux quand :",
          options: [
            "Tu as des instructions claires et concrètes",
            "Tu peux explorer les idées, concepts et possibilités",
          ],
        },
      ];
      console.log("Questions:", questions.length);


    const handleChange = (question, value) => {
        if (!value) return;
        if (!answers[question]) {
          setAnswers((prev) => ({ ...prev, [question]: value }));
        }
      else {

      }
      console.log("ANSWERS:", answers.length);
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
                disabled={answers.length <= questions.length}
            ><ArrowRight/>
            <p>{questions.lenght}</p>
            </button>

        </form>
        </>
    );
}
export default Mbti;
