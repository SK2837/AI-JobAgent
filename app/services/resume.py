from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

class ResumeBuilder:
    def __init__(self):
        # Initialize LLM. Expects OPENAI_API_KEY in environment.
        # Defaults to gpt-3.5-turbo for cost/speed, can be configured.
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        
    async def tailor_resume(self, base_resume_content: str, job_description: str) -> str:
        """
        Tailors a resume to a specific job description using an LLM.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert career coach and resume writer. Your goal is to tailor a candidate's resume to a specific job description to maximize their chances of getting an interview. Do not invent false information, but highlight relevant skills and experiences."),
            ("user", "Here is my base resume:\n\n{resume}\n\nHere is the job description:\n\n{job_description}\n\nPlease rewrite the resume to better match the job description. Focus on keywords and relevant achievements.")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            tailored_resume = await chain.ainvoke({
                "resume": base_resume_content,
                "job_description": job_description
            })
            return tailored_resume
        except Exception as e:
            # Fallback or re-raise depending on requirements. 
            # For now, return a basic error message or the original resume with a note.
            print(f"Error tailoring resume: {e}")
            return f"Error tailoring resume. Original content preserved.\n\n{base_resume_content}"
