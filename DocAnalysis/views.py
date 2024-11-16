import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import docx2txt
from PyPDF2 import PdfReader
from django.contrib import messages
import uuid
import openai
import requests
    
@csrf_exempt
def analyze_document(request):
    if request.method == 'POST' and request.FILES.get('document'):
        # Extract text from the uploaded document
        uploaded_file = request.FILES['document']
        
        # Generate a unique file path for temporary storage
        unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
        temporary_file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

        try:
            # Save the uploaded file to a temporary location
            with open(temporary_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Determine file format and extract text accordingly
            if uploaded_file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                # DOCX file
                document_text = docx2txt.process(temporary_file_path)
            elif uploaded_file.content_type == 'application/pdf':
                # PDF file using PyPDF2
                reader = PdfReader(temporary_file_path)
                document_text = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        document_text += text
            elif uploaded_file.content_type == 'text/plain':
                # TXT file
                with open(temporary_file_path, 'r', encoding='utf-8') as f:
                    document_text = f.read()
            else:
                os.remove(temporary_file_path)
                return JsonResponse({"error": "Formato de archivo no soportado."}, status=400)

            # Remove the temporary file
            os.remove(temporary_file_path)

            # Summarize the document using the updated OpenAI API method
            summary = summarize_with_openai(document_text)
            return JsonResponse({"summary": summary})

        except Exception as e:
            # Clean up temporary file in case of error
            if os.path.exists(temporary_file_path):
                os.remove(temporary_file_path)
            return JsonResponse({"error": f"Ocurrió un error durante el procesamiento: {str(e)}"}, status=500)

    return JsonResponse({"error": "Solicitud inválida."}, status=400)

def summarize_with_openai(document_text):
    try:
        # Prepare the request payload
        headers = {
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Eres un asistente que proporciona resúmenes útiles de documentos legales."},
                {"role": "user", "content": f"Por favor proporciona un resumen del siguiente documento legal: \"{document_text}\""}
            ],
            "max_tokens": 150,
            "temperature": 0.5
        }

        # Send the request to OpenAI API
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        
        if response.status_code == 200:
            response_data = response.json()
            summary = response_data['choices'][0]['message']['content'].strip()
            return summary
        else:
            return f"Error al obtener el resumen: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error durante la solicitud de resumen: {str(e)}"

@csrf_exempt
def ask_question(request):
    if request.method == 'POST':
        try:
            # Parse the request JSON
            data = json.loads(request.body)
            
            # Debugging the incoming data
            print("Received Data:", data)

            document_text = data.get('document_text', '')
            question = data.get('question', '')

            # Check if the necessary data is provided
            if not document_text or not question:
                return JsonResponse({"error": "Texto del documento o pregunta no proporcionados."}, status=400)

            # Generate the answer using OpenAI API
            answer = ask_openai_question(document_text, question)
            return JsonResponse({"answer": answer})

        except Exception as e:
            return JsonResponse({"error": f"Ocurrió un error durante el procesamiento: {str(e)}"}, status=500)

    return JsonResponse({"error": "Solicitud inválida."}, status=400)


# Function to interact with OpenAI API for Q&A
def ask_openai_question(document_text, question):
    try:
        headers = {
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Eres un asistente que responde preguntas basadas en documentos legales."},
                {"role": "user", "content": f"Basándote en el siguiente documento: \"{document_text}\", responde a la pregunta: \"{question}\""}
            ],
            "max_tokens": 150,
            "temperature": 0.5
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            answer = response_data['choices'][0]['message']['content'].strip()
            return answer
        else:
            return f"Error al obtener la respuesta: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error durante la solicitud a OpenAI: {str(e)}"



def index(request):
    return render(request, 'doc_analysis/analyze.html')