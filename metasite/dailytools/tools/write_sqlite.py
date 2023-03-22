from MusicLab.views import *
def write_database():
    music = Music.objects.all()
    for i in range(len(music)):
        musicnft = MusicNFT()
        musicnft.id = i
        musicnft.more1 =  [i['title'] for i in Music.objects.filter(id=i).values()][0]
        musicnft.save()
