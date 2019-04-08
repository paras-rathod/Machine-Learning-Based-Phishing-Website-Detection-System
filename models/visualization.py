import matplotlib.pyplot as plt
import mpld3 as mpld3
import json
from sys import path
path.append("./models/")
import os.path
import numpy as np



class visual:

    @staticmethod
    def pie_chart(features):
        labels = 'Phishing', 'Legitimate', 'Suspicious'
        phish = features.count(-1)
        legim = features.count(1)
        suspicious = features.count(0)

        sizes = [phish, legim, suspicious]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.plot()

        if os.path.isfile('/home/paras/PhishingML01/static/images/pie.png'):
            os.system('rm -f /home/paras/PhishingML01/static/images/pie.png')
        plt.savefig('/home/paras/PhishingML01/static/images/pie.png')
        plt.close();


    @staticmethod
    def barGraph(features):
        labels = ('Phishing', 'Legitimate', 'Suspicious')
        phish = features.count  (-1)
        legim = features.count(1)
        suspicious = features.count(0)

        sizes = [phish, legim, suspicious]


        plt.bar(labels[0], sizes[0], color='r')
        plt.bar(labels[1], sizes[1], color='g')
        plt.bar(labels[2], sizes[2], color='b')


        plt.plot()
        if os.path.isfile('/home/paras/PhishingML01/static/images/bar1.png'):
            os.system('rm -f /home/paras/PhishingML01/static/images/bar1.png')
        plt.savefig('/home/paras/PhishingML01/static/images/bar1.png')
        plt.close()

    @staticmethod
    def stackedGraph(features):


        #features = [1, 0, -1, 1, 1, 1, 0, -1, 1, 1, 1, 1, 0, -1, -1, 0, 1, -1, 0, -1, 1, 0, -1, 0, 1, -1, 0, -1, 0, 1]

        A = features[:12]
        B = features[12:18]
        C = features[18:23]
        D = features[23:30]

        A_y1 = A.count(-1)
        A_y2 = A.count(0)
        A_y3 = A.count(1)

        B_y1 = B.count(-1)
        B_y2 = B.count(0)
        B_y3 = B.count(1)

        C_y1 = C.count(-1)
        C_y2 = C.count(0)
        C_y3 = C.count(1)

        D_y1 = D.count(-1)
        D_y2 = D.count(0)
        D_y3 = D.count(1)

        l1 = [A_y1, B_y1, C_y1, D_y1]

        l2 = [A_y2, B_y2, C_y2, D_y2]

        l3 = [A_y3, B_y3, C_y3, D_y3]

        l4 = []
        for i in range(4):
            l4.append(l1[i]+l2[i])

        X = ('Address Bar', 'Abnormal', 'HTML and JavaScript', 'Domain')
        width = 0.35

        plt.bar(X, l1, width, color='r',)
        plt.bar(X, l2, width, color='b', bottom=l1)
        plt.bar(X, l3, width, color='g', bottom=l4)
        plt.xticks(range(4), rotation=10)

        if os.path.isfile('/home/paras/PhishingML01/static/images/stackedbar1.png'):
            os.system('rm -f /home/paras/PhishingML01/static/images/stackedbar1.png')
        plt.savefig('/home/paras/PhishingML01/static/images/stackedbar1.png')
        plt.close()


if __name__ == '__main__':

    features = [-1,1,-1,1,-1,-1,0,0,1,1,1,-1,-1,-1,1,-1,1,1,0,-1,1,-1,1,1,-1,-1,-1,1,0,1]
    visual.pie_chart(features)
    visual.barGraph(features)
    visual.stackedGraph(features)