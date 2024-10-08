import random
from datetime import datetime
import os
import sys

def shuffle_deck(deck):
    random.shuffle(deck)

def get_card(deck):
    num = random.randint(0, len(deck) - 1)
    card = deck[num]
    del deck[num]
    rev = random.randint(0, 1)
    drawn = (card, rev)
    return drawn

def get_deck(images_dir):
    return [
        {"name": "The Fool", "desc": "New beginnings, adventure, and spontaneity.", "rdesc": "Foolishness, recklessness, and risk-taking.", "sequence": 0, "image": os.path.join(images_dir, "00.jpeg")},
        {"name": "The Magician", "desc": "Resourcefulness, power, and inspired action.", "rdesc": "Manipulation, poor planning, and untapped talents.", "sequence": 1, "image": os.path.join(images_dir, "01.jpeg")},
        {"name": "The High Priestess", "desc": "Intuition, sacred knowledge, and divine feminine.", "rdesc": "Secrets, disconnected from intuition, withdrawal.", "sequence": 2, "image": os.path.join(images_dir, "02.jpeg")},
        {"name": "The Empress", "desc": "Fertility, beauty, nature, and abundance.", "rdesc": "Creative block, dependence on others.", "sequence": 3, "image": os.path.join(images_dir, "03.jpeg")},
        {"name": "The Emperor", "desc": "Authority, structure, control, and fatherhood.", "rdesc": "Domination, excessive control, lack of discipline.", "sequence": 4, "image": os.path.join(images_dir, "04.jpeg")},
        {"name": "The Hierophant", "desc": "Spiritual wisdom, religious beliefs, and conformity.", "rdesc": "Personal beliefs, freedom, challenging the status quo.", "sequence": 5, "image": os.path.join(images_dir, "05.jpeg")},
        {"name": "The Lovers", "desc": "Love, harmony, relationships, and values alignment.", "rdesc": "Self-love, disharmony, imbalance in relationships.", "sequence": 6, "image": os.path.join(images_dir, "06.jpeg")},
        {"name": "The Chariot", "desc": "Control, willpower, success, and determination.", "rdesc": "Self-discipline, opposition, lack of direction.", "sequence": 7, "image": os.path.join(images_dir, "07.jpeg")},
        {"name": "Strength", "desc": "Courage, persuasion, influence, and compassion.", "rdesc": "Self-doubt, low energy, raw emotion.", "sequence": 8, "image": os.path.join(images_dir, "11.jpeg")},
        {"name": "The Hermit", "desc": "Soul-searching, introspection, and inner guidance.", "rdesc": "Isolation, loneliness, withdrawal.", "sequence": 9, "image": os.path.join(images_dir, "09.jpeg")},
        {"name": "Wheel of Fortune", "desc": "Good luck, karma, and life cycles.", "rdesc": "Bad luck, resistance to change, breaking cycles.", "sequence": 10, "image": os.path.join(images_dir, "10.jpeg")},
        {"name": "Justice", "desc": "Fairness, truth, cause and effect, law.", "rdesc": "Unfairness, lack of accountability, dishonesty.", "sequence": 11, "image": os.path.join(images_dir, "08.jpeg")},
        {"name": "The Hanged Man", "desc": "Pause, surrender, letting go, and new perspectives.", "rdesc": "Delays, resistance, stalling, indecision.", "sequence": 12, "image": os.path.join(images_dir, "12.jpeg")},
        {"name": "Death", "desc": "Endings, change, transformation, transition.", "rdesc": "Resistance to change, personal transformation.", "sequence": 13, "image": os.path.join(images_dir, "13.jpeg")},
        {"name": "Temperance", "desc": "Balance, moderation, patience, and purpose.", "rdesc": "Imbalance, excess, lack of long-term vision.", "sequence": 14, "image": os.path.join(images_dir, "14.jpeg")},
        {"name": "The Devil", "desc": "Shadow self, attachment, addiction, restriction.", "rdesc": "Releasing limiting beliefs, exploring dark thoughts.", "sequence": 15, "image": os.path.join(images_dir, "15.jpeg")},
        {"name": "The Tower", "desc": "Sudden change, upheaval, chaos, and revelation.", "rdesc": "Avoidance of disaster, fear of change.", "sequence": 16, "image": os.path.join(images_dir, "16.jpeg")},
        {"name": "The Star", "desc": "Hope, faith, purpose, and renewal.", "rdesc": "Lack of faith, despair, disconnection.", "sequence": 17, "image": os.path.join(images_dir, "17.jpeg")},
        {"name": "The Moon", "desc": "Illusion, fear, anxiety, subconscious, and intuition.", "rdesc": "Release of fear, repressed emotion, inner confusion.", "sequence": 18, "image": os.path.join(images_dir, "18.jpeg")},
        {"name": "The Sun", "desc": "Positivity, fun, warmth, success, and vitality.", "rdesc": "Inner child, feeling down, overly optimistic.", "sequence": 19, "image": os.path.join(images_dir, "19.jpeg")},
        {"name": "Judgement", "desc": "Reflection, reckoning, and inner calling.", "rdesc": "Self-doubt, inner critic, ignoring the call.", "sequence": 20, "image": os.path.join(images_dir, "20.jpeg")},
        {"name": "The World", "desc": "Completion, integration, accomplishment, travel.", "rdesc": "Seeking personal closure, short-cuts, delays.", "sequence": 21, "image": os.path.join(images_dir, "21.jpeg")},
        {"name": "Ace of Wands", "desc": "Inspiration, new opportunities, growth, potential.", "rdesc": "An emerging idea, lack of direction, distractions.", "sequence": 22, "image": os.path.join(images_dir, "wa01.jpeg")},
        {"name": "Two of Wands", "desc": "Future planning, progress, decisions, discovery.", "rdesc": "Personal goals, inner alignment, fear of unknown.", "sequence": 23, "image": os.path.join(images_dir, "wa02.jpeg")},
        {"name": "Three of Wands", "desc": "Progress, expansion, foresight, overseas opportunities.", "rdesc": "Playing small, lack of foresight, unexpected delays.", "sequence": 24, "image": os.path.join(images_dir, "wa03.jpeg")},
        {"name": "Four of Wands", "desc": "Celebration, joy, harmony, relaxation, homecoming.", "rdesc": "Personal celebration, inner harmony, conflict with others.", "sequence": 25, "image": os.path.join(images_dir, "wa04.jpeg")},
        {"name": "Five of Wands", "desc": "Conflict, disagreements, competition, tension, diversity.", "rdesc": "Inner conflict, conflict avoidance, tension release.", "sequence": 26, "image": os.path.join(images_dir, "wa05.jpeg")},
        {"name": "Six of Wands", "desc": "Success, public recognition, progress, self-confidence.", "rdesc": "Private achievement, personal definition of success.", "sequence": 27, "image": os.path.join(images_dir, "wa06.jpeg")},
        {"name": "Seven of Wands", "desc": "Challenge, competition, protection, perseverance.", "rdesc": "Exhaustion, giving up, overwhelmed.", "sequence": 28, "image": os.path.join(images_dir, "wa07.jpeg")},
        {"name": "Eight of Wands", "desc": "Movement, fast-paced change, action, alignment.", "rdesc": "Delays, frustration, resisting change.", "sequence": 29, "image": os.path.join(images_dir, "wa08.jpeg")},
        {"name": "Nine of Wands", "desc": "Resilience, courage, persistence, test of faith, boundaries.", "rdesc": "Inner resources, struggle, overwhelm, defensive.", "sequence": 30, "image": os.path.join(images_dir, "wa09.jpeg")},
        {"name": "Ten of Wands", "desc": "Burden, extra responsibility, hard work, completion.", "rdesc": "Doing it all, carrying the burden, delegation.", "sequence": 31, "image": os.path.join(images_dir, "wa10.jpeg")},
        {"name": "Page of Wands", "desc": "Inspiration, ideas, discovery, limitless potential, free spirit.", "rdesc": "Newly formed ideas, redirecting energy, self-limiting beliefs.", "sequence": 32, "image": os.path.join(images_dir, "wapa.jpeg")},
        {"name": "Knight of Wands", "desc": "Energy, passion, inspired action, adventure, impulsiveness.", "rdesc": "Passion project, haste, scattered energy, delays.", "sequence": 33, "image": os.path.join(images_dir, "wakn.jpeg")},
        {"name": "Queen of Wands", "desc": "Courage, confidence, independence, social butterfly, determination.", "rdesc": "Self-respect, self-confidence, introverted, re-establish sense of self.", "sequence": 34, "image": os.path.join(images_dir, "waqu.jpeg")},
        {"name": "King of Wands", "desc": "Natural-born leader, vision, entrepreneur, honour.", "rdesc": "Impulsiveness, haste, ruthless, high expectations.", "sequence": 35, "image": os.path.join(images_dir, "waki.jpeg")},
        {"name": "Ace of Cups", "desc": "Love, new relationships, compassion, creativity.", "rdesc": "Self-love, intuition, repressed emotions.", "sequence": 36, "image": os.path.join(images_dir, "cu01.jpeg")},
        {"name": "Two of Cups", "desc": "Unified love, partnership, mutual attraction.", "rdesc": "Self-love, break-ups, disharmony, distrust.", "sequence": 37, "image": os.path.join(images_dir, "cu02.jpeg")},
        {"name": "Three of Cups", "desc": "Celebration, friendship, creativity, collaborations.", "rdesc": "Independence, alone time, hardcore partying, 'three's a crowd'.", "sequence": 38, "image": os.path.join(images_dir, "cu03.jpeg")},
        {"name": "Four of Cups", "desc": "Meditation, contemplation, apathy, re-evaluation.", "rdesc": "Retreat, withdrawal, checking in for alignment.", "sequence": 39, "image": os.path.join(images_dir, "cu04.jpeg")},
        {"name": "Five of Cups", "desc": "Regret, failure, disappointment, pessimism.", "rdesc": "Personal setbacks, self-forgiveness, moving on.", "sequence": 40, "image": os.path.join(images_dir, "cu05.jpeg")},
        {"name": "Six of Cups", "desc": "Revisiting the past, childhood memories, innocence, joy.", "rdesc": "Living in the past, forgiveness, lacking playfulness.", "sequence": 41, "image": os.path.join(images_dir, "cu06.jpeg")},
        {"name": "Seven of Cups", "desc": "Opportunities, choices, wishful thinking, illusion.", "rdesc": "Alignment, personal values, overwhelmed by choices.", "sequence": 42, "image": os.path.join(images_dir, "cu07.jpeg")},
        {"name": "Eight of Cups", "desc": "Disappointment, abandonment, withdrawal, escapism.", "rdesc": "Trying one more time, indecision, aimless drifting, walking away.", "sequence": 43, "image": os.path.join(images_dir, "cu08.jpeg")},
        {"name": "Nine of Cups", "desc": "Contentment, satisfaction, gratitude, wish come true.", "rdesc": "Inner happiness, materialism, dissatisfaction.", "sequence": 44, "image": os.path.join(images_dir, "cu09.jpeg")},
        {"name": "Ten of Cups", "desc": "Divine love, blissful relationships, harmony, alignment.", "rdesc": "Disconnection, misaligned values, struggling relationships.", "sequence": 45, "image": os.path.join(images_dir, "cu10.jpeg")},
        {"name": "Page of Cups", "desc": "Creative opportunities, intuitive messages, curiosity, possibility.", "rdesc": "New ideas, doubting intuition, emotional immaturity.", "sequence": 46, "image": os.path.join(images_dir, "cupa.jpeg")},
        {"name": "Knight of Cups", "desc": "Romance, charm, 'Knight in shining armor', imagination.", "rdesc": "Overactive imagination, unrealistic, jealous, moody.", "sequence": 47, "image": os.path.join(images_dir, "cukn.jpeg")},
        {"name": "Queen of Cups", "desc": "Compassionate, caring, emotionally stable, intuitive, in flow.", "rdesc": "Inner feelings, self-care, self-love, co-dependency.", "sequence": 48, "image": os.path.join(images_dir, "cuqu.jpeg")},
        {"name": "King of Cups", "desc": "Emotionally balanced, compassionate, diplomatic.", "rdesc": "Self-compassion, inner feelings, moodiness, emotionally manipulative.", "sequence": 49, "image": os.path.join(images_dir, "cuki.jpeg")},
        {"name": "Ace of Swords", "desc": "Breakthrough, clarity, sharp mind.", "rdesc": "Inner clarity, re-thinking an idea, clouded judgment.", "sequence": 50, "image": os.path.join(images_dir, "sw01.jpeg")},
        {"name": "Two of Swords", "desc": "Difficult decisions, weighing up options, an impasse, avoidance.", "rdesc": "Indecision, confusion, information overload.", "sequence": 51, "image": os.path.join(images_dir, "sw02.jpeg")},
        {"name": "Three of Swords", "desc": "Heartbreak, emotional pain, sorrow, grief, hurt.", "rdesc": "Negative self-talk, releasing pain, optimism, forgiveness.", "sequence": 52, "image": os.path.join(images_dir, "sw03.jpeg")},
        {"name": "Four of Swords", "desc": "Rest, relaxation, meditation, contemplation, recuperation.", "rdesc": "Exhaustion, burn-out, deep contemplation, stagnation.", "sequence": 53, "image": os.path.join(images_dir, "sw04.jpeg")},
        {"name": "Five of Swords", "desc": "Conflict, disagreements, competition, defeat, winning at all costs.", "rdesc": "Reconciliation, making amends, past resentment.", "sequence": 54, "image": os.path.join(images_dir, "sw05.jpeg")},
        {"name": "Six of Swords", "desc": "Transition, change, rite of passage, releasing baggage.", "rdesc": "Personal transition, resistance to change, unfinished business.", "sequence": 55, "image": os.path.join(images_dir, "sw06.jpeg")},
        {"name": "Seven of Swords", "desc": "Betrayal, deception, getting away with something, acting strategically.", "rdesc": "Imposter syndrome, keeping secrets, hiding true intentions.", "sequence": 56, "image": os.path.join(images_dir, "sw07.jpeg")},
        {"name": "Eight of Swords", "desc": "Negative thoughts, self-imposed restriction, imprisonment, victim mentality.", "rdesc": "Self-limiting beliefs, inner critic, releasing negative thoughts, open to new perspectives.", "sequence": 57, "image": os.path.join(images_dir, "sw08.jpeg")},
        {"name": "Nine of Swords", "desc": "Anxiety, worry, fear, depression, nightmares.", "rdesc": "Inner turmoil, deep-seated fears, secrets, releasing worry.", "sequence": 58, "image": os.path.join(images_dir, "sw09.jpeg")},
        {"name": "Ten of Swords", "desc": "Painful endings, deep wounds, betrayal, loss, crisis.", "rdesc": "Recovery, regeneration, resisting an inevitable end.", "sequence": 59, "image": os.path.join(images_dir, "sw10.jpeg")},
        {"name": "Page of Swords", "desc": "New ideas, curiosity, thirst for knowledge, new ways of communicating.", "rdesc": "Self-expression, all talk and no action, haphazard action, haste.", "sequence": 60, "image": os.path.join(images_dir, "swpa.jpeg")},
        {"name": "Knight of Swords", "desc": "Ambitious, action-oriented, driven to succeed, fast-thinking.", "rdesc": "Restless, unfocused, impulsive, burn-out.", "sequence": 61, "image": os.path.join(images_dir, "swkn.jpeg")},
        {"name": "Queen of Swords", "desc": "Independent, unbiased judgment, clear boundaries, direct communication.", "rdesc": "Overly-emotional, easily influenced, bitchy, cold-hearted.", "sequence": 62, "image": os.path.join(images_dir, "swqu.jpeg")},
        {"name": "King of Swords", "desc": "Mental clarity, intellectual power, authority, truth.", "rdesc": "Quiet power, inner truth, misuse of power, manipulation.", "sequence": 63, "image": os.path.join(images_dir, "swki.jpeg")},
        {"name": "Ace of Coins", "desc": "A new financial or career opportunity, manifestation, abundance.", "rdesc": "Lost opportunity, lack of planning and foresight.", "sequence": 64, "image": os.path.join(images_dir, "pe01.jpeg")},
        {"name": "Two of Coins", "desc": "Multiple priorities, time management, prioritization, adaptability.", "rdesc": "Over-committed, disorganization, reprioritization.", "sequence": 65, "image": os.path.join(images_dir, "pe02.jpeg")},
        {"name": "Three of Coins", "desc": "Teamwork, collaboration, learning, implementation.", "rdesc": "Disharmony, misalignment, working alone.", "sequence": 66, "image": os.path.join(images_dir, "pe03.jpeg")},
        {"name": "Four of Coins", "desc": "Saving money, security, conservatism, scarcity, control.", "rdesc": "Over-spending, greed, self-protection.", "sequence": 67, "image": os.path.join(images_dir, "pe04.jpeg")},
        {"name": "Five of Coins", "desc": "Financial loss, poverty, lack mindset, isolation, worry.", "rdesc": "Recovery from financial loss, spiritual poverty.", "sequence": 68, "image": os.path.join(images_dir, "pe05.jpeg")},
        {"name": "Six of Coins", "desc": "Giving, receiving, sharing wealth, generosity, charity.", "rdesc": "Self-care, unpaid debts, one-sided charity.", "sequence": 69, "image": os.path.join(images_dir, "pe06.jpeg")},
        {"name": "Seven of Coins", "desc": "Long-term view, sustainable results, perseverance, investment.", "rdesc": "Lack of long-term vision, limited success or reward.", "sequence": 70, "image": os.path.join(images_dir, "pe07.jpeg")},
        {"name": "Eight of Coins", "desc": "Apprenticeship, repetitive tasks, mastery, skill development.", "rdesc": "Self-development, perfectionism, misdirected activity.", "sequence": 71, "image": os.path.join(images_dir, "pe08.jpeg")},
        {"name": "Nine of Coins", "desc": "Abundance, luxury, self-sufficiency, financial independence.", "rdesc": "Self-worth, over-investment in work, hustling.", "sequence": 72, "image": os.path.join(images_dir, "pe09.jpeg")},
        {"name": "Ten of Coins", "desc": "Wealth, financial security, family, long-term success, contribution.", "rdesc": "The dark side of wealth, financial failure or loss.", "sequence": 73, "image": os.path.join(images_dir, "pe10.jpeg")},
        {"name": "Page of Coins", "desc": "Manifestation, financial opportunity, skill development.", "rdesc": "Lack of progress, procrastination, learn from failure.", "sequence": 74, "image": os.path.join(images_dir, "pepa.jpeg")},
        {"name": "Knight of Coins", "desc": "Hard work, productivity, routine, conservatism.", "rdesc": "Self-discipline, boredom, feeling ‘stuck’, perfectionism.", "sequence": 75, "image": os.path.join(images_dir, "pekn.jpeg")},
        {"name": "Queen of Coins", "desc": "Nurturing, practical, providing financially, a working parent.", "rdesc": "Financial independence, self-care, work-home conflict.", "sequence": 76, "image": os.path.join(images_dir, "pequ.jpeg")},
        {"name": "King of Coins", "desc": "Wealth, business, leadership, security, discipline, abundance.", "rdesc": "Financially inept, obsessed with wealth and status, stubborn.", "sequence": 77, "image": os.path.join(images_dir, "peki.jpeg")}
    ]

def get_tarot_card_by_birthdate(birthdate_str):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    images_dir = os.path.join(script_dir, "images")
    deck = get_deck(images_dir)
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d %H:%M")
    random.seed(birthdate.timestamp())
    card, reversed = get_card(deck)
    return {
        "name": card["name"],
        "description": card["rdesc"] if reversed else card["desc"],
        "image": card["image"]
    }

def get_daily_tarot_card():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    images_dir = os.path.join(script_dir, "images")
    deck = get_deck(images_dir)
    shuffle_deck(deck)
    card, reversed = get_card(deck)
    return {
        "name": card["name"],
        "description": card["rdesc"] if reversed else card["desc"],
        "image": card["image"]
    }

def check_image_paths():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    images_dir = os.path.join(script_dir, "images")
    deck = get_deck(images_dir)
    for card in deck:
        image_path = card['image']
        if os.path.exists(image_path):
            print(f"Image for {card['name']} exists: {image_path}")
        else:
            print(f"Image for {card['name']} is missing: {image_path}")

if __name__ == "__main__":
    check_image_paths()






