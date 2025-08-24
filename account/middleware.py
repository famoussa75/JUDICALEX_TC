from django.shortcuts import redirect
from django.urls import resolve

class LoginRequiredMiddleware:
    """
    Middleware pour rediriger les utilisateurs non authentifiés vers la page de connexion.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Liste des URL ou préfixes à exclure
        excluded_paths = ['/account/login/', '/admin/', '/static/']

        # Vérifie si l'utilisateur est authentifié ou si le chemin est exclu
        if not request.user.is_authenticated and not any(request.path.startswith(path) for path in excluded_paths):
            # Redirige vers la page de connexion
            return redirect('login')

        return self.get_response(request)
