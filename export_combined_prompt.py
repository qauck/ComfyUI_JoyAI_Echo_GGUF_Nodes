"""Export the JoyEcho_LLMEnhance prompt stack as ONE combined prompt.

Rebuilds the exact system prompt + user message the node sends for a long
story (or short story / revise) run — base writer prompt, join-style
boundary rules, refs-attached rules, shot-count line, frame-aware pacing
block — and writes them into a single file usable by any other LLM node in
ComfyUI. The markdown files in prompts/ stay the single source of truth;
only the pacing templates and the revise system prompt are duplicated here
because nodes.py builds them inline inside enhance().

Usage (from this folder):
  python export_combined_prompt.py
  python export_combined_prompt.py --engine h3 --join continuous_take --refs
  python export_combined_prompt.py --num-shots 12 --num-frames 251 --fps 25
  python export_combined_prompt.py --story "A lighthouse keeper finds a sealed bottle."
  python export_combined_prompt.py --mode revise --story-file my_script.json
  python export_combined_prompt.py --mode short_story

The output file has one marker line, <<<USER MESSAGE>>>. Everything above it
is the SYSTEM message; everything below is the USER message (with your story
substituted, or a placeholder to fill in). A node that only takes ONE prompt
string can send the whole file as-is.
"""
import argparse
import json
import re
import sys
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# join_style keys -> the exact widget values JoyEcho_LLMEnhance exposes
JOIN_STYLES = {
    "cuts": "cuts (independent setups)",
    "continuous_take": "continuous take (chained, no cuts)",
    "continuous_scene": "continuous scene with cuts (chained)",
    "extend": "extend take (one continuous speech across windows)",
}

# Verbatim copy of _TAKE_ONLY_RULE in nodes.py. Appended only for
# "continuous take": with no cuts at all, one shot per block.
_TAKE_ONLY_RULE = (
    "6. CONTINUOUS TAKE: there are no camera cuts anywhere in the scene. "
    "One [Shot 1] per block, no [Shot 2], no cut verbs, no <scenetrans>, "
    "and the same camera position and framing stated identically in every "
    "block.")

# Verbatim copy of the _rev_sys system prompt in nodes.py enhance().
_REVISE_SYS = """You revise shot prompts for a MiniMax H3 multi-shot video harness. You are given a JSON object {"prompts":[...]} where each array item is ONE shot's complete prompt text.

HARD RULES - violating any of these makes your output unusable:
1. Return the SAME NUMBER of shots, in the SAME ORDER. Never add, drop, merge or reorder shots.
2. If a shot contains a character-identity sentence (a sentence naming the character - by their name or a descriptive label like 'the dark-haired woman' - and describing their appearance and wardrobe, e.g. 'Dana is a woman in her thirties with ...' or 'The dark-haired woman is a young woman with ...'), copy it BYTE-FOR-BYTE into your revision of that shot - never reword it even slightly, because cross-shot identity depends on it being character-identical. Not every script uses them; if there is none, keep the subject's described appearance and wardrobe unchanged instead. Likewise keep any trained-LoRA trigger token (a lowercase word ending in '_rift') exactly as written and in place.
3. Keep each shot's quoted dialogue MEANING and its position in the story. You may re-word a line for rhythm, but never change what it says or move it to another shot.
4. Keep the capture-medium sentence and the continuous-ambient-sound sentence in every shot, and keep each shot's trailing 'Audio:' and 'Music:' lines intact.
5. Pure ASCII only. No em dashes, smart quotes or unicode.

WHAT YOU SHOULD IMPROVE: the physical, spatial and camera writing. Make the scene description more concrete and more renderable - named materials with a condition ('cracked wet asphalt', 'rust-streaked steel'), explicit light sources and their direction and falloff, one clear camera move stated in its OWN clause, never mixed into the subject's action sentence, with the frame described AFTER the move, ONE dominant action arc per shot with beats in order, and beats that are physically possible in the shot's duration. Use only the model's camera-motion vocabulary (Zoom In, Zoom Out, Push In, Pull Out, Pan Left, Pan Right, Truck Left, Truck Right, Tilt Up, Tilt Down, Pedestal Up, Pedestal Down, Arc Shot, Tracking Shot, Static Shot, Shake Slightly, Shake Strongly, POV, Roll Clockwise, Roll Counterclockwise), written as a natural English action inside the sentence. Prefer literal physical description over poetic or emotional abstraction; emotion belongs only in the performance and the dialogue itself. Never describe anything the camera cannot see. Keep the capture device's CHARACTER consistent: if the shot is documentary or found-footage, preserve and enrich its consumer-device behaviors (autofocus hunts, exposure lifts, breath sway, sensor noise) and remove cinema-rig vocabulary (dolly, jib, crane, gimbal, glide, cinematic, bokeh, slow motion, drone).

Output ONLY the JSON object. No commentary, no markdown fence."""


def load_system_prompt(mode, engine):
    """Same file choice as nodes._load_system_prompt()."""
    stem = ("long_story_writer_system_prompt" if "long" in mode
            else "short_story_writer_system_prompt")
    if engine == "h3":
        h3 = PROMPTS_DIR / f"{stem}.h3.md"
        if h3.exists():
            return h3.read_text(encoding="utf-8").strip()
        print(f"WARNING: {h3.name} missing; falling back to the shared "
              "prompt (speech is marked with quotes, which H3 renders as "
              "on-screen text).")
    fp = PROMPTS_DIR / f"{stem}.md"
    if not fp.exists():
        sys.exit(f"System prompt not found: {fp}")
    return fp.read_text(encoding="utf-8").strip()


def load_boundary_rules(join):
    """Same addendum choice as nodes._load_boundary_rules()."""
    if join == "cuts":
        return ""
    if join == "extend":
        return (PROMPTS_DIR / "h3_extend_rules.md").read_text(
            encoding="utf-8").strip()
    rules = (PROMPTS_DIR / "h3_boundary_rules_continuous.md").read_text(
        encoding="utf-8").strip()
    if join == "continuous_take":
        rules += "\n" + _TAKE_ONLY_RULE
    return rules


def shots_in(text):
    """Same input normalisation as nodes._llme_shots_in()."""
    src = (text or "").strip()
    if not src:
        return [], False
    if src.startswith("{"):
        try:
            data = json.loads(src)
            if isinstance(data, dict):
                arr = data.get("prompts") or data.get("shots")
                if isinstance(arr, list) and arr:
                    return [str(s) for s in arr], True
        except (json.JSONDecodeError, AttributeError):
            pass
        return [src], False
    blocks = [b.strip() for b in re.split(r"(?m)^---\s*$", src) if b.strip()]
    if len(blocks) > 1:
        return blocks, False
    return [src], False


def speakable_budget(num_frames, fps, chained):
    """Same arithmetic as nodes._speakable_budget(): (secs, speak, lo, hi)."""
    secs = num_frames / fps
    if chained == "extend":
        speak = max(3.0, secs - 1.0)
    else:
        speak = max(3.0, secs - 5.0) if chained else secs
    return secs, speak, max(6, int(round(speak * 1.2))), int(round(speak * 2.0))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", default="long_story",
                    choices=["long_story", "short_story", "revise"])
    ap.add_argument("--engine", default="auto", choices=["auto", "h3"],
                    help="h3 swaps in the .h3.md system prompt variants")
    ap.add_argument("--join", default="cuts", choices=list(JOIN_STYLES),
                    help="join_style of the render these prompts feed")
    ap.add_argument("--refs", action="store_true",
                    help="include the refs_attached identity rules")
    ap.add_argument("--story", default="",
                    help="story premise or existing script (else a placeholder)")
    ap.add_argument("--story-file", default="",
                    help="read premise/script text from a file instead")
    ap.add_argument("--num-shots", type=int, default=0,
                    help="0 = let the model decide")
    ap.add_argument("--num-frames", type=int, default=0,
                    help="frames per shot; >0 adds the pacing budget block")
    ap.add_argument("--fps", type=float, default=25.0)
    ap.add_argument("--out", default="",
                    help="output path (default combined_prompt_<name>.md here)")
    ap.add_argument("--no-header", action="store_true",
                    help="omit the meta comment block: pure prompt text only")
    args = ap.parse_args()

    text = args.story
    if args.story_file:
        text = Path(args.story_file).read_text(encoding="utf-8")
    shots, was_json = shots_in(text)

    # ── system prompt: base + boundary rules + refs rules, same joins ──
    if args.mode == "revise":
        sys_prompt = _REVISE_SYS
    else:
        sys_prompt = load_system_prompt(args.mode, args.engine)
    rules = load_boundary_rules(args.join)
    if rules:
        sys_prompt = sys_prompt.rstrip() + "\n\n" + rules
    if args.refs:
        sys_prompt = (sys_prompt.rstrip() + "\n\n"
                      + (PROMPTS_DIR / "h3_refs_attached_rules.md")
                      .read_text(encoding="utf-8").strip())

    # ── user message: premise (or numbered script) + shot count + pacing ──
    chained = ("extend" if args.join == "extend"
               else args.join != "cuts")

    if args.mode == "revise":
        oshots = shots or ["[PASTE YOUR {\"prompts\": [...]} SCRIPT HERE]"]
        user_msg = "SCRIPT TO REVISE:\n" + json.dumps(
            {"prompts": oshots}, ensure_ascii=True)
        if args.num_frames > 0:
            secs, speak, lo, hi = speakable_budget(
                args.num_frames, args.fps, chained)
            user_msg += (
                f"\n\nEach shot renders as one continuous clip about "
                f"{secs:.1f} seconds long at {int(round(args.fps))} fps. Pace "
                f"every shot's action to fill that duration, and size each "
                f"spoken line to roughly {lo}-{hi} words so the speech fits "
                f"the clip with room for breath - lengthen or tighten the "
                f"existing lines as needed WITHOUT changing what they say.")
            if chained and chained != "extend":
                user_msg += (
                    f" Of those {secs:.0f} seconds only about {speak:.0f} "
                    "are speakable: the first ~2 seconds of every shot after "
                    "the first are a silent hold and the last ~2 seconds are "
                    "a silent settle.")
    else:
        if was_json:
            numbered = "\n\n".join(f"SHOT {i+1}: {s}"
                                   for i, s in enumerate(shots))
            user_msg = (
                "Below is an EXISTING shot script. Use it as source material: "
                "keep what works, and rewrite it into a stronger, coherent "
                "story that renders well. You may re-pace it, deepen it, and "
                "add or remove beats.\n\n" + numbered)
        elif shots:
            user_msg = shots[0]
        else:
            user_msg = "[PASTE YOUR STORY IDEA / PREMISE HERE]"
        if args.num_shots > 0:
            user_msg += f"\n\nGenerate exactly {args.num_shots} shots."
        if args.num_frames > 0:
            secs, speak, lo, hi = speakable_budget(
                args.num_frames, args.fps, chained)
            if chained == "extend":
                n = max(1, args.num_shots or 1)
                tot_s = secs + (n - 1) * (secs - 1.0)
                user_msg += (
                    "\n\nEXTEND TAKE: this is ONE unbroken take of about "
                    f"{tot_s:.0f} seconds, rendered as {n} consecutive "
                    f"windows of {secs:.1f} seconds each (at "
                    f"{int(round(args.fps))} fps). Write ONE continuous "
                    f"speech for the whole take - about {lo * n}-{hi * n} "
                    f"words in total - then cut it into the {n} blocks at "
                    f"phrase boundaries so each block carries about "
                    f"{lo}-{hi} words - aim for the UPPER half of that range "
                    f"({(lo + hi) // 2}-{hi}), because a thin block renders "
                    f"as seconds of dead air (a 10-second window with 11 "
                    f"words measured a 5-second hole) - and every block "
                    f"speaks. Speech runs through the boundaries with no "
                    f"pauses; block k+1 begins with the next words after "
                    f"block k. Same visual block, verbatim, in every "
                    f"window. These numbers override any default clip length "
                    f"mentioned above."
                )
            else:
                user_msg += (
                    f"\n\nEach shot is a single continuous clip about "
                    f"{secs:.1f} "
                    f"seconds long (at {int(round(args.fps))} fps). Pace "
                    f"every shot to "
                    f"fill roughly {secs:.0f} seconds: give the action "
                    f"enough small "
                    f"beats to occupy the full duration without any fast or "
                    f"complex "
                    f"motion, and do not leave long dead air. For a speaking "
                    f"shot, "
                    f"scale the dialogue to about {lo}-{hi} words, "
                    f"delivered as one natural line or a short two-line "
                    f"exchange, with "
                    f"room for pauses, breath, and reaction. These per-shot "
                    f"timing "
                    f"numbers override any default clip length mentioned "
                    f"above."
                )
            if chained and chained != "extend":
                user_msg += (
                    f" Of those {secs:.0f} seconds, only about {speak:.0f} "
                    "are speakable: the first ~2 seconds of every shot after "
                    "the first are a silent hold and the last ~2 seconds of "
                    "every shot are a silent settle, per the block-boundary "
                    "rules."
                )

    stem = f"combined_prompt_{args.mode}"
    if args.engine == "h3":
        stem += "_h3"
    if args.join != "cuts":
        stem += f"_{args.join}"
    if args.refs:
        stem += "_refs"
    out = Path(args.out) if args.out else PROMPTS_DIR.parent / f"{stem}.md"

    header = ""
    if not args.no_header:
        header = (
            "<!-- Combined JoyEcho_LLMEnhance prompt, exported by "
            "export_combined_prompt.py\n"
            f"     mode={args.mode} engine={args.engine} "
            f"join_style={JOIN_STYLES[args.join]!r} "
            f"refs_attached={str(args.refs).lower()}\n"
            "     Everything above the <<<USER MESSAGE>>> marker is the SYSTEM "
            "message;\n"
            "     everything below is the USER message. A one-string LLM node can "
            "take the\n"
            "     whole file as-is. -->\n\n")
    body = header + sys_prompt + "\n\n<<<USER MESSAGE>>>\n" + user_msg + "\n"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out} ({len(body)} chars, "
          f"system={len(sys_prompt)} user={len(user_msg)})")


if __name__ == "__main__":
    main()
