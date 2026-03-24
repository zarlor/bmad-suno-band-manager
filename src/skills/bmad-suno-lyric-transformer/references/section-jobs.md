# Section Job Framework

> **Last validated:** March 2026. Section job definitions are songwriting craft principles, not Suno-specific — they do not require re-validation with Suno updates.

Every song section has a specific job in the emotional arc. Understanding these jobs is critical for deciding where to place lyrics and how to structure a poem-to-song transformation.

## Section Roles

| Section | Job | Emotional Function | Typical Lines |
|---------|-----|--------------------|---------------|
| **Intro** | Set the stage | Create atmosphere, establish mood before words | 0-4 (often instrumental) |
| **Verse** | Setup / Tell the story | Deliver narrative, build context, paint scenes | 4-8 |
| **Pre-Chorus** | Lift / Create tension | Transitional energy rise, prepare for payoff | 2-4 |
| **Chorus** | Payoff / Emotional anchor | Deliver the hook, the core feeling, the thing that sticks | 2-6 |
| **Bridge** | Contrast / New perspective | Break the pattern, offer a different angle, surprise | 2-6 |
| **Breakdown** | Breathe / Strip back | Reduce energy, create space, intimate moment | 2-4 |
| **Build-Up** | Escalate / Rising tension | Increasing energy leading to climax | 2-4 |
| **Outro** | Resolve / Close | Bring it home — resolution, fade, final statement | 2-6 |

## Transformation Decision Guide

When converting raw text to song structure, ask these questions:

### "Where's the hook?"
- The most emotionally resonant, imagistic, or rhythmic line(s)
- This becomes the chorus or chorus seed
- If no obvious hook exists, derive one from the poem's central image or feeling

### "Where's the turn?"
- The moment the perspective shifts, deepens, or surprises
- This becomes the bridge
- Poems without a turn may need a bridge written to provide contrast

### "What's the story arc?"
- Lines that set scenes or provide context → verses
- Lines that build tension → pre-chorus
- Lines that release/resolve → chorus or outro

### "What should repeat?"
- Repetition = emphasis = memorability
- The chorus repeats. What phrase deserves to be heard 3+ times?
- Consider also: anaphora (repeated line openings), callbacks (later sections echoing earlier phrases)

## Common Poem-to-Song Structures

### Short Poem (8-16 lines)
```
Verse 1 (first half of poem)
Chorus (derived from emotional core)
Verse 2 (second half of poem)
Chorus
```

### Song Duration — Let the Words Decide
Not all songs need to be 3-4 minutes. A short duration (e.g., 1:49) can be a feature when it matches the emotional content. Don't pad short poems just for runtime — let the song be the length the words demand. Short tracks create contrast in a playlist between longer epic tracks and short punches. A 90-second song that lands every line hits harder than a 3-minute song with filler.

### Very Short Poem (under 15 lines)
Poems under 15 lines need special handling — Suno fills short content with looping instrumental, producing a song that feels empty or aimless. Strategies:

**Double delivery:** Deliver the poem twice with different energy. Clean/quiet first pass, then heavy/intense second pass. The repetition is intentional — the same words change meaning through musical recontextualization. This works when the poem's meaning deepens or shifts under a different emotional lens.
```
Verse 1 (full poem, clean delivery)
Chorus (extracted hook)
Verse 2 (full poem, heavy delivery)
Final Chorus
```

**Chorus extraction:** Pull the poem's strongest, most repeatable lines into a standalone chorus. This gives Suno enough structural repetition to build a full song around limited source text.

**Thesis isolation:** Build through the poem, add a guitar solo or instrumental break, then deliver ONLY the final thesis statement as its own section. Powerful when the poem has a clear thesis line that deserves to land in isolation.
```
Verse 1
Verse 2
Guitar Solo
Outro (thesis line only)
[End]
```

**What NOT to do:** Do not pad short poems with `[Instrumental break]` tags in the lyrics — this literally asks Suno to noodle and produces a song that is mostly instrumental filler.

### Medium Poem (16-30 lines)
```
Verse 1
Pre-Chorus
Chorus
Verse 2
Pre-Chorus
Chorus
Bridge (the "turn" or a new perspective)
Final Chorus
```

### Long Poem (30+ lines)
```
Verse 1
Chorus
Verse 2
Chorus
Bridge
Verse 3 (or shortened recap)
Final Chorus
Outro
```

### Poem That Doesn't Need a Chorus
Some poems are genuinely better as continuous narrative. Signs:
- The poem is a single sustained meditation with no natural hook
- Adding repetition would break the flow
- The emotional power is in the progression, not a single moment

In this case, structure as:
```
Verse 1
Verse 2
Bridge
Verse 3
Outro
[End]
```
Use descriptor metatags to guide energy changes instead of relying on chorus repetition.

### Through-Composed Structure — Production Notes
Through-composed (no repeating chorus) works well when:
- The poem has a clear arc: building tension, climax, resolution.
- Word density naturally drives dynamic shifts — dense lines for intensity, sparse lines for breathing room.
- The style prompt supports the dynamic range needed (e.g., a style prompt that includes both quiet and heavy descriptors).

Critical requirement: always place a hard `[End]` tag after the final delivery to prevent Suno from looping or generating trailing instrumental. Without `[End]`, through-composed songs are especially prone to meandering because Suno has no chorus to signal "this is the structure repeating."

## Structural Metaphor in Song Design

Different time signatures for different section types can serve as a form-serves-content technique — the musical structure itself becomes a storytelling device. When a poem's themes lend themselves to it, the Lyric Transformer should consider suggesting structural metaphors where the musical form embodies the lyrical meaning.

### Examples

| Lyrical Theme | Musical Treatment | Effect |
|---|---|---|
| Chaos, instability, disorientation | Odd time signatures (5/4, 7/8) in verses | The listener feels off-balance, mirroring the content |
| Resolution, arrival, clarity | Straight 4/4 in choruses | Landing on solid ground after rhythmic instability |
| Freedom, looseness | NOLA funk groove, swung rhythms | The music breathes and moves freely |
| Confinement, rigidity, control | Rigid tempo, pounding metronomic drums | Mechanical precision creates a trapped feeling |
| Building dread | Accelerating tempo or increasing rhythmic density | Tension ratchets up through the music itself |

### Application Guidance

This technique is most powerful for prog and through-composed structures where the musical journey parallels the lyrical journey. The Lyric Transformer should flag opportunities for structural metaphor when:
- The poem has contrasting emotional states across sections (e.g., turmoil in verses, peace in choruses)
- The poem's themes include concepts that have natural musical analogs (freedom/confinement, chaos/order, tension/release)
- The target genre supports rhythmic experimentation (prog, post-metal, NOLA funk — less applicable to straightforward rock/pop)

Note: Time signature changes are inconsistently respected by Suno (see metatag-reference.md experimental tags), so structural metaphor should be treated as aspirational — worth attempting for the payoff when it lands, but not something to depend on for the song to work.
