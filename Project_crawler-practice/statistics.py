import os
import matplotlib.pyplot as plt

path = 'G:/我的雲端硬碟/SideProject/Database'

birds_name = os.listdir(path)
birds_name.remove('mp3fail.txt')
try:
    birds_name.remove('desktop.ini')
except:
    pass
data = dict()
for name in birds_name:
    mp3_path = os.path.join(path, name, 'mp3')
    mp3_name = os.listdir(mp3_path)
    try:
        mp3_name.remove('desktop.ini')
    except:
        pass
    counts = len(mp3_name)
    data[name] = counts
data = dict((k,data[k]) for k in sorted(data.keys()))

fig, ax = plt.subplots(1,1, figsize = (10,90))
plt.barh(list(data.keys()), data.values(), label = 'Counts')
plt.xlim(0,100)
plt.ylim(-1,len(data.keys()))
plt.xlabel('Counts', fontsize = 20, fontweight = 'bold')
plt.ylabel('Birds name', fontsize = 20, fontweight = 'bold')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.title('Birds counts', fontsize = 30, fontweight = 'bold')
plt.legend(fontsize = 10)
plt.grid(axis = 'x', alpha = 0.5)
plt.subplots_adjust(top = 0.98, bottom = 0.007, left = 0.73, right = 0.95, hspace = 0, wspace = 0)
plt.savefig('statistics.png',dpi = 300)
plt.show()
