import salabim as sim
import datetime as dt
import calendar

SL_W,SL_H,SL_X=500,10,400             # width, height and xpos of year & date slider
YSL_Y,DSL_Y=90,50                     # ypos of year and date slider

years=[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

# check my comment out

class MyAnimateSlider(sim.AnimateSlider):
#due to bug in salabim override sim.AnimateSlider class
    def remove(self):
        if self.installed:
            self.slider.destroy()
        super().remove()

class Mover:
    def __init__(self,years):
        self.vyear=0
        self.syear=years[0]
        self.syear_x=SL_X   
        self.reset_date()
        
    def reset_date(self):
        self.vdate=1
        self.sdate=dt.date(self.syear, 1, 1)
        self.sdate_x=SL_X

class MySlider:
    def __init__(self,env):
        self.env=env
        self.env.firsty,self.envfirstd,self.env.firstsh=True,True,True
        
        self.env.ys=MyAnimateSlider(x=SL_X, y=YSL_Y, width=SL_W, height=SL_H, vmin=0,v=move.vyear,
                          vmax=len(years)-1,resolution=1, show_value=False,action=self.show_year)     

        self.env.yt=sim.AnimateText(text=str(move.syear),x=move.syear_x,y=YSL_Y-10)   

        self.env.ds=MyAnimateSlider(x=SL_X, y=DSL_Y, width=SL_W, height=SL_H, vmin=1,v=move.vdate,
                          vmax=self.diny(move.syear),resolution=1, show_value=False,action=self.show_date)   

        self.env.dt=sim.AnimateText(text=f'{move.sdate.strftime("%m-%d")}',x=move.sdate_x,y=DSL_Y-10)        
        
    def hide_sliders(self):        
        if self.env.firstsh:
            sim.AnimateCombined((self.env.ys,self.env.yt,self.env.ds,self.env.dt)).remove()           
            self.env.firstsh=False        
        else:
            self.__init__(self.env)
       
        
    def show_date(self,v):     
        if getattr(self.env,'firstd',True):
            self.env.firstd=False
            return       

        move.vdate=int(v)
        move.sdate= dt.date(move.syear, 1, 1) + dt.timedelta(days=int(v)-1)

        self.env.dt.remove()
        move.sdate_x=SL_X + move.vdate/self.diny(move.syear)*SL_W
        self.env.dt=sim.AnimateText(text=lambda t:f'{move.sdate.strftime("%m-%d")}',x=move.sdate_x,y=DSL_Y-10)           
        
    def show_year(self,v):
        if getattr(self.env,'firsty',True):
            self.env.firsty=False
            return   

        move.vyear=int(v)
        move.syear=years[int(v)]
        move.reset_date()

        self.env.yt.remove()
        move.syear_x=SL_X+int(v)/len(years)*SL_W
        self.env.yt=sim.AnimateText(text=lambda t:f'{move.syear}',x=move.syear_x,y=YSL_Y-10)   

        self.env.ds.remove()   
        self.env.ds=MyAnimateSlider(x=SL_X, y=DSL_Y, width=SL_W, height=SL_H, vmin=1,
                                vmax=self.diny(move.syear),resolution=1, show_value=False,action=self.show_date)     

        self.env.dt.remove()    
        self.env.dt=sim.AnimateText(text=lambda t:f'{dt.date(move.syear, 1, 1).strftime("%m-%d")}',x=SL_X,y=DSL_Y-10)       
        
        
    def diny(self,myyear):
        myyear=dt.date(myyear,1,1).year
        return 365 + calendar.isleap(myyear)

    def action(self):   
        self.env.main().activate()   

move=Mover(years=years)