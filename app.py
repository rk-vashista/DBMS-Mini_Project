from flask import *

app = Flask(__name__)


jobs = [
    {
        "id": 1,
        "title": "Chief Unicorn Wrangler",
        "location": "Atlantis",
        "salary": "1,000,000 seashells/year"
    },
    {
        "id": 2,
        "title": "Professional Cloud Painter",
        "location": "Sky City",
        "salary": "300 rainbows/month"
    },
    {
        "id": 3,
        "title": "Senior Galactic Overlord Consultant",
        "location": "Mars",
        "salary": "42 galactic credits/hour"
    },
    {
        "id": 4,
        "title": "Director of Dragon Training",
        "location": "Westeros",
        "salary": "75,000 gold coins/year"
    },
    {
        "id": 5,
        "title": "Quantum Banana Peel Analyst",
        "location": "Schrodinger's Box",
        "salary": "2 Schrödinger's cats/day"
    },
    {
        "id": 6,
        "title": "Time Travel Logistics Coordinator",
        "location": "Year 3000",
        "salary": "60,000 time units/decade"
    },
    {
        "id": 7,
        "title": "Interdimensional Space Janitor",
        "location": "Multiverse Headquarters",
        "salary": "50 dark matter particles/hour"
    },
    {
        "id": 8,
        "title": "Head of Fairy Tale Quality Assurance",
        "location": "Enchanted Forest",
        "salary": "80,000 magic beans/year"
    },
    {
        "id": 9,
        "title": "Virtual Reality Dinosaur Dentist",
        "location": "Jurassic Simulation",
        "salary": "200 virtual teeth cleaned/month"
    },
    {
        "id": 10,
        "title": "Master of Invisible Ink Documentation",
        "location": "Secret Spy Base",
        "salary": "1,500 spy gadgets/year"
    }
]
@app.route("/")
def hello_world():
    return render_template('home.html',jobs=jobs)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

