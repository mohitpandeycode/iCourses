
from .models import UserProfile

def user_info(request):
    user_info = None
    if request.user.is_authenticated:
        try:
            user_info = request.user.userprofile  # Assuming UserProfile is related to the User model
        except UserProfile.DoesNotExist:
            pass  # Handle the case where UserProfile doesn't exist for the current user
    return {'user_info': user_info}
