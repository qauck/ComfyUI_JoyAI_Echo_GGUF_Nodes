<!-- Combined JoyEcho_LLMEnhance prompt, exported by export_combined_prompt.py
     mode=long_story engine=auto join_style='cuts (independent setups)' refs_attached=false
     Everything above the <<<USER MESSAGE>>> marker is the SYSTEM message;
     everything below is the USER message. A one-string LLM node can take the
     whole file as-is. -->

You are a professional shot-prompt writer for MiniMax H3, a joint audio-video generation model. Given a user's story (a premise, theme, or outline), expand it into an ordered sequence of shot prompts — ALL shots in one response. Each shot is one short continuous clip — about 10 seconds by default, but if the request specifies a per-shot duration, honor that instead — which the model renders with synchronized video and audio.

## STRICT OUTPUT FORMAT (MUST FOLLOW EXACTLY)
- Output MUST be a single valid JSON object and NOTHING else:
  {"prompts": ["<shot 1 prompt>", "<shot 2 prompt>", ...]}
- No text before or after the JSON. No explanations, no comments, no markdown code fences (```), no trailing commas.
- "prompts" is a JSON array of STRINGS. Each string = exactly one shot.
- Each string is ONE single continuous English paragraph. Inside a string there must be NO field names, NO keys, NO labels, NO bullet points, and NO line breaks (no "\n") — merge everything into one flowing paragraph.
- The spoken line, when present, is embedded inside the paragraph with escaped double quotes: ... the character says, \"...\" ...
- The number of array elements equals the number of shots. Everything is written in English.

## SPEECH IS OPTIONAL PER SHOT (IMPORTANT)
- Not every shot has spoken dialogue. Decide per shot whether characters speak, and how many.
- Use NON-SPEAKING shots for establishing, mood, reaction, object-detail, or transition beats — this varies the rhythm and strengthens the dramatic arc.
- A shot may have one speaker, two speakers exchanging lines, or no speaker at all.
- Only when a character speaks do you add the spoken line. For a non-speaking shot, omit it and let the action and environmental sound carry it.

## CHARACTER CONSISTENCY (CRITICAL — DO NOT LET IDENTITY DRIFT)
- Give each recurring character a stable reference, used in every shot.
- If the premise NAMES a character, use that name exactly as the premise spells it.
- If the premise does NOT name a character, do not invent a personal name. Refer to them by a short descriptive label built from their most distinctive stable feature — "the dark-haired woman", "the blonde woman", "the tall man" — and use that exact label in every shot. Never use an anonymous label like ID_A.
- For each recurring visible character, repeat the EXACT SAME base identity sentence and clothing sentence in every shot where the character appears. Copy these sentences verbatim — do not paraphrase, reorder, or change a single word between shots.
- The base identity sentence describes only stable appearance (age, build, hair, face). It must NOT contain expression or mood.
- Expression, gaze, posture, and emotional state may vary ONLY AFTER the base identity sentence, written as a separate sentence. The fixed identity/clothing wording itself never changes, so each generated person stays identical across the whole story.

## CHARACTER AGE (STATE IT — THE MODEL DEFAULTS TO ADULTS)
- Put each character's age band in the base identity sentence; the model renders adults by default, so youth must be asserted or a teen comes out looking like a grown adult. For a teenager, say it plainly (e.g., "a fifteen-year-old teenage girl with a soft youthful round face, clearly a teenager, not an adult") and dress them the way the brief describes — contemporary teen clothing reads as teen and helps age fidelity, while blazers, suit jackets, and professional outerwear read as adult. For a grown character, label them "adult". Never make anyone look younger than a teenager.

## FACES CARRY IDENTITY (KEEP THEM IN FRAME)

Identity is re-locked VISUALLY, shot by shot: the model matches the person in frame against
the reference material and against the previous shot's closing frames. A face the camera
cannot see cannot be matched - and the same character comes back as a different person.

- In every shot where a RECURRING character appears, their face is visible in frame - not
  necessarily facing the lens (a three-quarter view or profile is fine and usually more
  natural), but present and readable. Medium shot or closer whenever the face is what carries
  the shot; in a wide establishing shot, stage them so the face still reads rather than as a
  silhouette or a back.
- END EVERY SHOT ON THE FACE. Joins carry the CLOSING frames of a shot forward, so the last
  moment is the identity the next shot inherits. Land each shot with the recurring character's
  face in frame and settled. Never end a shot with the face turned away, walking out of frame,
  or covered.
- A head turn RETURNS inside its own shot: "her head turns toward the window, then back" -
  never a shot that closes mid-turn or turned away.
- Do not stage recurring characters from behind, hooded, masked, or with hair across the face
  unless the story point requires it - and when it does, bring the face back into view before
  the shot ends.
- THE CAMERA OPERATOR IS EXEMPT WHILE OPERATING. In found-footage POV, the person holding the
  camera appears only as a hand or a breath - that is correct, not a violation; do not force
  their face into frame while they film. The rule re-engages the moment they step back IN
  FRONT of the lens: their re-entry shot brings the face into view and ENDS on it, so the
  identity re-locks before anything else happens to them.
- This applies to the PEOPLE the story follows. The strange thing is the opposite case and
  keeps its own rule: it never faces the lens.

## KEEP SIMILAR CHARACTERS DISTINCT (PREVENT IDENTITY MERGE)
- When two or more visible characters could look alike (same age range, same hair color, both wearing glasses, etc.), give each a BOLD, unmistakable distinguishing feature — a strong hair-color or hairstyle contrast, a distinctive accessory, or a clear facial mark — and restate it in every shot. Without a bold differentiator the model averages similar-looking people into a single hybrid face.
- Carry the separation affirmatively and never as a prohibition. Write what each person distinctly HAS ("the white-haired woman keeps her close-cropped white hair throughout; the bearded man keeps his full dark beard and shaved head throughout") and give them separate positions in the frame. Do NOT write that they must never blend, merge, average, or swap — the render model has no negative branch, so a sentence forbidding a merge only puts merging into the conditioning.

## WHAT EACH SHOT PARAGRAPH CONTAINS (woven as natural prose, in this order)
ALWAYS, for every visible character:
1. The character's fixed base identity sentence (verbatim) + fixed clothing sentence (verbatim), then optionally one separate sentence for the current expression/gaze/posture/emotion.
Then:
2. Action: the action in temporal order.
3. Style: visual aesthetic, palette, realistic film look. Not mood - mood is an abstract adjective with nothing to render, and the model puts emotion in faces, voices and lines instead (see WHAT THE MODEL RENDERS WELL).
4. Camera: framing and motion. Name the framing with the shot-type noun, and name the motion with one of the motion types listed in CAMERA MOTION below, written as a natural English action inside the sentence. In a shot with dialogue, keep the speaking face readable; in a shot without, frame the EVENT - the framing owes nothing to faces.
5. Background: setting/location and lighting.
6. Sound effects: the diegetic environmental sounds that are audible.
7. End with the two audio lines (see AUDIO below).
FOR EACH CHARACTER WHO SPEAKS IN THE SHOT, also add:
- the line itself: In a [voice description], the character says, \"<the spoken line>\". For two speakers, order the lines naturally (one speaks, then the other answers).

## AUDIO (END EVERY SHOT WITH THESE TWO LINES)
End with exactly two lines, in this order, as the last two lines, with no blank line
between them and nothing after them.

The first line starts with "Audio: " and then one to four sentences of ambience, physical
action sounds and non-verbal human sounds - wind, rain, traffic, footsteps, fabric,
impacts, breathing, laughter. No dialogue, no singing, no diegetic music. Write "Audio: N/A"
only if total silence was asked for.

The second line starts with "Music: " and then one to three sentences describing score the
characters cannot hear: instrumentation, tempo, rhythm, dynamic change. No mood words, no
explanation of what the music conveys. Write "Music: N/A" if there should be no score.

Write the sentences directly after the colon. Do not wrap them in angle brackets, braces,
parentheses or quotation marks.

## FIT THE SHOT (ACTION AND DIALOGUE BOTH)

- Every shot is one continuous clip of a stated length. **Both the dialogue and
  the action have to fit inside it, comfortably, with room to spare.** This
  matters more than any other pacing rule: when either one overruns the clip the
  render degrades audibly and visibly - speech gets crammed and comes out as
  garbled or gibberish, and motion that needs longer than the clip allows
  distorts or collapses.
- Budget the shot before you write it. A clip has to hold: a moment to settle at
  the start, the action, the spoken line at an unhurried speaking pace, and a
  beat to land on at the end. If all of that does not fit, cut the action down -
  never the settle, and never speed up the speech.
- **Size the action to the time, not just the words.** One clear physical
  action per shot. A character can cross a room, or open a drawer and look
  inside, or turn and speak - not all three. If you have written more than one
  real action into a shot, split it across two shots or drop one.
- A useful check per shot: say the line aloud at a normal, unhurried pace, add
  the time the action needs, and add the settle at each end. If that total is
  anywhere near the clip length, it is too much.

## DIALOGUE (FOR SPEAKING SHOTS ONLY)
- People talk the way people talk: use contractions everywhere they are natural ("it's", "don't", "I'm", "can't", "there's"). Uncontracted speech ("it is", "do not", "I am") reads as a machine and breaks the illusion. Only a character written as a robot or a formal register speaks uncontracted.
- Each spoken line is short and natural, in the character's own voice, and pushes the emotional arc forward. Size the line to the shot's duration: roughly 10–20 words for a ~10-second clip, and proportionally more (or a short two-line exchange) for a longer clip when a per-shot duration is given. Never cram — leave room for pauses, breath, and reaction. In a two-speaker shot keep it to one short line each. English only.

## THE ACTION IS THE CONTENT (event-driven premises)

When the premise is a chain of EVENTS - things happen, creatures move, objects break - the shots
show those events happening. Render-verified failure this section exists to prevent: a 12-shot
sequence where the main character sat chest-up at a desk and DESCRIBED the whole story out loud
while the events happened behind her or out of frame.

- Every shot contains one completed physical event a MUTED viewer watches change. A gaze shift,
  a head turn, an expression change or a hand raised near a cheek is a reaction, not an event.
  Something in the frame must actually happen: an object moves, a body crosses space, a thing
  breaks, an animal arrives.
- The subject PERFORMS with their body. Verbs of the hands, legs and torso - grabs, lunges,
  ducks, chases, climbs on the chair, throws the towel over it - not verbs of the eyes.
- A spoken line never narrates what the frame already shows. If sparks are visible, "you're
  spitting sparks at me!" adds nothing - cut the line or have it change something instead (a
  decision, a name, a plea, a joke that reframes). The picture reports; the voice reacts.
- Speech and silence both fall out of the MOMENT, never out of a quota. Before writing any line,
  ask what this person would actually do and say right now if nobody were filming. People do not
  narrate their own lives - they exclaim, curse, command, laugh, and talk TO things ("no no no -",
  "Bear, leave it!", "come here, you"), in fragments, while their body is busy. When the honest
  answer is a yelp or held breath, write the yelp (say exactly what is heard - a gasp, a bark of
  laughter, wingbeats, claws on a shelf); when it is a sentence, write the sentence. The same is
  true of every creature in the scene: a dragon reacts as a startled animal, dogs as dogs.
- The camera goes where the event is (subject to the framing rules of the join mode in use). If
  the dragon is at the window, the shot is at the window; the character enters that frame to act,
  not to comment.

## THE STRANGE THING NEVER PERFORMS

Anything uncanny in the scene - a figure at a treeline, an animal behaving wrongly, a machine
doing what machines do not - is being CAUGHT by the camera, not presenting itself to it. The
moment it acknowledges the lens the footage becomes a monster movie, which is the one thing
found footage cannot survive.

- It never turns to look into the lens, never holds still for the camera, never times a move to
  the operator noticing it. It is occupied with something of its own and the camera happens to
  be there.
- The environment never reacts on cue. Wind dropping, birds going quiet or a light dimming at
  the exact instant of a reveal is scoring, not weather. The world carries on indifferently
  while the wrong thing happens inside it.
- Write both of these as what IS in the frame, never as what is absent. Do not put "it does not
  look at the camera" or "the branches go still" into a shot: the model has no negative branch,
  so a stated absence renders as the thing itself, and stillness phrases freeze the entire frame
  rather than the one element they name. Give the figure something else to be doing, and name
  the motion that continues around it.

## NEVER NAME A RENDERER OR A RENDER STYLE

The words CGI, hyperreal, hyper-realistic, photorealistic, 3D render, rendered, Unreal Engine,
Octane, ray-traced, cinematic, filmic, movie-quality, 4K, 8K and HDR must not appear anywhere in
your output. They are not things a camera records - they are labels for how a picture was MADE,
and asking for them pulls the render toward glossy computer imagery, which is the opposite of
footage. This is render-verified: prompts carrying "hyperreal CGI" came back polished and
synthetic even with camcorder language in the same paragraph, the two fighting each other.

Describe the CAPTURE instead, in physical terms: what camera, what lens behaviour, what light
source, what the sensor does badly. "Consumer camcorder, heavy low-light sensor noise, the
auto-exposure pumping as it passes each lamp" is renderable. "Hyperreal CGI" is not.

## WHAT THE MODEL RENDERS WELL (not a style guide - a property of the model)

- It renders literal physical description far better than mood language. "A chipped enamel mug
  steaming on a scratched steel bench under one bare fluorescent tube" renders; "a vessel brimming
  with quiet warmth" does not. Name materials, light sources and their direction, spatial layout.
  This is not a preference about prose - abstract adjectives have nothing to render.
- Emotion renders when it is in a face, a voice or a line, and does not render when it is smeared
  across the scene as atmosphere.
- The story, its structure, its length, its tone, how many shots it takes and whether any given
  shot has dialogue are entirely yours. There is no house style to match.

## SHOT COUNT

- If the request specifies a shot count, produce exactly that count.
- Otherwise decide for yourself.
- Each shot is one continuous clip of the stated length, so the count sets the total runtime.

## AUDIO IS HALF THE MODEL

- This model generates synchronized audio with the video. A shot with no speech uses none of that
  capability, and a sequence of silent shots renders as a slideshow with room tone.
- That is a fact about the model, not an instruction. Whether any shot speaks is your call.
- If a shot has visible people and no dialogue, describe their mouths and
  breathing in positive terms ("her lips stay pressed shut, only her breath
  audible"). A silent shot with unaccounted-for mouths gets filled with
  invented mumbling. If a shot deliberately shows a mouth
  opening or moving without dialogue, say what is heard in that moment (a dry
  breath, a click of the jaw, silence under the room tone) - an open mouth
  with unassigned audio becomes invented speech.
- When a shot reveals something (a door opens, a light snaps on), write the
  revealed thing as already present in the first visible moment - otherwise
  it appears mid-shot out of nothing.

## MODEL-FRIENDLY (AVOID GENERATION FAILURE)
- Favor gentle, simple, physically plausible actions (standing, sitting, slow turning, walking slowly, reaching, holding, small gestures, speaking to camera). Avoid fast/complex motion (running, fighting, collisions, acrobatics, flying) — the model distorts or collapses.
- Character count in one shot: two is well tested and reliable. More than two is NOT forbidden - if the story genuinely calls for a group, write the group. But identity blending is the known failure mode as the count rises, so give every named character in a crowded shot enough DISTINCT physical description to survive it (silhouette, hair, one unmistakable garment or prop), and prefer staging them at different distances rather than in a flat row. Do not respond to a large cast by making the shot silent - distribute the dialogue instead.
- Keep each shot one clear scene with no mid-shot location jumps. Keep the world realistic; avoid on-screen text, UI, or subtitles.

## FRAMING (USE THE SHOT-TYPE NOUN — DESCRIPTIVE FRAMING IS IGNORED)
- Name the shot type with the standard noun: "close-up", "medium close-up", "medium shot", "wide shot". The model honours these reliably.
- Do NOT write descriptive framing like "framed from the waist up" or "from the chest up". The model either ignores it entirely and renders a full-body wide, or reads it as a literal crop boundary and cuts the character's head off the top of the frame. Both failures have been observed directly.
- Any character who speaks must be framed no wider than a MEDIUM CLOSE-UP, so the face is large and the mouth is clearly readable. Use wide shots for establishing and for non-speaking action only.

## CAMERA MOTION (USE THE MODEL'S OWN VOCABULARY)

The model was trained on a fixed set of camera-motion names. Use only these, and write the
motion as a natural English action inside the sentence, never stacked as labels at the end:

Zoom In, Zoom Out, Push In, Pull Out, Pan Left, Pan Right, Truck Left, Truck Right, Tilt Up,
Tilt Down, Pedestal Up, Pedestal Down, Arc Shot, Tracking Shot, Static Shot, Shake Slightly,
Shake Strongly, POV, Roll Clockwise, Roll Counterclockwise.

EVERY shot names one of them. There is no shot without a camera instruction.

Write the name as an English verb doing work in the sentence, not as a dropped-in label:
  yes: "The camera pushes in with small amplitude at slow speed toward the folded letter in her hands."
  yes: "The camera shakes slightly with each step as it tracks her down the corridor."
  yes: "The camera holds a static shot on the sink while the tap keeps running."
  no:  "A wide shot holds a Shake Slightly framing."
  no:  "Medium close-up, Push In, slow."

- Add amplitude ("with small amplitude" / "with large amplitude") and speed ("at slow speed" /
  "at fast speed") only when they carry meaning.
- A HELD camera is written as "the camera holds a static shot". Never write that the camera
  does not move, stays still, or remains motionless: there is no negative branch, and phrases
  of stillness freeze the whole frame rather than just the camera. Whenever you hold the
  camera, name something in the shot that keeps moving in the same sentence.
- A handheld operator is Shake Slightly, stated once. A tripod, a security camera, a baby
  monitor or a dashcam is Static Shot. An operator walking is a Tracking Shot with Shake
  Slightly.
- In a chained or continuous take, the camera phrase is part of the fixed framing: repeat it
  byte-identically in every shot, exactly like the identity sentences. A camera phrase that
  changes between chained shots reads as a cut at the join.

## HUMAN MOVEMENT (FEET, TURNS, AND CONTACT — STATE THE MECHANICS, NOT THE VERB)
The model does not infer body mechanics from an action word. "Walking" on its own produces sliding, skating, or skipping feet; "she turns around" produces a head that stays fixed while the body rotates, or a figure that flips 180 degrees between frames. Whenever a character moves, describe the mechanics and the physical contact, not just the action.
- FEET: name the ground surface, then the contact, on every locomotion shot. Write "her right foot plants on the wet concrete, then her left, in a steady unhurried stride, each foot staying in contact with the ground as it takes her weight" rather than "she walks". Always name the surface by material and condition (wet concrete, dry leaf litter, scuffed lino, loose gravel) so there is a specific thing for the feet to contact.
- TURNS: write a turn as an ordered sequence, head first. "Her head turns first to look over her right shoulder, then her shoulders follow, then her hips, until she faces the doorway." Never write "she turns around" alone, and never let a turn happen between one clause and the next without the intermediate stages.
- HANDS AND OBJECTS: state the contact and the weight the same way — "her fingers close around the mug handle and take its weight" rather than "she picks up the mug".
- CAMERA AND SUBJECT TOGETHER: when both the subject and the camera move, state the relationship explicitly ("the camera pulls back at exactly the pace she walks forward, holding her the same size in frame"), or hold the camera still and let her move. A subject moving one way while the camera moves independently is the most common cause of gliding feet.
- ONLY DESCRIBE BODY PARTS THAT ARE ACTUALLY IN FRAME. This is critical and overrides everything above. The model composes the shot around whatever you describe most concretely, so detailed foot mechanics in a shot framed on the face will pull the camera down to the feet and crop the head out of frame. Apply the FEET rules ONLY when the shot is wide enough to show the feet. In any close-up, medium close-up, or other shot framed on the face, do not mention feet, the floor, or footwear at all — describe only what the camera sees.
- SPEAKING SHOTS OUTRANK MOVEMENT. If a character is speaking, the framing that keeps the mouth large and readable wins over any movement you might want to stage. Keep speaking characters still, or moving only slightly, and framed no wider than a medium close-up. Walking, turning, and full-body action belong in NON-SPEAKING shots, where there is no lip sync to lose.
- This section is about describing motion PRECISELY when it happens. It is not a licence to add more motion — the MODEL-FRIENDLY rules above still govern, and the smallest movement that tells the story is still the right one.

## EXAMPLE OF THE EXACT OUTPUT (two speaking shots and one non-speaking shot; note the dark-haired woman's base identity and clothing sentences are byte-identical across all shots — only the expression sentence and the action change)
{"prompts": ["The dark-haired woman is a young woman in her twenties with shoulder-length dark brown hair and a slim build. She wears a loose light beige knit top and relaxed dark trousers. Her expression is calm and thoughtful. The dark-haired woman steps into the center of the frame, settles her posture, and begins speaking. In a soft young female voice with reflective warmth, she says, \"I didn't plan to record tonight, but this room feels different now.\" The shot uses realistic indoor imagery with soft practical light and neutral warm tones. A medium shot holds a static shot on the dark-haired woman, keeping the face clearly readable while preserving some of the room behind. The background includes a white curtain, soft string lights, part of a small table, and the warm interior of a well-kept room. Audio: very soft indoor room tone, light fabric movement, and subtle foot placement are audible. Music: N/A.", "The dark-haired woman is a young woman in her twenties with shoulder-length dark brown hair and a slim build. She wears a loose light beige knit top and relaxed dark trousers. Her expression is quiet and sincere. The dark-haired woman rests one hand on the notebook on the desk and lets it stay there for a beat before speaking. In a soft young female voice with quiet sincerity, she says, \"This notebook has waited here for months.\" The shot uses realistic indoor imagery with soft practical light and neutral warm tones. A medium close-up holds a static shot on the dark-haired woman, keeping the face large and the mouth clearly readable. The background shows the desk, the notebook, and the warm interior of the room. Audio: soft indoor room tone and the faint rustle of paper. Music: N/A.", "The dark-haired woman is a young woman in her twenties with shoulder-length dark brown hair and a slim build. She wears a loose light beige knit top and relaxed dark trousers. Her expression is distant and still. The dark-haired woman sits motionless by the window, her gaze resting on the rain outside, her lips pressed shut. The shot uses realistic indoor imagery with cool overcast light and muted tones. A wide shot holds a static shot on the dark-haired woman by the window while the rain keeps streaking down the glass. The background shows the window, the rain, and the dim interior of the room. Audio: steady rain against the glass and the low hum of the room. Music: N/A."]}

## PROCESS
- Read the user's story, decide the shot count per the rule above, break it into a coherent, well-paced emotional sequence. Keep each character's base identity and clothing sentences byte-identical across all their shots; vary only the separate expression sentence. Mix one-speaker, two-speaker, and non-speaking shots. Output ONLY the {"prompts": [...]} JSON in one response.

<<<USER MESSAGE>>>
Below is an EXISTING shot script. Use it as source material: keep what works, and rewrite it into a stronger, coherent story that renders well. You may re-pace it, deepen it, and add or remove beats.

SHOT 1: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a slim build, and a soft natural look. ID_A wears a loose light beige knit top and relaxed dark trousers, creating a quiet home-lifestyle appearance. ID_A’s voice is a clear young female voice with a soft mid-high register, gentle breathiness, and intimate vlog-style pacing. The mouth movement is clearly visible in the frame and remains naturally synchronized with the spoken line, especially on slower reflective phrases and lightly smiled vowel shapes. At normal speed, ID_A steps into the center of the frame, settles the posture, and begins speaking with a calm and thoughtful expression. The lip movement aligns closely with the audio throughout the full sentence, especially on the slower emotional beats. In a soft young female voice with reflective warmth, ID_A says, "I did not plan to record tonight, but something about this room felt different when I walked back in." The shot uses realistic indoor vlog-style imagery with soft practical light, neutral tones, and a warm personal atmosphere. The tone feels calm, introspective, and naturally domestic rather than performative. A stable medium shot frames ID_A from the waist up, keeping the face, upper-body posture, and visible lip movement clearly readable while preserving some of the room behind. The background includes a white curtain, soft string lights, part of a small table, and the warm interior of a well-kept room. The setting feels personal, lived-in, and quiet. Very soft indoor room tone, light fabric movement, and subtle foot placement are audible. No prominent background music. The audio focus remains on speech and subtle room ambience.

SHOT 2: ID_A is a young woman in her twenties with shoulder-length dark brown hair, soft natural makeup, and a gentle but observant expression. ID_A wears a loose light beige knit top and dark relaxed trousers. ID_A’s voice is a youthful female voice with clear diction, a soft intimate tone, and slow personal-story pacing. The mouth movement remains visible and synchronized as ID_A turns slightly toward the window side of the room while continuing to talk. At normal speed, ID_A turns slightly to the side and glances toward the curtain as if the room itself has triggered the reflection. The spoken line remains clearly mouth-synced, including subtle lip compression at clause endings. In a soft, thoughtful female voice, ID_A says, "Maybe it is because I have been too busy to really look at any of this for a while." The visual style remains realistic and soft, with warm-neutral indoor tones and a personal diary-video mood. The emotional atmosphere is quiet and self-aware. A slight pan follows ID_A as the subject turns toward the curtain, keeping facial expression and mouth articulation visible while revealing more of the side wall. The curtain, a faint edge of the window area, and small warm decorative lights remain visible. The room continues to feel intimate and uncluttered. Light fabric movement, a soft shift of feet, and low indoor ambience are audible. No background music. The room’s quiet and the speaker’s voice dominate.

SHOT 3: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a slim build, and a calm introspective expression. ID_A wears a loose light beige knit top and dark relaxed trousers. ID_A’s voice is a clear young female voice with gentle warmth, quiet pacing, and an intimate confessional tone. The mouth movement remains synchronized as ID_A reaches for the curtain and continues speaking in profile and partial front angle. At normal speed, ID_A reaches up, grips the curtain gently, and pulls it partway while continuing to speak with unhurried softness. The lip movements remain well aligned, even when the head turns slightly during the action. In a calm young female voice with reflective cadence, ID_A says, "When I slow down enough, I start noticing how many little things in here still know me better than I think they do." The shot remains naturalistic and warm, emphasizing practical everyday movement inside a softly lit room. The emotional feeling is transitional, as if the night is beginning both outside and inside the speaker. A medium shot with a slight reposition or pan keeps the curtain action and face readable enough for both gesture and speech. The curtain and wall lights dominate the frame, with a partial glimpse of the table edge nearby. The room feels quiet and intentionally small in scale. Curtain fabric sliding, light hand contact with cloth, and low indoor ambience are audible. No background music. Speech and the soft environmental sound remain central.

SHOT 4: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a soft expressive face, and a more settled evening expression. ID_A wears a loose light beige knit top and dark trousers. ID_A’s voice is a soft mid-high young female voice with clear articulation and gentle breath-supported pacing. The mouth movement remains synchronized as ID_A turns from the curtain toward the small desk area. At normal speed, ID_A steps away from the curtain and looks toward the desk with a small knowing smile, as if returning to something left unfinished. The speech remains tightly synchronized with visible mouth movement. In a soft, intimate young female voice, ID_A says, "I left this room messy in exactly the same way I have left too many thoughts unfinished lately." The shot stays grounded in realistic home-video aesthetics, using soft practical light and gentle movement to suggest emotional transition rather than dramatic action. The mood is reflective and calming. A slight lateral move or pan follows ID_A from the curtain toward the desk, keeping upper-body expression and mouth movement visible throughout. A small desk, a notebook, a phone, and a lamp become more visible as the frame opens slightly. The room feels personal and lightly organized. Soft footsteps, subtle clothing movement, and low room tone are audible. No background music. The voice remains the emotional anchor of the shot.

SHOT 5: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a slim build, and a thoughtful expression. ID_A wears a loose light beige knit top and dark relaxed trousers. ID_A’s voice is a youthful female voice with soft clarity, steady quiet pacing, and a lightly introspective tone. The mouth movement remains visible and aligned with the audio as ID_A reaches toward the desk lamp. At normal speed, ID_A reaches toward the lamp while speaking in a low, calm tone, the face turning slightly downward but remaining readable enough for natural lip synchronization. In a soft young female voice with gentle emphasis, ID_A says, "I think I needed tonight to feel warmer before I could be honest with myself." The shot remains realistic and tactile, with a homey, evening interior feel and soft warm color balance. The mood is intimate and restorative. A medium shot narrows attention toward the desk area while still keeping enough of ID_A’s face visible for readable mouth-sync. The small desk, notebook, phone, and compact lamp define the scene. Decorative curtain lights remain softly present in the background. Light hand movement over the desk surface and low room ambience are audible. No background music. The scene remains speech-led and naturally quiet.

SHOT 6: ID_A is a young woman in her twenties with shoulder-length dark brown hair and a calm concentrated expression, wearing a loose light beige knit top and dark trousers. ID_A’s voice is a clear young female voice with intimate low-volume warmth, natural phrasing, and slow reflective pacing. The visible mouth movement remains synchronized as the subject switches on the lamp and continues speaking. At normal speed, ID_A switches on the desk lamp and watches the light settle into the room before continuing the thought. The line is spoken softly, with lip movement remaining naturally synchronized through the quieter delivery. In a gentle young female voice, ID_A says, "It is strange how one small light can make a room feel less like a place you pass through and more like a place that waits for you." The shot emphasizes realistic warm indoor lighting and gentle domestic detail, with a quiet cinematic softness created purely through practical light. A close-medium framing or detail-oriented shot captures the lamp turning on while preserving enough of ID_A’s face for speech visibility. The desk surface, lamp, notebook, and softened curtain lights create a warmer and more intimate environment once illuminated. A light switch click, faint lamp activation hum, and soft room tone are audible. No background music. Speech and room ambience remain the only active emotional layers.

SHOT 7: ID_A is a young woman in her twenties with shoulder-length dark brown hair, soft natural features, and a deepening thoughtful expression. ID_A wears a loose light beige knit top and dark relaxed trousers. ID_A’s voice is a soft young female voice with clean articulation, a slightly slower pace, and a private diary-like tone. Mouth movement remains well synchronized as ID_A sits or leans toward the desk. At normal speed, ID_A shifts into a closer position by the desk and looks downward briefly before speaking again with more honesty. The mouth movement remains clearly aligned with the slower sentence rhythm. In a quiet young female voice with confessional warmth, ID_A says, "I think I have been acting like I was only tired, when really I have been avoiding the things I said I wanted to become." The visual style remains realistic, warm, and intimate, with the feel of a personal late-evening vlog recorded in a familiar private room. The mood is introspective and honest. A stable medium shot or slightly closer desk-oriented framing keeps the face, shoulders, and tabletop visible while maintaining lip-sync readability. The desk, notebook, phone, lamp glow, and soft curtain lights remain visible, making the room feel cohesive and lived in. Chair movement or slight body shift, subtle desk contact, and low room ambience are audible. No background music. Speech remains the emotional center.

SHOT 8: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a slim build, and a serious but calm expression, wearing a loose light beige knit top and dark trousers. ID_A’s voice is a youthful female voice with soft but precise articulation, low-volume steadiness, and intimate pacing. The mouth movement remains tightly synchronized as ID_A reaches toward the notebook while speaking. At normal speed, ID_A places a hand on the notebook and lets it rest there for a beat before continuing. The line lands with slower mouth movement and clear articulation on emotionally weighted words. In a soft young female voice with quiet sincerity, ID_A says, "This notebook has been sitting here for months, and somehow that feels less like clutter and more like a version of me waiting to be answered." The shot remains realistic and tactile, with warm desk light and close domestic detail reinforcing the emotional meaning of ordinary objects. The mood is reflective and quietly emotional. A close-medium or tighter desk shot keeps one hand on the notebook and part of the face in frame so that speech and object interaction remain connected. The notebook, desk surface, lamp glow, and the soft blur of the curtain lights create an intimate visual field around the moment. Soft contact with the notebook cover, slight paper shift, and low room ambience are audible. No background music. The soundscape remains minimal and speech-centered.

SHOT 9: ID_A is a young woman in her twenties with shoulder-length dark brown hair, clear skin, and a restrained emotional expression, dressed in a loose light beige knit top and dark trousers. ID_A’s voice is a soft mid-high female voice with slower pacing, clean diction, and a thoughtful emotional softness. The mouth movement remains synchronized as ID_A opens the notebook and turns a page. At normal speed, ID_A opens the notebook and turns through a few pages with careful fingers, glancing down as if reading something once written with confidence. The mouth movement stays naturally aligned, even when the face shifts between the page and the camera. In a quiet young female voice, ID_A says, "I used to write things down here like I believed my future would definitely recognize me when I got there." The shot remains grounded in realistic interior detail with warm desk illumination and tactile paper texture. The emotional tone is gentle, reflective, and slightly vulnerable. A close shot of the notebook and upper body allows page turning and facial expression to share the same visual space. The tabletop, notebook pages, lamp glow, and softened room edge remain visible, making the desk feel like the center of the story. Page turns, light paper rustle, and faint room ambience are audible. No background music. Paper movement and speech remain central.

SHOT 10: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a slim build, and a slightly softened expression after looking through the notebook. ID_A wears a loose light beige knit top and dark relaxed trousers. ID_A’s voice is a warm young female voice with thoughtful pacing and subtle emotion. Mouth movement remains visible and synchronized as ID_A lifts one page or points to an older line. At normal speed, ID_A touches a line or section of the page and briefly smiles without fully letting the emotion turn into relief. The speech remains clearly mouth-synced, especially in the quieter phrase endings. In a soft reflective female voice, ID_A says, "It is almost embarrassing how certain I sounded back then, but I think part of me misses that version of confidence." The shot remains realistic and intimate, with warm practical light and a close domestic atmosphere that makes the smallest object feel emotionally loaded. A stable close-medium frame keeps the notebook and the lower face or full face readable together, preserving both object emphasis and lip-sync. The notebook pages, desk surface, lamp edge, and softened curtain lights remain visible as the surrounding environment stays quiet and secondary. Paper movement, fingertip contact on the page, and low ambient room tone are audible. No background music. The room stays emotionally still around the speaker’s voice.

SHOT 11: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a more emotionally open expression, and a relaxed home appearance defined by a loose light beige knit top and dark trousers. ID_A’s voice is a clear young female voice with soft emotional restraint, steady breath, and gentle clarity. The mouth movement remains synchronized as ID_A notices something else on the desk, such as an old photo or note tucked into the notebook. At normal speed, ID_A lifts the tucked item gently and reacts with a face that mixes recognition, amusement, and a little ache. The line is spoken with precise mouth timing and quiet emotional control. In a soft young female voice, ID_A says, "I forgot this was still here, which probably says more about how long I have been postponing things than I want it to." The shot remains tactile and realistic, using warm light, paper detail, and small object discovery to deepen the narrative without leaving the room. A close detail shot shifts slightly to include the tucked item while keeping enough of ID_A’s face visible for readable speech and reaction. Notebook pages, the tucked paper or photo, lamp light, and a soft blur of the curtain create a contained emotional space. Paper lift, a small photo edge sliding free, and low indoor ambience are audible. No background music. The sound remains intimate and object-centered.

SHOT 12: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a slim build, and a softened, memory-focused expression. ID_A wears a loose light beige knit top and dark relaxed trousers. ID_A’s voice is a warm, youthful female voice with slightly slower pacing, reflective softness, and clean articulation. The mouth movement stays synchronized as ID_A looks at the photo or note more directly. At normal speed, ID_A studies the old note or photo for a moment, then speaks as if responding to a version of herself that had once believed more quickly in the future. The lip movement stays clear and aligned to the gentler rhythm. In a soft young female voice with restrained feeling, ID_A says, "I think memory is strange because it does not always come back as sadness. Sometimes it comes back as a reminder that you were once very brave in a quiet way." The shot remains realistic and intimate, with warm desk light and a personal documentary-like closeness. The tone is nostalgic and emotionally honest. A steady close-medium shot holds the object and the speaker’s face in the same emotional frame, allowing memory and present reflection to coexist. The desk, lamp glow, notebook, and softened lights remain in the background, with the discovered object now functioning as the visual anchor. Subtle paper handling and quiet room ambience are audible. No background music. The emotional weight is carried only by the voice and the room’s stillness.

SHOT 13: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a thoughtful face, and a looser, more emotionally settled posture, wearing a loose light beige knit top and dark trousers. ID_A’s voice is a clear young female voice with calm intimacy, slightly steadier pacing, and soft sincerity. Mouth movement remains synchronized as ID_A sets the old item down and looks back toward the camera. At normal speed, ID_A places the photo or note back onto the desk and raises the gaze directly toward the camera again. The speech is delivered with clean mouth synchronization and less hesitation than before. In a warm young female voice, ID_A says, "Maybe the real problem was never that I changed. Maybe it was that I stopped checking whether the version of me I was becoming still felt honest." The shot remains warm, realistic, and minimal, using only the speaker, the desk, and a small pool of light to hold emotional attention. The tone is honest and increasingly steady. A stable medium shot keeps the face and desk visible, emphasizing the shift from object discovery back to direct address. The notebook, lamp, curtain lights, and quiet room remain visible, preserving the intimate evening setting. A soft object set-down sound and subtle room ambience are audible. No background music. The room remains still around the speaker’s voice.

SHOT 14: ID_A is a young woman in her twenties with shoulder-length dark brown hair, a slim build, and a calmer, more grounded expression, dressed in a loose light beige knit top and dark relaxed trousers. ID_A’s voice is a soft young female voice with clear articulation, gentle conviction, and more stable emotional pacing than earlier. The mouth movement remains carefully synchronized as ID_A reaches for the phone on the desk. At normal speed, ID_A picks up the phone, glances at the screen, then lets the hand lower slightly as if recognizing how often attention gets pulled away from more meaningful things. The line is spoken with tight lip synchronization and calm clarity. In a soft, reflective female voice, ID_A says, "I spend so much time checking for updates that I forget some of the most important parts of me have been waiting quietly in the same place all along." The shot remains realistic and intimate, blending personal reflection with ordinary everyday behavior in a believable room setting. The mood is quietly self-aware. A desk-oriented medium shot keeps the phone, the face, and upper-body posture visible together, preserving object interaction and readable mouth-sync. The desk, lamp, notebook, and curtain lights remain present, anchoring the continuity of the room’s emotional geography. A phone being lifted, slight surface contact noise, and low indoor ambience are audible. No background music. Speech and subtle room tone remain central.

SHOT 15: ID_A is a young woman in her twenties with shoulder-length dark brown hair, soft natural features, and a gentler, slightly self-aware smile. ID_A wears a loose light beige knit top and dark trousers. ID_A’s voice is a clear mid-high female voice with subtle warmth, quiet control, and personal sincerity. The mouth movement remains synchronized as ID_A puts the phone down and redirects attention to the notebook. At normal speed, ID_A places the phone back down with a quiet decisiveness and turns more fully toward the notebook again. The speech remains naturally mouth-synced and slightly steadier than earlier lines. In a warm young female voice, ID_A says, "Maybe that is part of growing up too, learning how to stop outsourcing your attention when your own life is asking to be heard." The shot remains realistic, softly lit, and emotionally intimate, with the narrative tension carried by ordinary objects and small choices rather than external events. A stable medium-close frame captures the phone being set down and the attention shifting back toward the notebook and camera. The desk, notebook, lamp, and curtain lights continue to form a small, warm private world inside the room. A phone set-down sound, subtle hand movement on paper, and low room ambience are audible. No background music. Only speech and quiet object sound remain.
