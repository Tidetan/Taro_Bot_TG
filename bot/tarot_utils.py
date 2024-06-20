import random
from datetime import datetime


def shuffle_deck(deck):
    random.shuffle(deck)

def get_card(deck):
    num = random.randint(0, len(deck) - 1)
    card = deck[num]
    del deck[num]
    rev = random.randint(0, 1)
    drawn = (card, rev)
    return drawn

def get_daily_tarot_card():
    deck = get_deck()
    shuffle_deck(deck)
    card, reversed = get_card(deck)
    return {
        "name": card["name"],
        "description": card["rdesc"] if reversed else card["desc"]
    }


def get_deck():
    return [
        {"name": "The Fool", "desc": "New beginnings, adventure, and spontaneity.", "rdesc": "Foolishness, recklessness, and risk-taking.", "sequence": 0},
        {"name": "The Magician", "desc": "Resourcefulness, power, and inspired action.", "rdesc": "Manipulation, poor planning, and untapped talents.", "sequence": 1},
        {"name": "The High Priestess", "desc": "Intuition, sacred knowledge, and divine feminine.", "rdesc": "Secrets, disconnected from intuition, withdrawal.", "sequence": 2},
        {"name": "The Empress", "desc": "Fertility, beauty, nature, and abundance.", "rdesc": "Creative block, dependence on others.", "sequence": 3},
        {"name": "The Emperor", "desc": "Authority, structure, control, and fatherhood.", "rdesc": "Domination, excessive control, lack of discipline.", "sequence": 4},
        {"name": "The Hierophant", "desc": "Spiritual wisdom, religious beliefs, and conformity.", "rdesc": "Personal beliefs, freedom, challenging the status quo.", "sequence": 5},
        {"name": "The Lovers", "desc": "Love, harmony, relationships, and values alignment.", "rdesc": "Self-love, disharmony, imbalance in relationships.", "sequence": 6},
        {"name": "The Chariot", "desc": "Control, willpower, success, and determination.", "rdesc": "Self-discipline, opposition, lack of direction.", "sequence": 7},
        {"name": "Strength", "desc": "Courage, persuasion, influence, and compassion.", "rdesc": "Self-doubt, low energy, raw emotion.", "sequence": 8},
        {"name": "The Hermit", "desc": "Soul-searching, introspection, and inner guidance.", "rdesc": "Isolation, loneliness, withdrawal.", "sequence": 9},
        {"name": "Wheel of Fortune", "desc": "Good luck, karma, and life cycles.", "rdesc": "Bad luck, resistance to change, breaking cycles.", "sequence": 10},
        {"name": "Justice", "desc": "Fairness, truth, cause and effect, law.", "rdesc": "Unfairness, lack of accountability, dishonesty.", "sequence": 11},
        {"name": "The Hanged Man", "desc": "Pause, surrender, letting go, and new perspectives.", "rdesc": "Delays, resistance, stalling, indecision.", "sequence": 12},
        {"name": "Death", "desc": "Endings, change, transformation, transition.", "rdesc": "Resistance to change, personal transformation.", "sequence": 13},
        {"name": "Temperance", "desc": "Balance, moderation, patience, and purpose.", "rdesc": "Imbalance, excess, lack of long-term vision.", "sequence": 14},
        {"name": "The Devil", "desc": "Shadow self, attachment, addiction, restriction.", "rdesc": "Releasing limiting beliefs, exploring dark thoughts.", "sequence": 15},
        {"name": "The Tower", "desc": "Sudden change, upheaval, chaos, and revelation.", "rdesc": "Avoidance of disaster, fear of change.", "sequence": 16},
        {"name": "The Star", "desc": "Hope, faith, purpose, and renewal.", "rdesc": "Lack of faith, despair, disconnection.", "sequence": 17},
        {"name": "The Moon", "desc": "Illusion, fear, anxiety, subconscious, and intuition.", "rdesc": "Release of fear, repressed emotion, inner confusion.", "sequence": 18},
        {"name": "The Sun", "desc": "Positivity, fun, warmth, success, and vitality.", "rdesc": "Inner child, feeling down, overly optimistic.", "sequence": 19},
        {"name": "Judgement", "desc": "Reflection, reckoning, and inner calling.", "rdesc": "Self-doubt, inner critic, ignoring the call.", "sequence": 20},
        {"name": "The World", "desc": "Completion, integration, accomplishment, travel.", "rdesc": "Seeking personal closure, short-cuts, delays.", "sequence": 21},
        {"name": "Ace of Wands", "desc": "Inspiration, new opportunities, growth, potential.", "rdesc": "An emerging idea, lack of direction, distractions.", "sequence": 22},
        {"name": "Two of Wands", "desc": "Future planning, progress, decisions, discovery.", "rdesc": "Personal goals, inner alignment, fear of unknown.", "sequence": 23},
        {"name": "Three of Wands", "desc": "Progress, expansion, foresight, overseas opportunities.", "rdesc": "Playing small, lack of foresight, unexpected delays.", "sequence": 24},
        {"name": "Four of Wands", "desc": "Celebration, joy, harmony, relaxation, homecoming.", "rdesc": "Personal celebration, inner harmony, conflict with others.", "sequence": 25},
        {"name": "Five of Wands", "desc": "Conflict, disagreements, competition, tension, diversity.", "rdesc": "Inner conflict, conflict avoidance, tension release.", "sequence": 26},
        {"name": "Six of Wands", "desc": "Success, public recognition, progress, self-confidence.", "rdesc": "Private achievement, personal definition of success.", "sequence": 27},
        {"name": "Seven of Wands", "desc": "Challenge, competition, protection, perseverance.", "rdesc": "Exhaustion, giving up, overwhelmed.", "sequence": 28},
        {"name": "Eight of Wands", "desc": "Movement, fast-paced change, action, alignment.", "rdesc": "Delays, frustration, resisting change.", "sequence": 29},
        {"name": "Nine of Wands", "desc": "Resilience, courage, persistence, test of faith, boundaries.", "rdesc": "Inner resources, struggle, overwhelm, defensive.", "sequence": 30},
        {"name": "Ten of Wands", "desc": "Burden, extra responsibility, hard work, completion.", "rdesc": "Doing it all, carrying the burden, delegation.", "sequence": 31},
        {"name": "Page of Wands", "desc": "Inspiration, ideas, discovery, limitless potential, free spirit.", "rdesc": "Newly formed ideas, redirecting energy, self-limiting beliefs.", "sequence": 32},
        {"name": "Knight of Wands", "desc": "Energy, passion, inspired action, adventure, impulsiveness.", "rdesc": "Passion project, haste, scattered energy, delays.", "sequence": 33},
        {"name": "Queen of Wands", "desc": "Courage, confidence, independence, social butterfly, determination.", "rdesc": "Self-respect, self-confidence, introverted, re-establish sense of self.", "sequence": 34},
        {"name": "King of Wands", "desc": "Natural-born leader, vision, entrepreneur, honour.", "rdesc": "Impulsiveness, haste, ruthless, high expectations.", "sequence": 35},
        {"name": "Ace of Cups", "desc": "Love, new relationships, compassion, creativity.", "rdesc": "Self-love, intuition, repressed emotions.", "sequence": 36},
        {"name": "Two of Cups", "desc": "Unified love, partnership, mutual attraction.", "rdesc": "Self-love, break-ups, disharmony, distrust.", "sequence": 37},
        {"name": "Three of Cups", "desc": "Celebration, friendship, creativity, collaborations.", "rdesc": "Independence, alone time, hardcore partying, 'three's a crowd'.", "sequence": 38},
        {"name": "Four of Cups", "desc": "Meditation, contemplation, apathy, re-evaluation.", "rdesc": "Retreat, withdrawal, checking in for alignment.", "sequence": 39},
        {"name": "Five of Cups", "desc": "Regret, failure, disappointment, pessimism.", "rdesc": "Personal setbacks, self-forgiveness, moving on.", "sequence": 40},
        {"name": "Six of Cups", "desc": "Revisiting the past, childhood memories, innocence, joy.", "rdesc": "Living in the past, forgiveness, lacking playfulness.", "sequence": 41},
        {"name": "Seven of Cups", "desc": "Opportunities, choices, wishful thinking, illusion.", "rdesc": "Alignment, personal values, overwhelmed by choices.", "sequence": 42},
        {"name": "Eight of Cups", "desc": "Disappointment, abandonment, withdrawal, escapism.", "rdesc": "Trying one more time, indecision, aimless drifting, walking away.", "sequence": 43},
        {"name": "Nine of Cups", "desc": "Contentment, satisfaction, gratitude, wish come true.", "rdesc": "Inner happiness, materialism, dissatisfaction.", "sequence": 44},
        {"name": "Ten of Cups", "desc": "Divine love, blissful relationships, harmony, alignment.", "rdesc": "Disconnection, misaligned values, struggling relationships.", "sequence": 45},
        {"name": "Page of Cups", "desc": "Creative opportunities, intuitive messages, curiosity, possibility.", "rdesc": "New ideas, doubting intuition, emotional immaturity.", "sequence": 46},
        {"name": "Knight of Cups", "desc": "Romance, charm, 'Knight in shining armor', imagination.", "rdesc": "Overactive imagination, unrealistic, jealous, moody.", "sequence": 47},
        {"name": "Queen of Cups", "desc": "Compassionate, caring, emotionally stable, intuitive, in flow.", "rdesc": "Inner feelings, self-care, self-love, co-dependency.", "sequence": 48},
        {"name": "King of Cups", "desc": "Emotionally balanced, compassionate, diplomatic.", "rdesc": "Self-compassion, inner feelings, moodiness, emotionally manipulative.", "sequence": 49},
        {"name": "Ace of Swords", "desc": "Breakthrough, clarity, sharp mind.", "rdesc": "Inner clarity, re-thinking an idea, clouded judgment.", "sequence": 50},
        {"name": "Two of Swords", "desc": "Difficult decisions, weighing up options, an impasse, avoidance.", "rdesc": "Indecision, confusion, information overload.", "sequence": 51},
        {"name": "Three of Swords", "desc": "Heartbreak, emotional pain, sorrow, grief, hurt.", "rdesc": "Negative self-talk, releasing pain, optimism, forgiveness.", "sequence": 52},
        {"name": "Four of Swords", "desc": "Rest, relaxation, meditation, contemplation, recuperation.", "rdesc": "Exhaustion, burn-out, deep contemplation, stagnation.", "sequence": 53},
        {"name": "Five of Swords", "desc": "Conflict, disagreements, competition, defeat, winning at all costs.", "rdesc": "Reconciliation, making amends, past resentment.", "sequence": 54},
        {"name": "Six of Swords", "desc": "Transition, change, rite of passage, releasing baggage.", "rdesc": "Personal transition, resistance to change, unfinished business.", "sequence": 55},
        {"name": "Seven of Swords", "desc": "Betrayal, deception, getting away with something, acting strategically.", "rdesc": "Imposter syndrome, keeping secrets, hiding true intentions.", "sequence": 56},
        {"name": "Eight of Swords", "desc": "Negative thoughts, self-imposed restriction, imprisonment, victim mentality.", "rdesc": "Self-limiting beliefs, inner critic, releasing negative thoughts, open to new perspectives.", "sequence": 57},
        {"name": "Nine of Swords", "desc": "Anxiety, worry, fear, depression, nightmares.", "rdesc": "Inner turmoil, deep-seated fears, secrets, releasing worry.", "sequence": 58},
        {"name": "Ten of Swords", "desc": "Painful endings, deep wounds, betrayal, loss, crisis.", "rdesc": "Recovery, regeneration, resisting an inevitable end.", "sequence": 59},
        {"name": "Page of Swords", "desc": "New ideas, curiosity, thirst for knowledge, new ways of communicating.", "rdesc": "Self-expression, all talk and no action, haphazard action, haste.", "sequence": 60},
        {"name": "Knight of Swords", "desc": "Ambitious, action-oriented, driven to succeed, fast-thinking.", "rdesc": "Restless, unfocused, impulsive, burn-out.", "sequence": 61},
        {"name": "Queen of Swords", "desc": "Independent, unbiased judgment, clear boundaries, direct communication.", "rdesc": "Overly-emotional, easily influenced, bitchy, cold-hearted.", "sequence": 62},
        {"name": "King of Swords", "desc": "Mental clarity, intellectual power, authority, truth.", "rdesc": "Quiet power, inner truth, misuse of power, manipulation.", "sequence": 63},
        {"name": "Ace of Pentacles", "desc": "A new financial or career opportunity, manifestation, abundance.", "rdesc": "Lost opportunity, lack of planning and foresight.", "sequence": 64},
        {"name": "Two of Pentacles", "desc": "Multiple priorities, time management, prioritization, adaptability.", "rdesc": "Over-committed, disorganization, reprioritization.", "sequence": 65},
        {"name": "Three of Pentacles", "desc": "Teamwork, collaboration, learning, implementation.", "rdesc": "Disharmony, misalignment, working alone.", "sequence": 66},
        {"name": "Four of Pentacles", "desc": "Saving money, security, conservatism, scarcity, control.", "rdesc": "Over-spending, greed, self-protection.", "sequence": 67},
        {"name": "Five of Pentacles", "desc": "Financial loss, poverty, lack mindset, isolation, worry.", "rdesc": "Recovery from financial loss, spiritual poverty.", "sequence": 68},
        {"name": "Six of Pentacles", "desc": "Giving, receiving, sharing wealth, generosity, charity.", "rdesc": "Self-care, unpaid debts, one-sided charity.", "sequence": 69},
        {"name": "Seven of Pentacles", "desc": "Long-term view, sustainable results, perseverance, investment.", "rdesc": "Lack of long-term vision, limited success or reward.", "sequence": 70},
        {"name": "Eight of Pentacles", "desc": "Apprenticeship, repetitive tasks, mastery, skill development.", "rdesc": "Self-development, perfectionism, misdirected activity.", "sequence": 71},
        {"name": "Nine of Pentacles", "desc": "Abundance, luxury, self-sufficiency, financial independence.", "rdesc": "Self-worth, over-investment in work, hustling.", "sequence": 72},
        {"name": "Ten of Pentacles", "desc": "Wealth, financial security, family, long-term success, contribution.", "rdesc": "The dark side of wealth, financial failure or loss.", "sequence": 73},
        {"name": "Page of Pentacles", "desc": "Manifestation, financial opportunity, skill development.", "rdesc": "Lack of progress, procrastination, learn from failure.", "sequence": 74},
        {"name": "Knight of Pentacles", "desc": "Hard work, productivity, routine, conservatism.", "rdesc": "Self-discipline, boredom, feeling ‘stuck’, perfectionism.", "sequence": 75},
        {"name": "Queen of Pentacles", "desc": "Nurturing, practical, providing financially, a working parent.", "rdesc": "Financial independence, self-care, work-home conflict.", "sequence": 76},
        {"name": "King of Pentacles", "desc": "Wealth, business, leadership, security, discipline, abundance.", "rdesc": "Financially inept, obsessed with wealth and status, stubborn.", "sequence": 77}
    ]

def get_tarot_card_by_birthdate(birthdate_str):
    deck = get_deck()
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d %H:%M")
    random.seed(birthdate.timestamp())
    card, reversed = get_card(deck)
    return {
        "name": card["name"],
        "description": card["rdesc"] if reversed else card["desc"]
    }



