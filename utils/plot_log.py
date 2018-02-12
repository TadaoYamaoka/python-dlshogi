import argparse
import re
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('log', type=str)
args = parser.parse_args()

ptn = re.compile(r'iteration = ([0-9]+), loss = ([0-9.]+), accuracy = ([0-9.]+)')

iteration_list = []
loss_list = []
accuracy_list = []
for line in open(args.log, 'r'):
    m = ptn.search(line)
    if m:
        iteration_list.append(int(m.group(1)))
        loss_list.append(float(m.group(2)))
        accuracy_list.append(float(m.group(3)))

fig, ax1 = plt.subplots()
p1, = ax1.plot(iteration_list, loss_list, 'b', label='loss')
ax1.set_xlabel('iterations')

ax2=ax1.twinx()
p2, = ax2.plot(iteration_list, accuracy_list, 'g', label='accuracy')

ax1.legend(handles=[p1, p2])

plt.show()
