from django.urls import path
from .views import *

urlpatterns = [
    path('Deposit/', DepositView.as_view(), name='deposit'),
    path('Withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('Loan_request/', LoanRecieveView.as_view(), name='loan_request'),
    path('Pay_loan/<int:loan_id>/', LoanPayView.as_view(), name='pay_loan'),
    path('Transaction_list/', TransactionReportView.as_view(), name='transaction_list'),
    path('Loan_list/', LoanListView.as_view(), name='loan_list'),
]
