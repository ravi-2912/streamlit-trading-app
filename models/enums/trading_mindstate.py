from enum import Enum


class TradingMindState(str, Enum):
    # ENERGY STATES
    exhausted = "Exhausted"
    tired = "Tired"
    sleepy = "Sleepy"
    lazy = "Lazy"
    fresh = "Fresh"
    energetic = "Energetic"
    hyper = "Hyper"

    # EMOTIONAL STATES - NEGATIVE
    sad = "Sad"
    gloomy = "Gloomy"
    anxious = "Anxious"
    fearful = "Fearful"
    angry = "Angry"
    frustrated = "Frustrated"
    panicked = "Panicked"
    depressed = "Depressed"
    regretful = "Regretful"
    disappointed = "Disappointed"
    vengeful = "Vengeful"

    # EMOTIONAL STATES - POSITIVE
    happy = "Happy"
    calm = "Calm"
    confident = "Confident"
    excited = "Excited"
    hopeful = "Hopeful"
    euphoric = "Euphoric"
    satisfied = "Satisfied"
    grateful = "Grateful"

    # FOCUS / COGNITIVE STATES
    focused = "Focused"
    distracted = "Distracted"
    confused = "Confused"
    overwhelmed = "Overwhelmed"
    mindful = "Mindful"
    impulsive = "Impulsive"
    rational = "Rational"
    reactive = "Reactive"
    indifferent = "Indifferent"
    zoned_out = "Zoned Out"
    tunnel_vision = "Tunnel Vision"
    flow = "In Flow"

    # GENERAL STATES
    normal = "Normal"
    active = "Active"
    neutral = "Neutral"
    aggressive = "Aggressive"
    defensive = "Defensive"
    cautious = "Cautious"
    reckless = "Reckless"
    overconfident = "Overconfident"
    disciplined = "Disciplined"
    emotional = "Emotional"
    robotic = "Robotic"
    burnt_out = "Burnt Out"
    patient = "Patient"
    bored = "Bored"
    curious = "Curious"

    # STRESS STATES
    stressed = "Stressed"
    under_pressure = "Under Pressure"
    relief = "Relief"
