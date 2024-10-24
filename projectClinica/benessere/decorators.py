from django.core.exceptions import PermissionDenied
from functools import wraps

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Depuração: Verifique se o usuário está autenticado e seus grupos
            print(f"Usuário autenticado: {request.user.is_authenticated}")
            print(f"Nome do usuário: {request.user.username}")
            print(f"Grupos do usuário: {[group.name for group in request.user.groups.all()]}")  # Imprime os grupos do usuário
            
            # Verifique se o usuário pertence ao grupo
            if not request.user.groups.filter(name=group_name).exists():
                print(f"Usuário {request.user.username} não pertence ao grupo {group_name}.")
                raise PermissionDenied  # Erro 403 se não estiver no grupo
            print(f"Usuário {request.user.username} pertence ao grupo {group_name}.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
