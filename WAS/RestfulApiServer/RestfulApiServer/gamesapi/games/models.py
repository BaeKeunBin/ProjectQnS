from django.db import models

# Create your models here.
class Game(models.Model):
	Creates = models.DateTimeField(auto_now_add=True)
	Name = models.CharField(max_length =200, blank =True, default ='')
	release_date = models.DateTimeField()
	game_category = models.CharField(max_length=200,blank=True,default='')
	played = models.BooleanField(default=False)

	class Meta:
		ordering = ('Name',)