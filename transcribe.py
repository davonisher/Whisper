from openai import OpenAI
import os
from dotenv import load_dotenv
from docx import Document
import logging

# File path
file_path = "/Users/macbook/Downloads/Thesis structuur/Recordings/Recording 1.m4a"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Instantiate OpenAI client
client = OpenAI(api_key="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")

def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"

            )
        return transcript

    except Exception as e:
        logging.error(f"Error in transcribing file {file_path}: {e}")
        return None


def save_transcription_to_word_doc(transcribed_text, input_file_name, output_folder):
    if not transcribed_text:  # Skip if transcription is None
        return

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        doc = Document()
        doc.add_paragraph(transcribed_text)

        output_file_name = os.path.splitext(os.path.basename(input_file_name))[0] + ".docx"
        output_file_path = os.path.join(output_folder, output_file_name)

        doc.save(output_file_path)
        logging.info(f"Transcription saved to: {output_file_path}")
    except Exception as e:
        logging.error(f"Error saving transcription for {input_file_name}: {e}")

def main():
    output_folder = "/Users/macbook/Downloads"

    if not os.path.isfile(file_path):
        logging.warning(f"File not found: {file_path}")
    else:
        transcribed_text = transcribe_audio(file_path)
        save_transcription_to_word_doc(transcribed_text, file_path, output_folder)

system_prompt = "You are a helpful assistant. Your task is to correct any spelling discrepancies in the transcribed text. Make sure that the format is always like this example: Spreker 1: Oké. Nou, allereerst fijn dat je er bent. Spreker 2: Dank u wel. Spreker 1: Ben je er mee akkoord dat ik dit interview opneem? Spreker 2: Jawel. Only add necessary punctuation such as periods, commas, and capitalization, and use only the context provided."

def generate_corrected_transcript(temperature, system_prompt, audio_file):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcribe_audio(file_path)
            }
        ]
    )
    return response['choices'][0]['message']['content']



if __name__ == "__main__":
    main()