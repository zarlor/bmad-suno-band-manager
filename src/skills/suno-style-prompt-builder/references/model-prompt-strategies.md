# Model-Specific Prompt Strategies

> **Related references:** Style prompts work in conjunction with lyric metatags — for the full metatag catalog (section tags, vocal delivery, effects, production tags), see `suno-lyric-transformer/references/metatag-reference.md`. For mapping user feedback to style prompt adjustments, see `suno-feedback-elicitor/references/suno-parameter-map.md`.
>
> **Last validated:** April 6, 2026 (Suno v5.5 Pro, v5 Pro, v4.5-all, v4.5 Pro, v4.5+ Pro, v4 Pro). Updated with v5.5 community testing findings: corrected Voices Audio Influence ranges (JG BeatsLab), added Skill Level dropdown, My Taste magic wand/Style Augmentation, Personas/Voices coexistence, HookGenius 1000+ prompt analysis (tag count 5-8, cinematic modifier, production tags, conflicting tags), Weirdness-during-Extend drift finding, spoken word limitations, Custom Model consent. Suno updates models and prompt behavior frequently — use web search to verify strategies against current documentation when uncertain.

## Quick Reference

| Model | Style | Sweet Spot | Strengths |
|-------|-------|-----------|-----------|
| v4.5-all (free) | Conversational sentences | Flowing descriptions, natural language | Heavier/faster genres, longer-form (~8 min) |
| v4.5 Pro | Conversational + nuanced | Like v4.5-all with more detail responsiveness | Intelligent prompt enhancement |
| v4.5+ Pro | Advanced conversational | More control over structure | Advanced creation methods |
| v5 Pro | Crisp film-brief | 5-8 descriptors, emotional > technical | Natural vocals, instrument separation, polish |
| v5.5 Pro | Crisp film-brief (same as v5) | 5-8 descriptors, can be more granular | Most expressive, Voices, Custom Models, My Taste |
| v4 Pro | Simple descriptors | Keep it straightforward | Improved sound quality over v3 |

## v4.5 Family (v4.5-all, v4.5 Pro, v4.5+ Pro)

### Prompt Style: Conversational

Write style prompts as flowing, descriptive sentences. The model responds well to narrative descriptions of the sound.

### Construction Pattern

```
[Genre and mood sentence]. [Instrumentation and texture sentence]. [Production and mix sentence]. [Energy and dynamics sentence].
```

### Example Prompts

**Indie folk-rock:**
> Create a melodic, emotional indie folk-rock song with organic textures and warm analog production. Acoustic guitar layered with subtle electronic elements, gentle percussion building through the song. Intimate male vocals with clear diction and restrained delivery, opening up on choruses.

**Upbeat pop:**
> Energetic, feel-good pop with a modern radio-ready sound. Bright synths, punchy drums, and a driving bass line. Female vocals with a confident, playful delivery. Big chorus with layered harmonies and a catchy hook.

**Dark electronic:**
> Deep, brooding electronic track with industrial textures and a slow-burning build. Heavy sub-bass, glitchy percussion, distorted synth drones. Minimal vocals — whispered, processed, barely human. Tension throughout, no release until the final drop.

### Tips

- Can be more verbose than v5 — the model handles longer descriptions well
- Conversational tone works: "Create a..." or "This should sound like..."
- Good for describing energy arcs: "begins with soft ambient layers, builds to..."
- Prompt Enhancement helper available in the UI — mention this to users

## v5 Pro

### Prompt Style: Crisp Film-Brief

Write style prompts as tight, evocative descriptors — like a creative brief for a film soundtrack. Emotional and textural language over technical specifications.

### Construction Pattern

```
[genre], [mood/emotion], [2-3 key sonic textures], [vocal character], [production quality notes]
```

Keep to **5-8 descriptors**. Each one should earn its place.

### Example Prompts

**Indie folk-rock:**
> indie folk-rock, melancholic warmth, acoustic guitar over ambient pads, breathy male vocal, intimate lo-fi mix with wide stereo field

**Upbeat pop:**
> modern pop, confident and bright, punchy drums, sparkling synths, female vocal with playful edge, radio-ready mix, big chorus harmonies

**Dark electronic:**
> dark electronic, industrial tension, sub-bass drones, glitchy percussion, whispered processed vocals, cinematic slow-burn

### Tips

- **Emotional descriptors beat technical ones:** "raw, yearning" > "120 BPM". Use rhythm nouns instead of BPM values: "halftime groove," "double-time driving," "shuffle feel." (v5 may respond better to BPM in style prompts than v4/v4.5 — see Universal Rules — but rhythm nouns remain more reliable.)
- **Production-quality descriptors are highly effective in v5:** "radio-ready mix", "punchy drums", "wide stereo field", "crisp high-end", "warm bass"
- **Include mix notes:** register, tone, phrasing, harmony
- **Vocals sound more natural** in v5 — breaths, phrasing, harmonies are authentic
- **Better instrument separation** — can request specific instrument prominence
- **Composition-aware architecture** — v5 uses early style/genre info to maintain coherent sections throughout the song
- **Better nuanced interpretation** of complex prompts vs. v4.5
- **Full negative prompting support** — v5 handles in-prompt negatives ("no [element]") more reliably than v4.5's limited support
- **Existing v4/v4.5 prompts often work "even better" on v5** — migration is typically seamless
- **Section-level editing** available in editor — structure control shifted from prompt to editor
- Don't waste characters on things the editor handles (song structure, section ordering)

**Tested v5 Pro descriptors (from live testing):**
- "down-tuned" and "crushing" — effective for pushing v5 from rock toward metal weight
- "raw melodic singing" — key phrasing for gritty-but-not-screaming vocals (overcorrects less than "clean singing with grit on peaks")
- "dual gritty male vocals" + "raw melodic singing" — achieved gritty-but-melodic without triggering screaming
- "heavy swamp metal" with Exclude Styles blocking screaming — got heavy without full scream on v5
- NOLA funk elements came through well across multiple sections on v5
- v5 had more dynamism and better section transitions than v4.5+ Pro for complex multi-tempo songs
- "NOLA funk groove" functions as BOTH a genre descriptor AND a rhythmic looseness instruction — NOLA funk and jazz are inherently rhythmically loose (swing, syncopation, playing around the beat). This makes it a better vehicle for odd time signatures and time changes than pure metal, which tends to be metronomically precise. Non-obvious but powerful finding.

**Confirmed Descriptor Effects (from community research):**

These descriptors produce consistent, predictable results across v5 generations:

| Descriptor | What Suno Produces |
|---|---|
| `atmospheric` | Reverb, space, ambient pads |
| `airy` | Reverb/space on vocals |
| `lo-fi warmth` | Vintage character, low-pass filtering |
| `polished radio-ready` | Clean, modern, commercial mix |
| `raw live recording` | Less processed, room sound |
| `driving` | Forward momentum, energetic basslines |
| `lush` | Layered pads, dense production |
| `punchy` | Low-end presence, tight transients |
| `wide stereo` | Spatial separation |
| `gated drums` | 80s-style drum processing |
| `vintage Rhodes` | More specific/effective than "piano" |

**Three-Pass Layered Prompting (v5 technique):**

For complex songs, build the prompt in three conceptual passes rather than trying to specify everything at once:

1. **Idea pass** — define concept, mood, genre (the style prompt core)
2. **Lyric pass** — write/refine lyrics with structural tags
3. **Performance pass** — add vocal delivery cues, energy tags, dynamics

This separates concerns and prevents overloading any single input field.

**Confirmed Suno behavior (from Gemini analysis of production outputs):**
- "NOLA funk swing" lands as syncopation, not true swing — Suno interprets swing as a syncopation instruction rather than a jazz swing feel
- "Odd time signatures" is consistently ignored in 4/4 rock/metal context — the strong 4/4 pull of rock and metal genres overrides time signature instructions
- Suno adds unscripted guitar solos regularly — expect them even when not requested, especially in rock/metal genres
- Structural/section directions embedded in long style prompts are largely ignored — Suno treats the style prompt as a tonal palette, not a roadmap. Use metatags and the editor for structural control, not the style prompt.

## v5.5 Pro

### Prompt Style: Same as v5 Pro — Crisp Film-Brief

v5.5 is an additive update over v5. It uses the same audio engine, metatags, and character limits. All v5 prompts work identically on v5.5, often with better results. No migration required.

### What Changed

- **Most expressive model yet** -- better at interpreting subtle, nuanced descriptors that v5 would flatten or ignore
- **More varied output** per generation -- generate 3-5 versions and pick the standout; the spread between "best" and "average" is wider
- **v5.5-optimized prompts can be more specific:** where v5 would use simpler terms like "808s, hi-hats," v5.5 responds well to granular detail: "deep sub 808s, glitchy hi-hat rolls, pitched vocal chops"
- 48kHz sample rate, up to 8 min generation, internal codename "chirp-fenix" (v5 was "chirp-crow")
- **Workflow paradigm shift:** v5.5 encourages generate -> inspect -> replace sections -> refine (not regenerate from scratch)

### v5.5 New Features

**Voices (replaces Personas):**
- Actual voice cloning from a 15s-4min audio sample with anti-deepfake verification
- Pro/Premier only
- **Skill Level dropdown** (Beginner/Intermediate/Advanced/Professional): NOT cosmetic — actively reshapes model interpretation. **Always select Professional** regardless of actual singing ability. Testing confirmed Professional produces the most stable, consistent results across every test.
- Drop gender descriptors ("male vocals", "female singer") when using Voices -- the Voice already defines these, freeing characters for production detail
- Audio Influence for Voices varies by goal (higher than the 25% default for Personas). Independent testing (JG BeatsLab, March 2026) found the practical ceiling is lower than Suno's UI suggests — at 85%, resemblance only reached ~70% with increasing artifacts:

  | Goal | Range | Notes |
  |------|-------|-------|
  | Voice as subtle flavor | 30-40% | Gentle influence, maximum generation polish |
  | Balanced voice + quality | 40-60% | **Recommended starting point** — recognizable with manageable artifacts |
  | Identity-focused | 60-70% | Quality trade-off begins here |
  | Maximum fidelity (caution) | 70-80% | Diminishing returns; artifacts increase faster than resemblance |

  Start at 50% and iterate in 5-10% increments. Pushing above 70% is counterproductive.
- Pairs well with delivery metatags (`[Whispered]`, `[Belted]`, `[Breathy]`, `[Raspy]` etc.) -- Voice sets *who* sings, metatags set *how*
- **Style Personas are NOT gone** — they are integrated into the Voices tab in v5.5. The button changed, but both features coexist. Personas still work on v4.5/v5/v5.5. Key difference: Voices is actual voice cloning, Personas is style essence capture.

**Getting the best voice clone:**
- **Clean recording matters more than expensive hardware** -- minimal background noise, no heavy reverb. A quiet room with a decent mic beats a studio mic in a noisy space. No compression, no background music. 44.1kHz minimum sample rate. The cleaner the input, the better the clone.
- **Consistency WITHIN a single clip wins** -- pick a part of your recording where you sound most like a single, stable version of yourself. No style switching, no big dynamic swings, no mixed energy levels within ONE sample. JG BeatsLab day-one testing found consistency dramatically outperformed mixed-register clips: "longer, more varied recordings underperformed compared to shorter, focused clips every time."
- **Optimal length is 20-30 seconds of clean consistent content per clip** -- longer samples (3+ min) actively underperformed in testing. Focus beats breadth within a single clip.
- **Variety across MULTIPLE clips, not within one** -- one clip works, three clips across different moods works better for capturing range and character. The resolution to the apparent consistency-vs-variety tension: each clip should be internally consistent (one stable character sustained), variety lives at the profile level by uploading multiple Voice profiles (e.g., "Narrative Rock," "Ballad Intimate," "Speak-Sing Confessional"). When a song is built, pick the Voice profile that matches the target vibe.
- **Natural delivery, not performance** -- Suno captures your natural vocal tone, not a performance. Sing or speak normally. First-take recordings that lean operatic, theatrical, or "poetry-voice" are a documented failure mode — the model captures the affect as character, and Voice generations will deliver that affect back on every generated song. Re-record if the first take feels performative.
- **Preserve vocal quirks, don't smooth them out** -- slight rasp, slide between notes, natural vibrato, sibilant character — the model captures character, and character is what makes a voice recognizable. Don't try to sound "cleaner" than you naturally do. (Sibilance is largely a mic technique issue, not a voice issue — angling the mic 15-30 degrees off-axis reduces direct sibilant hits without changing the voice itself. A pop filter placed further back also helps.)
- **Skill Level: Professional, always** -- JG BeatsLab testing was emphatic: "Professional produced the most stable, most consistent, most usable results across every test. The difference between Beginner and Professional is substantial — it actively reshapes how your voice is interpreted by the model. Set it to Professional. Every time." Not cosmetic. Not optional. Cannot be changed after recording — re-record if your Voice wasn't set to Professional the first time.
- **Range considerations** -- the Voice captures your current range, not your historical peak. If your range has narrowed, song selection for Voice tracks should work within current comfort. Most heartland rock / Americana / singer-songwriter territory doesn't require wide range anyway — it requires conviction.

**The v5.5 Voice-Character Principle** (corrected April 2026):

v5.5 Voice cloning trains on the user's vocal samples and captures **vocal character** — timbre, lilt, vibrato tendencies, attack patterns, dynamics behavior, mic artifacts. That's the literal training. **There is no "trained genre gravity"** — a prior version of this doc framed the Voice as carrying trained genre bias and pulling generations toward a trained baseline. That framing was overstated. Suno adapts the captured character to the genre prompt: a Voice trained on a sample in one style can be used for songs in many styles. Training material genre ≠ output generation genre. (Example: a Voice trained on a Renaissance bawdy-song sample reliably generates folk, soft rock, and belt-forward arrangements depending on the song's prompt direction.)

**What Voice clones actually do:** They carry vocal character — how the singer delivers (breath, attack, held-note dynamics, vibrato tendencies, mic artifacts). This character is genre-neutral in itself. Suno's base model does associate some vocal characters with arrangement-default genres, which can *look* like "gravity" in early generations when the prompt is weak — but the cause is arrangement-default inference from voice character, not genre pre-baking in the clone. At most, the voice NAME ("Rock," "Soft," "Cleaner Rock") can lean Suno's interpretation via name-as-hint, but this is a subtler effect than the "gravity" framing implied. When matching a Voice to a song, frame it as **"the captured character fits X register well"** or **"this character's lineage is compatible with Y lane"** — NOT **"fighting the Voice's trained gravity toward Z."**

**Practical rules when shaping a song with a Voice:**

1. **Drop descriptors that duplicate what the Voice already delivers.** If the Voice captures vulnerable-breathy delivery, don't add "vulnerable delivery," "breathy," "soft male vocal" to the style prompt — they're redundant and can conflict with the captured character Suno will already reproduce. Use that budget for song-specific arrangement direction instead.

2. **Load descriptors that specify what the song needs from the arrangement.** The style prompt drives arrangement (instrumentation, genre, production, dynamics); the Voice provides the vocal character. Be explicit about arrangement — "overdriven rhythm guitar with crunch," "driving mid-tempo rock groove," "intimate fingerpicked acoustic" — rather than redundantly labeling what the Voice does.

3. **Keep Style Influence tight (65+)** so the prompt leads the arrangement firmly. The Voice character will shape the vocal delivery within that arrangement regardless; Style Influence governs how much the prompt directs the band.

4. **Never specify Vocal Gender when a Voice is active** — Voice defines it. Leaving Vocal Gender empty lets the Voice do its job; specifying can fight it.

5. **Voice-aware exclusion strategy** — when the Voice physically cannot produce harsh/screamed vocals (most clean-voice Voice clones can't), harsh-vocal exclusions are wasted Exclude Styles space. Focus exclusions on production and genre-direction protection (`heavy metal, heavy distortion, steel guitar, autotune, pop sheen`) instead of vocal protection. The clean Voice IS the natural guardrail against harsh vocals — trust it and reclaim the exclusion budget for what actually needs protection.

6. **Audio Influence floor caution** — the 30-40% "subtle flavor" range in the table above works with Professional-level Voices. For non-Professional Voices, dropping below ~40% can trigger a robotic-timbre failure mode where Suno's default interpretation bleeds into the Voice character and lands in uncanny valley. If a Voice wasn't set to Professional at recording time, keep Audio Influence at 50%+ until re-recording.

**Practical case study (what it actually validates):** A song written for a vulnerable-folk-leaning Voice clone but styled as heartland southern rock. First attempt used "warm vocals, vulnerable storytelling, clean male delivery" in the style prompt — all descriptors the Voice already delivered — plus "gentle Wurlitzer touches" and Audio Influence 20% (a Persona genre-departure setting, wrong for Voices). Result: robotic timbre, keyboards dominated the mix, too laid-back for the intended rock urgency. Fixed by: (1) dropping all vocal descriptors the Voice already delivered, (2) killing keyboards entirely from the style prompt, (3) loading rock-forward arrangement descriptors ("overdriven rhythm guitar with crunch," "cutting lead guitar accents," "driving mid-tempo rock groove"), (4) raising Audio Influence to 55% (Voice sweet spot), (5) removing harsh-vocal exclusions (the clean Voice couldn't produce them anyway), (6) specifying "heartland southern rock" as the genre anchor. Result: recognizable voice identity with the target rock arrangement.

**What the case study actually validates:** (a) correct Audio Influence setting for Voices (55% sweet spot), (b) don't duplicate descriptors the Voice already delivers, (c) specify arrangement/production direction explicitly. It does NOT validate "the Voice has genre gravity." The original framing attributed the failure to genre-gravity; the actual causes were the duplicate descriptors + wrong Audio Influence + prompt direction not being specific enough about the arrangement.

**Custom Models:**
- Train on 6+ original tracks, 2-5 min training time, up to 3 custom models per account
- Pro/Premier only
- Drop generic production descriptors your model already knows -- if your Custom Model was trained on lo-fi indie tracks, you don't need "lo-fi warmth" in every prompt
- Think of Custom Model as "producer" and the prompt as "songwriter" -- the model brings the sonic palette, the prompt brings the creative direction
- Train separate models for separate styles -- mixing genres in training data confuses the model

**Training Data Best Practices:**
- **Format:** WAV at 44.1kHz preferred. Heavily compressed MP3 at low bitrates introduces artifacts that interfere with feature extraction.
- **Loudness:** System auto-normalizes (RMS leveling, DC offset removal, spectral masking, onset detection, key/scale estimation). Dynamic range preservation matters more than loudness — streaming-standard ~-14 LUFS is a reasonable baseline. Over-limited/brick-wall-mastered tracks may lose the dynamic character the model is trying to learn.
- **Quantity:** Minimum 6 tracks. 8-12 stylistically consistent tracks is the inferred sweet spot. No documented upper limit. Emphasis from all sources is on stylistic consistency over quantity.
- **Length:** Full-length tracks (3-5 minutes) provide richer training data for arrangement pattern learning. Short clips may not contain enough structural variety.
- **Quality:** Clean, well-mixed audio with minimal background noise and no heavy reverb. The system isolates vocals from mixed audio automatically, but acapella recordings may yield higher quality vocal style capture.

**Overfitting Mitigation:**
- Training data too narrow/homogeneous causes repetitive output with reduced variety
- Include variety within your chosen style lane — different tempos, moods, arrangements, instrumentation variations
- Overly detailed prompts + tightly-trained Custom Model = 'narrow and repetitive as if the AI has fewer options'
- Keep prompts shorter/simpler when using a well-trained Custom Model — it already knows your baseline

**Retraining (documentation gap):** No sources provide clear guidance on updating existing models, deletion workflow, or whether retraining from scratch produces different results. The 3-model limit serves as both a practical constraint and a platform retention mechanism.

Sources: [Custom Models — Suno Help](https://help.suno.com/en/articles/11362497) | [Blake Crosley: Suno Definitive Reference](https://blakecrosley.com/guides/suno) | [AudioNewsRoom: Suno v5.5](https://audionewsroom.net/2026/03/suno-v5-5-what-you-give-up-to-make-it-yours.html)

- **Voice + Custom Model is the most powerful combo:** who sings (Voice) + what style (Custom Model) + detailed prompt (creative direction)
- **Privacy/consent note (AudioNewsRoom):** The consent required to use Voices and Custom Models grants Suno permission to use your data for training their global models. This is NOT optional and NOT a private silo — you are uploading your creative fingerprint to their infrastructure.

**Voices limitations:** Voices is directional influence, not true vocal reproduction — the output drifts across generations and lacks true identity consistency (JG BeatsLab testing). Realistic for demo vocals, pre-production emotional direction, and hearing yourself in new compositions. **Not suitable for** spoken word/narration (Voices drifts toward singing patterns, inconsistent tone between sections, unnatural pacing in longer spoken passages — Suno remains music-first).

**My Taste:**
- Passive personalization that shapes generation defaults based on your listening/generation history
- All tiers (including free), enabled by default
- Takes 20-30 generations to show noticeable influence
- **Magic wand / Style Augmentation:** Click the **magic wand icon** next to the style input in the Create form — Suno auto-generates a personalized style description from your My Taste profile. This is the primary way My Taste manifests.
- **Detailed manual prompts always override My Taste** — if you provide your own style prompt, My Taste is subordinate
- **Controls:** Avatar menu > "My Taste" to view, edit, or disable. No documented reset mechanism beyond disabling.

### v5.5 Personalization Stack

Layers from broadest to most specific:
1. **My Taste** -- shapes generation defaults passively
2. **Custom Model** -- sets production DNA and sonic identity
3. **Voice** -- applies a specific vocal tone and character
4. **Prompt** -- steers the specific song (always the most important layer)

### Tips

- All v5 Pro tips above still apply -- v5.5 is additive, not a replacement
- Lean into specificity: replace broad descriptors with granular ones where you have a clear sonic vision
- When using Voices, reallocate the characters you save from dropping gender/vocal descriptors toward production detail
- When using Custom Models, reallocate the characters you save from dropping generic production descriptors toward song-specific creative direction
- The generate -> replace sections -> refine loop is more efficient than regenerating from scratch on v5.5

## v4 Pro

### Prompt Style: Simple Descriptors

Straightforward genre + mood + basic production notes. Less nuanced than v4.5+ models.

**IMPORTANT: v4 Pro has a 200-character hard limit** (not 1,000 like v4.5+/v5). Every word must earn its place.

### Construction Pattern

```
[genre], [mood], [key instruments], [vocal type], [one production note]
```

### Example

> indie folk-rock, melancholic, acoustic guitar and ambient synths, male vocals, warm production

### Tips

- **200-character hard limit** — be extremely concise
- Keep it simpler than v4.5/v5
- Don't over-describe — diminishing returns on detail
- Focus on genre accuracy and mood

## Universal Rules (All Models)

1. **Character limits** — v4 Pro: 200-char hard limit. v4.5+/v5/v5.5: 1,000-char hard limit (API confirmed). All silently truncated at their respective limits.
2. **Critical zone (first ~200 chars)** — front-loaded terms have the strongest influence on generation. Front-load all essential genre, mood, and vocal descriptors within the first ~200 characters. Content beyond ~200 chars is supplementary but not wasted — it adds nuance and specificity. v5.5's improved descriptor interpretation may extend the effective window beyond 200 chars. A concise 100-char prompt can outperform a cluttered 200-char one, but a well-crafted 250-char prompt with specific descriptors can outperform a generic 150-char one. This is a priority guide, not a character limit.
3. **Word order is weighted** — front-loaded terms dominate generation. Priority order: Genre → Mood/Energy → Instruments → Vocals → Production. Whatever appears first sets the primary sound; everything after is progressively more "flavoring."

    **Exception for non-default vocal arrangements:** When the song requires a vocal arrangement that isn't the genre default (group backing vocals throughout a rockabilly or psychedelic-blues song, dual-vocal interplay in a singer-songwriter context, call-and-response in a genre where backing vocals are sparse), promote the arrangement descriptor to **position 1 of the style prompt** ahead of even genre. Example: `group backing vocals throughout, psychedelic swamp voodoo blues, narcotic gris-gris groove, ...`. Production-tested April 2026 on a song where positioning "group backing vocals" at position 3 produced inconsistent backing vocals; moving it to position 1 (combined with lyric-side wordless-chant intro — see lyric transformer's metatag-reference.md "Establishing Non-Default Vocal Arrangements") landed the pattern reliably. The genre signal stays strong enough at position 2 to drive the overall sound; what changes is Suno's pre-commit to the non-default arrangement being part of the song's identity.
4. **5-8 descriptors is the sweet spot** (HookGenius 1000+ prompt analysis, April 2026) — fewer than 4 produces generic results; exceeding 10 causes conflicting signals and quality degradation. Each descriptor should earn its place.
5. **Hyper-specific beats generic** — "1980s synth-pop" not "pop"; "distorted electric guitar, power chords" not "guitar." Era descriptors instead of artist names: "late 70s disco" not an artist name.
6. **Genre and mood always go first** — they're the strongest signal (see rule 3)
7. **Never put style cues inside lyrics** — style prompt and lyrics are separate inputs
8. **No asterisks or special formatting** in style prompts
9. **Never put artist names in style prompts** — Suno does not reliably replicate named artists. Decompose references into concrete sonic descriptors instead.
10. **Negative/exclusion prompts go at the END of the style prompt** — positive descriptors first, cleanup last. "no [element]" is the most reliable in-prompt phrasing. Alternatively, use the separate Exclude Styles field. v5 handles in-prompt negatives better than v4.5.
11. **Comma separation works across all models** — consistent delimiter
12. **Describe, don't command** — "dreamy shoegaze with female vocals" over "Create a dreamy shoegaze song." (v4.5 examples use "Create a..." which matches Suno's own v4.5 docs, but descriptive style generally works better.)
13. **Production tags are the most underused category** (HookGenius analysis) — adding even one production descriptor ("radio-ready mix", "punchy drums", "wide stereo") meaningfully improves output distinctiveness. Most users rely only on genre + mood.
14. **"Cinematic" is a universal quality modifier** — HookGenius's 1000+ prompt analysis found it consistently elevates production quality across every tested genre. Most versatile single tag for enhancing output. (Note: in guitar/bass-led arrangements, "cinematic" can pull keyboard/synth — see Dangerous Words above.)
15. **Conflicting tags produce bland compromise** — "aggressive, peaceful" or similar contradictions cause Suno to default to a generic middle ground, not an interesting hybrid. Opposing descriptors cancel out.
16. **Callback phrasing during Replace Section** — when using Replace Section or Extend, re-inject genre/mood and use callback phrases like "continue same chorus energy" every 1-2 extends to prevent drift.
13. **BPM in style prompts — model-dependent** — on v4/v4.5, BPM tags have zero detectable effect on Suno's output (confirmed by librosa analysis: songs tagged 60 BPM were delivered at 95.7 BPM; songs tagged 65-150 BPM across sections were delivered at a steady 123 BPM). On v5, BPM and key in the style prompt may be more effective than lyric tags (e.g., `"deep house, 122 BPM, A minor, hypnotic groove"`), though rhythm nouns remain more reliable for most use cases. Suno still picks its own tempo based on genre context and arrangement.
14. **Use rhythm nouns for tempo feel** — "halftime groove," "double-time driving," "shuffle," "breakbeat" lock rhythmic feel far more reliably than BPM numbers or tempo adjectives like "slow" or "fast." These describe specific drum patterns Suno can interpret.
15. **Perceived tempo is controlled through lyrics, not the style prompt** — Suno delivers a single steady BPM per song. Perceived tempo changes come from lyrical density (short fragmented lines = slower feel, packed lines = faster feel), arrangement dynamics (instrument dropout = slower feel), and half-time/double-time drum patterns. The style prompt can request rhythm nouns and "tempo changes" as priming, but the actual perceived control lives in the lyrics field.

## Genre Keyword Ordering

Front-loaded terms dominate the generation. Whatever genre term appears first in the style prompt sets the primary sound — Suno treats it as the anchor, and everything after it is progressively more "flavoring."

When a genre should act as a secondary influence rather than the core sound, append qualifier words like "accents" or "undertones" to push it into the background. For example, `atmospheric swamp metal accents` tells Suno to use swamp metal as coloring rather than the main genre.

**Practical rule:** Put your dominant genre first. Demote secondary genres with "accents," "undertones," "influences," or "elements."

### First-Genre Dominance — Quantifying the Anchor

Community research is sharper than "first matters": **genre and subgenre tags collectively determine ~60-70% of arrangement output, with the first-position term holding the strongest single signal** (HookGenius 1000+ prompt analysis, 2026). A three- or four-genre fusion prompt is not a balanced stew. It's a dominant anchor in position one with increasingly faint color pulls from each subsequent term.

**Why this matters for counter-genre work:** When you're trying to push against a genre's gravity — accessible textures inside a heavy lane, slow pace inside a driving lane, acoustic framing under an electric identity — the counter-target genre has to occupy position one. Burying it at position 3 or 4 gives the counter-lane negligible arrangement influence, and Suno defaults to the first-position genre's conventions.

**Example:** `progressive metal, heartland rock, acoustic singer-songwriter` will read as progressive metal with trace heartland influence — the acoustic anchor contributes almost nothing. To actually produce an acoustic-leaning track, the compound must open `acoustic singer-songwriter, ...` with metal and heartland demoted behind it.

**Practical rule:** If you want genre X to drive the arrangement, X is position one. "Accents" / "undertones" / "influences" demote later terms but don't promote earlier ones — there is no way to get a buried genre to lead.

### Brass-Band Gravity — Aggressive Counter-Emphasis Required

When the prompt includes brass-band genre descriptors (`brass band`, `second-line`, `sousaphone`, `New Orleans funk-rock-brass fusion`, etc.), the brass gravity is exceptionally strong — strong enough that single-mention guitar or rhythm-section descriptors get buried in the gen output even when present in the critical zone.

**Production-confirmed pattern (LV Mask, 2026-04-28):**

| Descriptor approach | Result |
|---|---|
| Genre-first + single guitar mention at position 5 (`Modern New Orleans funk-rock-brass fusion, ... electric guitar accents, ...`) | Guitar buried in output; brass dominates the mix |
| `rock-funk fusion, funk, New Orleans second-line, brass-band, swing` (user test) | Brass-heavy output, guitar barely audible |
| Single substantive guitar mention promoted to position 2 (`New Orleans funk-rock-brass fusion, overdriven rhythm guitar with cutting accents, ...`) | Guitar still gets buried in observed gens |
| **`Guitar-driven New Orleans funk-rock with brass band horns, overdriven rhythm guitar with cutting electric lead, ...`** — **THREE explicit guitar mentions in critical zone (Guitar-driven framing + overdriven rhythm guitar + cutting electric lead)** | Guitar finally surfaces in the mix; brass and guitar coexist as intended |

**Why this matters:** Standard guidance (single substantive descriptor at position 2-3 to promote a sub-element) is inadequate for brass-band genre gravity. Brass-band conventions are deeply trained — Suno defaults to brass-led arrangements when any brass-band-genre descriptor appears, and only aggressive counter-emphasis (genre-modifier framing + multiple explicit descriptors in the critical zone) shifts the balance.

**Practical rule:** When prompting for brass-band-fusion genres where guitar (or any non-brass instrument) needs to surface in the mix, treat the counter-element as a genre-modifier first, then reinforce with multiple explicit instrument mentions in the critical zone. Do not assume single-mention promotion will work — it has been observed to fail repeatedly with brass-band gravity.

**Counter-intuitive guidance:** This may LOOK like over-correction (three guitar mentions in 200 chars feels heavy-handed). Production testing confirms it's the right level for brass-band gravity specifically. The over-correction concern is wrong here — brass-band gravity requires it.

### Genre Term Behavior Table

Specific genre terms produce specific results. This table documents what Suno actually generates for common genre keywords, based on production testing.

| Genre Term(s) | What Suno Produces | Notes |
|---|---|---|
| `progressive metal` | Dream Theater-style technical shred | Avoid unless you specifically want technical wankery |
| `progressive groove metal` | Mastodon-adjacent pocket grooves | Better choice for most prog-metal needs |
| `prog rock` | Softer, more atmospheric progressive sound | Good for builds, dynamics, and patient arrangements |
| `heavy swamp metal` | Down/Crowbar-style low-end weight | Reliable for southern heaviness |
| `heavy swamp metal power ballad` | Gentle verses that build to heavy | Communicates "power ballad with weight" without invoking theatrical/keyboard territory |
| `dark alternative rock, slow and heavy, raw emotional weight, spacious oppressive mix, claustrophobic atmosphere` | Non-metal heaviness with emotional devastation | Good for pushing a metal band into non-metal territory; works for songs about powerlessness rather than power |
| `post-metal, post-hardcore` | Isis/Cult of Luna patient builds | Adding post-hardcore introduces off-tempo, prog-adjacent moments |
| `speed metal` | Fast, aggressive, thrash-adjacent | Straightforward — does what it says |
| `hard rock` | Straightforward driving energy | Clean, uncomplicated rock foundation |
| `hard rock` + `NOLA second line groove` + `brass band accents` | NOLA parade groove with rock weight | The combination pulls toward parade-style rhythms |
| `crushing slow heavy swamp metal` + `pounding heartbeat kick drum` | Heavy, deliberate, single-tempo weight | Stacking slow/heavy modifiers locks Suno into a plodding pace |
| `prog rock` + `slow build then fade` | Atmospheric with proper decrescendo | One of the few reliable ways to get Suno to actually come back down |
| `Acoustic, intimate, solo voice with gentle guitar, bluesy, swampy, sparse and warm, quiet reflection, raw clean vocals, stripped down, empty room atmosphere` | Acoustic track that retains band identity | `bluesy, swampy` keeps NOLA identity; `empty room atmosphere` = reverb/space; explicitly exclude `heavy guitars, drums` in Exclude Styles |
| `heartland rock` | Accessible mid-tempo rock with Petty/Mellencamp/Springsteen character — chimey or mid-gain driven electric guitars, rock-forward without metal weight | **Safe rock term for Voice tracks** — no harsh vocal trigger. Good starting point when a clean-voice Voice clone needs rock energy without metal pull |
| `southern rock` | Rootsy rock with Allman/Skynyrd character — can pull slide/steel guitar as a byproduct of the genre association | Safe vocal-wise (no harsh-vocal triggers). Exclude `steel guitar` if you want to avoid the slide side. Pairs well with `heartland` to anchor toward the accessible end rather than jam-band end |
| `heartland southern rock` | Combined — intersection of accessible singer-songwriter rock with rootsy grit and drive | **Validated on Voice tracks** — clean folk-tagged Voice with "overdriven rhythm guitar with crunch" + "driving mid-tempo rock groove" as reinforcement produces rock presence without metal pull. Good for confessional rock songs that need both weight and accessibility |

### Era Tags as Sonic Targets

Era-specific descriptors in the style prompt give Suno a production aesthetic target that single descriptors can't match. Use instead of artist names to evoke a period's sound.

| Era Tag | What Suno Produces | Notes |
|---|---|---|
| `80s synth` | Analog synthesizers, gated reverb, drum machines | Pairs well with synthwave, new wave |
| `90s grunge` | Distorted Seattle-sound guitars, raw production | Alternative rock territory |
| `90s hip-hop` / `90s boom bap` | Golden age sampling, hard drums, vinyl texture | Classic hip-hop production |
| `90s R&B` | New jack swing era production | Smooth, polished, Motown-adjacent |
| `2000s emo` | MySpace-era emotional rock | Pop punk, confessional |
| `2010s trap` | Atlanta trap wave, 808s, hi-hats | Modern hip-hop production |
| `60s psychedelic` | Summer of love sound, analog warmth | Reverb-heavy, experimental |
| `70s disco` / `70s soul` | Dance floor funk, Blaxploitation-era warmth | Groove-heavy, warm production |
| `vintage` / `retro` | General throwback sound | Broad — pair with a decade for specificity |

**Practical rule:** Era tags are stronger than individual production descriptors. `90s R&B` achieves more than listing "smooth, warm, polished, swing drums" individually. Combine era tags with genre for maximum precision: `90s boom bap, conscious rap` or `80s synth, darkwave`.

### Dangerous Words and Keyboard Triggers

Certain words reliably pull Suno into unwanted instrumental territory — typically theatrical, keyboard/synth-heavy, or cinematic-light arrangements. Avoid these when guitars and bass should lead.

| Word/Phrase | What Suno Does | Fix |
|---|---|---|
| `baroque` | Maps to theatrical/classical keyboard territory — Disney-adjacent | Describe Baroque qualities without the word: Bach counterpoint = `intricate interlocking guitar and bass melodies`; minor key ornamentation = `dark minor key, precise and ornate` |
| `orchestral`, `orchestral accents` | Defaults to light/cinematic strings, not heavy | Specify HEAVY orchestral instruments explicitly: `cello, heavy strings, kettle drums` — these live in metal's frequency range |
| `cinematic` | Pulls keyboard/synth-heavy arrangements | Use `dynamic shifts`, `building from gentle to crushing` instead |
| `rock opera` | Pulls keyboard/synth-heavy, theatrical arrangements | Use `power ballad`, `dynamic shifts`, `building from gentle to crushing` instead |

**"Baroque" workaround in detail:** If the song concept calls for Baroque-influenced metal, never use the word. Instead, describe the specific qualities you want — `intricate interlocking guitar and bass melodies` for counterpoint, `dark minor key, precise and ornate` for ornamentation. For orchestral weight, specify instruments that live in metal's frequency range: `cello, heavy strings, kettle drums`. Avoid `orchestral` as a standalone descriptor.

## Exclude Styles Field

The Exclude Styles field (Pro/Premier only) is a separate input from the style prompt. Key behaviors:

- **Functions as probability reduction, not a hard ban** — excluded elements are less likely but can still appear. Treat it as strong guidance, not a guarantee.
- **In-prompt negatives also work:** "no [element]" at the end of the style prompt is an alternative or supplement. v5 handles these more reliably than v4.5.
- **Limit to 2-3 most important exclusions** — too many exclusions destabilize the arrangement and produce unpredictable results. Prioritize the exclusions that matter most for the song.
- **Combine with positive instructions** — telling Suno what you DO want is more reliable than only excluding what you don't. Use Exclude Styles as a safety net alongside positive vocal/instrument guidance in the style prompt.

### CRITICAL RULE: Excludes Defend Against Drift From the CURRENT Prompt ONLY

**Suno is stateless. It has zero knowledge of:**
- Prior generations of this song (regen iterations, earlier versions, previous Creates)
- Other bands' renderings of the same lyrics (e.g., if the user has both a Solitary Fire version and a Lenny's Voice version of the same poem, Suno generating one knows nothing about the other)
- The user's broader catalog, band profiles, genre lanes, or historical patterns
- Any context that isn't in the style prompt, Exclude Styles, lyrics, sliders, voice selection, or persona/audio input for this specific generation

**The ONLY inputs that influence Suno's output are the ones submitted with the current Create.** The Exclude Styles list should defend against drift risks that the CURRENT style prompt's own descriptors might introduce. Nothing else.

**Common violations to avoid when building exclusion lists:**

- ❌ "Defend against SF-DNA drift on this LV version" — Suno doesn't know SF exists. If metal-coded words aren't in the LV style prompt, metal won't creep in from the parallel SF version.
- ❌ "The earlier generation drifted toward X, so exclude X in the next attempt" — Suno doesn't remember prior generations. If the current prompt still contains descriptors that pull toward X, excluding X is valid. If the current prompt doesn't contain those descriptors, the exclusion is defending against a ghost.
- ❌ "The user's Band A catalog never uses instrument Y, so exclude Y on Band B's version of this song" — Suno doesn't know about Band A. Only exclude Y if the CURRENT prompt might pull it in.

**The correct question for every exclude candidate:** *"What in my current style prompt could plausibly pull Suno toward this element?"* If the answer is "nothing in this prompt pulls that way," the exclude is wasted exclusion-field budget.

**Parallel-band-rendering work is the highest-risk context for this error.** When a song exists in two band catalogs (same poem, different genre/voice rendering), the temptation is to frame excludes as "defense against the other band's version." That framing is always wrong — Suno cannot be influenced by a version it has no knowledge of. Build excludes fresh for each rendering based on that specific prompt's descriptors.

## Vocal Behavior and Triggers

### Scream/Harsh Vocal Triggers

Certain words reliably trigger unwanted screaming or harsh vocals, even when the intent is melodic:

- `metal` on its own (without melodic vocal guidance)
- `sludge`
- `doom`
- `!` in lyrics (exclamation marks push vocal delivery toward shouting/screaming)

**Fix:** Always pair heavy genre terms with explicit positive vocal instructions. For example, `heavy swamp metal, raw melodic singing` or `sludge metal, gritty male vocals, no screaming` (plus "screaming" in Exclude Styles). Telling Suno what you DO want from the vocals is more reliable than only excluding what you don't.

### "Technical" as a Modifier

The word "technical" behaves differently depending on what it modifies:

- `technical guitar riffs` → produces shreddy, noodly guitar work
- `rocking guitar riffs` → better choice for most heavy songs that need energy without wankery
- `driving technical bass` → produces slightly more interesting bass lines without going overboard; worth including as a standard ingredient in bass-heavy arrangements

## Instrument-Specific Guidance

### Drum Programming

Drum descriptors are highly context-dependent — the same term produces different results depending on surrounding genre and energy keywords.

- **"Second line" drums** shift meaning based on context: paired with slow + atmospheric terms, they produce a hip-hop pocket feel; paired with up-tempo + energetic + hard rock terms, they produce a NOLA parade groove
- **Splitting funk from drums:** To get funky bass and guitars without funk drums, describe the funk in the bass/guitar descriptors and keep the drum descriptors in metal territory (e.g., `funky bass groove, driving metal drums`)
- **Swing and groove patterns:**
  - `swinging drums` + `blues-metal intensity` → Bill Ward-style groove (loose, behind-the-beat swagger)
  - `pounding drums` → rigid, mechanical, metronomic feel (use when you want deliberate, machine-like precision)

### Bass Prominence (Known Limitation)

Suno cannot reliably produce bass-forward rock or metal mixes. This has been tested extensively:

- Requesting "bass-forward" or "prominent bass" in the style prompt produces marginal results at best — bass remains buried in the mix
- `bass and drums only, no guitar` combined with guitar in the Exclude Styles field was the most effective approach found, but this requires removing guitar entirely rather than simply featuring bass
- `funk metal` as a genre term triggers slap/pop bass (Flea-style), NOT overdriven fingerstyle (Geddy Lee-style) — there is currently no reliable way to get prominent overdriven bass in a full-band rock/metal context

**Treat bass-forward rock/metal as a known platform limitation.** If a song concept depends on prominent bass, consider the "bass and drums only" approach or accept that bass will sit in a typical supporting-instrument position in the mix.

### Instrument Bleed-Through

The style prompt sets a GLOBAL instrument palette. Instruments mentioned anywhere in the style prompt bleed into ALL sections regardless of section-level `[Instrument: ...]` tags. This is a fundamental Suno limitation:

- Section-level `[Instrument: ...]` tags CANNOT introduce instruments not in the style prompt — they can only emphasize instruments already in the palette
- Adding "accents" after instrument names (e.g., "brass accents") reduces but does not eliminate bleed
- Placing section-specific instruments at the very END of the prompt minimizes but does not prevent bleed
- **Recommended workflow for section-specific instrumentation:** (1) Generate with all instruments in the prompt (accepting bleed), (2) Extract stems (Suno Pro splits into up to 12 stems including a dedicated brass stem), (3) Mute/remove unwanted instrument stems per section in a DAW like Audacity
- **Note:** External DAW editing is a one-way operation — once you edit outside Suno, you lose Suno's editing capabilities on that version

## Dynamic Control via Style Prompt

Style prompt directives for energy and dynamics override lyric-level energy tags (like `[Building]` or `[Fade]`). This is powerful but requires careful handling.

### Build and Climax

- `slow massive build to crushing climax` makes Suno build ALL the way through the song, steadily increasing intensity. It will ignore any fade or cooldown tags in the lyrics — the style prompt's arc instruction wins.

### Decrescendo and Comedowns

Getting Suno to bring energy back down is harder than building up. Patterns that work:

- `slow build then fade` — tells Suno the arc goes up AND comes back down
- `dynamic shifts loud to quiet` — encourages contrast rather than one-directional energy
- `prog rock` + `slow build then fade` — the prog rock genre context supports patient dynamics, making the fade instruction more effective

**Key insight:** If a song needs to come DOWN after a peak, the decrescendo instruction must be in the style prompt. Lyric tags alone are not enough to counteract a style prompt that implies continuous build.

### Three-Phase Dynamic Arc (Quiet → Massive → Quiet)

Getting Suno to execute a full quiet-to-massive-to-quiet arc requires redundancy. State the arc **twice** in the style prompt using different phrasing: `building from gentle to crushing then returning to gentle` AND `dynamic arc quiet to massive to quiet`. One statement is not enough — Suno latches onto "crushing" and rides it out through the end of the song. The redundancy forces Suno to register the full arc rather than just the peak.

### Brass-Out-At-Outro Limitation (Brass-Band-Fusion Genres)

**Documented platform limitation across v5 Pro and v5.5 Pro: brass-fade-out instructions in section tags or style prompts are unreliably honored for brass-band-fusion genres.**

Two production tests on the same source song confirmed the failure:
- **SF rendering on v5 Pro** (swamp-metal + NOLA brass fusion, 2026-03-23) — used in-bracket per-section instrumentation tags including `[OUTRO — return to slow, sparse intro feel; sung; no brass; only final word whispered]`. Result: horns persisted throughout the song instead of fading at the outro. Documented as the primary failure mode at publish time.
- **LV rendering on v5.5 Pro** (Galactic-style modern NOLA funk-rock-brass fusion, 2026-04-28) — used v5.5 Pro's "significantly improved prompt accuracy," in-bracket per-section instrumentation (`[Intro] [Instrument: bare rock guitar, no brass]` ... `[Outro] [Instrument: no brass, bare rock guitar]`), AND stacked absence descriptors at intro/outro in the style prompt. Result: same failure — brass hits persisted into the outro and even after the whispered "nothingness" through fade.

**Implication for Pro-tier users:** No surgical post-gen fix is available without Studio tier (Replace Section / 12-track stem extraction / Remove FX). Pure prompt-side techniques cannot reliably engineer brass-fade-out for brass-band-fusion genres. Re-rolls don't fix it because the failure is consistent across attempts — Suno's brass-band genre gravity overrides outro fade instructions specifically.

**How to architect around this:**
- **Plan for brass-persisting** when building brass-band-fusion songs. Don't expect the bookend-sparse three-act dynamic to land via prompt instructions alone.
- **Lyric-level adaptation:** if the song concept needs a sparse outro, consider whether the song works as a brass-band-fusion at all, or whether a different sub-genre anchor (rock-with-horn-section, NOLA R&B, etc.) would land the dynamic better than brass-band-led territory.
- **Subjective evaluation:** the build-up half of the three-act dynamic (Intro → V1 → Pre-Chorus carnival peak) DOES land cleanly in brass-band-fusion genres on v5.5 Pro. The failure is specifically the back-half release. Songs whose structural success doesn't depend on a sparse outro are unaffected.
- **Studio-tier path** (NOT available to Pro users): post-gen 12-track stem extraction allows muting the brass stem on intro/outro, with Replace Section available for surgical re-gen of just the bookends.

**The 8th LV dynamic archetype (build-peak-elevated-settle)** is a direct consequence of this limitation — outro can't return to bookend-sparse when brass keeps playing. This archetype emerged organically from the constraint rather than as an intentional design choice.

## Slider Guidelines

### Weirdness and Style Influence by Song Type

These are starting-point ranges based on production testing. Adjust per song, but these give a reliable baseline.

| Song Type | Weirdness | Style Influence | Notes |
|---|---|---|---|
| Acoustic/stripped | 40 | 80 | Lower Weirdness for compliance; high SI to honor the style prompt's genre descriptors |
| Structured songs (verse-chorus) | 50-55 | 75-80 | Higher Style Influence keeps structure tight |
| Dark alternative | 50-55 | 75-80 | Standard settings; may need lower Weirdness for compliance when pushing a metal band into non-metal territory |
| Through-composed | 55-60 | 70-75 | Slightly looser to allow organic flow |
| Funk-forward | 60 | 65-70 | Weirdness adds rhythmic surprise; lower SI lets funk breathe |
| Post-metal | 60-65 | 65 | Needs room for patient builds and textural exploration |
| Prog | 65-75 | 65 | Higher Weirdness encourages unexpected transitions |
| Circular / agitated | 75 | 65 | High Weirdness for unsettling, looping energy |

**General principle:** Weirdness adds unpredictability and non-obvious choices. Style Influence controls how tightly Suno follows the prompt versus doing its own thing. For conventional songs, keep SI high. For experimental work, back SI off and let Weirdness drive.

**Weirdness is strongest during Extend and Bridge generation** — this is the primary cause of style drift in extended tracks. High Weirdness during Extend is more destabilizing than during initial generation. Keep Weirdness conservative during Extend operations; too-high Weirdness during Replace Section can also cause Persona/Voice identity shifts. Use callback phrasing ("continue same chorus energy") and re-inject genre/mood every 1-2 extends to prevent drift.

**Style Influence above ~80 plateaus** — increasing further rarely improves genre accuracy, and can reduce vocal phrasing variation especially in vocals.

### Default Weirdness Normalizes Counter-Genre Prompts

JG BeatsLab's v5.5 testing documents a default-Weirdness behavior that matters specifically for counter-genre work: _"v5.5 doesn't refuse niche genres — it reformats them. Give it a dungeon synth prompt and it will accept it, then quietly pull the output toward a polished, cinematic equilibrium."_ JG's practical guidance: _"Increase Weirdness for unusual fusions. The default Weirdness setting tries to normalize everything, which defeats the purpose of genre blending."_

This is the core counter-genre problem. Default Weirdness (50-55) quietly normalizes unusual descriptor combinations back toward Suno's trained equilibrium — polished, cinematic, conventionally-arranged. For prompts that mix against genre gravity (accessible inside heavy, slow inside driving, acoustic inside electric), push Weirdness to **60-70** to give the model permission to honor the unusual combination rather than reformatting it.

This supersedes earlier conservative-Weirdness-for-accessibility guidance in this document. The accessibility problem wasn't Weirdness — it was genre-gravity pulling output back to the first-position anchor's defaults. Higher Weirdness attacks that normalization directly.

**Note:** The Extend-drift caution above still applies — higher Weirdness during Extend is more destabilizing than during initial generation. Use elevated Weirdness at the front end of the song, keep it conservative during Extend operations.

## Counter-Genre Prompting

Counter-genre prompting is when the desired output works **against** the gravity of the named genre — accessible clean guitars in a hard-rock prompt, a slow deliberate pace in a driving prompt, acoustic textures under an electric framing. Suno's default behavior is to honor genre conventions, and every new descriptor you add has to fight the first-position genre's gravity. Three techniques applied together reliably shift the arrangement instead of just decorating it.

### Displacement-Budget Descriptors

Adding `clean guitars` to a heavy-rock prompt doesn't remove the power chords — it just adds cleanness _alongside_ them. The power chords survive because nothing structurally displaces them. To actually displace an unwanted instrument voicing, fill the instrument's role-slot with a **structurally incompatible** descriptor — one that can't coexist with what you're trying to avoid.

| Wanted | Unwanted | Weak ask (doesn't displace) | Strong ask (displaces) |
|---|---|---|---|
| Accessible guitar texture | Power chords | `clean guitars` | `fingerpicked arpeggiated voicings` |
| Spacious feel | Wall-of-sound | `spacious mix` | `sparse instrumentation, single-guitar verses` |
| Restrained dynamics | Full-band bombast | `controlled dynamics` | `subdued mid-range, no full-band payoff` |

Think of the descriptor budget as a **displacement budget**: each descriptor either crowds out its opposite or just sits next to it. Descriptors that occupy the same role-slot and can't structurally coexist are the ones that move the arrangement. Descriptors that name a quality without naming a form are weaker — Suno can honor `clean` while still deploying power chords.

Production observation (session-14 LV track): `fingerpicked arpeggiated voicings` produced the first fingerpicked section across any iteration of the song. Prior attempts using `clean guitars` had never displaced the power chords. Single-observation data, not A/B — but consistent with the displacement framing.

### Triple-Signal Tempo Stacking

Rhythm nouns (`halftime`, `double-time`, `shuffle`, `breakbeat`) land more reliably than tempo adjectives (`slow`, `fast`) — this is documented above. The counter-genre extension: stack **three aligned signals** simultaneously so genre-gravity can't overpower any single one of them.

1. **Genre with aligned tempo default** — pick a genre whose native tempo already points where you want to go. `slowcore`, `doom`, or `dirge` for slow; `speed metal`, `breakbeat electronica` for fast. Using a counter-tempo genre forces the other two signals to fight it.
2. **Numeric BPM approximation** — give a specific number even though Suno treats it as loose guidance. Numbers anchor the direction; they don't lock the result.
3. **Rhythm noun** — specify the rhythmic feel directly: `halftime feel`, `driving quarter-note pulse`, `swung eighth-note groove`.

Example counter-genre slow prompt against a driving rock identity: `heartland rock at 72 BPM halftime feel with patient southern slow-build dynamics` stacks all three (genre with slower default, BPM number, rhythm noun).

Production observation (session-14 LV track): switching from single-signal (`slow`) to triple-signal stacking dropped felt tempo ~6 BPM, raw tempo ~32 BPM, and improved halftime cleanness from a 2.2× non-clean ratio to a 1.95× near-clean ratio. The strongest confirmed-win technique of the three.

### 6/8 and 12/8 Compound Meter

Time signature support was added in the Suno Studio 1.2 update (Feb 2026). Compound meter (6/8, 12/8) subdivides each beat into threes rather than twos — so at the same numeric BPM, a 6/8 feel perceptually reads slower than a 4/4 feel, because the listener counts triplet subdivisions and the "pulse" lands more like a lilt than a drive. This is a general music-theory fact, not a Suno-specific property, but it gives a second lever on perceptual tempo when genre-gravity keeps pulling the numeric BPM upward: instead of fighting for a lower number, change the meter and let the triplet subdivision slow the feel.

**Tag form:** Append `[6/8]` or `[12/8]` to the style prompt or as a section metatag. Time signature support in the Studio generator is the underlying feature; in the Legacy editor (Pro tier) the tag form is what's available.

Production observation (session-14 LV track): inconclusive. Numeric BPM did drop but the felt subdivision still landed closer to 4/4 halftime than to a 6/8 lilt. Needs isolated testing on a song where the compound meter is the only tempo-perception lever being pulled — session-14 stacked it with triple-signal tempo and displacement descriptors, so the 6/8 contribution can't be isolated.

### Synthesis — All Three Together

A counter-genre prompt deploying all three techniques in their right slots looks like:

```
acoustic singer-songwriter, heartland rock at 72 BPM halftime feel with patient southern slow-build dynamics,
fingerpicked arpeggiated voicings, subdued mid-range, no full-band payoff, [6/8]

Weirdness: 65 | Style Influence: 75
```

- **Position 1 anchor** — `acoustic singer-songwriter` — the counter-lane, not the electric default
- **Triple-signal tempo** — genre (heartland, slower default than prog or speed), BPM (72), rhythm noun (halftime feel) all aligned
- **Displacement descriptors** — `fingerpicked arpeggiated voicings`, `subdued mid-range, no full-band payoff` — occupy role-slots that the unwanted qualities would need
- **Compound meter** — `[6/8]` as a second lever on perceptual slow
- **Elevated Weirdness (65)** — permission for Suno to honor the unusual combination instead of reformatting to polished cinematic defaults

Any one of these alone can fail. Applied together they build redundant pressure against genre gravity — if one signal gets overridden by the anchor, the others hold the line.

## Persona Style Prompt Integration

The Persona auto-populates the Style of Music field. Song-specific prompts should **build on** this base, not replace it. The Style Prompt Builder should assume the Persona's Styles content is already present and add song-specific elements on top. The Persona's Styles field contains universal band DNA — the sonic identity that should be consistent across all songs. Song-specific elements (odd time signatures, tempo changes, brass accents, genre departures) get layered per-song on top of that foundation.

### Persona Interaction Guidelines

- **Edit the auto-filled Style of Music intentionally** — the Persona populates it, but don't just leave it and pile on. Review and trim.
- **Keep style simple when Persona is active:** 1-2 genres, 1 mood, 2-4 instruments max. The Persona already carries vocal identity and character — the style prompt is the producer brief, not the artist identity.
- **Change ONE variable at a time** — adjust either the music direction OR the Persona settings, not both simultaneously. This isolates what's working vs. what's not.
- **Mental model:** Persona = artist identity (vocals, character); Style prompt = producer brief (sonic direction for this specific song).

### Voices Interaction Guidelines (v5.5, replaces Personas)

In v5.5, **Voices** succeeds Personas for vocal identity. Voices is actual voice cloning (from a 15s-4min audio sample with anti-deepfake verification), while Personas is style essence capture from a source generation. **Style Personas are NOT gone** — they coexist within the Voices tab in v5.5. Both features work on v5.5; Personas also work on v4.5/v5.

- **Drop gender descriptors when using Voices** — "male vocals", "female singer", etc. are redundant because the Voice already defines these. This frees characters for production detail.
- **Audio Influence for Voices is use-case dependent** — start at 40-60% for balanced voice + quality. Go higher (60-70%) if voice identity is paramount, lower (30-40%) if voice is just flavoring. Do not exceed 70% without accepting quality trade-offs — see the Voices Audio Influence table in the v5.5 Pro section above.
- **Pairs well with delivery metatags** — `[Whispered]`, `[Belted]`, `[Breathy]`, `[Raspy]` etc. Voice sets *who* sings, metatags set *how* they deliver each section.
- **15s-4min audio sample required** plus anti-deepfake verification (you must prove you own or have rights to the voice).

### Custom Model Interaction Guidelines (v5.5)

Custom Models let you train Suno on your own tracks to establish a production DNA. Think of the Custom Model as "producer" and the prompt as "songwriter."

- **Drop generic production descriptors your model already knows** — if your Custom Model was trained on lo-fi indie tracks, "lo-fi warmth" is redundant in every prompt. Use those characters for song-specific direction instead.
- **Train separate models for separate styles** — mixing genres in training data confuses the model. A "dark electronic" model and an "acoustic folk" model will each outperform a single model trained on both.
- **Voice + Custom Model is the most powerful combo** — who sings (Voice) + what style (Custom Model) + detailed prompt (creative direction). This is the full v5.5 personalization stack in action.

**Prompt strategy shift with Custom Models:**
When a Custom Model is active, the priority order changes from genre-first to **mood/production-first** since genre is already encoded in the model. Simpler, more natural-language prompts may produce better results than highly detailed tag-heavy prompts because the model already handles foundational style characteristics.

**Optimal formula with Custom Models:** MOOD + PRODUCTION TEXTURE + ENERGY/TEMPO + SPECIFIC INSTRUMENTS + VOCAL DIRECTION

**What becomes redundant:** Base genre tags, broad stylistic descriptors matching training data, foundation-level production characteristics. Use that freed prompt budget for mood modifiers, production specifications, and contextual modifiers like 'cinematic', 'anthemic', 'intimate'.

- **Privacy/consent note:** Voices and Custom Models consent grants Suno permission to use your data for training their global models. Not optional, not a private silo.

## Cover Feature

Cover re-performs an existing song in a new style — it preserves the melody, lyrics, and structure while changing genre, instrumentation, vocal character, and production. Cover prompts use production language, clear genre descriptors, and specific instrumentation.

**CRITICAL: Covers are NOT eligible for commercial use — even on your own songs.** For commercial releases, create a fresh generation instead. This is a Suno platform restriction, not a suggestion.

## Persona and Inspo Playlist Behavior

### Inspo Playlist Warning

Using your own songs as Inspo playlist entries homogenizes the sound across generations. Suno pulls tonal and structural patterns from Inspo tracks, which flattens out the distinctiveness of new songs. **Drop Inspo when a song needs its own identity** — particularly for songs that are meant to stand apart from the rest of a catalog.

### Persona / Audio Influence on Era

Personas pull the overall sound toward the era of the source song used to create them. A persona built from a 70s-sounding track will drag new generations toward 70s production aesthetics, even when the style prompt targets a different era.

- Reducing Audio Influence to 10-15% helps but does not fully overcome the era pull
- For era-specific pieces where production style matters, consider generating without a persona entirely
- Alternatively, create era-specific personas — a "modern" persona and a "vintage" persona, for example — rather than fighting a single persona's baked-in era bias

**Note on Voices (v5.5):** Voices replaces Personas in v5.5. Because Voices is actual voice cloning rather than style essence capture, it carries less era bias than Personas -- the Voice contributes vocal tone without dragging production aesthetics from a source song. This makes Voices more flexible for era-specific work.

### Audio Influence Slider Behavior

The Audio Influence slider controls how strongly the persona's source audio shapes the generation. The effective range is **15-25%** — values outside this range are either too detached or produce diminishing returns.

| Audio Influence | Behavior |
|---|---|
| 15% | Nearly loses persona identity — too detached for most uses |
| 20% | Holds identity loosely — allows significant genre departure. Use for experimental tracks or era-specific pieces where the persona's default era would interfere |
| 25% (default) | Strong persona anchor — the standard setting for both typical tracks AND acoustic/stripped songs |
| Above 25% | Diminishing returns — 40% tested, did not override an incompatible style prompt |

**Critical finding:** Acoustic and stripped-down songs can handle full 25% Audio Influence. The style prompt's genre descriptors override the persona's instrumental heaviness — the persona contributes only vocal identity. Only reduce Audio Influence when pushing into a different *heavy* genre where the persona's heaviness would compete with the target genre's heaviness.

## Iteration Best Practices

- **Generate 3-5 versions** per prompt before modifying — v5 produces more varied results than v4.5, and the desired result often appears on the 2nd or 3rd generation
- **Change only 1-2 variables** per iteration — isolate what works vs. what doesn't
- **Style Influence above ~80 plateaus** — increasing further rarely improves genre accuracy
- **For v5 Pro users:** Suno Studio offers section editing, stem separation (up to 12 stems), alternates, and warp markers. For structural problems (wrong arrangement, bad section), use Studio editing rather than re-prompting entirely

## Reference Track Translation Guide

When a user says "sounds like X meets Y," decompose into concrete attributes. **Never put artist names directly into the style prompt** — describe the sonic qualities of the era and style instead.

### Confidence Check (Critical — Prevents Hallucination)

Before decomposing any reference, honestly assess: **do you confidently know this artist/song well enough to accurately describe their distinctive sonic characteristics?**

- **If confident** — proceed with decomposition using the extraction framework below
- **If uncertain** (obscure artist, very recent release, regional/niche genre, or you're unsure of specific details) — **use web search first** (if a search tool is available) to research the artist's sound, genre, instrumentation, vocal style, and production approach. Then decompose from researched facts, not guesses.
- **If uncertain and no search available** — tell the user honestly: "I'm not confident I know [artist] well enough to describe their sound accurately. Can you tell me what you like about their sound — the vibe, the instruments, the vocals?" Then decompose from the user's description instead.

**Never fabricate sonic details for an artist you don't confidently know.** A wrong decomposition produces a style prompt that sounds nothing like what the user intended — and they won't know why until they hear the result.

### What to Extract from a Reference

- **Genre/subgenre** — what musical tradition?
- **Era/production style** — vintage analog? modern digital? lo-fi?
- **Vocal character** — what makes their voice distinctive?
- **Instrumentation signature** — what instruments define their sound?
- **Energy/dynamics** — how does the song move? build? stay flat? explode?
- **Emotional tone** — what feeling does it evoke?

### Example Decomposition

- "Bon Iver meets Radiohead" → falsetto vocals, ambient electronics, acoustic guitar foundation, experimental song structures, melancholic beauty with electronic tension, lo-fi warmth with glitchy textures
- "Dolly Parton meets Daft Punk" → country storytelling over electronic production, warm female vocals with robotic harmonies, acoustic meets synthesized, playful but polished

Always show the user your decomposition before building the prompt so they can confirm or correct your interpretation.

## Community Research Sources

> **Last updated:** April 20, 2026. These informed the v5.5 findings above. Verify against current Suno behavior.

- [HookGenius: 1000+ Prompt Analysis](https://hookgenius.app/learn/suno-style-tag-research/) — Tag count sweet spot (5-8), "cinematic" modifier, production tag findings, conflicting tag behavior
- [HookGenius: Complete Suno Prompt Guide 2026](https://hookgenius.app/learn/suno-prompt-guide-2026/) — Genre tags carry 60-70% of arrangement influence, first-position dominance rule, descriptor specificity
- [HookGenius: Suno Tempo BPM Guide](https://hookgenius.app/learn/suno-tempo-bpm-guide/) — BPM number as approximate guidance, rhythm-noun vs. adjective, dual specification pattern
- [HookGenius: Negative Prompting Guide](https://hookgenius.app/learn/suno-negative-prompting/) — Exclude Styles behavior and in-prompt negatives
- [JG BeatsLab: 7 v5.5 Behaviors](https://www.jgbeatslab.com/ai-music-lab-blog/suno-v5-5-behaviors-every-creator-needs-to-know) — "Polished cinematic equilibrium" normalization behavior, Weirdness guidance for unusual fusions
- [JG BeatsLab: Voices Day One Testing](https://www.jgbeatslab.com/ai-music-lab-blog/suno-v5-5-voices-tested) — Voices Audio Influence real-world ranges, Skill Level dropdown
- [Blake Crosley: v5.5 Reference (MILO-1080)](https://blakecrosley.com/guides/suno) — Meta tags, Style-of-Music field, numeric BPM as approximate guidance
- [AudioNewsRoom: Voices/Custom Models Consent](https://audionewsroom.net/2026/03/suno-v5-5-what-you-give-up-to-make-it-yours.html) — Privacy analysis
- [JackRighteous: Creative Control Sliders](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/creative-control-sliders-suno-v5) — Genre-specific slider ranges, Extend drift findings
- [Suno Official v5.5 Docs](https://help.suno.com/en/articles/11362305) — What's New, Voices, Custom Models, My Taste
- [Suno Studio 1.2 Release Notes](https://suno.com/blog/studio1_2) — Time Signature support, Warp Markers, Remove FX, Alternates (Feb 2026)
