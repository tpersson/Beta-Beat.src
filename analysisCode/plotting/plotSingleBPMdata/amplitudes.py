''' Calculated amplitudes of (1,2) resonance from measurements of 2012 MD '''



amplitudes_12 = {
            'amplitude':      [17.1672808749,   9.2151775626,    31.3601047278,  25.2163327588,   29.7559348384,   40.2639344047,   32.7770205886] , 
            'norm_amplitude': [0.0179956524844, 0.0119260119406, 0.052262605647, 0.0450366489406, 0.0573652471161, 0.0792956680707, 0.0741217455546] , 
            'tune':           [.0955,           .095,            .095,           .095,            .095,            .0945,           .0945]
            }

# Nonminal sigma as calculated from 2012 MD
kick_strengths = {
                  'X': [5.5, 6.2, 6.9, 7.2, 7.6, 7.8, 8.2 ]
                  'Y': [5.1, 4.9, 5.4, 5.7, 6.1, 6.2, 6.5 ]  
}

def plot_amplitudes():

    fig = plt.figure(figsize=(23, 13))
    fig.patch.set_facecolor('white')
    tx = fig.add_subplot(1, 1, 1)

    #tx = fig.add_subplot(1,1,1)
    #ty = fig.add_subplot(2,1,2)

    fig.suptitle('1,2 amplitude')
    tx.set_xlabel('$Q_x$ [1/turn]')
    ty.set_xlabel('$Q_y$ [1/turn]')
    tx.set_ylabel('Amp [a.u.]')
    ty.set_ylabel('Amp [a.u.]')


if __name__ == "__main__":






