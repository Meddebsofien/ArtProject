from django.shortcuts import get_object_or_404, render, redirect
from .models import Publication
from django.contrib import messages
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
    
    # Render the form with the current values of the publication
    return render(request, 'publication_update.html', {'publication': publication})
def publication_details(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'publication_details.html', {'publication': publication})

def publication_delete(request, pk):
    publication = Publication.objects.filter(id=pk)
    publication.delete()
    messages.success(request , "Post deleted Successefully")
    return redirect('/publications')  # Replace with your desired redirect URL
