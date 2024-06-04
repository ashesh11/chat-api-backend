from django.db import models

from account.models.account import UserAccount


class Chat(models.Model):
    user1 = models.ForeignKey(UserAccount, related_name='chat_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserAccount, related_name='chat_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f'Chat between {self.user1.email} and {self.user2.email}'
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.email}: {self.content[:20]}'
