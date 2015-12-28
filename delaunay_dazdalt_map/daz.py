# coding: UTF-8

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from scipy import genfromtxt


# �t�@�C���ǂݍ���
d = genfromtxt("daz.txt", delimiter=",")

# �O���t�쐬
fig = pyplot.figure()
ax = Axes3D(fig)

# �����x���̐ݒ�
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")

# �\���͈͂̐ݒ�
ax.set_xlim(4, 8)
ax.set_ylim(2, 5)
ax.set_zlim(1, 8)

# ���o�����ݒ�
d1 = d[d[:,0] >= 7]
d2 = d[(d[:,0] < 7) & ((d[:,1] > 3) & (d[:,1] <= 3.5))]
d3 = d[(d[:,0] < 7) & ((d[:,1] <= 3) | (d[:,1] > 3.5))]


# �O���t�`��
ax.plot(d1[:,0], d1[:,1], d1[:,2], "o", color="#cccccc", ms=4, mew=0.5)
ax.plot(d2[:,0], d2[:,1], d2[:,2], "o", color="#00cccc", ms=4, mew=0.5)
ax.plot(d3[:,0], d3[:,1], d3[:,2], "o", color="#ff0000", ms=4, mew=0.5)
pyplot.show()