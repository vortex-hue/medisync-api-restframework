from django.urls import path
from .views import Signup, Login, Getaccess, ChangePassword, DeleteAccount, ForgotPassword,\
    RecoverPassword, GenerateOTP, VerifyOTP, Account, PasswordChanger

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('getaccess/', Getaccess.as_view(), name='getaccess'),
    path('changepassword/', ChangePassword.as_view(), name='changepassword'),
    path('delete/', DeleteAccount.as_view(), name="deleteaccount"),
    path('forgotpassword/', ForgotPassword.as_view(), name='forgotpassword'),
    path('recoverpassword/', RecoverPassword.as_view(), name='recoverpassword'),
    path('generateOTP/<str:phone>/', GenerateOTP.as_view(), name='generateOTP'),
    path('verifyOTP/', VerifyOTP.as_view(), name="verifyOTP"),
    path('account/<str:account_no>/', Account.as_view(), name="Account"),
    path('', PasswordChanger.as_view(), name="PasswordChanger"),
]
