import asyncio
import os
from app.services.resume import ResumeBuilder

# Mock the API key if not present to avoid immediate crash in test initialization, 
# though the actual call will fail or need mocking if no key is valid.
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sk-mock-key-for-testing"

async def test_resume_builder():
    print("Testing ResumeBuilder...")
    builder = ResumeBuilder()
    
    base_resume = "Software Engineer with 5 years of experience in Python and FastAPI."
    job_description = "Looking for a Senior Python Developer with experience in AI and LangChain."
    
    print("Invoking LLM (this might fail if no valid API key is present)...")
    try:
        tailored = await builder.tailor_resume(base_resume, job_description)
        print("\n--- Tailored Resume Start ---")
        print(tailored[:200] + "...") # Print first 200 chars
        print("--- Tailored Resume End ---\n")
        
        if "Error tailoring resume" in tailored:
            print("Test Result: Handled missing key/error gracefully.")
        else:
            print("Test Result: Success (LLM responded).")
            
    except Exception as e:
        print(f"Test Failed with unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_resume_builder())
