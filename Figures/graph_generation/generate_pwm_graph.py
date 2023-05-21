from matplotlib import pyplot as plt
import numpy as np


# Make a pulse width graph - make a space of 1 second. We are using 60hz, and want to be able to vary the pulse width, so 100*60 = 6000 steps in the graph
x = np.linspace(0, 1, 3000)
y = np.zeros(3000)

def add_pulses(pwm_value, cycles, start_cycle=0, max_pwm=65536):
    pulse_width = (pwm_value * 100) // max_pwm
    print(pulse_width)
    for n in range(cycles):
        current_cycle = start_cycle + n
        for m in range(pulse_width):
            y[(current_cycle*100)+m+1] = 1

# make first 20 cycles low pwm (1000)
add_pulses(10000, 10)   
# make next 20 cycle mid pwm (5000)
add_pulses(20000, 10, start_cycle=10)
# make next 20 cycles high pwm (9000)
add_pulses(32000, 10, start_cycle=20)


# make the output plot size short and long
plt.figure(figsize=(15, 2))

# no ticks on x axis
plt.xticks([])
# no ticks on y axis
plt.yticks([])
# Plot it
plt.plot(x, y)
# plot with the space below the lines filled in
plt.fill_between(x, y, 0, color='blue')

# make the font size bigger
plt.rcParams.update({'font.size': 14})
# add space below for the text
plt.subplots_adjust(bottom=0.2)
# take aways on the sides
plt.subplots_adjust(left=0.02, right=0.98)
# put a label under the first third showing "short pulses"
plt.text(0.33/2, -0.1, "short pulses", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
# put a label under the second third showing "medium pulses"
plt.text(0.33 + 0.33/2, -0.1, "medium pulses", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
# put a label under the last third showing "long pulses"
plt.text(0.66 + 0.33/2, -0.1, "long pulses", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)

plt.show()
