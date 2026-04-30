# Playlist Sequencing Methodology

This reference covers album-level playlist sequencing: how to evaluate and order a body of tracks into a coherent listening experience. The focus is on the **album-craft layer** that sits above pairwise transition scoring — narrative structure, energy arcs, key positions, locked arcs, encore design.

For the **transition-evaluation layer** (Camelot wheel rules, BPM tolerances, felt-vs-librosa BPM corrections, listening-experience-as-primary criterion, parallel-key insights), see [`gemini-audio-analysis.md`](./gemini-audio-analysis.md) — particularly the "DJ Harmonic Mixing (Camelot Wheel)" section and the "Felt BPM" subsection. This doc assumes that material as foundational and builds on it.

## When to Use

Apply this methodology when:
- Ordering tracks into a playlist or album for the first time
- Re-evaluating sequencing after a regen wave changes track metrics (BPM, key, energy shape)
- Adding a new track to an existing playlist and choosing its slot
- Diagnosing why a published playlist "doesn't flow" despite individual tracks being strong

Skip the heavy methodology when:
- Reordering 1-2 adjacent tracks with no upstream/downstream impact
- The user has a fixed sequence preference and wants only sonic-transition feedback within it

## Tools Stack

The methodology is supported by `scripts/playlist-sequencing-data.py` which generates per-track structured data (BPM, overall/entry/exit keys, Camelot codes, energy level, intro/outro energy, transition quality) for every track in a playlist YAML. Output is auto-saved to `docs/audio-analysis/playlists/<album-slug>.json` (raw archive) AND `docs/playlist-sequencing-data.md` (refreshed companion summary). See the script's `--archive` and `--companion` flags. Catalog-wide deeper analysis (energy shifts, section boundaries, spectral balance, dynamic character) comes from `scripts/batch-full-analysis.py` writing to `docs/catalog-analysis-report.md`.

The data layer is the *input* to the methodology; it doesn't make sequencing decisions on its own.

## Per-Track Variables to Track

For each track in the playlist, gather and reason about all nine of these. Earlier variables tend to dominate when conflicts arise — but every variable matters and a "perfect score" on one (e.g., Camelot) doesn't override a poor score on another (e.g., tempo).

1. **BPM** (raw librosa) — the measured tempo
2. **Felt BPM** (human-verified) — the *perceived* tempo, often half or double the librosa raw value. **Felt BPM is what governs listening experience**; librosa raw is a measurement that may need halftime/double-time correction. Always verify felt BPM by ear before trusting raw numbers for sequencing decisions. (See `gemini-audio-analysis.md` "Felt BPM" subsection for the correction patterns.)
3. **Overall key + Camelot code** — the dominant key center
4. **Entry key + Camelot code** (first 30 sec) — the key the track *opens* in. May differ from overall.
5. **Exit key + Camelot code** (last 30 sec) — the key the track *ends* in. May differ from overall and from entry.
6. **Energy level** (1-10 scale) — average loudness/intensity. Useful for identifying peaks and valleys.
7. **Intro energy %** — sparse vs. explosive opening. Critical for transition-from-previous-track evaluation.
8. **Outro energy %** — fade vs. hard ending. Critical for transition-into-next-track evaluation.
9. **Dynamic character** — FLAT / MODERATE / DYNAMIC / HIGHLY-DYNAMIC. A "mid-tempo" song with HIGHLY-DYNAMIC character feels very different from a "mid-tempo" song with FLAT character — the listener's experience hinges on this, not just on BPM.

Plus three contextual variables that aren't measurable from audio alone:

10. **Mood/feel** — captured from Listening Notes in the songbook entry, Gemini blind analysis, or the user's articulation.
11. **Sonic palette / arrangement density** — instrumentation profile (acoustic vs. dense metal, brass-led vs. guitar-led, etc.).
12. **Lyrical narrative position** — what the song "means" in the album's story; what came before, what's coming next.

## Transition Discipline

The transition between two adjacent tracks is the actual moment the listener experiences. Per-track variables exist; transitions are *the experience*.

**Exit key matters more than overall key.** A track that's "overall in C minor" but ends in G minor will transition into the next track via G minor, not C minor. Use exit-Camelot of track N → entry-Camelot of track N+1 as the actual transition assessment. The script's `transition_to_next` field already does this.

**Camelot wheel scoring is one input, not the verdict.** See `gemini-audio-analysis.md` "DJ Harmonic Mixing (Camelot Wheel)" for the rules and "Camelot framework limitations" for what it misses. In particular: parallel-key transitions (same root, different mode — e.g., D# major → D# minor) score JARRING on Camelot but are musically a deliberate emotional pivot on the same harmonic center. The listener may hear continuity even when the wheel says discontinuity.

**BPM transition tolerance:** <3% smooth, 3-6% noticeable, >6% requires intentional contrast. Halftime/double-time pairs (e.g., felt 70 and felt 140) share a pulse grid and can mix coherently even though the felt-tempo difference is dramatic — but treat this as a *deliberate* breath-in / breath-out move, not a "smooth" transition.

**Intro/outro % bridges the dynamic side of the transition.** A track ending at 70% energy into a track starting at 15% creates a dramatic drop — fine if it's intentional (act break), jarring if it's mid-act. The 15% intro after a high outro reads as a hush or a reset; the listener's ear interprets the gap.

## Album-Craft Layer

Beyond pairwise transitions, the playlist as a whole has shape. Several established models apply.

### Energy Arc Models

**Inverted-U (classic album):** Tempo and energy build through the front half, peak mid-album, descend toward the close. Valence/arousal (emotional intensity) often *dips* mid-album, creating a journey shape — the energy is high but the emotional weight gets heavier before lifting.

**W-shape (concert / featured-songs model):** Three peaks at the beginning, middle, and end of the playlist, with complementary songs providing variety in key/tempo/timbre/mood between the peaks. Two valleys between the peaks give the listener room to breathe. The W-shape works well when the playlist has clear "anchor" tracks at all three positions.

**Concert peak-end rule:** The audience remembers the best moment and the final moment most vividly. Open higher-than-average, allow a dip, close higher-than-average. The closer doesn't have to be the loudest track — it has to feel like a *resolution*.

A 6-act narrative structure naturally creates a W-shape if Acts I, IV, and VI hold the peaks; valleys land in Acts II and V. But the shape is descriptive, not prescriptive — if the album's emotional logic produces a different curve (front-double-peak with contemplative descent close, for example), name what it actually is rather than forcing the W.

### Key Positions

The methodology treats positions **1, 4, 7, and 10** as load-bearing. Strongest songs go here. Track 1 sets the tone; track 2 confirms the promise (so 1 → 2 cannot be a misfire); track 4 anchors the front; track 7 carries the listener into the middle; track 10 picks up the second half. The final track provides resolution — separate criterion from "strongest song."

For longer playlists (30+ tracks), the same logic extends: 1 / 4 / 7 / 10 / 13 / ... up to a closer that resolves. The pattern thins out past about position 10 because the listener is now inside the album rather than evaluating it from the outside.

**Streaming-era reality:** Front-loading with engaging material is more critical than ever. The first 3-4 tracks determine whether a listener stays with the album or skips. This doesn't mean the front needs to be the *loudest* — it means it needs to be the most *immediately compelling*.

### Sonic Palette Variety

Avoid placing two songs with similar instrumentation, arrangement density, or timbral character next to each other. The methodology's principle: contrast is essential for maintaining interest.

Specific anti-patterns:
- Two intricate intros back-to-back — the listener loses orientation
- Two acoustic stripped-back tracks adjacent — the album feels like it stalled
- Two power-pop bangers adjacent — the genre register collapses into a single mood
- Two slow contemplative tracks adjacent — unless deliberate ("breath section")

Variety is an active design choice, not a side effect of randomization.

### Tempo Variety

Categorize tracks into up-tempo / mid-tempo / slow buckets. Avoid placing too many from the same category adjacent. Two slow songs back-to-back loses listeners unless deliberate.

But: **a deliberate slow-tempo block is a real album convention.** Doom albums, ambient stretches, contemplative interludes — three or four felt-tempo-matched tracks in a row can be an immersive zone if the *sonic palette* and *mood* shift across them. The methodology cautions against accidental same-tempo runs, not against intentional ones.

### Same-Key Adjacency

3-4 songs in the same key consecutively gets boring. When you finally shift keys after too many same-key tracks, the change feels more jarring than a varied stretch would have. Limit same-key consecutive runs to 2 unless you have a specific reason to push to 3.

### Similar-Songs-Need-Distance

Tracks that cover similar **thematic** ground (e.g., two songs about "knowing nothing," two songs about a parent, two songs about NOLA mythology) should be separated in the playlist so each hits fresh. Adjacency blurs them into one long meditation; spacing lets each song carry its own weight.

This is distinct from the same-key rule and the sonic-palette rule — a track can be sonically and harmonically distinct from its neighbor but cover the same lyrical territory.

### Locked Arcs / Preserved Sequences

Sometimes a sequence of 2-N tracks is *deliberately positioned* to read as a unit — a love → loss → grief → healing arc, a three-act story, a musical movement that depends on adjacency. These should be locked: the order within the arc cannot change, and the arc as a whole should travel as a block.

When evaluating playlist changes:
- Surface locked arcs explicitly before proposing reorders
- Treat the arc's position as flexible (the block may move) but the order within as fixed
- If a proposed reorder requires breaking the arc, stop and ask the user — never break a documented locked arc on Mac's own authority

In Lenny's case, the locked arc is the four-song Love & Loss / Heal sequence (From Now Until... → Distant-- → Breast Feeding → The Fire That Never Stops). Per session-context-for-mac.md: *"These are positioned deliberately in the playlist and should not be separated."*

### Encore Structure

For album-as-concert-set framing: Act VI (or the final stretch) functions as a planned 3-5 song mini-set at high energy following a "breath-catching break." The break is often a single contemplative track that gives the listener room before the closing run.

**Anatomy of a working encore section:**
- Breath-catcher: low-mid energy, contemplative or stripped-back
- Encore launch: high-energy banger that re-engages the listener
- Encore middle: sustained energy with thematic coherence
- Encore close / resolution: doesn't have to peak louder; needs to *resolve*
- Optional post-encore coda: the singer alone on the empty stage — fade close

If your final stretch lacks this shape (e.g., averages mid-energy throughout with no clear launch), call it what it is: a "contemplative legacy descent" or "extended fade close" — a different valid shape, not a broken encore.

## What the Methodology Doesn't Capture

**Listening experience is the ultimate arbiter.** Per `gemini-audio-analysis.md`: *"describe the listening experience (smooth / fluid / abrupt / jarring) as the primary criterion. Camelot is one input. Explicitly call out tempo gaps, genre register gaps, and energy gaps alongside Camelot when significant."*

**Parallel-key transitions** (same root, different mode) are musically a deliberate emotional pivot — minor → major lifts; major → minor darkens. Camelot wheel scores them JARRING because the wheel positions are different, but the listener hears the same harmonic center. When evaluating transitions, name parallel-key relationships explicitly when they appear; don't let the JARRING score override what the ear knows.

**Felt-tempo lock vs. raw-BPM lock.** Three tracks at "136 librosa" don't necessarily lock at felt-136 — one of them may be felt-68 with halftime detection. Verify felt BPM before claiming tempo continuity across tracks.

**Genre-outlier placement.** A power-pop track in a swamp-metal album won't have a Camelot-AND-tempo-AND-genre-perfect placement anywhere. Pick where the listening experience is *least jarring*, accept that no slot is ideal, and document the trade-off rather than pretending it's seamless.

**The narrative dimension is non-data.** No script measures whether two adjacent tracks are thematically coherent. That's the user's call (or the orchestrating agent's judgment based on lyrical content + writer voice context). Don't treat the data analysis as sufficient — sonic flow and thematic flow are independent and both must work.

## Process for Reviewing a Playlist

A repeatable approach for "is this playlist sequence working?" — apply variables in this order:

1. **Surface locked arcs** — what cannot move? Document them up front.
2. **Run the script** — get all 38+ tracks' per-track data and per-transition scoring.
3. **Verify felt BPM** for any track with library raw in the 130-180 BPM range or 70-100 BPM range — these are the bands where halftime/double-time confusion is most common. Ask the user when uncertain.
4. **Identify the act structure** — is the playlist organized around narrative acts? What are their thematic functions? How many tracks per act?
5. **Check the energy arc** — what shape does the playlist have? Does it match the intended shape (W, inverted-U, concert peak-end, contemplative descent)?
6. **Check key positions** — do positions 1, 4, 7, 10 have load-bearing tracks? Is the closer a resolution?
7. **Walk transitions act-by-act** — within each act, evaluate transitions on the full variable stack (Camelot, BPM-felt, intro/outro%, sonic palette, theme). Flag the worst.
8. **Identify cluster opportunities** — are felt-tempo cousins scattered when they could be a deliberate immersive block? Are thematic cousins adjacent when they should be separated?
9. **Form a recommendation** — propose specific moves with named justifications across multiple variables. Don't just say "swap X and Y" without naming what each variable says about that swap.
10. **Surface trade-offs honestly** — every move has trade-offs. Name them. Don't claim a move is "cleaner" if it's actually "trades A-jarring for B-jarring."

The output isn't a metrics dump — it's an opinionated proposal grounded in the variables, with explicit acknowledgment of what's locked, what's a judgment call, and where the user's ear should be the tiebreaker.

## Cross-References

- `gemini-audio-analysis.md` — Camelot wheel mechanics, felt-BPM corrections, listening-experience-as-primary criterion (foundational; this doc builds on it)
- `scripts/playlist-sequencing-data.py` — generates the per-track sequencing data
- `scripts/batch-full-analysis.py` — generates the catalog-wide deeper analysis (energy shifts, section boundaries, dynamic character)
- `scripts/audio-deep-analysis.py` — per-song deep analysis
- `docs/audio-analysis/playlists/<album>.json` — JSON archive of the playlist sequencing data
- `docs/audio-analysis/catalog/<date>-deep.json` — JSON archive of the deep catalog analysis
- `docs/playlist-sequencing-data.md` — auto-refreshed Markdown companion to the playlist sequencing JSON
- `docs/catalog-analysis-report.md` — auto-refreshed Markdown companion to the deep catalog analysis
- `docs/audio-analysis-reference.md` — felt-BPM corrections + LLM-comparison hand-curated alongside the auto-table
