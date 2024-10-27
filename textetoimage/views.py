from django.shortcuts import render
import requests
import io
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from PIL import Image
def prompt_form(request):
    return render(request, "promptext.html")
# URL de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}



def query_huggingface_api(prompt):
    """Fonction pour interagir avec l'API Hugging Face."""
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content
    else:
        raise ValueError(f"Erreur API Hugging Face {response.status_code}: {response.text}")

def generate_image(request):
    """Génère une image à partir du prompt et la retourne sous forme de binaire."""
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        try:
            image_bytes = query_huggingface_api(prompt)
            return HttpResponse(image_bytes, content_type="image/png")
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
