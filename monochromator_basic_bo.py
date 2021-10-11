import epics
from bayes_opt import BayesianOptimization
import time
import datetime

# accelerator parameters
pvname_1 = 'FBCK:FB04:LG01:S3DES'   # BC1 peak current set   
pvname_2 = 'ACCL:LI21:1:L1S_S_AV'   # L1S amplitude  
pvname_3 = 'ACCL:LI21:1:L1S_S_PV'   # L1S phase
pvname_4 = 'ACCL:LI21:180:L1X_S_AV' # L1X amplitude*
pvname_5 = 'ACCL:LI21:180:L1X_S_PV' # L1X phase*
pvname_6 = 'FBCK:FB04:LG01:S5DES'   # BC2 peak current set*
pvname_7 = 'ACCL:LI22:1:ADES'       # L2 amplitude
pvname_8 = 'ACCL:LI22:1:PDES'       # L2 phase
pvname_9 = 'ACCL:LI25:1:ADES'       # L3 amplitude 
pvname_10 = 'ACCL:LI25:1:PDES'      # L3 phase
# quads?

# mono target PV
pvname_11 = 'XPP:SB2:BMMON:SUM'     # i2pm sum   

timestamp = (datetime.datetime.now()).strftime("%m-%d_%H-%M")
        
# choose some vars
def evaluate(var4,var5,var6):

    epics.caput(pvname_4,var4)
    epics.caput(pvname_5,var5)
    epics.caput(pvname_6,var6)

    time.sleep(3)
    
    objective = epics.caget(pvname_11)
    
    f= open(f"optimizer_iterations_{timestamp}.txt", "a+")
    f.write('%s' % ' '.join(map('{:.4f}'.format, [var4, var5, var6])) + ' {0:.4f}\n'.format(objective))
    f.close()
    
    return -1*objective

def init_state():
    var_init = [
    epics.caget(pvname_4), \
    epics.caget(pvname_5), \
    epics.caget(pvname_6),
    epics.caget(pvname_11)
    ]
    return var_init

# save init state
var_init = init_state()

f= open(f"optimizer_iterations_{timestamp}.txt", "a+")
f.write('%s' % ' '.join(map('{:.4f}'.format, var_init)))
f.close()

# define optimization bounds
pbounds = {'var4': (-5.0, -3.0),
           'var5': (2.0, 7.0),
           'var6': (-1.0, 2.0)
          }

optimizer = BayesianOptimization(
    f = evaluate,
    pbounds = pbounds,
    random_state = 1,
)

optimizer.maximize(
    init_points=5,
    n_iter=10,
)


# opt_var = optimizer.max['params']['var1']

opt_signal = -1*optimizer.max['target']
print('optimum signal ', opt_signal)