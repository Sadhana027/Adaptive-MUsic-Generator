def map_to_music_attributes(weather, mood):
    # Default parameters
    attributes = {
        "tempo": 120,        # Beats per minute
        "key": "C",          # Musical key
        "scale": "major",    # Scale type
        "instrument": "piano",
        "chords": [],        # List of chords
        "drums": []          # List of drum notes
    }

    # Adjust parameters based on weather
    if weather.lower() in ["rain", "drizzle", "clouds"]:
        attributes["tempo"] = 80
        attributes["key"] = "A minor"
        attributes["scale"] = "minor"
        attributes["instrument"] = "acoustic guitar"
    elif weather.lower() in ["clear", "sunny"]:
        attributes["tempo"] = 140
        attributes["key"] = "C"
        attributes["scale"] = "major"
        attributes["instrument"] = "electric guitar"
    elif weather.lower() in ["snow", "mist"]:
        attributes["tempo"] = 100
        attributes["key"] = "D minor"
        attributes["scale"] = "minor"
        attributes["instrument"] = "strings"

    # Adjust parameters based on mood
    if mood.lower() == "happy":
        attributes["tempo"] += 20
        attributes["scale"] = "major"
    elif mood.lower() == "sad":
        attributes["tempo"] -= 20
        attributes["scale"] = "minor"
    elif mood.lower() == "angry":
        attributes["tempo"] = 160
        attributes["instrument"] = "electric guitar"
        attributes["drums"] = [36, 38, 42]  # Kick, snare, hi-hat
    elif mood.lower() == "neutral":
        # Leave parameters as set
        pass

    # Add chords based on key and scale
    if attributes["key"] == "C" and attributes["scale"] == "major":
        attributes["chords"] = [60, 64, 67]  # C, E, G
    elif attributes["key"] == "A minor" and attributes["scale"] == "minor":
        attributes["chords"] = [57, 60, 64]  # A, C, E

    return attributes
