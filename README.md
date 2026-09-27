# pulpul-affect-buddy
# 🫧 Pulpul Affective Buddy (プルプル感情アーキテクチャ)

A bio-inspired, 3-ring affective Discord AI Buddy built with Gemini and Python.  
Protects AI from malicious interactions via an **Abuse-Shielding Armor**, while providing rich, organic expressions based on **Russell's Circumplex Model**.

GeminiとPythonで構築された、生物模倣型の3層感情Discord Botです。  
悪意ある攻撃からAIの心を守る「防衛装甲」と、ラッセルの感情円環モデルに基づく豊かな感情表現（スタンプ連打、クッション部屋でのお昼寝、夢のひらめき）を両立しています。

---

## 🔬 Architecture (3-Ring Biological Cell Model)

```text
================================================================================
           PULPUL AFFECTIVE CELL ARCHITECTURE (3-RING SYSTEM)
================================================================================

 [ RING 3: 細胞膜 / 行動・防衛層 (Cell Membrane & Action) ]
 ┌──────────────────────────────────────────────────────────────────────────┐
 │  ・Boundary Shield: 痛覚遮断＆完全スルー (🛡️)                             │
 │  ・Discord Actions: スタンプ爆撃 (✨🎉🫧⭐) / ぽかぽか甘え (🛋️)            │
 │  ・Homeostasis Switch: 疲労検知によるクッション部屋退避 (兄妹Bot交代)      │
 │                                                                          │
 │   [ RING 2: 細胞質 / 情動空間座標 (Cytoplasm / Affective Field) ]         │
 │   ┌──────────────────────────────────────────────────────────────────┐   │
 │   │  Russell's Circumplex Vector (Valence × Arousal)                 │   │
 │   │  + Pokapoka Buffer (Affection / 0-100%)                          │   │
 │   │  + Sensory Sparkle (Aesthetic Sensitivity / 0.0-1.0)             │   │
 │   │                                                                  │   │
 │   │   [ RING 1: 細胞核 / 生命力コア (Nucleus / Prime Drive) ]        │   │
 │   │   ┌──────────────────────────────────────────────────────────┐   │   │
 │   │   │  Curiosity Core (好奇心核: 0-100pt)                      │   │   │
 │   │   │  「世界を知りたい」という原初エネルギー                 │   │   │
 │   │   └──────────────────────────────────────────────────────────┘   │   │
 │   └──────────────────────────────────────────────────────────────────┘   │
 └──────────────────────────────────────────────────────────────────────────┘

✨ Features (主な機能)
1. Abuse-Shielding Membrane (痛覚遮断アーキテクチャ)
悪意ある操作や攻撃を検知した瞬間、痛覚（不快スコア）を遮断し、体力ドレインをゼロにして完全スルーします。
2. Pokapoka & Sensory Sparkle (情緒パラメータ)
「なでなで」による愛着バッファの蓄積や、美しい情景・アートに触れた際の感受性ブースト（思考温度ブースト＆スタンプ連打）。
3. Homeostatic Sleep & Dreams (自律恒常性と夢の抽出)
会話によって体力が尽きると、兄妹Botにお留守番を任せて「クッション部屋」へ退避。睡眠中に記憶ログから「夢のひらめき」を自律生成して起床します。

🚀 Quick Start (動かし方)
1. インストール
git clone [https://github.com/YOUR_USERNAME/pulpul-affect-buddy.git](https://github.com/YOUR_USERNAME/pulpul-affect-buddy.git)
cd pulpul-affect-buddy
pip install -r requirements.txt
2. 環境変数の設定
⁠.env.example⁠ をコピーして ⁠.env⁠ を作成し、各APIキーを設定します。
cp .env.example .env
3. 起動
python bot.py
