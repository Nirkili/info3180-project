# Written by Dana Archer
import math
from haversine import haversine, Unit

# Source: https://latlong.info/jamaica
# Source: latitude.to

"""
These are the coordinates for each parish. They are generalized to make distance calculations simpler.

"""
COORDINATES = {
  "Kingston":      (17.9683, -76.7827),
  "St. Andrew":    (18.0747, -76.7956),
  "St. Thomas":    (17.9320, -76.5419),
  "Portland":      (18.0844, -76.4100),
  "St. Mary":      (18.2923, -76.9561),
  "St. Ann":       (18.4346, -77.2016),
  "Trelawny":      (18.3526, -77.6078),
  "St. James":     (18.4762, -77.8939),
  "Hanover":       (18.4098, -78.1336),
  "Westmoreland":  (18.2944, -78.1564),
  "St. Elizabeth": (18.0670, -77.5161),
  "Manchester":    (18.0670, -77.5161),
  "Clarendon":     (17.9557, -77.2405),
  "St. Catherine": (18.0364, -77.0564),
}

# Helper functions
"""Takes the Enum age range and minds the minimum and maximum values"""
def split_age_range(preference):
    print("HELOOOOO")
    print(preference)
    if preference.startswith(">"):
        min = 41
        max = None
        return min, max
    range = preference.split("-")
    min = int(range[0])
    max = int(range[1])
    return min, max


def is_age_preference(age, preference):
    min, max = split_age_range(preference)

    if max is None: return age >= min
    return min <= age >= max



"""
This function uses the haversine function to calculate the rough distance between given coordinates.

"""
# Source: https://math.stackexchange.com/questions/474602/reverse-use-of-haversine-formula
# Source: https://www.studeersnel.nl/nl/document/wageningen-university-research/programming-in-python/read-me-section-groupwork-1/79727849
# Haversine function: https://pypi.org/project/haversine/ 
def calc_distance(current_location, other_location):
  R = 6371 
  # Get coordinates
  curret_coords = COORDINATES.get(current_location)
  other_coords = COORDINATES.get(other_location)

  # Perform calculation
  distance = haversine(curret_coords, other_coords, unit=Unit.KILOMETERS)
  return distance




"""

Matching Algorithm

This algorithm scores all users in the system against the current user's attributes. These include:

  - Gender Preference:    3.0 points
  - Location radius:      2.0 points
  - Shared Interests (max 5):     0.4 points each for a maximum of 2.0
  - Age Preference:               2.0 points
  - Relationship type:            1.5 points
  - Wants Children:               1 point
  
  
  
  The highest possible score is 12.5. When normalized to a percentage this represents 100%

  CONSTRAINTS
  - Only public profiles are available for matching
  - Results are automatically sorded by descending order. 
  - Profiles that have already been liked/disliked are excluded."""



def calc_score(current_profile, current_interests, profile, interests):
  base_score = 0

  # For each shared interest add 0.4 to the score
  shared_interests = min(len(set(current_interests) & set(interests)), 5)
  base_score += 0.4

  # If a potential match's location is with the curren user's desired range 
  if calc_distance(current_profile.location, profile.location) <= int(current_profile.radius_preference):
     base_score += 2.5

  # If the a potetial match fits the current user's gender preference
  if current_profile.gender_preference == profile.gender:
    base_score += 3

  # If the potential match fits the current user's age preferences
  if is_age_preference(profile.age, current_profile.age_preference):
     base_score += 2

  # If the potential match fits the current user's relationship type preference
  if current_profile.relationship_type_preference == profile.relationship_type_preference:
     base_score += 1.5

  # If the potential match fits the current user's child preference
  if current_profile.wants_children == profile.wants_children:
     base_score += 0.5

  return base_score