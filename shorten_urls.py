# scipt for shortening urls
import pyshorteners as ps

urls = [
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/e6k61tz8",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/dds7s7uo",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/1vx7d5e5",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/es7bh0ob",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/y50c7z6y",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/62oj28fz",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/rg1nwinf",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/vf33rklf",
    "https://dotpattern-en-ws-release-6d71031de72d.herokuapp.com/InitializeParticipant/8m2zucb8"
]
for i, long_url in enumerate(urls):

    #TinyURL shortener service
    type_tiny = ps.Shortener()
    short_url = type_tiny.tinyurl.short(long_url)
    
    print(f"P{i+1}: " + short_url)


