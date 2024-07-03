import ollama

import json
from typing import Dict, List

def text_summarize(text: str, content_type: str):
    print("mourya llama")
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    if not isinstance(content_type, str):
        raise TypeError("Content type must be a string.")
    valid_types = ['job', 'course', 'scholarship']
    if content_type not in valid_types:
        raise ValueError(f"content_type must be one of {valid_types}, got '{content_type}' instead.")
    
    # Compute the number of words in the original text
    text_length = count_words(text)
    # Calculate the summary length based on the text length
    sum_length = calculate_summary_length(text_length)
    # Generate the appropriate summarization prompt
    #summary = summarize(text, sum_length, content_type)


    # for content in summarize(text, sum_length, content_type):
    #     print(content, end='', flush=True)
    for content in summarize(text, sum_length, content_type):
        yield content


def count_words(text: str):
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    normalized_text = ' '.join(text.split())
    words = normalized_text.split()
    return len(words)


def calculate_summary_length(text_length: int):
    if text_length < 0:
        raise ValueError("Input must be a non-negative integer representing the word count of the text.")
    if text_length == 0:
        return 0  # No words to summarize if the text length is 0.
    summary_length = text_length  # Default to full length if no specific rules are applied.
    if text_length > 50:
        if text_length < 300:
            summary_length = int(0.5 * text_length)  # 50% of original for short texts.
        elif text_length < 1000:
            summary_length = max(int(0.3 * text_length), 150)  # Scale down to 30% or 150 words, whichever is more.
        else:
            summary_length = max(int(0.1 * text_length), 300)  # Scale down to 10% or 300 words, whichever is more.
    return summary_length

def summarize(text: str, sum_length: int, content_type: str) -> List[Dict[str, str]]:
    if content_type not in ['job', 'course', 'scholarship']:
        raise ValueError("content_type must be one of 'job', 'course', or 'scholarship'")
    # Specific instructions based on content type
    content_specific_prompt = {
        'job': "Your task is to summarize this job description. Focus on key responsibilities, required qualifications, and employment benefits.",
        'course': "Your task is to summarize this online course description. Highlight the main learning objectives, course outline, and target audience.",
        'scholarship': "Your task is to summarize the scholarship details. Include important eligibility criteria, scholarship benefits, and application deadlines."
    }
    user_prompt = {
        'role': 'user',
        'content': f"""You are an expert summarizer capable of understanding the content and summarizing aptly, keeping most valid information intact.
                    Develop a summarizer that efficiently condenses the text into a concise summary. 
                    The summaries should capture essential information and convey the main points clearly and accurately. 
                    The summarizer must be able to handle content related to {content_type}s. 
                    It should prioritize key facts, arguments, and conclusions while maintaining the integrity and tone of the original text. 
                    Aim for a summary that is approximately {sum_length} words of the size. 
                    Focus on clarity, brevity, and relevance to ensure the summary is both informative and readable. 
                    The text is as follows: {text} {content_specific_prompt}"""
                }

    stream = ollama.chat(
    model='llama3',
    messages=[user_prompt],
    stream = True
    )
    for chunk in stream:
        yield chunk['message']['content']
    # stream=True)
    # for chunk in stream:
    #   print(chunk['message']['content'], end='', flush=True)
    #return stream

if __name__=="__main__":
    txt = "mourya"
    text_summarize(txt,'nothing')