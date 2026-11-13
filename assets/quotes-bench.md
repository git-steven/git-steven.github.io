# 💬 Quotes bench

A living list of epigraphs: what's in which post, what's on the shortlist, and what's still waiting on the bench. Every entry keeps the angle it was picked for, so a future draft can grab one without working out all over again why it fits.

**Keeping it current**

* When a 📌 pick lands in its post, move its row from **📌 Picked** to **✅ In use** and flip its entry to ✅.
* When a quote gets cut, delete the row and flip the entry back to ⏳. Leave the angle alone; it was a good idea once.
* When there's a new article, give it a key in the table below before tagging anything with it.
* Entries are written in the same epigraph format the posts use, so they paste straight in.

## 📑 Keys

**Status:** ✅ in use · 📌 picked for a specific slot, not placed in the post yet · ⏳ on the bench · ⚠️ attribution or exact wording needs a check before it ships

| Key | Post | File |
|---|---|---|
| `layered` | 🗄️ Simplicity That Still Works: Layered Architecture | `_posts/2025-08-14-layered-architecture.md` |
| `hootl` | 🪜 Autonomous AI Systems: HOOTL | `_posts/2026-10-15-aut-ai-hootl.md` |
| `spectrum` | 🌈 Autonomy is a spectrum, not a switch | `_posts/2026-10-20-autonomy-is-a-spectrum.md` |
| `rap-sheet` | 🧾 Reading the Rap Sheet | `_posts/2026-10-21-reading-the-rap-sheet.md` |
| `leash` | 🔄 Autonomy on a Leash | `_posts/2026-11-03-gated-loop-ai-code.md` |
| `no-return` | 🚪 There Is No Return | `_posts/2026-11-04-eop-no-return.md` |
| `croc` | 🐊 The Polyglot and the Crocodile | `_posts/2026-11-05-elixir-polyglot-crocodile.md` |
| `4hats` | 🎩 Four Hats for One Process | `_posts/2026-11-06-elixir-four-hats.md` |
| `amnesia` | 🧠 Curing your database's amnesia | `_posts/2026-11-10-curing-your-databases-amnesia.md` |

## ✅ In use

| Quote | Who | Post | Where |
|---|---|---|---|
| "Good architecture doesn't hide complexity — it organizes it." | anonymous ("a pragmatic software architect") | `layered` | top of post |
| "The future is already here. It's just not evenly distributed." | William Gibson | `hootl` | 👥 Part 3 Introduction |
| "It's a simple complex system. That's the technical name for it…" | James S. A. Corey, _Caliban's War_ | `spectrum` | 📝 Introduction |
| "Finding Not Not Guilty." | a real disposition string | `rap-sheet` | 📝 Introduction |
| "Any fool can write code that a computer can understand…" | Martin Fowler, _Refactoring_ | `leash` | 📝 Introduction |
| "Doors and corners, kid. That's where they get you." | Detective Miller, _Leviathan Wakes_ | `no-return` | 📝 Introduction |
| "Composing simple components, simple in that same respect, is the way we write robust software." | Rich Hickey, _Simple Made Easy_ | `no-return` | 🛤️ What replaced the door |
| "Asking a question should not change the answer." | Bertrand Meyer, _Object-Oriented Software Construction_ | `amnesia` | ⚖️ CQRS |
| "Capture all changes to an application state as a sequence of events." | Martin Fowler, _Event Sourcing_ | `amnesia` | 📜 Event Sourcing |
| "A well-done CRUD is much better than a poorly done Event Sourcing." | Oskar Dudycz, _When not to use Event Sourcing?_ | `amnesia` | 🤝 Conclusion |

## 📌 Picked

Chosen on 2026-11-10 and waiting to be placed. Full text and angles are in the genre sections below.

| Post | Slot | Pick | Runners-up |
|---|---|---|---|
| `croc` | 📝 Introduction | Perlis, epigram #19 | Yoda ("unlearn"), Bohr ⚠️ |
| `croc` | 🧱 Elixir-isms | Spoon Boy, _The Matrix_ | Armstrong (banana), Kay |
| `4hats` | 📝 Introduction | Wheeler to Feynman, "the same electron" | Armstrong ("Everything is a process") ⚠️, Kay |
| `amnesia` | 📝 Introduction | Wheeler, "the past has no existence except as it is recorded in the present" | Orwell, _Blade Runner_, Chiang ⚠️ |

`no-return` stays as it is: Miller and Hickey already carry it. Slots that were considered and left empty for now: `croc` 🧬 Concurrency is grammar (Virding), `4hats` 📏 338 Words (Deep Thought).

---

## 🛸 Science fiction

> History has stopped. Nothing exists except an endless present in which the Party is always right.
> — **George Orwell**, _Nineteen Eighty-Four_ (1949), Winston Smith

* ⏳ `amnesia` → 📝 Introduction (runner-up to Wheeler). Also works above 📜 Event Sourcing › One fact, two records.
* *Angle:* a row updated in place is exactly this: an endless present that is always right. "Every `UPDATE` is a small act of forgetting," with a 1949 pedigree.

> Who controls the past controls the future: who controls the present controls the past.
> — **George Orwell**, _Nineteen Eighty-Four_ (1949), Party slogan

* ⏳ `amnesia` → 📜 Event Sourcing › One fact, two records
* *Angle:* the case for keeping effective and recorded time apart. Edit the March row and you've done the Ministry of Truth's job for it. Use one Orwell per post, not both.

> All those moments will be lost in time, like tears in rain.
> — **Roy Batty**, _Blade Runner_ (1982)

* ⏳ `amnesia` → 📝 Introduction
* *Angle:* every overwritten row. Beautiful, and so familiar that it reads as decoration rather than argument.

> It is just an illusion we have here on Earth that one moment follows another one, like beads on a string, and that once a moment is gone it is gone forever.
> — **Kurt Vonnegut**, _Slaughterhouse-Five_ (1969), on the Tralfamadorians

* ⏳ `amnesia` → 📜 Event Sourcing › Stop overwriting the evidence
* *Angle:* the Tralfamadorians see every moment at once, which makes them an event store with good eyesight. "Gone forever" is CRUD's default setting.

> Our memories are not the impartial accumulation of every second we've lived; they're the narrative that we assembled out of selected moments.
> — **Ted Chiang**, "The Truth of Fact, the Truth of Feeling" (2013), in _Exhalation_ (2019)

* ⏳ ⚠️ `amnesia` → 📝 Introduction, or 📜 Event Sourcing › The read model is a function, not a copy
* *Angle:* a whole story about a lifelog proving the narrator's memory wrong. The row is the narrative; the log is the impartial accumulation. Fresher than _Blade Runner_, but it needs a beat to land.
* ⚠️ *Check:* the first clause is confirmed in quote collections; check the full sentence against _Exhalation_.

> Time is an illusion. Lunchtime doubly so.
> — **Ford Prefect**, in Douglas Adams' _The Hitchhiker's Guide to the Galaxy_ (1979)

* ⏳ `amnesia` → 📜 Event Sourcing › Stop overwriting the evidence
* *Angle:* the SLA clock paused because the customer went to lunch, and the row remembers only "80 minutes." Use it if the post wants a laugh before the fold.

> All of this has happened before, and all of this will happen again.
> — _Battlestar Galactica_ (2004–2009), echoing J. M. Barrie's _Peter Pan_ (1911)

* ⏳ `amnesia` → 📜 Event Sourcing › What it costs
* *Angle:* replay. Fine for a projector. For the notifier that sends the survey twice, it's the whole problem.

> You must unlearn what you have learned.
> — **Yoda**, _The Empire Strikes Back_ (1980)

* ⏳ `croc` → 📝 Introduction
* *Angle:* the polyglot's problem in six words: the Ruby, Python and Java habits are what the crocodile eats. Better known than Perlis, less precise.

> Do. Or do not. There is no try.
> — **Yoda**, _The Empire Strikes Back_ (1980)

* ⏳ `croc` → 🧬 Concurrency is grammar, not a library
* *Angle:* "let it crash": the recovery policy lives in a supervisor, not a `rescue` block. It's a pun and it knows it. Don't use both Yodas.

> Do not try and bend the spoon. That's impossible… Then you'll see that it is not the spoon that bends, it is only yourself.
> — **Spoon Boy**, _The Matrix_ (1999)

* 📌 `croc` → 🧱 Elixir-isms
* *Angle:* immutability vs rebinding: you cannot bend the value, you can only give the name a new one. The intro's "You can give a name a new value. You cannot change the old one" says the same thing.

> I admire its purity. A survivor… unclouded by conscience, remorse, or delusions of morality.
> — **Ash**, _Alien_ (1979)

* ⏳ `croc` → 🏛️ What's under the clothes, or 🗝️ The log that bites
* *Angle:* purity plus survival is immutability plus uptime, and the crocodile metaphor gets an apex predator. The "morality" half is dead weight; quote only up to "A survivor" if it reads better.

> I think the problem, to be quite honest with you, is that you've never actually known what the question is.
> — **Deep Thought**, in Douglas Adams' _The Hitchhiker's Guide to the Galaxy_ (1979)

* ⏳ `4hats` → 📏 338 Words (recommended; the slot is empty for now)
* *Angle:* "300" was the answer, and nobody checked whether the question was asked in bytes or words. A number without its unit is 42.

> We all change, when you think about it. We're all different people all through our lives, and that's okay, that's good, you've gotta keep moving, so long as you remember all the people that you used to be.
> — **The Eleventh Doctor**, _Doctor Who_, "The Time of the Doctor" (2013)

* ⏳ `4hats` → 📜 Commanded: the aggregate hat. Also `amnesia` → 📜 Event Sourcing.
* *Angle:* a new body with the same history. A crashed aggregate process restarts and replays its stream until it's itself again; it's regeneration with an event store.

> Murphy's law doesn't mean that something bad will happen. It means that whatever can happen, will happen.
> — **Cooper**, _Interstellar_ (2014)

* ⏳ `4hats` → 🗓️ Oban: the job hat
* *Angle:* "Retries are a policy, not a prayer." Plan for everything that can happen at 3 a.m., not just the bad parts.

> There ain't no such thing as a free lunch.
> — **Mannie**, in Robert A. Heinlein's _The Moon Is a Harsh Mistress_ (1966)

* ⏳ `4hats` → ⚖️ Where the hats pinch
* *Angle:* the intro says the fourth hat is free and the Oban section calls Oban Pro "the honest footnote on an otherwise free lunch." This section is the bill. (The phrase predates Heinlein; he's the one who made it famous.)

> I'll be back.
> — **The Terminator**, _The Terminator_ (1984)

* ⏳ `no-return` → 🗝️ The door was never the point
* *Angle:* the thesis is that early return didn't die, it came back with a type signature. A cliché, but short enough to get away with.

> Once men turned their thinking over to machines in the hope that this would set them free. But that only permitted other men with machines to enslave them.
> — **Frank Herbert**, _Dune_ (1965), Reverend Mother Gaius Helen Mohiam

* ⏳ `hootl` · `spectrum`
* *Angle:* the cautionary bookend to taking the human out of the loop; the answer is "earn it, audit it."

> This mission is too important for me to allow you to jeopardize it.
> — **HAL 9000**, _2001: A Space Odyssey_ (1968)

* ⏳ `hootl` · `spectrum`
* *Angle:* a machine that decided it had earned full autonomy, and nobody could reconstruct why.

> Any sufficiently advanced technology is indistinguishable from magic.
> — **Arthur C. Clarke**, third law, _Profiles of the Future_ (1973 edition)

* ⏳ `hootl`
* *Angle:* audit records and metrics exist so that the system isn't magic.

> A robot may not injure a human being or, through inaction, allow a human being to come to harm.
> — **Isaac Asimov**, First Law of Robotics, _I, Robot_ (1950)

* ⏳ `hootl`
* *Angle:* the "through inaction" clause is the tenant-screening story. Familiar to the point of cliché.

---

## 🏛️ Software architecture heroes

> A language that doesn't affect the way you think about programming, is not worth knowing.
> — **Alan Perlis**, "Epigrams on Programming" #19, _SIGPLAN Notices_ (1982)

* 📌 `croc` → 📝 Introduction
* *Angle:* the whole article in one line. Elixir's clothes are familiar; the thinking isn't, and that's the reason to learn it.

> Syntactic sugar causes cancer of the semicolon.
> — **Alan Perlis**, "Epigrams on Programming" #3, _SIGPLAN Notices_ (1982)

* ⏳ `croc` → 🗝️ The log that bites
* *Angle:* "The syntax is the bait." The Ruby-flavored sugar is what gets you in the water.

> Any sufficiently complicated concurrent program in another language contains an ad hoc informally-specified bug-ridden slow implementation of half of Erlang.
> — **Robert Virding**, "Virding's First Rule of Programming," erlang-questions mailing list (2008)

* ⏳ `croc` → 🧬 Concurrency is grammar, not a library (recommended; the slot is empty for now)
* *Angle:* the section argues that concurrency belongs in the language rather than an import. Virding, who co-created Erlang, made the same point as a Greenspun parody.

> The problem with object-oriented languages is they've got all this implicit environment that they carry around with them. You wanted a banana but what you got was a gorilla holding the banana and the entire jungle.
> — **Joe Armstrong**, in Peter Seibel's _Coders at Work_ (2009)

* ⏳ `croc` → 🧱 Elixir-isms › Modules: where the classes went
* *Angle:* "Data is data, and it never learns any methods." From the man who built the runtime, and it keeps the article's animal theme going.

> Everything is a process. … Processes do what they are supposed to do or fail.
> — **Joe Armstrong**, _Making reliable distributed systems in the presence of software errors_ (PhD thesis, 2003), "the Erlang view of the world"

* ⏳ ⚠️ `4hats` → 📝 Introduction (first sentence alone) · `croc` → 🧬 Concurrency is grammar (the "or fail" line, for "let it crash")
* *Angle:* the four hats in three words, from the source the crocodile post already cites as [10].
* ⚠️ *Check:* both lines appear in summaries of the thesis's list; confirm the wording against the PDF.

> I'm sorry that I long ago coined the term "objects" for this topic because it gets many people to focus on the lesser idea. The big idea is "messaging".
> — **Alan Kay**, squeak-dev mailing list (10 October 1998)

* ⏳ `4hats` → 📝 Introduction · `croc` → 🧱 Elixir-isms › Modules: where the classes went
* *Angle:* the man who coined "objects" says the mailbox was the point. Elixir has no objects and is all mailboxes, which arguably makes it more Kay-OO than Java.

> I call it my billion-dollar mistake. It was the invention of the null reference in 1965.
> — **Tony Hoare**, "Null References: The Billion Dollar Mistake," QCon London (2009)

* ⏳ `no-return` → 🧱 Everything is a value, including nothing
* *Angle:* Elixir's `nil` is a value that `if` hands back on purpose. Hoare's null was a hole pretending to be a value.

> The go to statement as it stands is just too primitive; it is too much an invitation to make a mess of one's program.
> — **Edsger W. Dijkstra**, "Go To Statement Considered Harmful," _Communications of the ACM_ (1968)

* ⏳ `no-return` → 🧱 Guard clauses: the orthodoxy with no receipts
* *Angle:* the ancestor of every "one exit per function" rule. The letter is about `goto`; `return` inherited the suspicion without ever being tried.

> One accurate measurement is worth a thousand expert opinions.
> — **Grace Hopper** (attributed)

* ⏳ ⚠️ `4hats` → 📏 338 Words · `no-return` → 🧱 Guard clauses: the orthodoxy with no receipts
* *Angle:* "The receipts, since the 300-byte claim didn't bring any." The same jab fits the no-receipts guard-clause folklore.
* ⚠️ *Check:* Wikiquote lists this as unsourced. Fine as "attributed"; don't present it as a citation.

> The truth is the log. The database is a cache of a subset of the log.
> — **Pat Helland**, "Immutability Changes Everything," CIDR (2015)

* ⏳ `amnesia` → 📜 Event Sourcing › The read model is a function, not a copy, or 📜 Event Sourcing
* *Angle:* the strongest software-hero line for the post. The catch is that the section already quotes Kleppmann's "just a cached view of the event log," so using both repeats the point. Use Helland as the epigraph only if the Kleppmann line goes.

> A log is perhaps the simplest possible storage abstraction. It is an append-only, totally-ordered sequence of records ordered by time.
> — **Jay Kreps**, "The Log: What every software engineer should know about real-time data's unifying abstraction" (2013)

* ⏳ `amnesia` → 📜 Event Sourcing
* *Angle:* an alternate to Fowler's definition, from the Kafka side of the house. Plainer, and less of a pitch.

> If it hurts, do it more often.
> — **Martin Fowler**, [FrequencyReducesDifficulty](https://martinfowler.com/bliki/FrequencyReducesDifficulty.html) (2011)

* ⏳ `hootl` · `leash`
* *Angle:* recalibrate, retrain and re-test the threshold on a schedule, not when the letter arrives. Also fits CI/CD and gated-loop pieces.

> Program to an interface, not an implementation.
> — **Gamma, Helm, Johnson, Vlissides**, _Design Patterns_ (1994)

* ⏳ `croc` → 🧱 Elixir-isms › Behaviours: interfaces, British spelling · `layered`
* *Angle:* ports, adapters and gates between components. In `croc`, a behaviour is literally this rule with a compiler warning attached. A weak fit for the autonomy pieces.

---

## ⚛️ Quantum physics

> "Feynman, I know why all electrons have the same charge and the same mass." "Why?" "Because, they are all the same electron!"
> — **John Archibald Wheeler**, on the phone to Richard Feynman, as Feynman told it in his Nobel lecture (1965)

* 📌 `4hats` → 📝 Introduction. Also works above 🎩 Same head, different hat.
* *Angle:* "Four hats. Same head." Every Elixir library is the same 338-word process, and Wheeler said the same about every electron in the universe. Wrong about electrons, as it turned out, and right about Phoenix.

> The past has no existence except as it is recorded in the present.
> — **John Archibald Wheeler**, "The 'Past' and the 'Delayed-Choice' Double-Slit Experiment," in _Mathematical Foundations of Quantum Theory_, ed. A. R. Marlow (1978)

* 📌 `amnesia` → 📝 Introduction. Also fits `4hats` → 📜 Commanded.
* *Angle:* event sourcing as physics. If it isn't in the log, it didn't happen, and the rows are just the present's reading of the record.
* *Source:* in context, Wheeler is answering whether a delayed choice changes the past: "Neither; the lesson presents itself rather like this, that the past has no existence except as it is recorded in the present." Bohm, Dewdney and Hiley disputed the conclusion in _Nature_ (1985), so if anyone pushes back, you're in good company.

> We have to remember that what we observe is not nature herself, but nature exposed to our method of questioning.
> — **Werner Heisenberg**, _Physics and Philosophy_ (1958)

* ⏳ ⚠️ `amnesia` → ⚖️ CQRS, as a foil to Meyer
* *Angle:* in quantum mechanics, asking a question *does* change the answer. CQRS is the decision not to run your read path on quantum rules. It's a better pairing in the body than as a second epigraph.
* ⚠️ *Check:* the wording varies across editions ("nature herself" / "nature in itself"), and some collections cite _The Physicist's Conception of Nature_ instead.

> If I were forced to sum up in one sentence what the Copenhagen interpretation says to me, it would be "Shut up and calculate!"
> — **N. David Mermin**, "What's Wrong with this Pillow?", _Physics Today_ (April 1989)

* ⏳ `no-return` → 🧱 Everything is a value, including nothing
* *Angle:* expression-oriented programming in four words: no statements, just the value. As a bonus, everyone credits Feynman, and Mermin spent a 2004 column showing it was him. Trim to the last four words if space is tight.

> Anyone who is not shocked by quantum theory has not understood it.
> — **Niels Bohr** (1952), as recalled in Werner Heisenberg's _Physics and Beyond_ (1971)

* ⏳ ⚠️ `croc` → 📝 Introduction
* *Angle:* "Then it bites." If `x = 1` hasn't surprised you, you haven't understood `=` yet.
* ⚠️ *Check:* this is secondhand (Heisenberg's recollection), and the wording varies. Present it as attributed.

> Nature isn't classical, dammit, and if you want to make a simulation of nature, you'd better make it quantum mechanical, and by golly it's a wonderful problem, because it doesn't look so easy.
> — **Richard Feynman**, "Simulating Physics with Computers" (MIT talk 1981, _International Journal of Theoretical Physics_ 1982)

* ⏳ `croc` → 🧬 Concurrency is grammar, not a library
* *Angle:* the world is concurrent, so a language that pretends otherwise is simulating the wrong universe. Long; trim after "quantum mechanical."

---

## 📖 Off-genre, too good to drop

Not science fiction, software or physics, but kept because the fit is exact.

> Happy families are all alike; every unhappy family is unhappy in its own way.
> — **Leo Tolstoy**, _Anna Karenina_ (1878)

* ⏳ `no-return` → ⚠️ Beware!
* *Angle:* the `with` railway in one sentence. The happy path has one shape, every failure has its own, and normalizing the errors is how you make the unhappy families alike.

> Memory can change the shape of a room; it can change the color of a car. And memories can be distorted. They're just an interpretation, they're not a record, and they're irrelevant if you have the facts.
> — **Leonard Shelby**, _Memento_ (2000)

* ⏳ ⚠️ `amnesia` → 📝 Introduction, or 📜 Event Sourcing › The read model is a function, not a copy
* *Angle:* "they're not a record" is the whole post. The irony that Leonard's own record is the unreliable part is a bonus for anyone who's seen the film.
* ⚠️ *Check:* fan transcripts differ slightly ("And memories" / "Memories"); check against the film.

> …by a lucky chance it swallowed a clock which goes tick tick inside it, and so before it can reach me I hear the tick and bolt.
> — **Captain Hook**, in J. M. Barrie's _Peter and Wendy_ (1911), on the crocodile

* ⏳ `croc` → 🗝️ The log that bites
* *Angle:* the BEAM "interrupts it every 4,000 calls." The original literary crocodile also keeps time from the inside.
