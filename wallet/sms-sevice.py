class SMSService:
    @staticmethod
    def notify_user_of_deposit(user: User, amount: float):
        message = f"کیف پول شما با مبلغ {amount} تومان شارژ شد."
        SMS.objects.create(user=user, message=message, status='sent')

    @staticmethod
    def notify_user_of_withdrawal(user: User, amount: float):
        message = f"مبلغ {amount} تومان از کیف پول شما برداشت شد."
        SMS.objects.create(user=user, message=message, status='sent')
