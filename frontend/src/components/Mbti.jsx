import React from "react";
import { useState } from "react";

const Mbti = (setShowMbti) => {
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

    const handleChange = (question, value) => {
      setAnswers((prev) => ({ ...prev, [question]: value }));
    };

    const handleSubmit = (e) => {
      e.preventDefault();
      console.log("Réponses:", answers);
    };
    return (
        <>
        <p>I’d love to learn a little more about you! Take a moment to answer these questions so I can get to know you better.</p>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {questions.map((q, index) => (
                <div key={index} className="flex flex-col">
                    <label className="font-semibold mb-2">{q.question}</label>
                    {q.options.map((option, i) => (
                        <label key={i} className="flex items-center gap-2">
                            <input
                                type="radio"
                                name={q.question}
                                value={option}
                                checked={answers[q.question] === option}
                                onChange={() => handleChange(q.question, option)}
                                className="cursor-pointer checked:"
                            />
                            {option}
                        </label>
                    ))}
                </div>
            ))}
            <button type="submit" onClick={setShowMbti(false)} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
                Submit
            </button>
        </form>
        </>
    );
}
export default Mbti;
