
# 1 try plotting  single figure
from minimatlab import *
x=linspace(-10,10,400)
y=sin(x)/2 + cos(x/2)
plot(x,y,'b--')
title('single figure')
#show()
# 2 plotting another one in the same window
hold()
y1=2*x
plot(x,y1,'-')
title('two figures')
#show()
# 3 add another subplot
subplot(2,2,3)
plot(x,y,'o')
title('subplot example')
# 4 test grid and legend
plot(2,2,2)
plot(x,y1,'g-')
title('subplot example 2')
grid(True)
legend(['y = sin(x)/2 + cos(x/2)', 'y = 2*x'])
show()
'''
from minimatlab import *
switch()
x=linspace(-10,10,400)
y=sin(x)/2 + cos(x/2)
plot(x,y,'b-')
title('single figure')
show()
'''