from django.contrib.auth.decorators import login_required
from user.models import CustomUser


# admin_dashboard/views.py
from django.shortcuts import get_object_or_404, redirect ,render
from django.contrib import messages
from reclamation.models import Reclamation , Reponse

@login_required
def repondre_reclamation(request, reclamation_id):
    reclamation = get_object_or_404(Reclamation, id=reclamation_id)
    
    if request.method == 'POST':
        reponse_text = request.POST.get('reponse')
        if reponse_text:
            Reponse.objects.create(reclamation=reclamation, reponse=reponse_text)
            reclamation.statut = 'Résolue'
            reclamation.save()
            messages.success(request, 'Votre réponse a été ajoutée avec succès.')
        else:
            messages.error(request, 'Veuillez entrer une réponse valide.')
    
    return redirect('liste_reclamationsadmin')  # Redirigez vers la liste des réclamations après la réponse


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def liste_reclamations(request):
    reclamations = Reclamation.objects.all()  
    return render(request, 'dashboard/liste_reclamations.html', {'reclamations': reclamations})


@login_required
def liste_User(request):
    users = CustomUser.objects.all()  
    return render(request, 'dashboard/liste_user.html', {'users': users})
