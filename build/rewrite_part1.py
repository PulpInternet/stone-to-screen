import re, json, html as H
SRC = '/mnt/user-data/uploads/From_Stone_to_Screen-2.html'
OUT = '/home/claude/v3/part1_rewritten.html'
t = open(SRC, encoding='utf8').read()
e = H.escape

HERO_KICKER = "A history of writing as memory and cost"
HERO_LEDE = "People have always had two problems: we forget, and everything we keep costs something. Writing solved the first, and every medium since has been a new answer to the second. This is the history of that trade, from a notched bone to a language model."

EPI = {
 "part1": "The first memory kept outside a head.",
 "part2": "Writing begins as a record of resources.",
 "part3": "What memory is kept on decides what it costs and how long it lasts.",
 "part4": "Copying gets cheaper, so memory spreads.",
 "part5": "Mainz, 1455. The cost of a copy collapses.",
 "part6": "The labor of writing falls, again and again.",
 "part7": "Sending without keeping, the one exception in this history.",
 "part8": "A letter becomes a number, the densest memory yet.",
 "part9": "Type that costs computation every time it is drawn.",
 "part10": "Memory that answers back."}

BODY = {
 "ishango": "Human memory fades, and it dies with its owner. About twenty thousand years ago, someone cut grouped notches into a baboon bone so a count could outlast the moment it was made. There is no language in it. It is the first surviving memory stored outside a person, and the first trade: a little effort now, so nothing has to be held in the head later.",
 "cuneiform": "The first writing was a ledger. Temple clerks in Uruk pressed reed wedges into wet clay to track grain, beer, and sheep: memory in the service of resources. The same marks soon carried law, prayer, and Gilgamesh. Clay was cheap and, once fired, nearly permanent, which is why hundreds of thousands of tablets survive.",
 "hammurabi": "Hammurabi had 282 laws cut into seven feet of basalt and set where people could see them. Stone is expensive and immovable, and that was the point: a public memory no single official could quietly change. Picture above, words below. Writing had moved from keeping accounts to keeping promises.",
 "hunefer": "Egypt kept two kinds of memory at two prices. Hieroglyphs carved in stone were costly and built to last forever. Reed pens on papyrus were cheap, light, and fast, for everything else. The ink, soot bound with gum, does not fade: Hunefer's Book of the Dead, made around 1275 BC, is still black.",
 "oracle": "At Anyang, Shang diviners carved questions into ox bone, cracked it with heat, read the answer, and recorded what happened. Question, answer, and outcome were kept together so they could be checked later. That habit of record keeping carried a script that is the direct ancestor of Chinese characters today, unbroken for three thousand years.",
 "ahiram": "The great compression. Instead of hundreds of signs, about twenty-two Phoenician letters, each standing for a sound. Fewer symbols meant less to memorize, so learning to write took weeks instead of a career. The cost of literacy fell, and nearly every alphabet in use today descends from this coastline.",
 "greek": "The Greeks turned the Phoenician letters they did not need into vowels, so a stranger could sound out any word without knowing it first. At Gortyn the law runs back and forth, the way an ox plows a field. In Athens, Plato complained that writing would weaken memory. He made the complaint in writing, which is the only reason we still have it.",
 "rosetta": "One decree in three scripts, cut in 196 BC. When hieroglyphs were forgotten, the Greek beside them survived, and in 1822 Champollion used it to read the rest. The same message stored three ways is why a lost script came back. Redundancy costs space, and it is how memory survives.",
 "trajan": "At the base of Trajan's Column, in AD 113, letters were painted with a brush and then cut in stone, keeping the brush's flared ends: serifs. One careful model of each capital became a standard others could copy instead of reinventing. A shared standard is memory too, held by every hand that follows it.",
 "isaiah": "The Great Isaiah Scroll: seventeen stitched skins, fifty-four columns, about seven meters, copied around 125 BC and sealed in a cave until 1947. Parchment is costly and durable. A scroll must be read in order, so finding one passage means unrolling everything before it. The book with pages would make finding things faster.",
 "treasures": "China honored the whole kit of writing: brush, ink stick, inkstone, and paper, the Four Treasures of the Study. Each was a resource to make, keep, and care for. A flexible brush turns every stroke into a gesture, so calligraphy became a record of the writer as well as the words.",
 "cailun": "In AD 105, Cai Lun presented the Han court with a recipe: pulp bark, rags, and old nets, lift a sheet, press it, and dry it. Paper was cheaper than silk and lighter than bamboo. When the cost of a surface falls, more gets written down. Paper reached Baghdad about seven centuries later and Europe after about a thousand years.",
 "khwarizmi": "In Baghdad's House of Wisdom, translators moved Greek, Persian, and Indian learning into Arabic, on paper made in the city. Al-Khwarizmi wrote the book that named algebra, and his name became the word algorithm. Indian numerals and zero traveled west with it. A number system with zero makes calculation cheap, putting memory and arithmetic in the same marks.",
 "diamond": "The Diamond Sutra is a woodblock print dated to the day, May 11, 868, and made, its closing lines say, for free distribution. Carve a page once and print it many times. The labor moves to the start, and every copy after that costs little. For a script with thousands of characters, a carved block was the efficient tool.",
 "jikji": "Movable type was invented twice in Asia: in clay by Bi Sheng around 1040, and in bronze in Korea. The Jikji, printed in 1377, is seventy-eight years older than Gutenberg's Bible. Reusable letters cut the cost of each new page. What Korea lacked was a market large enough to spread the cost of the system.",
 "kells": "While printing developed in Asia, monks in Iona and Kells made the handwritten page more valuable, not cheaper. The Chi Rho page of the Book of Kells spends a full page on three letters. Scarce, slow, and expensive, it was memory treated as treasure.",
 "mielot": "Jean Mielot, scribe to the Duke of Burgundy: quill, knife, and iron gall ink that bites into the page. One Bible took about a year of skilled work. Demand for books had outgrown the hands available to copy them. This is the resource problem print would solve.",
 "gutenberg": "Gutenberg's achievement was a system: an adjustable mold, a lead alloy, oil-based ink, and a converted screw press. The 42-line Bible appeared around 1455, and within fifty years presses ran in about 250 towns. The cost of a copy collapsed, and memory spread into thousands of identical books.",
 "press": "The machine itself: a screw drives a flat platen onto inked type. One person sets, one inks, one pulls. About 240 sheets an hour, from a design that barely changed for three and a half centuries. Speed per sheet, more than any new idea, changed what a society could afford to remember.",
 "punches": "Every metal letter began as a steel punch, cut in mirror image at final size. The punch strikes a matrix, and the matrix shapes the mold. One careful master is reused across thousands of letters. Garamont's designs from the 1530s still ship with your computer: five centuries of reuse from one investment.",
 "caslon": "By 1734 type is an industry with a catalog. Caslon's specimen sheet shows a whole family in graded sizes: one design, made once and sold many times. His letters set the first printing of the Declaration of Independence.",
 "typecase": "Four centuries after Gutenberg, pages were still built letter by letter from cases like this one. Then steam changed everything around them: Koenig's press printed The Times on November 29, 1814, at eleven hundred sheets an hour, and wood-pulp paper made the surface almost free. Mass literacy followed the falling cost.",
 "linotype": "Mergenthaler's Linotype, New York Tribune, 1886. An operator types; the machine assembles brass molds, spaces the line, and casts it in hot metal. One keyboard replaces several hands. The labor cost of setting text drops, and typing becomes how text enters every machine after it.",
 "fotosetter": "After five centuries in metal, type became light on film. The Fotosetter replaced the caster with a camera, and letters stopped weighing anything. They could touch, overlap, and stretch. Keeping a typeface no longer meant keeping tons of lead.",
 "phonograph": "In 1877, Edison recited a nursery rhyme into a horn, and a needle cut his voice into tinfoil. Phonograph means sound writing. For the first time, speech could be stored directly, with no one writing it down. Memory extended from words to voices.",
 "radio": "Marconi sent signals through open air in 1897. By the 1920s, voices reached millions of homes at once. Radio is the exception in this history: it sends without keeping anything. Unless someone records it, a broadcast is gone the moment it ends.",
 "tv": "Television put picture and voice in one box in the living room. In 1950 few American homes had one; by 1960 most did. Like radio, it broadcast without storing, and much of early television was never kept. Type survived on screen as captions, credits, and the news crawl.",
 "punchcard": "Computers met the alphabet through holes in cardboard. Hollerith's cards counted the 1890 census, and IBM's 80-column card held one line of uppercase text for decades. In 1963, ASCII gave every character a number: A is 65. A letter now took seven bits to store, the densest memory yet.",
 "vt100": "On the VT100 terminal of 1978, text was redrawn sixty times a second and vanished at power-off. Memory was so scarce that the whole font lived on one small chip, every letter in an identical cell. Its 80 columns echo the punched card, and its control codes still run terminals today.",
 "c64": "The best-selling computer model in history drew its entire alphabet on an 8 by 8 grid, using 2 kilobytes of memory. Designing a legible lowercase e in 64 dots is type design under hard limits. The blocky look came from scarcity, and people now choose it on purpose.",
 "mac": "In 1984 the Macintosh shipped with real typefaces, drawn pixel by pixel by Susan Kare. PostScript then described letters as math, scalable to any size from one small file, and the LaserWriter printed them. Typesetting moved from a building full of equipment to a desk.",
 "web": "In 1990, on a NeXT computer at CERN, Tim Berners-Lee wrote text that links to other text. A page no longer had to hold everything; it could point to memory kept elsewhere. Unicode gave every script on earth a number. Web fonts arrived around 2010, and the history of type became something a page could load on demand.",
 "moves": "In 1959, Saul Bass sent letters sliding across Hitchcock's screens, and the title sequence became an art. Type on a screen is not stored as a finished picture; it is computed and drawn again every frame. Movement has a cost, paid every time. Watch the letter breathe.",
 "reacts": "In 2016, variable fonts made a letter a point in a design space, with weight and width as live settings. One file now holds what used to take dozens, and the letter is computed as you go. Move across it, and it answers. The page has started reading back."}

INNOV = [("Memory outside the head", "The first trade: a little effort now, so a count no longer has to be held in anyone's mind."),
 ("A ledger of resources", "Writing begins as accounting. The first written memory was a record of grain and livestock."),
 ("Public, permanent memory", "Expensive stone buys a record that is hard to change and easy for everyone to see."),
 ("Two prices of memory", "Stone for what must last forever, papyrus for daily work: the medium chosen by how long the memory must last."),
 ("Records that can be checked", "Question, answer, and outcome kept together, so a claim could be tested later."),
 ("Compression", "About twenty-two signs instead of hundreds. Less to memorize, so the cost of literacy falls."),
 ("Readable by strangers", "Vowels let anyone sound out a word without already knowing it: memory that does not depend on the reader."),
 ("Redundancy", "The same message stored three ways. Duplication costs space, and it is how memory survives loss."),
 ("Standards", "One careful model copied by everyone, so no hand has to reinvent the letter."),
 ("Long documents", "Durable, costly parchment holds book-length text, but finding a passage means unrolling everything before it."),
 ("Tools as treasures", "Brush, ink, inkstone, and paper, each a resource made and kept with care."),
 ("Cheap surfaces", "When the surface gets cheaper, people write more down."),
 ("Calculation in the marks", "Numerals with zero make arithmetic cheap and put memory and computation in the same symbols."),
 ("Pay once, copy cheaply", "The cost moves to carving the block. Every copy after that costs little."),
 ("Reusable parts", "Letters cast once and recombined, cutting the cost of every new page."),
 ("Scarcity as value", "The opposite strategy: make each copy rare and precious instead of cheap."),
 ("The labor limit", "Demand for memory outgrows the hands available to copy it."),
 ("Copies at scale", "A complete system that makes copies cheap enough for whole societies to share the same texts."),
 ("Speed per sheet", "Output per hour, more than new ideas, changes what a society can afford to remember."),
 ("Master tooling", "One steel punch, reused across thousands of letters for centuries."),
 ("Made once, sold many times", "The type family: one design investment spread across a whole product line."),
 ("Falling costs", "Steam presses and wood pulp push the cost of text toward nothing, and reading spreads."),
 ("Keyboard entry", "One keyboard replaces several hands, and typing becomes the way text enters machines."),
 ("Weightless type", "Letters stored as images instead of metal. A typeface stops weighing tons."),
 ("Stored voice", "Speech recorded directly, with no one writing it down."),
 ("Sending without keeping", "One voice reaches millions, and nothing is kept unless someone records it."),
 ("Picture and voice, live", "Broadcast at scale, with much of it never stored."),
 ("Characters as numbers", "Every letter gets a number, the most compact memory yet."),
 ("Scarce memory, fixed cells", "A whole font on one small chip, every letter the same width because memory was precious."),
 ("Design under limits", "An alphabet in 2 kilobytes. The constraint shaped the letters."),
 ("Letters as math", "Outlines described by math, scalable to any size from one small file."),
 ("Memory by reference", "A page points to text kept elsewhere instead of holding it all."),
 ("Compute per frame", "Type redrawn every frame. Movement has an ongoing cost."),
 ("One file, many styles", "A whole range of weights and widths in one file, computed live as the reader moves.")]

CODA_TITLE = "The newest memory"
CODA = ["Large language models are the newest answer to the oldest problem. They hold a compressed memory of much of what is on this page: tablets, scrolls, sutras, broadsheets, scripts, captions, and code. Like every medium before them, they have a cost. Each answer uses electricity in a data center, and the power plants behind it use water.",
        "Every medium here was blamed for ruining something. Plato said writing would weaken memory. Scribes said print would cheapen the book. Radio would kill reading, and television would kill radio. None of them made people better or worse thinkers. Habits did.",
        "AI does not care what you mean. People do. The job is the one the clerks in Uruk had: keep what matters, spend only what it takes, and keep honest books. The tools keep changing. The job never did."]

# hero
assert t.count('<p class="kicker">') >= 1
t = re.sub(r'<p class="kicker">.*?</p>', f'<p class="kicker">{e(HERO_KICKER)}</p>', t, count=1, flags=re.S)
t, n = re.subn(r'<p class="lede">Five thousand years ago.*?</p>', f'<p class="lede">{e(HERO_LEDE)}</p>', t, count=1, flags=re.S); assert n == 1
# chapter lines
for pid, line in EPI.items():
    t, n = re.subn(rf'(<section class="part [a-z]+" id="{pid}"><header class="phead"><p class="pnum">.*?</p><h2>.*?</h2><p class="epi">).*?(</p>)', lambda m: m.group(1) + e(line) + m.group(2), t, count=1, flags=re.S); assert n == 1, pid
# moment bodies
for k, body in BODY.items():
    pat = rf'(<article class="beat[^"]*" id="{k}" data-i="\d+">.*?)<p class="body">.*?</p>'
    t, n = re.subn(pat, lambda m: m.group(1) + f'<p class="body">{e(body)}</p>', t, count=1, flags=re.S); assert n == 1, k
# coda
t, n = re.subn(r'(<section class="coda" id="coda"><p class="pnum">Closing</p><h2>).*?(</h2>).*?(</section>)',
               lambda m: m.group(1) + e(CODA_TITLE) + m.group(2) + ''.join(f'<p>{e(p)}</p>' for p in CODA) + m.group(3), t, count=1, flags=re.S); assert n == 1
# New here ledger
t, n = re.subn(r'var INNOV = \[.*?\];', lambda m: 'var INNOV = ' + json.dumps([{"t": a, "d": b} for a, b in INNOV]) + ';', t, count=1, flags=re.S); assert n == 1
open(OUT, 'w', encoding='utf8').write(t)
print('Part I rewritten:', len(BODY), 'moments,', len(EPI), 'chapter lines,', len(INNOV), 'ledger notes; em dash:', '\u2014' in re.sub(r'src="data:[^"]+"', '', t))
