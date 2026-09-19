# Conceptual support

Could someone arrive at this belief from the Bible without ever seeing the phrase?

A regex proves a wording is absent. It says nothing about whether the idea is there.
This report is the other half: for every case, the passages a reasonable reader could
build the belief from, and the passages that cut against it. Every verse is resolved and
quoted by `tools/verify.py` — the **quotations are mechanical, the gradings are judgement**,
and they are kept visibly separate.

Where a passage cuts **against** a belief and the tradition holding it has a standard answer,
that answer is printed beneath the objection. Without it this file would be a one-sided brief:
an objection presented as though it were a refutation.

**How the verdicts are decided.** The gradings involve judgement — no tool can decide whether
a passage supports an idea — but the criteria are explicit and each case records which test
decided it, so a grading can be challenged on stated grounds rather than on taste.

| Test | Decides |
| --- | --- |
| `states-directly` | At least one passage asserts the substance of the belief, not merely something compatible with it. **strong** |
| `converges` | Several passages independently imply it, none stating it outright. **strong** |
| `component-split` | The belief has separable components; the text supports at least one and is silent on, disputes, or contradicts another. Both must be named. **partial** |
| `inferential` | Support requires chaining passages, or combining ones that do not address the topic together. The belief supplies most of its own content. **weak** |
| `silent` | No passage addresses the question the belief answers. **none** |
| `asserts-otherwise` | A passage addresses the point and asserts something incompatible, with no standard reply. **contradicted** |

A `partial` where the unsupported component is actively CONTRADICTED is more damaging to the belief than one where it is merely unaddressed. The verdict alone does not carry that distinction, so the components field states it.

| Verdict | Cases | Meaning |
| --- | ---: | --- |
| `none` | 3 | No passage supplies the idea. The belief has to come from somewhere else. |
| `weak` | 6 | Something in the text gestures at it, but the belief adds most of its content. |
| `partial` | 10 | Real material supports part of the belief while another part is imported or disputed. |
| `strong` | 4 | The idea is well supported; only the wording, the label or the systematisation is post-biblical. |
| `contradicted` | 1 | The text addresses the point and says something incompatible. |

**101 passages resolved and quoted across 24 cases; 13 objections carry the tradition's reply.**

## "God helps those who help themselves"

`god-helps-those-who-help-themselves` &middot; verdict: **partial** &middot; decided by `component-split`

The work ethic is thoroughly biblical; the theology of self-reliance is the opposite of the New Testament's. The proverb smuggles the second in under the first.

**Supported:** Diligence as a virtue - Proverbs 6:6, 2 Thessalonians 3:10 support this directly.  
**Imported or disputed:** That divine help is CONDITIONAL on self-reliance. Not merely unsupported but contradicted: Romans 5:6 and Ephesians 2:8 make grace precisely what arrives where self-help fails.

- **supports** &nbsp; `Proverbs 6:6` — the sluggard is sent to the ant; diligence is commended in its own right  
  > Go to the ant, you lazybones; consider its ways, and be wise.
- **supports** &nbsp; `2 Thessalonians 3:10` — 'anyone unwilling to work should not eat' - the closest thing to the proverb in the NT  
  > For even when we were with you, we gave you this command: Anyone unwilling to work should not eat.
- **supports** &nbsp; `Proverbs 13:4` — the diligent soul is richly supplied  
  > The appetite of the lazy craves, and gets nothing, while the appetite of the diligent is richly supplied.
- **against** &nbsp; `Romans 5:6` — Christ died for us 'while we were still weak' - help arrives precisely where self-help fails  
  > For while we were still weak, at the right time Christ died for the ungodly.
- **against** &nbsp; `Ephesians 2:8` — salvation by grace 'not the result of works'  
  > For by grace you have been saved through faith, and this is not your own doing; it is the gift of God—
- **against** &nbsp; `Luke 18:13` — the tax collector who can only ask for mercy is the one justified  
  > But the tax collector, standing far off, would not even look up to heaven, but was beating his breast and saying, ‘God, be merciful to me, a sinner!’

*Dissent:* Some would grade this `contradicted`, on the grounds that the proverb's actual force is the soteriological half, not the work-ethic half. Graded partial because the saying is genuinely used in both senses.

---

## "Cleanliness is next to godliness"

`cleanliness-next-to-godliness` &middot; verdict: **weak** &middot; decided by `inferential`

Ritual purity is a huge biblical category, so the idea has a real Levitical shape - but Jesus explicitly relativises external cleanness, which is why this is not simply 'weak'.

- **supports** &nbsp; `Leviticus 11:44` — 'be holy, for I am holy' sits inside an extended purity code  
  > For I am the LORD your God; sanctify yourselves therefore, and be holy, for I am holy. You shall not defile yourselves with any swarming creature that moves on the earth.
- **supports** &nbsp; `Exodus 30:19` — priests wash before approaching the altar  
  > with the water Aaron and his sons shall wash their hands and their feet.
- **against** &nbsp; `Mark 7:15` — nothing outside a person can defile them  
  > there is nothing outside a person that by going in can defile, but the things that come out are what defile.”
  <br>↳ *Reply:* Read as relativising ritual purity in favour of moral purity rather than dismissing cleanness as a category - which leaves the proverb's sense intact if 'cleanliness' is taken morally.
- **against** &nbsp; `Matthew 23:25` — cleaning the outside of the cup while the inside is full of greed  
  > “Woe to you, scribes and Pharisees, hypocrites! For you clean the outside of the cup and of the plate, but inside they are full of greed and self-indulgence.

*Dissent:* DOWNGRADED from partial on review. The priestly washing and purity codes are about RITUAL purity; Wesley's proverb is about literal tidiness. That is a category shift, not a shared component, so the support is inferential rather than partial. Someone reading 'cleanliness' morally rather than hygienically could defend partial.

---

## "God works in mysterious ways"

`god-works-in-mysterious-ways` &middot; verdict: **strong** &middot; decided by `states-directly`

This one is a fair summary of a major biblical theme. Only the wording is Cowper's. Included to show the dataset does not treat 'not a verse' as 'not biblical'.

- **supports** &nbsp; `Isaiah 55:8` — 'my thoughts are not your thoughts'  
  > For my thoughts are not your thoughts, nor are your ways my ways, says the LORD.
- **supports** &nbsp; `Isaiah 55:9` — the heavens are higher than the earth, so are God's ways  
  > For as the heavens are higher than the earth, so are my ways higher than your ways and my thoughts than your thoughts.
- **supports** &nbsp; `Romans 11:33` — 'how unsearchable his judgments and how inscrutable his ways'  
  > O the depth of the riches and wisdom and knowledge of God! How unsearchable are his judgments and how inscrutable his ways!
- **supports** &nbsp; `Deuteronomy 29:29` — 'the secret things belong to the LORD our God'  
  > The secret things belong to the LORD our God, but the revealed things belong to us and to our children forever, to observe all the words of this law.
- **supports** &nbsp; `Ecclesiastes 11:5` — you do not know the work of God who makes everything  
  > Just as you do not know how the breath comes to the bones in the mother’s womb, so you do not know the work of God, who makes everything.

*Dissent:* Hard to dissent from: Isaiah 55:8-9 states the substance in as many words.

---

## "Spare the rod and spoil the child"

`spare-the-rod-spoil-the-child` &middot; verdict: **strong** &middot; decided by `states-directly`

The idea is plainly in Proverbs; only the rhyming form is Butler's. This is a misattributed QUOTE, not a misattributed belief - a distinction the lexical check alone cannot make.

- **supports** &nbsp; `Proverbs 13:24` — 'those who spare the rod hate their children'  
  > Those who spare the rod hate their children, but those who love them are diligent to discipline them.
- **supports** &nbsp; `Proverbs 22:15` — the rod of discipline drives folly out of a child  
  > Folly is bound up in the heart of a boy, but the rod of discipline drives it far away.
- **supports** &nbsp; `Proverbs 23:13` — do not withhold discipline  
  > Do not withhold discipline from your children; if you beat them with a rod, they will not die.
- **supports** &nbsp; `Proverbs 29:15` — the rod and reproof give wisdom  
  > The rod and reproof give wisdom, but a mother is disgraced by a neglected child.
- **against** &nbsp; `Ephesians 6:4` — 'do not provoke your children to anger' tempers the Proverbs material  
  > And, fathers, do not provoke your children to anger, but bring them up in the discipline and instruction of the Lord.
  <br>↳ *Reply:* Usually harmonised as setting a limit on the manner of discipline rather than forbidding it, so the Proverbs material stands with a caution attached.

*Dissent:* Dissent would come from those reading shevet as a shepherd's staff and the sayings as metaphors for guidance; that changes what the verses commend, not whether they commend it.

---

## "Hate the sin, love the sinner"

`hate-the-sin-love-the-sinner` &middot; verdict: **partial** &middot; decided by `component-split`

Both halves have support, but holding them together as a single policy is the later synthesis.

**Supported:** Both halves separately - Romans 12:9 for hating evil, John 8:11 for not condemning the person.  
**Imported or disputed:** Holding them together as a single pastoral policy, which is a later synthesis and is what the phrase actually asserts.

- **supports** &nbsp; `Romans 12:9` — 'hate what is evil, hold fast to what is good'  
  > Let love be genuine; hate what is evil, hold fast to what is good;
- **supports** &nbsp; `Psalms 97:10` — 'the LORD loves those who hate evil'  
  > The LORD loves those who hate evil; he guards the lives of his faithful; he rescues them from the hand of the wicked.
- **supports** &nbsp; `John 8:11` — 'neither do I condemn you. Go your way, and from now on do not sin again'  
  > She said, “No one, sir.” And Jesus said, “Neither do I condemn you. Go your way, and from now on do not sin again.”
- **against** &nbsp; `Matthew 7:3` — the log in your own eye complicates any sorting of sinners from sins  
  > Why do you see the speck in your neighbor’s eye, but do not notice the log in your own eye?
- **supports** &nbsp; `Jude 1:22` — 'have mercy on some who are wavering'  
  > And have mercy on some who are wavering;

*Dissent:* Critics of the phrase argue the synthesis is incoherent in practice; that is an ethical objection, not a textual one, and does not affect the grading.

---

## "This too shall pass"

`this-too-shall-pass` &middot; verdict: **partial** &middot; decided by `component-split`

The transience of affliction is a real biblical theme; the fatalistic framing of the saying is not quite the biblical one, which contrasts the temporary with the eternal rather than counselling endurance alone.

**Supported:** That affliction is temporary - 2 Corinthians 4:17, Psalm 30:5, 1 Peter 1:6.  
**Imported or disputed:** The fatalistic framing. The biblical texts contrast the temporary with the ETERNAL; the saying counsels endurance with no such horizon.

- **supports** &nbsp; `2 Corinthians 4:17` — 'this slight momentary affliction is preparing us for an eternal weight of glory'  
  > For this slight momentary affliction is preparing us for an eternal weight of glory beyond all measure,
- **supports** &nbsp; `Psalms 30:5` — 'weeping may linger for the night, but joy comes with the morning'  
  > For his anger is but for a moment; his favor is for a lifetime. Weeping may linger for the night, but joy comes with the morning.
- **supports** &nbsp; `Ecclesiastes 3:1` — a time for everything - the nearest thing to the saying's cadence  
  > For everything there is a season, and a time for every matter under heaven:
- **supports** &nbsp; `1 Peter 1:6` — 'for a little while you have had to suffer various trials'  
  > In this you rejoice, even if now for a little while you have had to suffer various trials,

*Dissent:* A reader who hears the saying as simple consolation rather than fatalism could defend `strong`.

---

## Three wise men, named, and kings

`three-wise-men` &middot; verdict: **weak** &middot; decided by `inferential`

The number comes from counting the gifts. The kingly status has a genuine intertext, which is worth naming rather than dismissing: Psalm 72 and Isaiah 60 describe kings bringing gifts, and the tradition read them into Matthew.

- **supports** &nbsp; `Matthew 2:11` — three gifts named - gold, frankincense, myrrh - hence the number  
  > On entering the house, they saw the child with Mary his mother; and they knelt down and paid him homage. Then, opening their treasure chests, they offered him gifts of gold, frankincense, and myrrh.
- **supports** &nbsp; `Psalms 72:10` — kings of Sheba and Seba bring gifts; a real source for 'kings'  
  > May the kings of Tarshish and of the isles render him tribute, may the kings of Sheba and Seba bring gifts.
- **supports** &nbsp; `Isaiah 60:3` — 'nations shall come to your light, and kings to the brightness of your dawn'  
  > Nations shall come to your light, and kings to the brightness of your dawn.
- **against** &nbsp; `Matthew 2:1` — Matthew says magoi, astrologers or Persian priests, not kings  
  > In the time of King Herod, after Jesus was born in Bethlehem of Judea, wise men from the East came to Jerusalem,
  <br>↳ *Reply:* The kingly reading is defended typologically rather than lexically - Psalm 72 and Isaiah 60 are taken as the prophecy Matthew's magi fulfil, which makes 'kings' an interpretation rather than a translation.
- **against** &nbsp; `Matthew 2:16` — Herod kills boys up to two years old, implying the visit was not at the birth  
  > When Herod saw that he had been tricked by the wise men, he was infuriated, and he sent and killed all the children in and around Bethlehem who were two years old or under, according to the time that he had learned from the wise men.

*Dissent:* The kingly element has a real intertext in Psalm 72 and Isaiah 60, which some would count as `partial`. Graded weak because those texts are read INTO Matthew rather than cited by him.

---

## The forbidden fruit was an apple

`forbidden-fruit-was-an-apple` &middot; verdict: **none** &middot; decided by `silent`

No passage anywhere names or hints at a species. This is one of the few cases where the concept audit comes back genuinely empty.

- **against** &nbsp; `Genesis 3:6` — the text says only 'fruit'; the species is simply not a question the narrative raises  
  > So when the woman saw that the tree was good for food, and that it was a delight to the eyes, and that the tree was to be desired to make one wise, she took of its fruit and ate; and she also gave some to her husband, who was with her, and he ate.

*Dissent:* No dissent available: the species is not a question the narrative raises.

---

## Jonah was swallowed by a whale

`jonah-and-the-whale` &middot; verdict: **partial** &middot; decided by `component-split`

A whale is a possible member of the category the text names. The belief is over-specification rather than error.

**Supported:** Swallowed by a large sea creature - the text says exactly this.  
**Imported or disputed:** That the creature was specifically a whale. The belief over-specifies a category the text leaves open.

- **supports** &nbsp; `Jonah 1:17` — 'a large fish' - ancient taxonomy did not separate whales from big fish  
  > But the LORD provided a large fish to swallow up Jonah; and Jonah was in the belly of the fish three days and three nights.
- **supports** &nbsp; `Matthew 12:40` — ketos, sea monster, is a category that includes whales  
  > For just as Jonah was three days and three nights in the belly of the sea monster, so for three days and three nights the Son of Man will be in the heart of the earth.

*Dissent:* Given that ancient taxonomy did not separate whales from large fish, some would call this no error at all and grade it `strong`.

---

## The serpent in Eden was Satan

`serpent-in-eden-is-satan` &middot; verdict: **strong** &middot; decided by `states-directly`

This is the case the lexical check most misleads on. Genesis never says it - but Revelation says it twice, explicitly, using the word 'ancient serpent'. The belief is thoroughly biblical; it is just not in Genesis.

- **supports** &nbsp; `Revelation 12:9` — 'the great dragon... that ancient serpent, who is called the Devil and Satan'  
  > The great dragon was thrown down, that ancient serpent, who is called the Devil and Satan, the deceiver of the whole world—he was thrown down to the earth, and his angels were thrown down with him.
- **supports** &nbsp; `Revelation 20:2` — the same identification repeated  
  > He seized the dragon, that ancient serpent, who is the Devil and Satan, and bound him for a thousand years,
- **supports** &nbsp; `Romans 16:20` — 'the God of peace will shortly crush Satan under your feet' echoes Genesis 3:15  
  > The God of peace will shortly crush Satan under your feet. The grace of our Lord Jesus Christ be with you.
- **against** &nbsp; `Genesis 3:1` — Genesis introduces the serpent as one of the wild animals God had made  
  > Now the serpent was more crafty than any other wild animal that the LORD God had made. He said to the woman, “Did God say, ‘You shall not eat from any tree in the garden’?”

*Dissent:* Dissent is possible on canonical grounds - Revelation is a different book written centuries later, so a reader restricting themselves to Genesis would grade `none`. Graded strong because the dataset asks whether the BIBLE supplies the idea, not whether Genesis does.

---

## Mary Magdalene was a prostitute

`mary-magdalene-was-a-prostitute` &middot; verdict: **none** &middot; decided by `silent`

Nothing connects them. The conflation requires reading Luke 7 onto Luke 8 against the text's own separation of the two scenes.

- **against** &nbsp; `Luke 8:2` — she is introduced by name as freed from seven demons, among the women funding the ministry  
  > as well as some women who had been cured of evil spirits and infirmities: Mary, called Magdalene, from whom seven demons had gone out,
- **against** &nbsp; `Luke 7:37` — the anointing woman is unnamed and in a different episode  
  > And a woman in the city, who was a sinner, having learned that he was eating in the Pharisee’s house, brought an alabaster jar of ointment.
- **against** &nbsp; `John 20:16` — she is the first witness of the resurrection, the opposite of a marginal figure  
  > Jesus said to her, “Mary!” She turned and said to him in Hebrew, “Rabbouni!” (which means Teacher).

*Dissent:* No dissent: the two women are in different chapters and the text never links them.

---

## The innkeeper turned them away to a stable

`nativity-stable-and-innkeeper` &middot; verdict: **weak** &middot; decided by `inferential`

'No room' plus a manger does imply displacement, so the scene is not invented from nothing. The innkeeper, the stable and the animals are all supplied.

- **supports** &nbsp; `Luke 2:7` — no room in the kataluma, and a manger, which does imply animal quarters nearby  
  > And she gave birth to her firstborn son and wrapped him in bands of cloth, and laid him in a manger, because there was no place for them in the inn.
- **supports** &nbsp; `Isaiah 1:3` — 'the ox knows its owner, and the donkey its master's crib' - where the animals come from  
  > The ox knows its owner, and the donkey its master’s crib; but Israel does not know, my people do not understand.
- **against** &nbsp; `Luke 22:11` — kataluma is the guest room of the Last Supper, not an inn  
  > and say to the owner of the house, ‘The teacher asks you, “Where is the guest room, where I may eat the Passover with my disciples?”’
- **against** &nbsp; `Luke 10:34` — Luke uses a different word, pandocheion, when he means a commercial inn  
  > He went to him and bandaged his wounds, having poured oil and wine on them. Then he put him on his own animal, brought him to an inn, and took care of him.

*Dissent:* 'No room' plus a manger does imply displacement, which some would count as partial support for the scene if not for the innkeeper.

---

## Jesus was 33 when he died

`jesus-was-33` &middot; verdict: **weak** &middot; decided by `inferential`

A real inference from two approximate data points, presented with false precision.

- **supports** &nbsp; `Luke 3:23` — 'about thirty years old' when he began  
  > Jesus was about thirty years old when he began his work. He was the son (as was thought) of Joseph son of Heli,
- **supports** &nbsp; `John 2:13` — the first of John's Passovers  
  > The Passover of the Jews was near, and Jesus went up to Jerusalem.
- **supports** &nbsp; `John 6:4` — a second Passover  
  > Now the Passover, the festival of the Jews, was near.
- **supports** &nbsp; `John 11:55` — a third, suggesting a ministry of roughly three years  
  > Now the Passover of the Jews was near, and many went up from the country to Jerusalem before the Passover to purify themselves.

*Dissent:* The inference is sound; only its precision is not. A reader treating 'about thirty' plus three Passovers as adequate would grade `partial`.

---

## Saint Peter admits people at the pearly gates

`peter-at-the-pearly-gates` &middot; verdict: **weak** &middot; decided by `inferential`

Both halves exist separately; the scene is the welding.

- **supports** &nbsp; `Matthew 16:19` — Peter is given 'the keys of the kingdom of heaven'  
  > I will give you the keys of the kingdom of heaven, and whatever you bind on earth will be bound in heaven, and whatever you loose on earth will be loosed in heaven.”
- **supports** &nbsp; `Revelation 21:21` — the twelve gates are twelve pearls  
  > And the twelve gates are twelve pearls, each of the gates is a single pearl, and the street of the city is pure gold, transparent as glass.
- **against** &nbsp; `Revelation 20:12` — judgement is by books opened before the throne, with no gatekeeper named  
  > And I saw the dead, great and small, standing before the throne, and books were opened. Also another book was opened, the book of life. And the dead were judged according to their works, as recorded in the books.

*Dissent:* The keys of Matthew 16:19 are real, so the figure of Peter holding keys is not invented - only the gatekeeping scene is.

---

## Satan rules hell and torments the damned

`satan-rules-hell` &middot; verdict: **contradicted** &middot; decided by `asserts-otherwise`

The ruler language is biblical but attached to the wrong domain: Satan rules THIS WORLD in the New Testament and is a prisoner of the lake of fire, not its warden.

- **supports** &nbsp; `John 12:31` — 'the ruler of this world will be driven out' - the source of the ruler idea  
  > Now is the judgment of this world; now the ruler of this world will be driven out.
- **supports** &nbsp; `2 Corinthians 4:4` — 'the god of this world has blinded the minds of unbelievers'  
  > In their case the god of this world has blinded the minds of the unbelievers, to keep them from seeing the light of the gospel of the glory of Christ, who is the image of God.
- **against** &nbsp; `Revelation 20:10` — the devil is thrown INTO the lake of fire and tormented there  
  > And the devil who had deceived them was thrown into the lake of fire and sulfur, where the beast and the false prophet were, and they will be tormented day and night forever and ever.
  <br>↳ *Reply:* No real reply is offered here - popular belief and the text simply diverge, which is why this is the dataset's only 'contradicted' verdict.
- **against** &nbsp; `Matthew 25:41` — the fire is 'prepared for the devil and his angels' - made for him, not by him  
  > Then he will say to those at his left hand, ‘You that are accursed, depart from me into the eternal fire prepared for the devil and his angels;

*Dissent:* The only verdict in the dataset with no reply recorded. Revelation 20:10 addresses the point directly and reverses it.

---

## Purgatory

`purgatory` &middot; verdict: **partial** &middot; decided by `component-split`

Genuine candidate texts exist and are contested rather than absent. This is not a doctrine conjured from nothing.

**Supported:** A post-mortem process involving fire and incompleteness - 1 Corinthians 3:15, Matthew 12:32 are real candidate texts.  
**Imported or disputed:** Purgatory as a distinct PLACE with a defined role in the economy of salvation. Le Goff dates the place-concept to the 12th century.

- **supports** &nbsp; `1 Corinthians 3:15` — 'saved, but only as through fire'  
  > If the work is burned up, the builder will suffer loss; the builder will be saved, but only as through fire.
- **supports** &nbsp; `Matthew 12:32` — 'neither in this age nor in the age to come' implies some post-mortem resolution  
  > Whoever speaks a word against the Son of Man will be forgiven, but whoever speaks against the Holy Spirit will not be forgiven, either in this age or in the age to come.
- **supports** &nbsp; `Hebrews 12:29` — 'our God is a consuming fire'  
  > for indeed our God is a consuming fire.
- **against** &nbsp; `Hebrews 9:27` — 'it is appointed for mortals to die once, and after that the judgment'  
  > And just as it is appointed for mortals to die once, and after that the judgment,
  <br>↳ *Reply:* Catholic theology reads the judgement as immediate and purgatory as the working-out of a verdict already given, not a second trial - so a single death and judgement is not in tension with it.
- **against** &nbsp; `Luke 23:43` — 'today you will be with me in Paradise' - no intermediate purification  
  > He replied, “Truly I tell you, today you will be with me in Paradise.”
  <br>↳ *Reply:* Read as a particular case rather than a rule: the thief is granted immediate entry by a direct promise of Christ, which says nothing about the ordinary path.

*Dissent:* Catholic theology would reject the framing entirely: it does not claim purgatory is described in scripture, so 'partial support' is not a deficiency on its own terms.

---

## The word "Trinity"

`the-word-trinity` &middot; verdict: **strong** &middot; decided by `converges`

Substantial material supports the doctrine. Only the vocabulary is post-biblical, which is exactly what the case says.

- **supports** &nbsp; `Matthew 28:19` — baptising in the name of the Father, Son and Holy Spirit  
  > Go therefore and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit,
- **supports** &nbsp; `2 Corinthians 13:13` — grace, love and communion attributed to the three together  
  > The grace of the Lord Jesus Christ, the love of God, and the communion of the Holy Spirit be with all of you.
- **supports** &nbsp; `John 1:1` — 'the Word was God'  
  > In the beginning was the Word, and the Word was with God, and the Word was God.
- **supports** &nbsp; `John 10:30` — 'the Father and I are one'  
  > The Father and I are one.”
- **supports** &nbsp; `John 14:16` — the Father sends another Advocate  
  > And I will ask the Father, and he will give you another Advocate, to be with you forever.

*Dissent:* Unitarian and some Jehovah's Witness readings would grade `weak`, holding that the passages are being harmonised rather than converging. That is the substance of a very old argument.

---

## The Immaculate Conception

`immaculate-conception` &middot; verdict: **weak** &middot; decided by `inferential`

The supporting texts are thin and two of them are translation artefacts, which is what makes this the dataset's strongest link to the mistranslations work.

- **supports** &nbsp; `Luke 1:28` — kecharitomene, 'favoured one', rendered 'full of grace' in Latin  
  > And he came to her and said, “Greetings, favored one! The Lord is with you.”
- **supports** &nbsp; `Luke 1:42` — 'blessed are you among women'  
  > and exclaimed with a loud cry, “Blessed are you among women, and blessed is the fruit of your womb.
- **against** &nbsp; `Romans 3:23` — The standard Protestant objection: if all have sinned, Mary is included. Note the limits of it - the verb hemarton (G264) is AORIST, 'all sinned', which is about committed acts, while the Immaculate Conception is about the inherited condition at conception. The two are different categories.  
  > since all have sinned and fall short of the glory of God;
  <br>↳ *Reply:* Catholic theology answers on two fronts. First, Paul's 'all' here is arguing that neither Jew nor Gentile is exempt by ethnicity, not running a census - and scripture already excepts one person from it at Hebrews 4:15 and 2 Corinthians 5:21, so 'all' is not a rigid universal. Second, Mary is not held to be exempt from redemption but redeemed differently: Ineffabilis Deus (1854) calls it preservative rather than liberative redemption - kept from the pit rather than pulled out of it. On that account she still needed a saviour and had one.
- **against** &nbsp; `Luke 1:47` — The stronger of the two objections: Mary calls God 'my Saviour', which several Fathers read as implying she needed saving like anyone else.  
  > and my spirit rejoices in God my Savior,
  <br>↳ *Reply:* The preservative-redemption answer applies here too, and Catholic theology treats this verse as consistent with the dogma rather than awkward for it - being preserved from sin is itself an act of a saviour, so the Magnificat is exactly what a preserved person would sing.

*Dissent:* Catholic theology would again reject the framing: the dogma is held on the authority of tradition, and Luke 1:28 is illustrative rather than probative.

---

## The seven deadly sins

`seven-deadly-sins` &middot; verdict: **partial** &middot; decided by `component-split`

Vice lists are a real biblical form, and one of them even has seven items - the contents just do not match.

**Supported:** The FORM - biblical vice lists exist, and Proverbs 6:16-19 is even a list of seven.  
**Imported or disputed:** The CONTENTS. Not one of the traditional seven matches Proverbs' list, and sloth (acedia) has no biblical vocabulary behind it at all.

- **supports** &nbsp; `Proverbs 6:16` — 'six things the LORD hates, seven that are an abomination'  
  > There are six things that the LORD hates, seven that are an abomination to him:
- **supports** &nbsp; `Proverbs 6:17` — the list itself: haughty eyes, a lying tongue, hands that shed innocent blood  
  > haughty eyes, a lying tongue, and hands that shed innocent blood,
- **supports** &nbsp; `Galatians 5:19` — the works of the flesh, a vice list of fifteen  
  > Now the works of the flesh are obvious: fornication, impurity, licentiousness,
- **supports** &nbsp; `Colossians 3:5` — another list: fornication, impurity, passion, evil desire, greed  
  > Put to death, therefore, whatever in you is earthly: fornication, impurity, passion, evil desire, and greed (which is idolatry).

*Dissent:* Someone treating the list as a convenient summary of Galatians 5:19-21 rather than a distinct claim could grade `strong`.

---

## Christmas on 25 December

`christmas-december-25` &middot; verdict: **none** &middot; decided by `silent`

No passage bears on the date. The one datum sometimes cited points, weakly, away from midwinter.

- **against** &nbsp; `Luke 2:8` — shepherds living in the fields at night, which some read as suggesting a warmer season  
  > In that region there were shepherds living in the fields, keeping watch over their flock by night.
  <br>↳ *Reply:* The shepherd argument is weak in both directions: flocks near Bethlehem could be pastured year-round in a mild climate, and Luke gives no month. Defenders of the date rest on the computation theory - a conception reckoned to 25 March, nine months earlier - rather than on anything in the nativity scene itself.

*Dissent:* Luke 2:8 is sometimes offered as weak counter-evidence for the season, which would make this `contradicted` rather than `none`. Graded none because shepherds in fields is too thin to establish a month.

---

## The Rapture as a distinct event

`the-rapture` &middot; verdict: **partial** &middot; decided by `component-split`

The catching-up is plainly described. What is post-biblical is the pre-tribulational, secret, two-stage scheme built around it.

**Supported:** A gathering of believers to meet Christ - 1 Thessalonians 4:16-17, 1 Corinthians 15:52 state this plainly.  
**Imported or disputed:** The pre-tribulational, secret, two-stage structure. Nothing in the passages separates the gathering from the public return.

- **supports** &nbsp; `1 Thessalonians 4:16` — the Lord descends with a cry of command and a trumpet  
  > For the Lord himself, with a cry of command, with the archangel’s call and with the sound of God’s trumpet, will descend from heaven, and the dead in Christ will rise first.
- **supports** &nbsp; `1 Thessalonians 4:17` — 'we will be caught up in the clouds to meet the Lord in the air'  
  > Then we who are alive, who are left, will be caught up in the clouds together with them to meet the Lord in the air; and so we will be with the Lord forever.
- **supports** &nbsp; `1 Corinthians 15:52` — 'we will be changed, in a moment, in the twinkling of an eye'  
  > in a moment, in the twinkling of an eye, at the last trumpet. For the trumpet will sound, and the dead will be raised imperishable, and we will be changed.
- **supports** &nbsp; `Matthew 24:40` — 'one will be taken and one will be left'  
  > Then two will be in the field; one will be taken and one will be left.
- **against** &nbsp; `1 Thessalonians 4:16` — a shout and a trumpet are not a secret removal  
  > For the Lord himself, with a cry of command, with the archangel’s call and with the sound of God’s trumpet, will descend from heaven, and the dead in Christ will rise first.
  <br>↳ *Reply:* Dispensationalist readings hold the shout and trumpet are directed at those being gathered rather than announced to the world. Critics regard this as strained, which is part of why the case is graded partial rather than strong.
- **against** &nbsp; `Matthew 24:29` — Matthew places the gathering AFTER the tribulation, not before  
  > “Immediately after the suffering of those days the sun will be darkened, and the moon will not give its light; the stars will fall from heaven, and the powers of heaven will be shaken.
  <br>↳ *Reply:* Dispensationalist readings hold that Matthew 24 concerns Christ's later appearing in glory while 1 Thessalonians 4 concerns a prior gathering, so the two describe different events rather than one contradictory sequence.

*Dissent:* Dispensationalist readers would grade `strong`, holding that the two-stage structure follows from harmonising these texts with Matthew 24 and Daniel.

---

## Inherited guilt from Adam

`original-sin-inherited-guilt` &middot; verdict: **partial** &middot; decided by `component-split`

Substantial material ties humanity's condition to Adam. The disputed specification is inherited GUILT as against inherited mortality, and one text cuts directly against it.

**Supported:** That humanity's condition is bound up with Adam's - Romans 5:12-19 is explicit.  
**Imported or disputed:** That what is inherited is GUILT rather than mortality and a corrupted nature. Ezekiel 18:20 cuts against, and the Eastern churches never drew the conclusion.

- **supports** &nbsp; `Romans 5:12` — death spread to all because all sinned  
  > Therefore, just as sin came into the world through one man, and death came through sin, and so death spread to all because all have sinned—
- **supports** &nbsp; `Romans 5:19` — 'by the one man's disobedience the many were made sinners'  
  > For just as by the one man’s disobedience the many were made sinners, so by the one man’s obedience the many will be made righteous.
- **supports** &nbsp; `Psalms 51:5` — 'I was born guilty, a sinner when my mother conceived me'  
  > Indeed, I was born guilty, a sinner when my mother conceived me.
- **supports** &nbsp; `Ephesians 2:3` — 'we were by nature children of wrath'  
  > All of us once lived among them in the passions of our flesh, following the desires of flesh and senses, and we were by nature children of wrath, like everyone else.
- **against** &nbsp; `Ezekiel 18:20` — 'A child shall not suffer for the iniquity of a parent'  
  > The person who sins shall die. A child shall not suffer for the iniquity of a parent, nor a parent suffer for the iniquity of a child; the righteousness of the righteous shall be his own, and the wickedness of the wicked shall be his own.
  <br>↳ *Reply:* Augustinian theology distinguishes the guilt inherited in Adam, which is a shared condition of nature, from the personal guilt of individual acts that Ezekiel is refusing to transfer between generations.

*Dissent:* Augustinian and Reformed readers would grade this `strong`; Orthodox readers closer to `weak`. The split is itself the finding.

---

## Angels are winged people who play harps on clouds

`angels-are-winged-humans-with-harps` &middot; verdict: **partial** &middot; decided by `component-split`

Wings are genuinely biblical for some heavenly beings; the humanlike composite and the idea that the dead become angels are not.

**Supported:** Wings on heavenly beings - Isaiah 6:2, Ezekiel 1:6, and Gabriel in 'swift flight' at Daniel 9:21.  
**Imported or disputed:** The humanlike composite with haloes and harps, and the idea that the dead become angels. Angels who meet people in scripture are taken for ordinary men, and Revelation 5:8 gives the harps to the elders.

- **supports** &nbsp; `Isaiah 6:2` — seraphim with six wings  
  > Seraphs were in attendance above him; each had six wings: with two they covered their faces, and with two they covered their feet, and with two they flew.
- **supports** &nbsp; `Ezekiel 1:6` — living creatures with four faces and four wings  
  > Each had four faces, and each of them had four wings.
- **supports** &nbsp; `Daniel 9:21` — Gabriel comes 'in swift flight'  
  > while I was speaking in prayer, the man Gabriel, whom I had seen before in a vision, came to me in swift flight at the time of the evening sacrifice.
- **supports** &nbsp; `Revelation 14:6` — an angel flying in midheaven  
  > Then I saw another angel flying in midheaven, with an eternal gospel to proclaim to those who live on the earth—to every nation and tribe and language and people.
- **against** &nbsp; `Genesis 18:2` — the visitors appear simply as three men  
  > He looked up and saw three men standing near him. When he saw them, he ran from the tent entrance to meet them, and bowed down to the ground.
- **against** &nbsp; `Luke 24:4` — 'two men in dazzling clothes' at the tomb  
  > While they were perplexed about this, suddenly two men in dazzling clothes stood beside them.
- **against** &nbsp; `Revelation 5:8` — it is the elders and living creatures who hold harps, not angels  
  > When he had taken the scroll, the four living creatures and the twenty-four elders fell before the Lamb, each holding a harp and golden bowls full of incense, which are the prayers of the saints.

*Dissent:* A reader treating seraphim and angels as one category would grade `strong` on the wings alone.

---

## Hell as a fiery underworld of graded punishments

`hell-as-dantes-underworld` &middot; verdict: **partial** &middot; decided by `component-split`

Fire, torment and exclusion are all described. The architecture - circles, matched punishments, demon torturers - is what Dante supplies.

**Supported:** Fire, torment and exclusion - Matthew 25:41, Mark 9:48, Luke 16:23, Revelation 20:14.  
**Imported or disputed:** The architecture: circles, punishments matched to sins, demons as staff. Dante supplies all of it.

- **supports** &nbsp; `Matthew 25:41` — 'eternal fire prepared for the devil and his angels'  
  > Then he will say to those at his left hand, ‘You that are accursed, depart from me into the eternal fire prepared for the devil and his angels;
- **supports** &nbsp; `Mark 9:48` — 'where their worm never dies, and the fire is never quenched'  
  > where their worm never dies, and the fire is never quenched.
- **supports** &nbsp; `Luke 16:23` — torment, thirst and a fixed chasm in the Hades parable  
  > In Hades, where he was being tormented, he looked up and saw Abraham far away with Lazarus by his side.
- **supports** &nbsp; `Revelation 20:14` — the lake of fire  
  > Then Death and Hades were thrown into the lake of fire. This is the second death, the lake of fire;
- **against** &nbsp; `Revelation 20:10` — demons are tormented in it rather than staffing it  
  > And the devil who had deceived them was thrown into the lake of fire and sulfur, where the beast and the false prophet were, and they will be tormented day and night forever and ever.
  <br>↳ *Reply:* The architecture is acknowledged as imaginative elaboration by most theologians; it is defended as pedagogy rather than description.

*Dissent:* Universalist and annihilationist readers would grade the supported component lower, since they read the fire language as figurative or terminal rather than as eternal conscious torment.

---

