"""
Pre-generated example songs for ElevenLabs Music API.
Each song has 6 scenes structured as a single 30-second composition.
The prompt is structured with [Scene N: Ts-Te] markers for timing.
Musical consistency is maintained via detailed genre, tempo, and mood descriptions.
"""

EXAMPLE_SONG_1 = {
    "theme": "desperate_tech_interview",
    "song_title": "Hire Me! (Desperate 80s Ballad)",
    "genre": "Desperate 80s Synth Pop Power Ballad",
    "bpm": 95,
    "mood": "Desperate, hopeful, emotional",
    "vocal_style": "Male, high-pitched, slightly desperate, pleading",
    "instrumentation": "Gated reverb drums, sustained synth chords, driving bassline, synth arpeggios",
    "scenes": [
        {
            "scene_num": 1,
            "time_range": "0-5s",
            "description": "Intro/Opening Plea",
            "lyrics": "I wrote the code, I fixed the bug, but will they see my worth? My hands are shaking, can they tell I'm scared beneath this shirt?",
            "musical_mood": "Start with heavy gated reverb drum hit, single synth chord sustained, vulnerable tone"
        },
        {
            "scene_num": 2,
            "time_range": "5-10s",
            "description": "CV Highlights/Credentials",
            "lyrics": "Five years of passion, Docker, React, and Python too. Stack Overflow answered all my questions, now I'm coming for you.",
            "musical_mood": "Vocals become faster, synth arpeggios begin, building confidence, steady percussion"
        },
        {
            "scene_num": 3,
            "time_range": "10-15s",
            "description": "Company Appeal/Obsession",
            "lyrics": "Your product changed my life, I'm a fan, I'm sincere. Every feature that you built, I've studied it so clear.",
            "musical_mood": "Drum fill, bassline increases in complexity, building tension and energy, more aggressive"
        },
        {
            "scene_num": 4,
            "time_range": "15-20s",
            "description": "The Big Ask/Climax",
            "lyrics": "Oh, hire me! I'm the one! I'm the one! I'm the perfect fit for the job!",
            "musical_mood": "Full loud chorus melody, power chord sustained, maximum energy, cheesy 80s synth flourish"
        },
        {
            "scene_num": 5,
            "time_range": "20-25s",
            "description": "Bridge/Vulnerability Return",
            "lyrics": "I'll bring the coffee, answer all your calls. I just need this chance before my spirit falls.",
            "musical_mood": "Sudden volume drop, solo piano and whispered vocals, intimate and quiet, emotional"
        },
        {
            "scene_num": 6,
            "time_range": "25-30s",
            "description": "Outro/Final Plea",
            "lyrics": "Don't say no, just say yes. Please believe in me.",
            "musical_mood": "Music fades out with dramatic synth flourish, sustained pitch bend, trailing echo effect"
        }
    ]
}

EXAMPLE_SONG_2 = {
    "theme": "aggressive_startup_anthem",
    "song_title": "Code Ready (Aggressive Tech Anthem)",
    "genre": "Aggressive Hip-Hop Rap, High-Energy Trap Beats",
    "bpm": 140,
    "mood": "Confident, aggressive, energetic, powerful",
    "vocal_style": "Male, deep voice, confident rap delivery, commanding presence",
    "instrumentation": "Heavy trap drums, aggressive 808s, rapid hi-hats, bass drops, synth stabs",
    "scenes": [
        {
            "scene_num": 1,
            "time_range": "0-5s",
            "description": "Intro/Raw Confidence",
            "lyrics": "Yo, I crush problems, break down walls, shippin' code every day. Your competitors sleep, I'm up grinding, that's the startup way.",
            "musical_mood": "Heavy bass drop intro, aggressive drums, commanding rap delivery, maximum energy"
        },
        {
            "scene_num": 2,
            "time_range": "5-10s",
            "description": "Technical Credentials",
            "lyrics": "From zero to one, I've scaled it before. AWS, Kubernetes, I know the score. Microservices, APIs, I architect the dream.",
            "musical_mood": "Fast hi-hats, synth stabs on beat, rapid-fire rap, relentless energy, no let-up"
        },
        {
            "scene_num": 3,
            "time_range": "10-15s",
            "description": "Product Knowledge Deep Dive",
            "lyrics": "Your product's fire, I study the grind. End-to-end vision, that's how I'm designed. User obsession, metrics obsession, growth is the game.",
            "musical_mood": "808 bass hits intensify, drum roll building, more aggressive synth layers, rising tension"
        },
        {
            "scene_num": 4,
            "time_range": "15-20s",
            "description": "The Climax/Peak Energy",
            "lyrics": "I don't just code, I build culture and teams. I mentor juniors, I ship big dreams. Full-stack believer, I'll own the whole stack.",
            "musical_mood": "Maximum volume, all instruments at full intensity, powerful rap flow, no apology"
        },
        {
            "scene_num": 5,
            "time_range": "20-25s",
            "description": "The Drive/Unstoppable Force",
            "lyrics": "Burnout? Never heard of it when we're changing the world. Vision cascades down, execute, unfurl. Feedback loops tight, we iterate fast.",
            "musical_mood": "Slight beat switch, snare cracks harder, momentum continues strong, relentless delivery"
        },
        {
            "scene_num": 6,
            "time_range": "25-30s",
            "description": "Outro/Final Ask",
            "lyrics": "Sign me up, let's go, this is my moment right here. I'll be the missing piece that you need, crystal clear!",
            "musical_mood": "Beat drops slightly lower, echo effects on final words, synth fade with bass sustain, powerful end"
        }
    ]
}

EXAMPLE_SONG_3 = {
    "theme": "quirky_creative_application",
    "song_title": "Let's Create Together (Indie Folk Pop)",
    "genre": "Indie Folk Pop, Whimsical Acoustic-Driven, Ukulele",
    "bpm": 115,
    "mood": "Cheerful, hopeful, creative, uplifting",
    "vocal_style": "Male, warm tone, conversational, enthusiastic, friendly",
    "instrumentation": "Ukulele, acoustic guitar, light percussion, warm strings, organic sounds",
    "scenes": [
        {
            "scene_num": 1,
            "time_range": "0-5s",
            "description": "Discovery/Serendipity",
            "lyrics": "I found your company on a Tuesday morning, coffee in my hand. I read your mission statement and I just felt so grand.",
            "musical_mood": "Soft ukulele intro, warm and welcoming, conversational tone, intimate acoustic start"
        },
        {
            "scene_num": 2,
            "time_range": "5-10s",
            "description": "Product Appreciation",
            "lyrics": "Your UI is beautiful, your backend is clean. Most creative product that I've ever seen. I want to be part of this journey so bright.",
            "musical_mood": "Acoustic guitar layers added, gentle percussion begins, warm and appreciative tone"
        },
        {
            "scene_num": 3,
            "time_range": "10-15s",
            "description": "Creative Alignment",
            "lyrics": "I bring ideas that nobody's thought, collaboration that can't be bought. I'll color outside the lines with you.",
            "musical_mood": "Light string arrangements added, uplifting melody, playful yet sincere, creative energy building"
        },
        {
            "scene_num": 4,
            "time_range": "15-20s",
            "description": "The Vision/Collaboration",
            "lyrics": "Let's build something magical, let's make something real. Empathy in code, that's the deal. Your vision plus my passion creates something gold.",
            "musical_mood": "Fuller arrangement, warm and inspiring, vocals brighten, hopeful and energetic peak"
        },
        {
            "scene_num": 5,
            "time_range": "20-25s",
            "description": "Flexibility/Commitment",
            "lyrics": "Remote or office, I'll show up and go hard. Creativity flowing like I'm holding no card. Flexibility, adaptation, that's in my heart.",
            "musical_mood": "Slightly softer moment, stripped back to ukulele and voice, intimate and sincere, dedicated tone"
        },
        {
            "scene_num": 6,
            "time_range": "25-30s",
            "description": "Outro/Call to Action",
            "lyrics": "Please take a chance on someone who cares, someone who's ready to share. I believe in your mission, let's make it happen together, fair?",
            "musical_mood": "Gentle fade with sustained ukulele chord, warm strings swell gently, hopeful and open-ended close"
        }
    ]
}

# List all examples for easy iteration
ALL_EXAMPLES = [EXAMPLE_SONG_1, EXAMPLE_SONG_2, EXAMPLE_SONG_3]
