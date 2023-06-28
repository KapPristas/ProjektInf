from psychopy import visual, core, event
import random
import csv
import yaml

REACTION_KEYS = ["z", "x", "n", "m", "f7", "f8"]
RESULTS = [["NR_EXP", "NR_TRIAL", "ST", "STIMULI COLOR", "STIMULI CONTENT", "ACC", "RT", "EXPE_ANS", "ANSWER", 'a', 'b', 'c',]]
a = 6 #correct stimuli
b = 6 #incorrect stimuli
c = 3 #neutral stimuli
ST = None #stimuli type

def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]

def reactionswait(keys):
    event.clearEvents()
    duration = 4.0 
    start_time = core.getTime()
    while core.getTime() - start_time < duration:
        key = event.getKeys(keyList=keys)
        if len(key) > 0:
            return key[0]
    return None

def show_text(info, win, keys=["space"]):
    info.draw()
    win.flip()
    reactions(keys)

def feedback(acc, experiment):
    if acc == True and experiment == False:
        feed = visual.TextStim(win=win, text="Dobra robota!", color="black", height=89)
        feed.draw()
        win.flip()
        core.wait(1.5)
        
    if acc == False and experiment == False:
        feed = visual.TextStim(win=win, text="Popełniono błąd", color="black", height=89)
        feed.draw()
        win.flip()
        core.wait(1.5)
            
    if acc == None and experiment == False:
        feed = visual.TextStim(win=win, text="Czas na odpowiedź minął, należy reagować szybciej", color="black", height=89)
        feed.draw()
        win.flip()
        core.wait(2.5)

def fix():
    top.draw()
    fix = visual.TextStim(win=win, text="+", color="black", height=89)
    fix.draw()
    win.flip()
    core.wait(0.9)

def loop(col, stim_type):
        global a
        global b
        global c
        if (col == "ZIELONY" and stim_type == 'z') or (col == "NIEBIESKI" and stim_type == 'x') or (col == "CZERWONY" and stim_type == 'n') or (col == "BRAZOWY" and stim_type == 'm'):
            if a <= 0:
                a1 = {"ZIELONY", "NIEBIESKI", "CZERWONY", "BRAZOWY", "ROZOWY"}
                a1.remove(col)
                col = random.choice(list(a1))
            else:
                a -= 1
                return col
        elif col == "ROZOWY":
            if c <= 0:
                col = random.choice(list({"ZIELONY", "NIEBIESKI", "CZERWONY", "BRAZOWY"}))
            else:
                c -= 1
                return col
        else:
            if b <= 0:
                if a <= 0:
                    col = "ROZOWY"
                else:
                    if stim_type == 'z':
                        col = "ZIELONY"
                    elif stim_type == 'x':
                        col = "NIEBIESKI"
                    elif stim_type == 'n':
                        col = "CZERWONY"
                    elif stim_type == 'm':
                        col = "BRAZOWY"
            else:
                b -= 1
                return col
        return loop(col, stim_type)

def part_of_experiment(n_trials, keys, experiment):
    for i in range(n_trials):
        fix()
        
        col = random.choice(list({"ZIELONY", "NIEBIESKI", "CZERWONY", "BRAZOWY", "ROZOWY"}))
        stim = {"z": visual.TextStim(win=win, text=col, color='#66CC00', height=89), 
            "x": visual.TextStim(win=win, text=col, color='#0088FF', height=89), 
            "n": visual.TextStim(win=win, text=col, color='#ff0202', height=89), 
            "m": visual.TextStim(win=win, text=col, color='#663300', height=89)
        }
        stim_type = random.choice(list(stim.keys()))

        col = loop(col, stim_type)
        
        stim[stim_type].text = col
        if stim_type == "z":
            color = "GREEN"
        elif stim_type == "x":
            color = "BLUE"
        elif stim_type == "n":
            color = "RED"
        elif stim_type == "m":
            color = "BROWN"
        
        top.draw()
        stim[stim_type].draw()
        win.callOnFlip(clock.reset)
        win.flip()
        
        
        key = reactionswait(keys)
        if key == "f7":
            win.close()
            core.quit()
        if key == "f8":             #For testing only, skip a sequence
            break
        rt = clock.getTime()
        
        if key == None:
            acc = None
        else:
            acc = stim_type == key
        
        if (col == "ZIELONY" and stim_type == 'z') or (col == "NIEBIESKI" and stim_type == 'x') or (col == "CZERWONY" and stim_type == 'n') or (col == "BRAZOWY" and stim_type == 'm'):
            ST = "Spojny"
        elif col == "ROZOWY":
            ST = "Neutralny"
        else:
            ST = "Niespojny"
        
        
        feedback(acc, experiment)
        RESULTS.append([conf['EXPNUM'] ,i + 1, ST, color, col, acc, rt, stim_type, key, a, b, c])
        ST = None
        color = None

conf = yaml.safe_load(open('config.yaml', encoding='utf-8'))
win = visual.Window(units="pix", size=(890, 890), color="#C0C0C0", fullscr=False)
clock = core.Clock()
win.setMouseVisible(False)
inst_tr = visual.ImageStim(win=win, image="inst.png")
top = visual.ImageStim(win=win, image="top.png", pos=(0, +350))
trbreak = visual.ImageStim(win=win, image="tpbreak.png")
trend = visual.ImageStim(win=win, image="trend.png")
expbreak = visual.ImageStim(win=win, image="expbreak.png")
expend = visual.ImageStim(win=win, image="expend.png")

show_text(info=inst_tr, win=win)
for i in range (3):
    part_of_experiment(conf['N_TRIALS_TRAINING'], REACTION_KEYS, experiment=False)
    a = 6
    b = 6
    c = 3
    if i <2:
        show_text(info=trbreak, win=win)
    else:
        show_text(info=trend, win=win)

for i in range (3):
    a = 32
    b = 32
    c = 16
    part_of_experiment(conf['N_TRIALS_EXPERIMENT'], REACTION_KEYS, experiment=True)
    if i <2:
        show_text(info=expbreak, win=win)
    else:
        show_text(info=expend, win=win)

with open("result.csv", "w", newline="") as f:
    write = csv.writer(f)
    write.writerows(RESULTS)