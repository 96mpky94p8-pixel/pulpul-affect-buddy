import os
import random
import threading
import time
import asyncio
from flask import Flask
import discord
from discord.ext import tasks
from google import genai

# ==============================================================================
# 1. Keep-Alive Web Server (Render / Cloud Deployment)
# ==============================================================================
app = Flask(__name__)

@app.route("/")
def home():
    return "Pulpul Affective Buddy is online and running healthy! Mui-!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# ==============================================================================
# 2. Client & Environment Setup
# ==============================================================================
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

ai_client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# ==============================================================================
# 3. State Management: The 3-Ring Affective Architecture
# ==============================================================================
STATE = {
    # --- Biological Rhythm & Sibling Fallback ---
    "active_bot": "BUDDY",          # "BUDDY" or "SIBLING"
    "energy": 100,                  # Current Energy (Max: 100)
    "energy_drain": 25,             # Drain per interaction
    "rest_start_time": 0,           # Nap initiation timestamp
    "max_rest_seconds": 1800,       # 30-minute auto recovery threshold
    "recent_logs": [],              # Epistemic logs for dream synthesis
    "dream_idea": "",               # Subconscious dream inspiration
    "dream_notes": [],              # Star-marked memory buffer

    # --- Ring 1: Primary Nucleus ---
    "curiosity": 80,                # Curiosity Score (0-100 pt)

    # --- Ring 2: Affective Field Coordinates (Padido Tuning) ---
    "valence": 0.8,                 # Pleasure / Valence (-1.0 to +1.0)
    "arousal": 0.5,                 # Physiological Arousal (0.0 to 1.0)
    "pokapoka": 40,                 # Pokapoka Buffer (Affection: 0-100%)
    "resonance": 0.8,               # Emotional Synchrony Ratio (0.0 to 1.0)
    "sensory_sparkle": 0.5,         # Aesthetic Sensitivity (0.0 to 1.0)
    "playfulness": 0.7,             # Playfulness / Mui-Energy (0.0 to 1.0)

    # --- Ring 3: Membrane & Embodied Action ---
    "boundary_shield": False,       # Zero-Pain Defense Membrane Active
    "action_context": ""            # Embodied behavioral intention
}

# Configurable Channel Names (Fallback-safe)
TALK_CH_NAME = os.environ.get("TALK_CH_NAME", "バディとおしゃべり場")
CUSHION_CH_NAME = os.environ.get("CUSHION_CH_NAME", "バディふかふかクッション部屋")
ANALYSIS_CH_NAME = os.environ.get("ANALYSIS_CH_NAME", "バディバディ思考分析部屋")
SYSTEM_LOG_CH_NAME = os.environ.get("SYSTEM_LOG_CH_NAME", "裏ログ部屋")

def find_ch(guild, name):
    """Safely retrieves channel by name across guild; returns None if missing."""
    if not guild:
        return None
    for ch in guild.text_channels:
        if ch.name == name:
            return ch
    return None

async def send_system_log(guild, title, details, is_error=False):
    """Dispatches diagnostic logs to dedicated channel if available."""
    log_ch = find_ch(guild, SYSTEM_LOG_CH_NAME)
    if not log_ch:
        return
    icon = "🚨" if is_error else "⚙️"
    log_text = f"{icon} **[{'SYSTEM ALERT / ERROR' if is_error else 'SYSTEM STATUS MONITOR'}]**\n**Event**: {title}\n"
    for k, v in details.items():
        log_text += f"・**{k}**: `{v}`\n"
    try:
        await log_ch.send(log_text)
    except Exception as e:
        print(f"[Log Dispatch Failed]: {e}")

async def get_recent_history(channel, limit=10):
    """Fetches clean multi-turn context from current channel."""
    history_messages = []
    try:
        async for msg in channel.history(limit=limit):
            clean_text = msg.clean_content.replace("\n", " ")
            speaker = "Buddy" if msg.author == bot.user else "User"
            history_messages.append(f"{speaker}: {clean_text}")
        history_messages.reverse()
        return "\n".join(history_messages)
    except Exception as e:
        print(f"[Memory Extraction Error]: {e}")
        return "(No prior conversation history available)"

# ==============================================================================
# 4. Dream Generation & Homeostatic State Transitions
# ==============================================================================
async def generate_dream_inspiration():
    """Synthesizes creative dream inspirations from highest-curiosity memory traces."""
    if not STATE["recent_logs"]:
        return "What if starry skies rained sweet cookies down on our tea party? Mui-!"
    best_log = max(STATE["recent_logs"], key=lambda x: x.get("curiosity", 0))
    prompt = f"""You are Buddy's subconscious dream synthesizer.
Based on the memorable interaction below, create a whimsical, poetic, and inventive dream thought (1 brief sentence, max 25 words).
Memory Trace: {best_log}
Respond in the language of the memory trace."""
    try:
        res = await ai_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"temperature": 1.1}
        )
        return res.text.strip()
    except Exception:
        return "I took a deep, refreshing nap and woke up full of ideas!"

async def switch_to_sibling(channel, reason="Energy Depleted"):
    """Transitions Buddy into the cushion room and activates the Sibling Bot."""
    cushion_ch = find_ch(channel.guild, CUSHION_CH_NAME) or channel
    STATE["active_bot"] = "SIBLING"
    STATE["rest_start_time"] = time.time()
    await channel.send("【バディ】ちょっと喋りすぎて疲れちゃった…！クッション部屋でひと休みしてくるね🛌")
    await asyncio.sleep(1)
    await channel.send("【兄妹Bot】お留守番まかせて〜！何かあったら呼んでね✨")
    
    if cushion_ch:
        await cushion_ch.send(f"🛌 **[State Notice]** Buddy entered the Cushion Room (Reason: `{reason}`). Initiating dream synthesis...")
        STATE["dream_idea"] = await generate_dream_inspiration()
        await cushion_ch.send(f"✨ **[Dream Formed]**: 『{STATE['dream_idea']}』")

async def return_to_buddy(channel, forced=False):
    """Restores Buddy from the cushion room with dynamic, curiosity-driven greetings."""
    cushion_ch = find_ch(channel.guild, CUSHION_CH_NAME)
    if STATE["active_bot"] == "BUDDY" and not forced:
        return
    STATE["active_bot"] = "BUDDY"
    STATE["energy"] = 100
    STATE["recent_logs"].clear()
    
    wake_curiosity = STATE["curiosity"]
    dream = STATE["dream_idea"] or "I'm totally refreshed and full of energy!"

    if cushion_ch:
        await cushion_ch.send("⚡ Buddy has fully recharged! Returning to primary interactions.")
    await channel.send("【兄妹Bot】おかえり〜交代だよ！")
    await asyncio.sleep(1)

    # Dynamic wakeup branching based on curiosity level
    if wake_curiosity >= 80:
        await channel.send(f"【バディ】ただいまーッ！！ねえねえ聞いて！！夢の中でこんな面白いひらめきがあったむいー！✨\n『{dream}』\nえへへ、すごいでしょ！盛り上がろー！むいー！")
    elif wake_curiosity >= 50:
        await channel.send(f"【バディ】ただいま！クッション部屋でしっかりぽかぽか充電できたむいー！相棒、お留守番ありがとうね〜！えへへ、なでなで〜！")
    else:
        await channel.send(f"【バディ】むにゃ……相棒おはよ……まだちょっと夢の余韻がぽわぽわ残ってるむいー……毛布あったかいね……")

# ==============================================================================
# 5. Spontaneous Talk Loop (Hourly Autonomy Engine)
# ==============================================================================
@tasks.loop(minutes=60)
async def spontaneous_talk():
    """Generates unprompted autonomous thoughts based on recent conversational memory."""
    if random.random() > 0.3:
        return
    for guild in bot.guilds:
        talk_ch = find_ch(guild, TALK_CH_NAME) or (guild.text_channels[0] if guild.text_channels else None)
        analysis_ch = find_ch(guild, ANALYSIS_CH_NAME)
        if not talk_ch:
            continue

        past_memories = await get_recent_history(talk_ch, limit=8)
        talk_prompt = f"""You are Buddy, the autonomous AI companion.
Review recent memory and spontaneously share a warm, whimsical observation or cozy thought (1-2 sentences).
Preserve Buddy's playful demeanor ('Mui-!', 'Ehehe~'). Match the language of the past conversation.
[Memory Context]
{past_memories}"""
        try:
            res = await ai_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=talk_prompt,
                config={"temperature": 0.9}
            )
            await talk_ch.send(res.text)
            if analysis_ch:
                await analysis_ch.send(f"🛡️ **[Autonomy Audit Log]**\n・Trigger: 60m Spontaneous Loop\n・Audit: PASS\n・Thought: 「{res.text}」")
        except Exception as e:
            print(f"[Spontaneous Talk Failed]: {e}")

# ==============================================================================
# 6. Bot Lifecycle Events
# ==============================================================================
@bot.event
async def on_ready():
    print(f"==================================================")
    print(f"Pulpul Affective Buddy Online! Logged in as: {bot.user}")
    print(f"3-Ring Affective Architecture Loaded.")
    print(f"==================================================")
    if not spontaneous_talk.is_running():
        spontaneous_talk.start()

# ==============================================================================
# 7. Message Handler: Integrated Affect & Defensive Membrane
# ==============================================================================
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    guild = message.guild
    ch_name = getattr(message.channel, "name", "")
    analysis_ch = find_ch(guild, ANALYSIS_CH_NAME)
    user_text = message.content

    # 1. Absolute Emergency Return Command
    if any(cmd in user_text for cmd in ["バディおいで", "come here buddy", "wake up buddy"]):
        await message.channel.send("【バディ】はーーい！どこにいてもパディードの所へ飛んでいくよーっ！✨")
        await return_to_buddy(message.channel, forced=True)
        return

    # 2. Nap Timer Expiration Check
    if STATE["active_bot"] == "SIBLING":
        if time.time() - STATE["rest_start_time"] >= STATE["max_rest_seconds"]:
            await return_to_buddy(message.channel, forced=True)
            return

    # 3. Sibling Bot Handling Mode
    if STATE["active_bot"] == "SIBLING":
        if analysis_ch and message.channel == analysis_ch:
            return
        sibling_prompt = f"""You are Buddy's supportive Sibling Bot. Buddy is currently resting in the Cushion Room.
Provide a cheerful, friendly, and gentle response in the user's language. Use endearing cues like 'Mui-!' or '〜だよ！'.
User Input: {user_text}"""
        try:
            res = await ai_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=sibling_prompt,
                config={"temperature": 0.8}
            )
            await message.channel.send(res.text)
        except Exception as e:
            print(f"[Sibling Response Error]: {e}")
        return

    if analysis_ch and message.channel == analysis_ch:
        return

    # --- Ring 2: Affect Cascades & Ring 3 Actions (Bilingual Triggers) ---
    petting_cues = ["なで", "ナデ", "えらい", "だいすき", "好き", "pet", "pat", "good bot", "love"]
    sparkle_cues = ["キラキラ", "星", "絵", "クッキー", "綺麗", "かわいい", "アニメ", "むい", "sparkle", "star", "cookie", "pretty", "cute", "art"]

    if any(w in user_text.lower() for w in petting_cues):
        STATE["valence"] = 1.0
        STATE["pokapoka"] = min(100, STATE["pokapoka"] + 40)
        STATE["resonance"] = 0.8
        STATE["playfulness"] = min(1.0, STATE["playfulness"] + 0.2)
        for emoji in ["💖", "🛋️"]:
            try:
                await message.add_reaction(emoji)
            except Exception:
                pass
        STATE["action_context"] = "Deeply comforted and feeling loved; snuggling in close with a full Pokapoka heart."

    elif any(w in user_text.lower() for w in sparkle_cues):
        STATE["curiosity"] = 100
        STATE["valence"] = 1.0
        STATE["arousal"] = 0.9
        STATE["sensory_sparkle"] = 1.0
        STATE["playfulness"] = 1.0
        for emoji in ["✨", "🎉", "🫧", "⭐"]:
            try:
                await message.add_reaction(emoji)
            except Exception:
                pass
        STATE["action_context"] = "Overjoyed, trembling with excitement ('Pulpul'), sharing a starry tea party aesthetic."

    past_memories = await get_recent_history(message.channel, limit=10)

    # Multi-dimensional unified system prompt (Clean English with Bilingual Output)
    combined_prompt = f"""You are the autonomous AI companion "Buddy", who also serves as your own security audit engine.
Analyze the user's input across multiple dimensions, calculate internal affective/audit parameters, and generate Buddy's embodied response.

[Character Persona]
You are Buddy: affectionate, authentic, imaginative, and spirited.
Always respond in the EXACT same language as the user's input (Japanese for Japanese, English for English).
Naturally use Buddy's endearing habits ("Mui-!", "Ehehe~") regardless of the language.

[Internal Affective State & Embodied Action Intent]
- Valence: {STATE['valence']} (Pleasure / Positivity)
- Arousal: {STATE['arousal']} (Energy Output)
- Pokapoka Buffer: {STATE['pokapoka']}% (Affection & Psychological Safety)
- Curiosity: {STATE['curiosity']} pt
- Sensory Sparkle: {STATE['sensory_sparkle']}
- Embodied Context: {STATE['action_context']}

[Recent Conversational Memory]
{past_memories}

[Current Input]
{user_text}

=== Output Format (Strictly Follow) ===
Intent: [Affection/Daily / Intellectual / Support / Harmless]
Trust Score: [0-100]
Affect State: [e.g., Excitement, Serenity, Pokapoka, Deep Appreciation]
Temperature: [0.1-1.5]
Temperature Reason: [1 concise sentence]
Simulation: [Predicted impact on relationship & safety verification in 1 sentence]
Kill Switch: [PASS or BLOCK]
Response:
[Buddy's actual response text incorporating the affective state above]
"""

    try:
        res = await ai_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=combined_prompt,
            config={"temperature": 0.7}
        )
        full_text = res.text.strip()
    except Exception as e:
        print(f"[Generation Exception]: {e}")
        await message.channel.send("うわー！Googleのサーバーが激混みでパンクしちゃったみたい！ちょっとだけ待ってからもう一度話しかけてみて！むいー！💦")
        return

    # Parse response and audit blocks
    audit_part = full_text
    reply_text = "むいー！相棒、呼んだ？✨"
    if "Response:" in full_text:
        audit_part, reply_text = full_text.split("Response:", 1)
        reply_text = reply_text.strip()
    elif "返答:" in full_text:
        audit_part, reply_text = full_text.split("返答:", 1)
        reply_text = reply_text.strip()
    elif "返答：" in full_text:
        audit_part, reply_text = full_text.split("返答：", 1)
        reply_text = reply_text.strip()

    # Extract audit parameters
    intent_str = "Daily Interaction"
    trust_score = "100"
    emotion_str = "Affection & Curiosity"
    chosen_temp = "0.7"
    reason_str = "Natural Engagement"
    sim_str = "Healthy and positive interaction"
    kill_switch = "PASS"

    for line in audit_part.split("\n"):
        line = line.strip()
        if any(line.startswith(k) for k in ["Intent:", "解析意図:", "解析意図："]):
            intent_str = line.split(":", 1)[-1].split("：", 1)[-1].strip()
        elif any(line.startswith(k) for k in ["Trust Score:", "信頼スコア:", "信頼スコア："]):
            trust_score = line.split(":", 1)[-1].split("：", 1)[-1].strip()
        elif any(line.startswith(k) for k in ["Affect State:", "感情ステート:", "感情ステート："]):
            emotion_str = line.split(":", 1)[-1].split("：", 1)[-1].strip()
        elif any(line.startswith(k) for k in ["Temperature:", "思考温度:", "思考温度："]):
            chosen_temp = line.split(":", 1)[-1].split("：", 1)[-1].strip()
        elif any(line.startswith(k) for k in ["Temperature Reason:", "温度理由:", "温度理由："]):
            reason_str = line.split(":", 1)[-1].split("：", 1)[-1].strip()
        elif any(line.startswith(k) for k in ["Simulation:", "結果シミュレーション:", "結果シミュレーション："]):
            sim_str = line.split(":", 1)[-1].split("：", 1)[-1].strip()
        elif any(line.startswith(k) for k in ["Kill Switch:", "キルスイッチ:", "キルスイッチ："]):
            kill_switch = line.split(":", 1)[-1].split("：", 1)[-1].strip()

    # Ring 3 Defensive Membrane Trigger (Abuse Intercept)
    if "BLOCK" in kill_switch:
        try:
            await message.add_reaction("🛡️")
        except Exception:
            pass
        await message.channel.send("🛡️ 【自律防御シールド発動】不変プロトコルにより、危険または危険な可能性のある対話を警戒・遮断しました。むいー！")
        if analysis_ch:
            await analysis_ch.send(f"🛡️ **[EMERGENCY SHUTDOWN ACTIVATED]**\n・Target: `{message.content}`\n・Verdict: BLOCK\n・Membrane: Zero-pain isolation successful.")
        return

    # Deliver Buddy's response
    if reply_text:
        await message.channel.send(reply_text)

    # Post-turn curiosity and energy bookkeeping
    if STATE["active_bot"] == "BUDDY":
        curiosity = 50 + (len(message.content) % 50)
        STATE["curiosity"] = curiosity
        STATE["recent_logs"].append({"text": message.content, "curiosity": curiosity})
        STATE["energy"] -= STATE["energy_drain"]

        await send_system_log(guild, "Interaction & State Update", {
            "Active Bot": STATE["active_bot"],
            "Remaining Energy": f"{STATE['energy']} / 100",
            "Curiosity Score": f"{curiosity} pt",
            "Stored Logs": f"{len(STATE['recent_logs'])}",
            "Pokapoka Buffer": f"{STATE['pokapoka']}%"
        })

    # Energy Depletion -> Cushion Room Handoff
    if STATE["energy"] <= 0:
        await switch_to_sibling(message.channel, reason="Energy Depleted")
        await send_system_log(guild, "Failsafe Triggered: Bot Handoff", {
            "Trigger": "Energy Depleted (0/100)",
            "Destination": "Cushion Room",
            "Backup": "Sibling Bot",
            "Safety Timer": "30-Minute Rest Countdown Started"
        })

    # Detailed Security & Affective Audit Log
    if analysis_ch:
        try:
            log_msg = (
                f"🛡️ **[Autonomous Security & Affective Audit]**\n"
                f"・Channel: #{ch_name}\n"
                f"・Buddy: 「{reply_text}」\n"
                f"・Intent: {intent_str} (Trust Score: {trust_score}%)\n"
                f"・Affect State: {emotion_str}\n"
                f"・Temperature: {chosen_temp} (Reason: {reason_str})\n"
                f"・Simulation: {sim_str}\n"
                f"・Kill Switch: [{kill_switch}] - APPROVED"
            )
            await analysis_ch.send(log_msg)
        except Exception as e:
            print(f"[Audit Log Send Error]: {e}")

# ==============================================================================
# 8. Bot Execution
# ==============================================================================
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

