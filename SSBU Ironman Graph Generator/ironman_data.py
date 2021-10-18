from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, show
from bokeh.models.sources import ColumnDataSource
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.io import curdoc

# Enter Player 1 and Player 2's names here
p1_name = "Player 1"
p2_name = "Player 2"
tooltip_text = "Match @x: "+p1_name+"'s @p1_chars vs "+p2_name+"'s @p2_chars"
# B = a win for Player 2; A = a win for Player 1
results = "BAAAABABABABBBABBBABAAABABABAAABBBBBAAABAAABBAAABBABBABBBABAABBAABAABBBBAAABABBABBABABAAAABABBBBAAABBBAAAAAABBBBBABAABBAAAABBBAAABBBBBBAAAABAABABBAAABBAABBBABBBAABABABABAB"
game_ct = len(results)
characters = ["Mario", "Donkey Kong", "Link", "Samus", "Dark Samus", "Yoshi", "Kirby", "Fox", "Pikachu", "Luigi", "Ness", "Captain Falcon", "Jigglypuff", "Peach", "Daisy", "Bowser", "Ice Climbers", "Sheik", "Zelda", "Dr. Mario", "Pichu", "Falco", "Marth", "Lucina", "Young Link", "Ganondorf", "Mewtwo", "Roy", "Chrom", "Mr. Game & Watch", "Meta Knight", "Pit", "Dark Pit", "Zero Suit Samus", "Wario", "Snake", "Ike", "Pokemon Trainer", "Diddy Kong", "Lucas", "Sonic", "King Dedede", "Olimar", "Lucario", "R.O.B.", "Toon Link", "Wolf", "Villager", "Mega Man", "Wii Fit Trainer", "Rosalina & Luma", "Little Mac", "Greninja", "Palutena", "Pac-Man", "Robin", "Shulk", "Bowser Jr.", "Duck Hunt", "Ryu", "Ken", "Cloud", "Corrin", "Bayonetta", "Inkling", "Ridley", "Simon", "Richter", "King K. Rool", "Isabelle", "Incineroar", "Piranha Plant", "Joker", "Hero", "Banjo & Kazooie", "Terry", "Byleth", "Min Min", "Steve", "Sephiroth", "Pyra/Mythra", "Kazuya", "Sora", "Mii Brawler", "Mii Swordfighter", "Mii Gunner", "WINNER!"]

x = [i for i in range(1,game_ct+2)]
p1_y = [1]
p2_y = [1]
p1_chars = ["Mario"]
p2_chars = ["Mario"]

p1_char = 1
p2_char = 1
for char in results:
	if char == "B":
		p2_char += 1
	else:
		p1_char += 1
	p1_y.append(p1_char)
	p1_chars.append(characters[p1_char-1])
	p2_y.append(p2_char)
	p2_chars.append(characters[p2_char-1])

source = ColumnDataSource({
	"x": x,
	"p1_y": p1_y,
	"p2_y": p2_y,
	"p1_chars": p1_chars,
	"p2_chars": p2_chars,
	"smash_64": [12 for i in range(game_ct+1)],
	"melee": [12+14 for i in range(game_ct+1)],
	"brawl": [12+14+15 for i in range(game_ct+1)],
	"smash_4": [12+14+15+21 for i in range(game_ct+1)],
	"ultimate": [12+14+15+21+23 for i in range(game_ct+1)]
	})

p = figure(
    y_range=(0, 100),
    toolbar_location=None,
    tools=[HoverTool(mode="vline", line_policy="nearest", names=[p1_name], tooltips=[("p1_chars", "@p1_chars"), ("p2_chars", "@p2_chars")])],
    tooltips=tooltip_text,
    sizing_mode="stretch_width",
    max_width=1500,
    plot_height=750,
)

curdoc().theme = "dark_minimal"

# add renderers
#p.circle(x, y, size=1)
p.line("x", "p1_y", line_width=2, line_color="red", name=p1_name, legend_label=p1_name, source=source)
p.line("x", "p2_y", line_width=2, line_color="orange", legend_label=p2_name, source=source)

# p.line("x", "smash_64", line_width=1, line_color="grey", source=source)
# p.line("x", "melee", line_width=1, line_color="grey", source=source)
# p.line("x", "brawl", line_width=1, line_color="grey", source=source)
# p.line("x", "smash_4", line_width=1, line_color="grey", source=source)
# p.line("x", "ultimate", line_width=1, line_color="grey", source=source)

#p.xaxis.bounds = (0,0)
#p.yaxis.bounds = (0,0)

# show the results
show(p)
html = file_html(p, CDN, "smash plot")