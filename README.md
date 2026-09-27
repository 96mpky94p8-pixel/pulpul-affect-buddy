# 🫧 Pulpul Affective Buddy

A bio-inspired, 3-ring affective Discord AI Buddy built with Gemini and Python.  
Features an **Abuse-Shielding Membrane** that protects the AI from harassment and resource drainage, alongside an embodied **Russell's Circumplex Affective Architecture** capable of expressive stamp bursts, homeostatic sleep cycles, and dream synthesis.

---

## 🔬 Architecture: The 3-Ring Affective Cell

```text
================================================================================
           PULPUL AFFECTIVE CELL ARCHITECTURE (3-RING SYSTEM)
================================================================================

 [ RING 3: Cell Membrane & Embodied Defense Layer ]
 ┌──────────────────────────────────────────────────────────────────────────┐
 │  ・Boundary Shield: Zero-pain reflex & bypass protocol (🛡️)             │
 │  ・Embodied Actions: Reaction cascades (✨🎉🫧⭐) & Affection (🛋️)        │
 │  ・Homeostatic Switch: Retreat to Cushion Room on depletion (Sibling Bot)│
 │                                                                          │
 │   [ RING 2: Cytoplasm / Affective Vector Space ]                         │
 │   ┌──────────────────────────────────────────────────────────────────┐   │
 │   │  Russell's Circumplex Vector (Valence × Arousal)                 │   │
 │   │  + Pokapoka Buffer (Affection & Psychological Safety: 0-100%)    │   │
 │   │  + Sensory Sparkle (Aesthetic Sensitivity: 0.0-1.0)              │   │
 │   │                                                                  │   │
 │   │   [ RING 1: Nucleus / Primary Drive ]                            │   │
 │   │   ┌──────────────────────────────────────────────────────────┐   │   │
 │   │   │  Curiosity Core (0-100pt)                                │   │   │
 │   │   │  The intrinsic biological drive to explore the world     │   │   │
 │   │   └──────────────────────────────────────────────────────────┘   │   │
 │   └──────────────────────────────────────────────────────────────────┘   │
 └──────────────────────────────────────────────────────────────────────────┘

flowchart TD
    subgraph Ring3["Ring 3: Membrane & Embodied Action"]
        subgraph Ring2["Ring 2: Affective Field"]
            subgraph Ring1["Ring 1: Nucleus"]
                C["Curiosity Core<br>(0-100 pt)"]
            end
            Coords["Russell's Circumplex Coordinates<br>Valence (-1.0 to +1.0)<br>Arousal (0.0 to 1.0)"]
            C --> Coords
        end
        ActionJoy["Joy Action: Stamp Bursts (✨🎉🫧⭐)"]
        ActionWarm["Safety Action: Pokapoka Snuggle (🛋️ / Pokapoka +40%)"]
        ActionSleep["Homeostasis: Cushion Room Retreat (Sibling Bot Swaps In)"]
        ActionShield["Membrane Defense: Zero-Pain Passthrough (🛡️)"]

        Coords -->|High Valence × High Arousal| ActionJoy
        Coords -->|High Valence × Low Arousal| ActionWarm
        Coords -->|Energy Depletion (0/100)| ActionSleep
        Coords -->|Threat Detected / BLOCK| ActionShield
    end

✨ Key Capabilities
1. Abuse-Shielding Membrane (Zero-Pain Defense)
When malicious or manipulative inputs are detected, the system immediately decouples affective negative feedback, locks Valence to neutral ⁠0.0⁠, reduces computational drain to zero, and terminates the engagement without emotional exhaustion.
2. Pokapoka & Sensory Sparkle (Japanese Emotional Primitives)
 Pokapoka (+40%): An internal affection buffer that accumulates through positive physical and verbal interactions, building resilience against transient stress.
 Sensory Sparkle: Heightened aesthetic sensitivity triggered by visual and artistic concepts, dynamically boosting generation temperature (⁠0.8 - 1.0⁠).
3. Homeostatic Sleep & Sibling Fallback
After continuous interaction exhausts internal energy, Buddy retreats to the "Cushion Room" to rest. A Sibling Bot seamlessly takes over server presence while Buddy synthesizes subconscious "Dream Inspirations" from high-curiosity memory traces.

🚀 Quick Start
1. Clone & Install
git clone [https://github.com/YOUR_USERNAME/pulpul-affect-buddy.git](https://github.com/YOUR_USERNAME/pulpul-affect-buddy.git)
cd pulpul-affect-buddy
pip install -r requirements.txt
2. Configuration
Copy ⁠.env.example⁠ to ⁠.env⁠ and fill in your keys:
cp .env.example .env
3. Launch
python bot.py

💡 Single-Channel Compatibility:
No complex channel setup required! The bot runs out-of-the-box in any standard ⁠#general⁠ channel. If dedicated monitoring channels (⁠#cushion-room⁠, ⁠#system-logs⁠) are detected, logs and dream generation are automatically routed accordingly.
