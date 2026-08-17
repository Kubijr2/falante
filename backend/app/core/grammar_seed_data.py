"""
Seed data for grammar_topics. Kept as plain Python data (not hardcoded in the
migration file) so it's easy to review, edit, or extend with new topics later
without touching migration logic.
"""

GRAMMAR_TOPICS = [
    {
        "slug": "ser-vs-estar",
        "title": "Ser vs. Estar",
        "category": "Verbs",
        "summary": "Two verbs that both mean \"to be\" — but pick the wrong one and you change the meaning.",
        "content": """## The core distinction

Portuguese has two verbs for "to be," and choosing between them is one of the
first real hurdles for English speakers.

- **Ser** — permanent or defining characteristics: identity, origin, profession, inherent qualities.
- **Estar** — temporary states, conditions, location, and how something is *right now*.

## Ser

Use **ser** for things that define what something *is*:

- **Identity:** *Eu sou o Carlos.* (I am Carlos.)
- **Origin/nationality:** *Ela é do Brasil.* (She's from Brazil.)
- **Profession:** *Nós somos estudantes.* (We are students.)
- **Inherent traits:** *O café é forte.* (The coffee is strong. — as a general quality)
- **Time and dates:** *São três horas.* (It's three o'clock.)

## Estar

Use **estar** for things that could change, especially states and locations:

- **Location:** *O livro está na mesa.* (The book is on the table.)
- **Temporary condition:** *Eu estou cansado.* (I am tired.)
- **Ongoing action:** *Ela está estudando.* (She is studying.)
- **Weather:** *Está chovendo.* (It's raining.)

## The trap: adjectives that change meaning

Some adjectives mean something different depending on which verb you use — this
is where most learners get tripped up:

| Adjective | with Ser | with Estar |
|---|---|---|
| chato | *Ele é chato.* — He's boring (personality) | *Ele está chato.* — He's being annoying (right now) |
| bonito | *Ela é bonita.* — She's pretty (in general) | *Ela está bonita.* — She looks pretty (today, in that outfit) |
| pronto | *Ele é pronto.* — He's a quick/sharp person | *Ele está pronto.* — He's ready (right now) |

## Quick test

Ask yourself: *is this describing what something fundamentally is, or the state
it happens to be in right now?* Identity, origin, and defining traits → **ser**.
Location, temporary condition, in-progress action → **estar**.
""",
    },
    {
        "slug": "por-vs-para",
        "title": "Por vs. Para",
        "category": "Prepositions",
        "summary": "Both often translate to \"for\" in English — but they answer different questions.",
        "content": """## The core distinction

English speakers often reach for "for" and get stuck, because Portuguese
splits that meaning across two prepositions that answer different questions.

- **Para** answers **"for what purpose / to where / for whom (destination)"** — direction, goal, deadline, recipient.
- **Por** answers **"because of what / through what / in exchange for what"** — cause, means, exchange, duration.

## Para

- **Destination:** *Vou para São Paulo.* (I'm going to São Paulo.)
- **Purpose/goal:** *Este livro é para aprender português.* (This book is for learning Portuguese.)
- **Recipient:** *Comprei um presente para você.* (I bought a gift for you.)
- **Deadline:** *Preciso terminar isso para sexta-feira.* (I need to finish this by Friday.)
- **Opinion:** *Para mim, isso é fácil.* (For me / in my opinion, this is easy.)

## Por

- **Cause/reason:** *Ele fez isso por amor.* (He did it out of/because of love.)
- **Through/via/along:** *Andamos pela praia.* (We walked along the beach.)
- **Exchange:** *Paguei vinte reais por esse livro.* (I paid twenty reais for this book.)
- **Duration:** *Estudei por duas horas.* (I studied for two hours.)
- **Means:** *Mandei por e-mail.* (I sent it by email.)
- **"On behalf of":** *Falei por ela.* (I spoke on her behalf / for her.)

## A useful mental shortcut

If you can substitute "in order to," "destined for," or "by [a deadline]" —
that's **para**. If you can substitute "because of," "through," "in exchange
for," or "for a duration of" — that's **por**.

## Common trap

*Obrigado por* vs *presente para*: "Thanks **for** the gift" uses **por**
(you're thanking someone *because of* something they did), but "a gift **for**
you" uses **para** (the gift's destination/recipient is you).

*Obrigado pelo presente.* — Thanks for the gift.
*O presente é para você.* — The gift is for you.
""",
    },
    {
        "slug": "object-pronouns",
        "title": "Object Pronouns",
        "category": "Pronouns",
        "summary": "Direct and indirect object pronouns, and where they actually go in a sentence.",
        "content": """## Direct vs. indirect

A **direct object** receives the action directly (*I see her*). An
**indirect object** is who/what the action is done *to* or *for* (*I gave
her the book* — "her" is indirect, "the book" is direct).

### Direct object pronouns

| Person | Pronoun | Example |
|---|---|---|
| me | me | *Ele me viu.* (He saw me.) |
| you (informal) | te | *Eu te vi.* (I saw you.) |
| him/it | o | *Eu o vi.* (I saw him.) |
| her/it | a | *Eu a vi.* (I saw her.) |
| us | nos | *Ela nos viu.* (She saw us.) |
| them (m/f) | os / as | *Eu os vi.* (I saw them.) |

### Indirect object pronouns

| Person | Pronoun | Example |
|---|---|---|
| to me | me | *Ele me deu o livro.* (He gave me the book.) |
| to you | te | *Eu te disse a verdade.* (I told you the truth.) |
| to him/her/it | lhe | *Eu lhe disse.* (I told him/her.) |
| to us | nos | *Ela nos escreveu.* (She wrote to us.) |
| to them | lhes | *Eu lhes expliquei.* (I explained to them.) |

Notice **me**, **te**, and **nos** are the same for both direct and indirect —
only the third-person forms differ (o/a/os/as vs. lhe/lhes).

## Placement: this is the part that trips people up

In everyday spoken Brazilian Portuguese, object pronouns almost always go
**before** the verb (this is called *próclise*):

*Eu te amo.* (I love you.) — not *Eu amo-te*, which is standard in
European Portuguese but sounds formal/unnatural in Brazil.

Pronouns move **after** the verb, attached with a hyphen, in more formal or
written contexts, especially after a positive command:

*Diga-me a verdade.* (Tell me the truth.)

With negatives, questions, and certain conjunctions, the pronoun goes
**before** the verb:

*Não me diga isso.* (Don't tell me that.)
*Quem te falou isso?* (Who told you that?)

## The practical rule for learners

In conversational Brazilian Portuguese, defaulting to **pronoun before the
verb** will sound natural in the overwhelming majority of everyday
situations. You can refine the formal placement rules later — get the
pronoun choice right first, worry about placement nuance second.
""",
    },
    {
        "slug": "past-tenses",
        "title": "Past Tenses: Pretérito Perfeito vs. Imperfeito",
        "category": "Tenses",
        "summary": "Two past tenses, one big question: was it a completed event, or an ongoing/background state?",
        "content": """## The core distinction

Portuguese (like Spanish and French) splits the simple past into two tenses
that English doesn't distinguish grammatically — English relies on context,
Portuguese builds the distinction into the verb form.

- **Pretérito Perfeito** — a completed action, a specific event that happened and ended.
- **Pretérito Imperfeito** — an ongoing, repeated, or background state in the past; "used to," "was ...ing."

## Pretérito Perfeito: the completed event

Use this for something that happened at a specific point and is *done*:

*Eu comi pizza ontem.* (I ate pizza yesterday. — one specific occasion)
*Ela viajou para o Brasil em 2023.* (She traveled to Brazil in 2023.)
*Nós chegamos às oito.* (We arrived at eight.)

Regular -ar verbs (falar): falei, falou, falamos, falaram
Regular -er verbs (comer): comi, comeu, comemos, comeram
Regular -ir verbs (partir): parti, partiu, partimos, partiram

## Pretérito Imperfeito: the ongoing/habitual background

Use this for repeated habits, ongoing states, descriptions, or "was
happening" when something else interrupted it:

*Eu comia pizza todo domingo.* (I used to eat pizza every Sunday. — a habit)
*Ela morava no Rio quando era criança.* (She lived in Rio when she was a child. — an ongoing state)
*Eu estava dormindo quando o telefone tocou.* (I was sleeping when the phone rang. — background action interrupted by a completed one)

Regular -ar verbs (falar): falava, falava, falávamos, falavam
Regular -er/-ir verbs (comer/partir): comia, comia, comíamos, comiam

## Putting them together

The two tenses are often used *in the same sentence*, and this is where the
distinction becomes intuitive: the imperfeito sets the scene, the perfeito
is the event that happens inside it.

*Eu estava assistindo TV quando você ligou.*
(I was watching TV [ongoing background] when you called [a specific completed event].)

## Quick test

Ask: is this a specific event with a clear beginning and end, or a repeated
habit / ongoing state / scene-setting description? Specific & completed →
**perfeito**. Repeated, ongoing, or descriptive → **imperfeito**.
""",
    },
    {
        "slug": "subjunctive",
        "title": "The Subjunctive Mood (Basics)",
        "category": "Mood",
        "summary": "The mood for doubt, desire, and hypotheticals — triggered by specific phrases, not tenses.",
        "content": """## What the subjunctive actually is

Every other verb form you've learned so far is the **indicative** mood —
used for stating facts. The **subjunctive** is a different mood entirely,
used for things that are *not* stated as certain facts: wishes, doubts,
emotions, hypotheticals, and requests.

English has a faint trace of this ("I suggest that he **be** here," not
"is") but Portuguese uses it constantly and has a full set of forms for it.

## The trigger, not the tense

The subjunctive isn't chosen based on *when* something happens — it's
triggered by the **structure of the sentence**, almost always after **que**,
when the first clause expresses doubt, desire, emotion, or a hypothetical.

## Present subjunctive forms (regular verbs)

Take the **eu** form of the present indicative, drop the final -o, and:
-ar verbs get -e endings; -er/-ir verbs get -a endings.

falar → eu falo → que eu **fale**, que você **fale**, que nós **falemos**
comer → eu como → que eu **coma**, que você **coma**, que nós **comamos**
partir → eu parto → que eu **parta**, que você **parta**, que nós **partamos**

## Common triggers

**Desire/hope:**
*Espero que você venha à festa.* (I hope you come to the party.)

**Doubt/uncertainty:**
*Duvido que ele saiba a resposta.* (I doubt he knows the answer.)

**Emotion:**
*Fico feliz que você esteja aqui.* (I'm happy that you're here.)

**Recommendation/request:**
*Sugiro que ela estude mais.* (I suggest that she study more.)

**Impersonal expressions of necessity/possibility:**
*É importante que você chegue cedo.* (It's important that you arrive early.)

## The test: compare it to a plain statement

*Eu sei que ela vem.* (I know that she's coming.) — a fact, stated with confidence → **indicative** (vem)
*Eu duvido que ela venha.* (I doubt that she's coming.) — uncertain → **subjunctive** (venha)

Same underlying idea, different mood, because the first clause changes
whether the *que* clause is being presented as fact or not.

## Where to go from here

This covers the present subjunctive, the one you'll encounter constantly in
everyday speech. Imperfect and future subjunctive follow their own patterns
and are worth tackling once the present subjunctive trigger-words feel
automatic.
""",
    },
]
