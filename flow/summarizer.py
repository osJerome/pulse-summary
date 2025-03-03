from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate


def generate_summaries(normalized_data: list[dict]) -> list:
    llm = OpenAI(temperature=0.3)

    # Create a prompt template for summarization
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="""
            Please provide a concise 1-2 sentence summary of the following information:
            
            {text}
            
            Summary:
        """,
    )

    # Create an LLM chain with the prompt template
    summary_chain = LLMChain(llm=llm, prompt=prompt_template)

    data_with_summaries = []

    for row in normalized_data:
        combined_text = (
            f"Description: {row.get('description', '')}\n"
            f"Metadata: {row.get('metadata', '')}\n"
            f"Message: {row.get('message_content', '')}"
        )

        # Generate summary using the invoke method
        try:
            chain_response = summary_chain.invoke({"text": combined_text})
            summary = chain_response.get("text", "")

            # Ensure summary is 1-2 sentences
            sentences = summary.split(".")
            if len(sentences) > 2:
                short_summary = ". ".join(sentences[:2]) + "."
            else:
                short_summary = summary

            row["summary"] = short_summary.strip()
            data_with_summaries.append(row)
        except Exception as e:
            print(f"Error generating summary: {e}")
            row["summary"] = "Summary could not be generated."
            data_with_summaries.append(row)

    return data_with_summaries
