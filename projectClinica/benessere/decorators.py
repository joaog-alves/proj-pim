from functools import wraps
from django.shortcuts import redirect

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Depuração: Verifique se o usuário está autenticado e seus grupos
            print(f"Usuário autenticado: {request.user.is_authenticated}")
            print(f"Nome do usuário: {request.user.username}")
            print(f"Grupos do usuário: {[group.name for group in request.user.groups.all()]}")  # Imprime os grupos do usuário
            
            # Verifique se o usuário está autenticado e pertence ao grupo
            if request.user.is_authenticated:
                if request.user.groups.filter(name=group_name).exists():
                    print(f"Usuário {request.user.username} pertence ao grupo {group_name}.")
                    return view_func(request, *args, **kwargs)
                else:
                    print(f"Usuário {request.user.username} não pertence ao grupo {group_name}.")
                    return redirect('acesso_negado')  # Redireciona para a página de acesso negado
            else:
                print("Usuário não autenticado.")
                return redirect('login')  # Redireciona para a página de login se o usuário não estiver autenticado
        return _wrapped_view
    return decorator
