import json
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from PythonProject import settings
from .models import Commentaire, Publication
from django.contrib import messages
from django.core.paginator import Paginator
import google.generativeai as genai
import requests
GOOGLE_API_KEY='AIzaSyA44yvXfrO788vxbfnSk2R2sdyRj1m8jGA'

def publication(request):
    list_publications=Publication.objects.all()
    context = {"list_publications": list_publications}  
    return render(request, "publication.html", context)
def publication_create(request):
    if request.method == 'POST':
        pub=Publication()
        pub.titre = request.POST.get('titre')
        pub.description = request.POST.get('description')
        if 'image' in request.FILES:  
            pub.image = request.FILES['image']  # Changed from request.FILES('titre') to request.FILES['image']

        pub.save()
        messages.success(request , 'created successfully')
        return redirect('/publications')
         
    return render(request, 'publication_create.html')
def publication_update(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    
    if request.method == 'POST':
        publication.titre = request.POST.get('titre')
        publication.description = request.POST.get('description')
        
        if 'image' in request.FILES:
            publication.image = request.FILES['image']
        
        publication.save()
        
        messages.success(request, 'Publication updated successfully')
        return redirect('/publications')  # Replace with your desired redirect URL
    
    return render(request, 'publication_update.html', {'publication': publication})
def publication_details(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    commentaires = publication.commentaires.all()  
    
    paginator = Paginator(commentaires, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'publication_details.html', {
        'publication': publication,
        'page_obj': page_obj  
    })

def publication_delete(request, pk):
    publication = Publication.objects.filter(id=pk)
    publication.delete()
    messages.success(request , "Post deleted Successefully")
    return redirect('/publications')  
def publication_comment(request, pk):
    publication = get_object_or_404(Publication, id=pk)
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
       
        commentaire = Commentaire(publication=publication, contenu=contenu)
        commentaire.save()
      

        messages.success(request, 'Commentaire ajouté avec succès!')
    commentaires = publication.commentaires.all()  # Ensure this fetches the related comments
    
    paginator = Paginator(commentaires, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'publication_details.html', {
        'publication': publication,
        'page_obj': page_obj  
    })
def commentaire_delete(request, pk):
    commentaire = get_object_or_404(Commentaire, pk=pk)
    
    
    commentaire.delete()
    return redirect('publication_details', pk=commentaire.publication.id)  
def commentaire_update(request, pk):
    commentaire = get_object_or_404(Commentaire, pk=pk)
    
    if request.method == 'POST':
        commentaire.contenu = request.POST.get('contenu')
        
        commentaire.save()
        
        messages.success(request, 'Comment updated successfully')
        return redirect('publication_details', pk=commentaire.publication.pk)  
    
    return render(request, 'commentaire_update.html', {'commentaire': commentaire})








def ai_generate_description(titre):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Generer un description pour ce titre d'une oeuvre d'art: {titre}"
    
    response = model.generate_content(prompt)
    return response.text

def generate_description(request):
    if request.method == "POST":
        data = json.loads(request.body)
        titre = data.get('titre', '')
        description = ai_generate_description(titre)

        print(f'Title: {titre}, Generated Description: {description}')  # Log the inputs and outputs

        if description:
            return JsonResponse({'description': description})
        else:
            return JsonResponse({'error': 'Failed to generate description'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)



