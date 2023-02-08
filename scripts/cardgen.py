#!/usr/bin/env python3
"""
  Build cards
"""

from xml.etree import ElementTree
from os import listdir
import math

# Open original file
tree = ElementTree.parse('template.svg')
root = tree.getroot()

# Append new tag: <a x='1' y='abc'>body text</a>
#new_tag = xml.etree.ElementTree.SubElement(et.getroot(), 'a')
#new_tag.text = 'body text'
#new_tag.attrib['x'] = '1' # must be str; cannot be an int
#new_tag.attrib['y'] = 'abc'

# Write back to file
#et.write('file.xml')                        

ElementTree.register_namespace("","http://www.w3.org/2000/svg")
ElementTree.register_namespace("xlink","http://www.w3.org/1999/xlink")
ns = {'xlink': 'http://www.w3.org/1999/xlink'}

storyAspects = ["Archetype", "Object", "Place", "Emotion", "Property", "Action"]

# Cards that will have wild/chaotic response to oracle & pacing
wildcards = [6, 42] # 6 of gold & 7 of clubs

storyicons = {}
for a in storyAspects:
  storyicons[a] = [("storyicons/" + a + "/" + f) for f in listdir("storyicons/" + a) if f.endswith(".svg")]

zodiacsigns = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
shengxiaosigns = [("guideicons/" + f) for f in listdir("guideicons/") if f.startswith("shengxiao-")]
ichingtrigrams = [("guideicons/" + f) for f in listdir("guideicons/") if f.startswith("iching-")]
futharkrunes = [("guideicons/" + f) for f in listdir("guideicons/") if f.startswith("rune-")]

for n in range(48):

  fname = f'cards/{(n+1):02d}.svg'

  ## Card Value
  cardValue = 1 + (n % 12)

  ## Card Suit
  cardSuit = 'guideicons/suit-'
  suitValue = math.floor(n/12) % 4
  if suitValue == 0:
    cardSuit += 'clubs'
  elif suitValue == 1:
    cardSuit += 'swords'
  elif suitValue == 2:
    cardSuit += 'cups'
  else:
    cardSuit += 'coins'
  cardSuit += '.svg'

  ## Yes / No oracle answers
  # 1-6 No  ;  7-12 Yes
  oracleAnswer = 'guideicons/oracle-' + ('yes' if (n >= 7) else 'no') + '.svg';

  # Special case for the wildcards: "invalid question" response
  if n in wildcards:
    oracleAnswer = 'guideicons/oracle-invalid.svg';


  ## Modifiers to the oracle answer
  # 1: and  ;  2-4: none  ;  5-8: but  ;  9-11: none  ;  12: and 
  oracleModifier = 'guideicons/oracle-modifier-'
  if cardValue == 1 or cardValue == 12:
    oracleModifier += 'and'
  elif cardValue >= 5 or cardValue <= 8:
    oracleModifier += 'but'
  else:
    oracleModifier += 'none'
  oracleModifier += '.svg'


  ## Pacing event progress
  pacingProgress = "guideicons/pacing-act-"
  if (n % 4 < 2):
    pacingProgress += "develop"
  else:
    pacingProgress += "resolve"
  pacingProgress += ".svg"

  ## Pacing event factor
  pacingFactor = "guideicons/pacing-"
  if cardValue == 1: # There's only 4 cards with "Yes, and...", exclude environment factor
    if (suitValue%2 == 1):
      pacingFactor += "character"
    else:
      pacingFactor += "quest"
  elif n in wildcards: # wildcard factors (matching "invalid question" ones)
    pacingFactor += "wildcard"
  else: # 42 remaining cards (divisible by 3 spread across all numbers)
    i = (n-4)%3
    if (i == 1):
      pacingFactor += "character"
    elif (i == 2):
      pacingFactor += "environment"
    else:
      pacingFactor += "quest"
  pacingFactor += ".svg"


  ## Zodiac signs
  zodiac = "guideicons/zodiac-"
  zodiac += zodiacsigns[n % len(zodiacsigns)]
  zodiac += ".svg"

  ## Chinese horoscope
  shengxiao = shengxiaosigns[math.floor(n/4) % len(shengxiaosigns)]

  ## I-Ching
  iching = ichingtrigrams[n % len(ichingtrigrams)]

  ## Elder Futhark runes
  rune = futharkrunes[n % len(futharkrunes)]

  print("Generating:", fname)

  tree.find('.//*[@id = "cardValue"]').text = f'{cardValue}'
  tree.find('.//*[@id = "cardSuit"]', ns).set('{http://www.w3.org/1999/xlink}href', cardSuit)
  tree.find('.//*[@id = "oracleAnswer"]', ns).set('{http://www.w3.org/1999/xlink}href', oracleAnswer)
  tree.find('.//*[@id = "oracleModifier"]', ns).set('{http://www.w3.org/1999/xlink}href', oracleModifier)
  tree.find('.//*[@id = "pacingProgress"]', ns).set('{http://www.w3.org/1999/xlink}href', pacingProgress)
  tree.find('.//*[@id = "pacingFactor"]', ns).set('{http://www.w3.org/1999/xlink}href', pacingFactor)

  tree.find('.//*[@id = "zodiac"]', ns).set('{http://www.w3.org/1999/xlink}href', zodiac)
  tree.find('.//*[@id = "shengxiao"]', ns).set('{http://www.w3.org/1999/xlink}href', shengxiao)
  tree.find('.//*[@id = "iching"]', ns).set('{http://www.w3.org/1999/xlink}href', iching)
  tree.find('.//*[@id = "rune"]', ns).set('{http://www.w3.org/1999/xlink}href', rune)

  for aspect in storyAspects:
    imagepath = storyicons[aspect][n % len(storyicons[aspect])]
    tree.find('.//*[@id = "story' + aspect + '"]', ns).set('{http://www.w3.org/1999/xlink}href', imagepath)

  tree.write(fname, encoding='unicode', xml_declaration=True)
