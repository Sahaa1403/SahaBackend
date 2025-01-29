from accounts.views.logout import Logout
from accounts.views.refresh import Refresh
from accounts.views.register import Register
from accounts.views.send_otp import SendOTP, SendUpdateOTP, SendEmailOTP
from accounts.views.verify_otp import VerifyOTP, VerifyAndUpdatePhoneNumber, VerifyEmailOTP
from .user_validation import *
from accounts.views.refresh_access import RefreshAccess
from accounts.views.profile import Profile
from accounts.views.overview import OverView