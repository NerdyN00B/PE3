import numpy as np
import matplotlib.pyplot as plt

def tesla_valve(h, forwards_area=0.4, backwards_area=0.22, cm=True):
    """
    Calculate the flow rate based on the height difference of water in a tank.
    
    parameters
    ----------
    h : array-like
        Height difference between the two tanks (m).
    forwards_area : float, optional
        effective area of the forwards flow (m^2). Default is 0.4 cm^2.
    backwards_area : float, optional
        effective area of the backwards flow (m^2). Default is 0.22 cm^2.
    cm : bool, optional
        If True, the height is in cm. Default is True.
    
    Returns
    -------
    flow : array-like
        Flow rate ((c)m^3/s) based on the height difference.
    """
    g = 9.81
    if cm:
        g *= 100
    flow = np.where(h >= 0,
                    forwards_area * np.sqrt(2 * g * h),
                    -1 * backwards_area * np.sqrt(-2 * g * h))
    
    return flow

frequency = 1

height_offset = 0

t = np.linspace(0, 2, 1000)

fig, (ax1, ax2) = plt.subplots(1, 2, dpi=300, layout='tight')

h = np.sin(2 * np.pi * frequency * t) + height_offset

flow = tesla_valve(h, forwards_area=0.4, backwards_area=0.22, cm=True)

ax1.plot(t, h, label='input signal', color='blue')
twinx = ax1.twinx()
ax1.set_xlabel('time (s)')
ax1.set_ylabel('height (cm)')
twinx.plot(t, flow, label='flow', color='red')
twinx.set_ylabel('flow (cm^3/s)')

input_fft = np.fft.fft(h)
output_fft = np.fft.fft(flow)
freq = np.fft.fftfreq(len(h), t[1] - t[0])
transfer_function = input_fft / output_fft
ax2.plot(freq[:len(freq)//2], 20*np.log10(np.abs(transfer_function))[:len(transfer_function)//2], 
         label='transfer function', color='k')
ax2.set_xscale('log')
ax2.set_xlabel('frequency (Hz)')
ax2.set_ylabel('gain (dB)')

plt.show()