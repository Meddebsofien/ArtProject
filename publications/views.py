from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Commentaire, Publication
from django.contrib import messages
from django.core.paginator import Paginator

def publication(request):
    list_publications=Publication.objects.all()
    context = {"list_publications": list_publications}  # Correspond à ce que tu veux utiliser dans le template
    return render(request, "publication.html", context)
def publication_create(request):
    if request.method == 'POST':
        pub=Publication()
        pub.titre = request.POST.get('titre')
        pub.description = request.POST.get('description')
        if 'image' in request.FILES:  # Check if 'image' is in request.FILES
            pub.image = request.FILES['image']  # Changed from request.FILES('titre') to request.FILES['image']

        pub.save()
        messages.success(request , 'created successfully')
        return redirect('/publications')
         
    return render(request, 'publication_create.html')
def publication_update(request, pk):
    # Fetch the specific publication instance or return a 404 if not found
    publication = get_object_or_404(Publication, pk=pk)
    
    if request.method == 'POST':
        # Update publication fields with values from the form
        publication.titre = request.POST.get('titre')
        publication.description = request.POST.get('description')
        
        # Update the image if a new one is uploaded
        if 'image' in request.FILES:
            publication.image = request.FILES['image']
        
        # Save the updated instance
        publication.save()
        
        # Success message and redirect
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
        return redirect('publication_details', pk=commentaire.publication.pk)  # Redirect to the publication's detail page
    
    return render(request, 'commentaire_update.html', {'commentaire': commentaire})