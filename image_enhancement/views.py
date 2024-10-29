from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import numpy as np
from PIL import Image
import io
from huggingface_hub import from_pretrained_keras

from keras.layers import TFSMLayer

model = TFSMLayer("C:\\Users\\user2024\\.cache\\huggingface\\hub\\models--keras-io--low-light-image-enhancement\\snapshots\\eb992d12eca55d932541b1c59f1e735718f41179", call_endpoint='serving_default')


class ImageEnhancementView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Vérifier la présence de l'image dans la requête
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)

        file = request.FILES['image']

        # Vérifiez les détails du fichier
        print("Uploaded file name:", file.name)
        print("Uploaded file size:", file.size)

        try:
            # Ouvrir l'image
            image = Image.open(file)

            # Afficher le mode de l'image avant conversion
            print("Image mode before conversion:", image.mode)

            # Convertir l'image en RGB si nécessaire
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Prétraitement : redimensionnement et normalisation
            image = image.resize((256, 256))
            image_array = np.array(image) / 255.0
            
            # Ajouter une dimension pour le batch
            image_array = np.expand_dims(image_array, axis=0)

            # Exécuter le modèle
            enhanced_image_array = model(image_array)

            # Log pour le débogage
            print("Model output:", enhanced_image_array)

            # S'assurer que la sortie a la forme attendue
            if enhanced_image_array.ndim == 4:
                enhanced_image_array = enhanced_image_array[0]

            # Appliquer le clipping sur chaque canal
            enhanced_image_array = np.clip(enhanced_image_array, 0, 1)

            # Vérifiez si la sortie a 24 canaux, nous prenons seulement les 3 premiers canaux
            if enhanced_image_array.shape[-1] == 24:
                enhanced_image_array = enhanced_image_array[..., :3]

            # Convertir le tableau en image
            enhanced_image = Image.fromarray((enhanced_image_array * 255).astype(np.uint8))

            # Enregistrer l'image améliorée dans un objet BytesIO
            img_byte_arr = io.BytesIO()
            enhanced_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            # Renvoyer l'image améliorée en tant que réponse HTTP
            return HttpResponse(img_byte_arr.getvalue(), content_type='image/png')

        except Exception as e:
            # Gestion des erreurs : renvoyer le message d'erreur en tant que réponse JSON
            return JsonResponse({'error': str(e)}, status=500)
