import salabim as sim
import mydate as my

while True:
    env = sim.Environment(trace=True)
    env.animate(True)

    myslider = my.MySlider(env)

    sim.AnimateButton(text="reset", x=200, y=50, action=myslider.action)
    sim.AnimateButton(text="hide date", width=60, x=500, y=650, action=myslider.hide_sliders)

    env.run(100)
    print(f'The last run was from {my.move.sdate.strftime("%m-%d-%Y")}')

    print(f'I really like version control')