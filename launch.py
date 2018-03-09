#Surindra Goolcharan
#Project Name: "Music to play Dota 2"

import os, socket,select
import sys
import time, datetime
import random
import win32api, win32con
from PIL import Image
from PIL import ImageDraw, ImageFont
import ctypes
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

import subprocess, shlex, re, fnmatch
from subprocess import call
from fuzzywuzzy import fuzz

chatter = []
chatterDonor = []


def duration(songName):

	try:
		return cachedDuration[songName]
	except:
		try:
			filename = 'D:\music\\'
			filename += songName
			filename += '^%^'
			filename += str(cacheRank[songName])
			filename += '.mp3'
			args=("C:\\Drive\\Code\\ffprobe\\bin\\ffprobe.exe","-show_entries", "format=duration","-i",filename)
			popen = subprocess.Popen(args, stdout = subprocess.PIPE)
			popen.wait()
			out = popen.stdout.read()
			out = str(out)
			for line in out.split('\\n'):
				line = line.strip()
				if line.startswith('duration='):
					lastline = line[9:-2]
			cachedDuration[songName] = float(lastline)
			if float(lastline) < 600:
				return(float(lastline))
			else:
				return(600)
		except:
			return(0)
	
def setPos(x,y):
	win32api.SetCursorPos((x,y))
def lC(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	#time.sleep(.01)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def rC(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
	#time.sleep(.01)
	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
	
heroDict = {"anti-mage": ("am", "antimage","andy","burning","anti-mage","magina"),"axe": ("axe","mogul","khan"),"bane": ("bane","atropos"),"bloodseeker": ("bs","bloodseeker","blood","seeker","bloodcyka"),"crystal maiden": ("cm","crystal","maiden"),"drow ranger": ("drow","ranger"),"earthshaker": ("es","earth","earthshaker"),"juggernaut": ("jugger","juggernaut"),"mirana": ("potm","mirana"),"shadow fiend": ("sf","shadow","fiend"),"morphling": ("morph","morphling"),"phantom lancer": ("pl","lancer"),"puck": ("puck"),"pudge": ("pudge","butcher"),"razor": ("razor"),"sand king": ("sk","sand"),"storm spirit": ("storm"),"sven": ("sven"),"tiny": ("tiny"),"vengeful spirit": ("venge","vengeful"),"windranger": ("wind","windrunner","alleria","windranger"),"zeus": ("zuus","zeus","merlini","olympus"),"kunkka": ("kunkka","admiral","coco","proudmoore"),"lina": ("lina","slayer","inverse"),"lich": ("lich","ethreain","kelthuzad"),"lion": ("lion"),"shadow shaman": ("rhasta","shaman"),"slardar": ("slardar","slithereen"),"tidehunter": ("tide","leviathan"),"witch doctor": ("witch","doctor","zharvakko"),"riki": ("riki","rikimaru"),"enigma": ("enigma"),"tinker": ("tinker","boush"),"sniper": ("kardel","sharpeye","sniper"),"necrophos": ("necrolyte","necrophos","rotundjere","necrolight"),"warlock": ("warlock","demnok","lannik"),"beastmaster": ("karroch","beastmaster","rexxar","bm","beast"),"queen of pain": ("akasha","qop","queen","pain"),"venomancer": ("lesale","deathbringer","veno","venomancer","hydralisk"),"faceless void": ("void","faceless","darkterror","gozerk"),"wraith king": ("ostarion","wraith","skeleton","wk"),"death prophet": ("dp","death","krobelus"),"phantom assassin": ("pa","mortred","assassin"),"pugna": ("oblivion","pugna"),"templar assassin": ("ta","templar","lanaya"),"viper": ("viper","netherdrake"),"luna": ("luna"),"dragon knight": ("dk","dragon","davion"),"dazzle": ("dazzle","priest","razzle"),"clockwerk": ("rattletrap","clockwerk","clockwork"),"leshrac": ("leshrac"),"natures prophet": ("furion","malfurion","natures","prophet"),"lifestealer": ("naix","lifestealer","gollum"),"dark seer": ("dark","seer","ishkafel"),"clinkz": ("clinkz","bone","fletcher"),"omniknight": ("omniknight","omni","purist"),"enchantress": ("aiushtha","enchantress","ench","bambi"),"huskar": ("huskar"),"night stalker": ("ns","night","stalker","balanar"),"broodmother": ("arachnia","broodmother","brood","broodmama"),"bounty hunter": ("bh","bounty","hunter","gondar"),"weaver": ("weaver","nerub","nerubian","anoobseran","skitskurr"),"jakiro": ("jakiro","twin"),"batrider": ("batrider","bat","jinzakk"),"chen": ("chen"),"spectre": ("mercurial","spectre"),"doom": ("lucifer","doom","doombringer","bringer"),"ancient apparition": ("aa","ancient","apparition","kaldr"),"ursa": ("ursa","ulfsaar","fuzzy","wuzzy"),"spirit breaker": ("bara","sb","breaker","barathrum","spacecow"),"gyrocopter": ("gyro","gyrocopter","aurel"),"alchemist": ("razzil","darkbrew","alch","alchemist"),"invoker": ("invoker","carl","kael"),"silencer": ("silencer","nortrom"),"outworld devourer": ("od","outworld","devourer","obsidian","destroyer"),"lycan": ("lycan","banehallow"),"brewmaster": ("brewmaster","mangix"),"shadow demon": ("demon","sd","eredar","giblet"),"lone druid": ("lone","druid","sylla","syllabear"),"chaos knight": ("ck","nessaj","chaos"),"meepo": ("meepo","geomancer"),"treant": ("rooftrellen","treant","tree","protector"),"ogre magi": ("aggron","stonebreak","ogre","magi"),"undying": ("undying","undy","dirge"),"rubick": ("rubick","magus","grand"),"disruptor": ("disruptor","stormcrafter","thrall"),"nyx assassin": ("nyx","anubarak","anoobarak"),"naga siren": ("slithice","naga","siren"),"keeper of the light": ("kotl","kotol","keeper","light","ezalor"),"io": ("io","wisp","guardian"),"visage": ("visage","necrolic"),"slark": ("slark","nightcrawler","murloc"),"medusa": ("medusa","gorgon"),"troll warlord": ("troll","warlord","jahrakal"),"centaur warrunner": ("centaur","bradwarden","warrunner","cent"),"magnus": ("s4","magnus","manoceros","magnataur"),"timbersaw": ("timber","shredder","timbersaw","rizzrack"),"bristleback": ("bristleback","rigwarl","bristle"),"tusk": ("ymir","tusk","tuskarr","saitama"),"skywrath mage": ("skywrath","dragonus","sky"),"abaddon": ("abba","abbadon","avernus","arthas"),"elder titan": ("et","elder","titan","tauren","chieftain"),"legion commander": ("lc","legion","commander","tresdin"),"ember spirit": ("ember","xin"),"earth spirit": ("kaolin","earthspirit"),"terrorblade": ("terror","tb","terrorblade"),"phoenix": ("phoenix","pheonix","feenix","icarus"),"oracle": ("oracle","nerif"),"techies": ("techies","squee","spleen","spoon","goblin"),"winter wyvern": ("arouth","winter","wyvern"),"arc warden": ("zet","arc","warden"),"monkey king":("monkey","wukong"),"underlord":("underlord","vrogros","pitlord")}

heroInfoDict = {"abaddon": [("mist coil","aphotic shield","curse of avernus","borrowed time"),("23 + 2.6","17 + 1.5","21 + 2.0","55-65","1.4","310","0.5","1800/800","+20% XP Gain","+25 Damage","+5 Armor","+200 Mana","15% Cooldown Reduction","+25 Movement Speed","?+300 Aphotic Shield Health","+25 Strength")],"alchemist": [("acid spray","unstable concoction","greevils greed","chemical rage"),("25 + 2.1","16 + 1.2","25 + 1.8","49-58","1.6","295","0.6","1800/800","+4 Armor","+20 Damage","+6 All Stats","?+100 Unstable Concoction Damage","+300 Damage","+30 Attack Speed","?-5 Acid Spray Armor","30% Lifesteal")],"ancient apparition": [("cold feet","ice vortex","chilling touch","ice blast"),("18 + 1.7","20 + 2.2","25 + 2.6","44-54","1.9","295","0.6","1800/800","+8% Spell Amplification","+60 Gold/Min","+30 Health Regen","?-1s Ice Vortex Cooldown","?+8% Ice Vortex Slow/Resistance","+400 Health","?+100 Chilling Touch Damage","?4 Charges of Cold Feet")],"anti-mage": [("mana break", "blink","spell shield","mana void"),("22 + 1.5","22 + 2.8","15 + 1.8","49-53","2.1","315","0.5","1800/800","+20 Damage","+150 Health","?-1s Blink Cooldown","+20 Attack Speed","+10 All Stats","15% Evasion","?-50s Mana Void Cooldown","+25 Agility")],"arc warden": [("flux","magnetic field","spark wraith","tempest double"),("24 + 3.0","15 + 1.8","24 + 2.6","44-54","0.1","285","0.6","1800/800","+25 Attack Speed","?+20 Flux DPS","+200 Health","+30 Damage","+100 Attack Range","10% Cooldown Reduction","?+250 Spark Wraith Damage","30% Lifesteal")],"axe": [("berserkers call","battle hunger","counter helix","culling blade"),("25 + 2.8","20 + 2.2","18 + 1.6","49-53","1.9","290","0.6","1800/800","+3 Mana Regen","+6 Strength","+250 Health","+75 Damage","+35 Movement Speed","+25 Health Regen","?+100 Battle Hunger DPS","+15 Armor")],"bane": [("enfeeble","brain sap","nightmare","fiends grip"),("22 + 2.4","22 + 2.4","22 + 2.4","59-65","4.1","310","0.6","1800/800","+200 Mana","+6 Armor","+30% XP Gain","+250 Health","+175 Cast Range","?+90 Enfeeble Damage Reduction","?+200 Brain Sap Damage/Heal","+100 Movement Speed")],"batrider": [("sticky napalm","flamebreak","firefly","flaming lasso"),("23 + 2.7","15 + 1.5","24 + 2.5","38-42","2.1","290","1.0","1200/800","+4 Armor","+10 Intelligence","+200 Health","+5% Spell Amplification","+35 Movement Speed","15% Cooldown Reduction","?+300 Flamebreak AoE/Knockback","?+8s Firefly Duration")],"beastmaster": [("wild axes","inner beast","primal roar"),("23 + 2.5","18 + 1.6","16 + 1.9","64-68","4.6","310","0.4","1800/800","+20 Movement Speed","+20% XP Gain","?+1 Boar Summoned","+12 Strength","+400 Health","12% Cooldown Reduction","+250 Wild Axes Damage","+120 Damage")],"bloodseeker": [("bloodrage","blood rite","thirst","rupture"),("23 + 2.7","24 + 3.0","18 + 1.7","57-63","3.4","290","0.5","1800/800","+225 Health","+25 Damage","?+75 Blood Rite Damage","+30 Attack Speed","+10 All Stats","?+14% Rupture Damage","30% Lifesteal","?-7s Blood Rite Cooldown")],"bounty hunter": [("shuriken toss","jinada","shadow walk","track"),("17 + 2.1","21 + 3.0","19 + 2.0","45-59","6.0","320","0.6","1800/800","+20% XP Gain","+175 Health","+15 Movement Speed","+40 Attack Speed","+120 Damage","?+75 Shuriken Toss Damage","?-5 Jinada Cooldown","25% Evasion")],"brewmaster": [("thunder clap","drunken haze","drunken brawler","primal split","hurl boulder","dispel magic","cyclone"),("23 + 3.2","22 + 2.0","14 + 1.3","52-59","2.1","300","0.6","1800/800","+3 Mana Regen","+30 Damage","+15% Magic Resistance","?+75 Thunder Clap Damage","+20 Strength","?+2s Thunder Clap Slow","?+2000 Health to Primal Split Units","+140 Attack Speed")],"bristleback": [("viscous nasal goo","quill spray","bristleback","warpath"),("22 + 2.2","17 + 1.8","14 + 2.8","44-54","3.4","290","1.0","1800/800","+2 Mana Regen","+8 Strength","?+4 Max Goo Stacks","+225 Health","10% Spell Lifesteal","+50 Attack Speed","?+25 Quill Stack Damage","+30 Health Regen")],"broodmother": [("spawn spiderlings","spin web","incapacitating bite","insatiable hunger"),("17 + 2.8","18 + 2.2","18 + 2.0","44-50","2.6","295","0.5","1800/800","+25% XP Gain","?+60 Spawn Spiderling Damage","+350 Health","20% Cooldown Reduction","+70 Attack Speed","?+14 Spiders Attack Damage","?+225 Spiders Health","?+8 Max Webs")],"centaur warrunner": [("hoof stomp","double edge","return","stampede"),("23 + 4.3","15 + 1.6","15 + 1.6","55-57","2.1","300","0.5","1800/800","+2 Mana Regen","+35 Damage","+10% Magic Resistance","+10% Evasion","+15 Strength","+10% Spell Amplification","?+1 Hoof Stomp Duration","?Gains Return Aura")],"chaos knight": [("chaos bolt","reality rift","chaos strike","phantasm"),("22 + 3.2","14 + 2.1","16 + 1.2","51-81","4.0","325","0.5","1800/800","+8 Intelligence","+15 Attack Speed","+10 Strength","+20 Movement Speed","+12 All Stats","+120 Gold/Min","?Reality Rift Pierces Spell Immune","20% Spell Reduction")],"chen": [("penitence","test of faith","holy persuasion","hand of god"),("23 + 1.8","15 + 2.1","21 + 2.8","43-53","1.1","300","0.6","1800/800","+125 Cast Range","+30 Movement Speed","?-10 Test of Faith Cooldown","+250 Health","?+1000 Creep Minimum Health","+120 Gold/Min","?+200 Hand of God Heal","?+2 Holy Persuasion Max Count")],"clinkz": [("strafe","searing arrows","skeleton walk","death pact"),("15 + 1.9","22 + 3.3","16 + 1.5","37-43","2.1","300","0.4","1800/800","+10% Magic Resistance","+10 Intelligence","?+30 Searing Arrows Damage","+15 Strength","+10 All Stats","20% Evasion","?+70 Strafe Attack Speed","+125 Attack Range")],"clockwerk": [("battery assault","power cogs","rocket flare","hookshot"),("26 + 3.2","13 + 2.3","17 + 1.3","54-56","1.9","315","0.6","1800/800","+200 Mana","+4 Armor","?+75 Rocket Flare Damage","+50 Damage","+12% Magic Resistance","?+40 Battery Assault Damage","?+10s Battery Assault Duration","+400 Health")],"crystal maiden": [("crystal nova","frostbite","arcane aura","freezing field"),("16 + 2.0","16 + 1.6","16 + 2.9","35-41","1.3","275","0.5","1800/800","+60 Damage","+15% Magic Resistance","+250 Health","+125 Cast Range","?+50 Freezing Field Damage","+120 Gold/Min","?+300 Crystal Nova Damage","?+1.5 Frostbite Duration")],"dark seer": [("vacuum","ion shell","surge","wall of replica"),("22 + 2.6","12 + 1.2","23 + 2.7","54-60","6.7","295","0.6","1800/800","+100 Cast Range","12% Evasion","+14 Health Regen","+120 Damage","?+75 Vacuum AoE","10% Cooldown Reduction","?+80 Ion Shell Damage","+25 Strength")],"dazzle": [("poison touch","shallow grave","shadow wave","weave"),("16 + 2.2","21 + 1.7","27 + 3.4","41-59","2.0","305","0.6","1800/800","+125 Health","+10 Intelligence","+60 Damage","+100 Cast Range","?+25 Poison Touch DPS","+25 Movement Speed","?+60 Shadow Wave Heal","?-6s Poison Touch Cooldown")],"death prophet": [("crypt swarm","silence","spirit siphon","exorcism"),("17 + 2.6","14 + 1.4","23 + 3.0","47-59","3.0","310","0.5","1800/800","+12% Magic Resistance","+5% Magic Resistance","+150 Cast Range","?-1.5s Crypt Swarm Cooldown","+50 Movement Speed","10% Cooldown Reduction","?+8 Exorcism Spirits","+600 Health")],"disruptor": [("thunder strike","glimpse","kinetic field","static storm"),("19 + 2.2","15 + 1.4","22 + 2.5","49-53","1.1","300","0.5","1800/800","+60 Gold/Min","+100 Cast Range","?+40 Thunder Strike Damage","?-3s Kinetic Field Cooldown","+10% Spell Amplification","+400 Health","+30% Magic Resistance","?+4 Thunder Strike Hits")],"doom": [("devour","scorched earth","infernal blade","doom"),("26 + 3.5","11 + 0.9","13 + 2.1","53-69","0.6","290","0.5","1800/800","?+80 Devour Bonus Gold","+275 Health","?+15 Scorched Earth Damage/Heal","+25 Movement Speed","?Devour Can Target Ancients","?+40 Doom DPS","+40 Health Regen","?+2% Infernal Blade Damage")],"dragon knight": [("breathe fire","dragon tail","dragon blood","elder dragon form"),("19 + 3.1","19 + 2.2","15 + 1.7","50-56","3.7","290","0.6","1800/800","+30 Attack Speed","+10 Strength","+40 Damage","+40% XP Gain","+300 Health","+120 Gold/Min","?2x Dragon Blood HP Regen/Armor","+75 Movement Speed")],"drow ranger": [("frost arrows","gust","precision aura","marksmanship"),("17 + 1.9","26 + 1.9","15 + 1.4","40-51","0.7","290","0.7","1800/800","+5 All Stats","+15 Movement Speed","+20 Attack Speed","+175 Health","+14 Strength","?+6% Precision Aura Damage","?+25 Marksmanship Agility","?+400 Gust Distance/Knockback")],"earth spirit": [("boulder smash","rolling boulder","geomagnetic grip","stone remnant","enchant remnant","magnetize"),("21 + 3.2","17 + 1.5","18 + 2.1","46-56","3.4","290","0.6","1800/800","+4 Armor","+10 Intelligence","+90 Gold/Min","+15% Magic Resistance","+300 Health","+15% Spell Amplification","?+300 Rolling Boulder Damage","?Geomagnetic Grip Targets Allies")],"earthshaker": [("fissure","enchant totem","aftershock","echo slam"),("22 + 3.2","12 + 1.4","16 + 1.8","46-56","2.7","310","0.9","1800/800","+250 Mana","+10 Strength","+50 Damage","+20 Movement Speed","?+350 Fissure Range","?+40 Echo Damage","?-2s Enchant Totem Cooldown","+600 Health")],"elder titan": [("echo stomp","astral spirit","natural order","earth splitter"),("24 + 2.6","14 + 1.8","23 + 1.6","47-57","3.0","315","0.4","1800/800","+10 Strength","+200 Mana","?+30 Echo Stomp Damage","+275 Health","+50 Attack Speed","+12% Magic Resistance","?+100 Astral Spirit Hero Attack","+15 Armor")],"ember spirit": [("searing chains","slight of fist","flame guard","fire remnant"),("19 + 2.1","22 + 1.8","20 + 1.8","52-56","1.1","310","0.5","1800/800","+30 Damage","+8% Spell Amplification","+6 All Stats","+20 Movement Speed","+10 Armor","?+500 Flame Guard Absorption","?+2s Searing Chains","20% Cooldown Reduction")],"enchantress": [("untouchable","enchant","natures attendants","impetus"),("16 + 1.3","19 + 1.8","21 + 3.1","52-62","0.7","340","0.4","1800/800","+25 Movement Speed","+6 All Stats","+50 Damage","?+8 Nature's Attendants Wisps","?+60 Untouchable Slow","+15% Magic Resistance","?Enchant Affects Ancients","?+6% Impetus Damage")],"enigma": [("malefice","demonic conversion","midnight pulse","black hole"),("17 + 2.4","14 + 1.0","20 + 3.4","42-48","4.0","300","0.5","1800/800","+12% Magic Resistance","+20 Movement Speed","+120 Gold/Min","15% Cooldown Reduction","?+1 Malefice Instance","+300 Health","?+8 Demonic Conversion Eidolons","+12 Armor")],"faceless void": [("time walk","time dilation","time lock","chronosphere"),("23 + 2.1","23 + 2.8","15 + 1.5","56-62","3.3","300","1.0","1800/800","+8 Strength","+15 Attack Speed","+25 Damage","+7 Armor","+120 Gold/Min","+300 Health","?+600 Timewalk Cast Range","20% Evasion")],"gyrocopter": [("rocket barrage","homing missile","flak cannon","call down"),("18 + 2.1","24 + 2.8","19 + 2.1","37-47","4.4","325","0.6","1800/800","+225 Health","+6% Spell Amplification","+30 Damage","+15% Magic Resistance","20% Cooldown Reduction","+35 Movement Speed","?+4 Flak Cannon Attacks","?3 Homing Missile Charges")],"huskar": [("inner vitality","burning spear","berserkers blood","life break"),("21 + 2.7","15 + 1.4","18 + 1.5","42-51","1.1","300","0.5","1800/800","?+5 Burning Spears DPS","+175 Health","15% Lifesteal","+30 Damage","+40 Attack Speed","+15 Strength","?+500 Life Break Cast Range","+100 Attack Range")],"invoker": [("cold snap","ghost walk","ice wall","deafening blast","alacrity","tornado","emp","chaos meteor","forge spirit","sun strike"),("16 + 2.2","14 + 1.9","16 + 4.0","35-41","1.0","280","0.5","1800/800","+125 Health","+15 Damage","+30% XP Gain","?+1 Forged Spirit Summmoned","+35 Attack Speed","+7 All Stats","?-18s Tornado Cooldown","?AoE Deafening Blast")],"io": [("tether","spirits","overcharge","relocate"),("17 + 2.2","14 + 1.6","23 + 1.7","43-52","0.0","295","0.7","1800/800","+6 Armor","+10% Magic Resistance","+10 Strength","+10 Mana Regen","+120 Gold/Min","+20 Health Regen","+150 Spirits Damage","?Tether Stuns")],"jakiro": [("dual breath","ice path","liquid fire","macropyre"),("25 + 2.6","10 + 1.2","28 + 2.8","53-61","2.4","290","0.5","1800/800","+8% Spell Amplification","+25% XP Gain","?+35 Dual Breath Damage","+125 Cast Range","+150 Gold/Min","+400 Attack Range","?+1.25s Ice Path Duration","?Macropyre Pure and Pierces Spell Immunity")],"juggernaut": [("blade fury","healing ward","blade dance","omnislash"),("20 + 2.2","26 + 2.4","14 + 1.4","48-52","3.7","300","0.6","1800/800","+20 Damage","+175 Health","+7 Armor","+20 Attack Speed","+8 All Stats","+20 Movement Speed","?+175 Blade Fury DPS","+20 Agility")],"keeper of the light": [("illuminate","mana leak","chakra magic","recall","blinding light","spirit form"),("14 + 2.1","15 + 1.6","25 + 2.8","43-50","1.1","335","0.5","1800/800","+20 Movement Speed","+7 Strength","?+300 Chakra Magic Mana","+20% XP Gain","+7 Armor","+10% Magic Resistance","?+200 Illuminate Damage/Heal","+400 Cast Range")],"kunkka": [("torrent","tidebringer","x marks the spot","ghostship"),("24 + 3.3","14 + 1.3","18 + 1.5","50-60","4.0","300","0.6","1800/800","?+40 Torrent Damage","+30 Damage","+30 Movement Speed","+15 Health Regen","+120 Gold/Min","+300 Health","?+200 Torrent AoE","+35% Magic Resistance")],"legion commander": [("overwhelming odds","press the attack","moment of courage","duel"),("26 + 2.9","18 + 1.7","20 + 2.2","61-65","2.6","320","0.5","1800/800","+20% XP Gain","+7 Strength","+20 Movement Speed","+30 Damage","?+10% Moment Proc Chance","+7 Armor","?-8 Press The Attack Cooldown","?+40 Duel Damage Bonus")],"leshrac": [("split earth","diabolic edict","lightning storm","pulse nova"),("16 + 1.8","23 + 1.7","26 + 3.0","41-45","3.3","325","0.5","1800/800","+25 Movement Speed","+175 Health","+15% Magic Resistance","+400 Mana","+15 Strength","+5% Spell Amplification","?+3s Lighting Storm Slow Duration","?+50 Diabolic Edict Explosions")],"lich": [("frost blast","ice armor","sacrifice","chain frost"),("18 + 1.9","15 + 2.0","18 + 3.3","42-51","1.1","315","0.5","1800/800","+25 Movement Speed","+175 Health","?-4 Frost Blast Cooldown","+125 Cast Range","+120 Gold/Min","+150 Damage","?Attacks Apply 30% MS and AS Slow","?+35 Frost Armor Structure Armor")],"lifestealer": [("rage","feast","open wounds","assimilate","infest"),("25 + 3.1","18 + 1.9","15 + 1.8","52-62","1.6","315","1.0","1800/800","+15 Attack Speed","+5 All Stats","+25 Damage","+250 Health","+25 Movement Speed","15% Evasion","?+1s Rage Duration","+15 Armor")],"lina": [("dragon slave","light strike array","fiery soul","laguna blade"),("18 + 1.8","16 + 1.5","27 + 3.2","40-58","1.3","295","0.5","1800/800","+125 Cast Range","?+80 Light Strike Array Damage","+40 Movement Speed","+50 Damage","+150 Attack Range","+6% Spell Amplification","?+35/3% Fiery Soul Per Stack","?-4s Dragon Slave Cooldown")],"lion": [("earth spike","hex","mana drain","finger of death"),("16 + 2.0","15 + 1.5","20 + 3.0","47-53","1.1","290","0.5","1800/800","+60 Damage","+75 Cast Range","+90 Gold/Min","?+80 Earth Spike Damage","+8% Spell Amplification","+20% Magic Resistance","?+3 Mana Drain Multi Target","+20 All Stats")],"lone druid": [("summon spirit bear","rabid","savage roar","battle cry","true form","druid form"),("17 + 2.4","24 + 2.7","13 + 1.4","42-46","3.4","325","0.4","1800/800","+175 Attack Range","+250 Health","?+50 Spirit Bear Damage","+50 Damage","?+50% Spirit Bear Magic Resistance","?+12 Spirit Bear Armor","?-10s Savage Roar Cooldown","?+1.5s Entangle Duration")],"luna": [("lucent beam","moon glaive","lunar blessing","eclipse"),("15 + 2.5","18 + 3.3","16 + 1.9","38-44","2.6","335","0.6","1800/800","+20 Movement Speed","+15 Damage","?+40 Lucent Beam Damage","+150 Health","+15% Magic Resistance","+25 Attack Speed","?-4s Lucent Beam Cooldown","+15 All Stats")],"lycan": [("summon wolves","howl","feral impulse","shapeshift"),("25 + 3.3","16 + 1.0","17 + 1.5","61-66","3.3","305","0.5","1800/800","+200 Health","+15 Damage","+12 Strength","?+12 Feral HP Regen","15% Cooldown Reduction","15% Evasion","?+2 Wolves Summoned","?+15s Shapeshift Duration")],"magnus": [("shockwave","empower","skewer","reverse polarity"),("21 + 3.2","15 + 2.5","19 + 1.6","53-65","4.1","310","0.8","1800/800","+15% Spell Amplification","+25 Attack Speed","+12 Strength","+90 Gold/Min","+40 Movement Speed","+10% Empower Damage/Cleave","+15 Armor","?+500 Skewer Range")],"medusa": [("split shot","mystic snake","mana shield","stone gaze"),("14 + 2.0","20 + 2.5","19 + 2.1","44-50","1.9","290","0.5","1800/800","+15 Damage","+12 Intelligence","+15% Evasion","+20 Attack Speed","+600 Mana","?+1 Split Shot target","?+2s Stone Gaze Stun","25% Lifesteal")],"meepo": [("earthbind","poof","geostrike","divided we stand"),("23 + 1.6","23 + 2.2","20 + 1.6","43-49","2.3","315","0.6","1800/800","+15 Damage","+4 Armor","+25 Movement Speed","+15% Lifesteal","+25 Attack Speed","10% Evasion","?-3s Poof Cooldown","+400 Health")],"mirana": [("starstorm","sacred arrow","leap","moonlight shadow"),("17 + 2.2","20 + 3.6","17 + 1.6","41-52","1.9","300","0.4","1800/800","+150 Health","+8 Agility","+30 Attack Speed","+5% Spell Amplification","?-4s Sacred Arrow Cooldown","+50 Damage","?+2 Multishot Sacred Arrows","?+100 Leap Attack Speed")],"monkey king":[("boundless strike","tree dance","primal spring","jingu mastery","mischief","wukongs command"),("18 + 2.8","22 + 3.2","20 + 1.8","52-58","0.1","305","0.6","1800/800","12% Evasion","+20 Attack Speed","?+75 Jingu Mastery Damage","+275 Health","+20% Magic Resistance","+40 Damage","?+100% Boundless Strike Crit","+25 Strength")],"morphling": [("waveform","adaptive strike","morph","hybrid","replicate"),("19 + 2.3","24 + 3.7","17 + 1.1","33-42","1.4","285","0.6","1800/800","+200 Mana","+8 Agility","+12% Cooldown Reduction","+25 Attack Speed","+40 Damage","+25 Movement Speed","?+50% Replicate Damage","?+400 Waveform Range")],"naga siren": [("mirror image","ensnare","rip tide","song of the siren"),("21 + 2.8","21 + 2.8","21 + 2.0","44-46","6.0","320","0.5","1800/800","+125 Health","+250 Mana","?-3s Ensnare Cooldown","+30 Attack Speed","+20 Strength","+15 Agility","?+1 Mirror Image Illusion","+40 Movement Speed")],"natures prophet": [("sprout","teleportation","natures call","wrath of nature"),("19 + 2.1","18 + 1.9","25 + 2.9","55-69","3.6","295","0.6","1800/800","+250 Health","+30 Damage","?+4 Treants Summoned","+20 Intelligence","+10 Armor","+35 Attack Speed","?2x Treant HP/Damage","?Removed Teleportation Cooldown")],"necrophos": [("death pulse","ghost shroud","heartstopper aura","reapers scythe"),("16 + 2.3","15 + 1.2","22 + 2.5","44-48","3.1","285","0.5","1800/800","+8 Strength","+40 Damage","+20 Movement Speed","+6 All Stats","+10% Magic Resistance","+5% Spell Amplification","?-1s Death Pulse Cooldown","+400 Health")],"night stalker": [("void","crippling fear","hunter in the night","darkness"),("23 + 3.1","18 + 2.3","13 + 1.6","61-65","5.6","295","0.5","1200/1800","?+100 Cast Range","+7 Strength","+25 Attack Speed","+300 Mana","+50 Damage","+30 Movement Speed","?-8s Crippling Fear Cooldown","+12 Armor")],"nyx assassin": [("impale","mana burn","spiked carapace","burrow","vendetta"),("18 + 2.3","19 + 2.2","18 + 2.1","49-53","3.7","300","0.5","1800/800","+175 Health","+5% Spell Amplification","?+50 Impale Damage","+12% Magic Resistance","+40 Agility","+120 Gold/Min","?200% Spiked Carapace Damage","+40 Movement Speed")],"ogre magi": [("fireblast","ignite","bloodlust","multicast"),("23 + 3.5","14 + 1.5","17 + 2.0","58-64","8.0","285","0.6","1800/800","+100 Cast Range","+60 Gold/Min","+12% Magic Resistance","+50 Damage","+30 Movement Speed","+350 Health","?+40 Bloodlust AS","+15% Spell Amplification")],"omniknight": [("purification","repel","degen aura","guardian angel"),("22 + 3.1","15 + 1.8","17 + 1.8","53-63","5.1","305","0.6","1800/800","+20% XP Gain","+60 Gold/Min","+8 Strength","+75 Cast Range","+6 Mana Regen","+100 Damage","?-16% Degen Aura","?+200 Purificaion Damage/Heal")],"oracle": [("fortunes end","fates edict","purifying flames","false promise"),("18 + 2.2","15 + 1.7","23 + 2.9","39-45","2.1","305","0.4","1800/800","+20% XP Gain","?+0.75s Fortune's End Max Duration","+60 Gold/Min","+200 Health","+20 Intelligence","+25 Movement Speed","?+2 False Promise Duration","+250 Cast Range")],"outworld devourer": [("arcane orb","astral imprisonment","essence aura","sanitys eclipse"),("19 + 2.6","24 + 2.0","26 + 2.7","40-55","3.4","315","0.5","1800/800","+10 Movement Speed","+250 Mana","+20 Attack Speed","+5 Armor","+275 Health","+15 Intelligence","+8% Spell Amplification","?+60s Arcane Orb Steal")],"phantom assassin": [("stifling dagger","phantom strike","blur","coup de grace"),("20 + 2.2","23 + 3.2","15 + 1.4","46-48","4.3","310","0.6","1800/800","+15 Damage","+150 Health","+20 Movement Speed","+10% Lifesteal","+10 All Stats","+35 Attack Speed","?Double Strike Stifling Dagger","+25 Agility")],"phantom lancer": [("spirit lance","doppelganger","phantom rush","juxtapose"),("21 + 2.0","29 + 2.8","21 + 2.0","51-73","4.1","290","0.6","1800/800","+20 Attack Speed","?+75 Spirit Lance Damage","+15% Cooldown Reduction","+8 All Stats","+15% Evasion","+15% Magic Resistance","?+600 Phantom Rush Range","+20 Strength")],"phoenix": [("icarus dive","fire spirits","sun ray","supernova"),("19 + 3.2","12 + 1.3","18 + 1.8","45-55","-0.3","285","1.0","1800/800","+200 Health","+20% XP Gain","+150 Gold/Min","?+65 Fire Spirits DPS","+8% Spell Amplification","+10 Armor","?+1s Supernova Stun Duration","?+2 Supernova Hit Count")],"puck": [("illusory orb","waning rift","phase shift","dream coil"),("15 + 2.0","22 + 1.7","25 + 2.4","53-64","1.1","295","0.4","1800/800","+175 Health","+8 Intelligence","+20% Magic Resistance","+50 Damage","?-3s Waning Rift Cooldown","+10% Spell Amplification","?+75% Illusory Orb Distance/Speed","+420 Gold/Min")],"pudge": [("meat hook","rot","flesh heap","dismember"),("25 + 3.5","14 + 1.5","14 + 1.5","52-58","1.0","280","0.7","1800/800","+2 Mana Regen","+8 Strength","+15 Movement Speed","+5 Armor","?+1s Dismember Duration","+150 Gold/Min","?+120 Rot Damage","?+1.75 Flesh Heap Stack Str")],"pugna": [("nether blast","decrepify","nether ward","life drain"),("17 + 1.5","16 + 1.0","26 + 4.5","45-53","1.3","335","0.5","1800/800","+225 Health","+3 Mana Regen","?-1s Netherblast Cooldown","?+1s Decrepify Duration","+150 Cast Range","?+0.75 Nether Ward Damage Per Mana","?+200 Nether Blast Damage","?+50% Life Drain Heal")],"queen of pain": [("shadow strike","blink","scream of pain","sonic wave"),("16 + 2.0","18 + 2.0","24 + 2.5","45-53","1.6","295","0.5","1800/800","+10 Strength","+25 Damage","+90 Gold/Min","12% Cooldown Reduction","+300 Health","+100 Attack Range","60% Spell Lifesteal","?550 AoE Shadow Strike")],"razor": [("plasma field","static link","unstable current","eye of the storm"),("21 + 2.6","22 + 1.8","21 + 1.8","45-47","2.1","295","0.4","1800/800","+15 Agility","+25 Movement Speed","+175 Cast Range","?+130 Unstable Current Damage","+40 Attack Speed","+400 Health","?+14 Static Link Damage Steal","+175 Attack Range")],"riki": [("smoke screen","blink strike","cloak and dagger","tricks of the trade"),("17 + 1.9","34 + 2.2","14 + 1.3","38-42","4.9","285","0.6","1800/800","+15 Movement Speed","+150 Health","+30% XP Gain","+10 Agility","+8 All Stats","+250 Cast Range","?-4s Smokescreen Cooldown","?+0.4s Backstab Multiplier")],"rubick": [("telekinesis","fade bolt","null field","spell steal"),("19 + 1.8","14 + 1.6","27 + 2.4","44-54","1.0","290","0.7","1800/800","+60 Damage","+60 Gold/Min","+15 Intelligence","+150 Health","+8% Spell Amplification","+75 Cast Range","?+400 Telekinesis Land Distance","20% Cooldown Reduction")],"sand king": [("burrowstrike","sand storm","caustic finale","epicenter"),("22 + 2.9","19 + 2.1","16 + 1.8","47-63","2.7","295","0.5","1800/800","+5 Armor","+10% Magic Resistance","?-50 Epicenter Attack Slow","?+50 Sand Storm DPS","+120 Gold/Min","+350 Health","?+4 Epicenter Pulses","+50 Health Regen")],"shadow demon": [("disruption","soul catcher","shadow poison","demonic purge"),("21 + 2.2","18 + 2.2","23 + 2.7","50-54","2.6","295","0.6","1800/800","+20 Movement Speed","+10 Strength","+8% Spell Amplification","+75 Cast Range","?-1.5s Shadow Poison Cooldown","+15% Magic Resistance","?-6s Soul Catcher Cooldown","?+400 Demonic Purge Damage")],"shadow fiend": [("shadowraze","necromastery","presence of the dark lord","requiem of souls"),("15 + 2.3","20 + 2.9","18 + 2.0","35-41","0.9","315","1.0","1800/800","+20 Attack Speed","+15 Movement Speed","+175 Health","+6% Spell Amplification","?+2 Damage Per Soul","15% Lifesteal","?+150 Shadow Raze Damage","+150 Attack Range")],"shadow shaman": [("ether shock","hex","shackles","mass serpent ward"),("21 + 2.1","16 + 1.6","21 + 3.0","71-78","2.3","285","0.4","1800/800","+25 Movement Speed","+200 Health","+35% XP Gain","+100 Cast Range","?+3s Shackles Duration","?+4 Wards Summoned","?+350 Ether Shock Damage","?+1 Serpent Wards Attacks HP")],"silencer": [("arcane curse","glaives of wisdom","last word","global silence"),("17 + 2.5","22 + 3.0","27 + 2.5","43-57","2.1","295","0.6","1800/800","+7 Intelligence","+4 Armor","+60 Gold/Min","+200 Health","+12% Magic Resistance","+30 Attack Speed","?+25% Curse Slow","+200 Attack Range")],"skywrath mage": [("arcane bolt","concussive shot","ancient seal","mystic flare"),("19 + 1.8","13 + 0.8","27 + 3.6","39-49","-0.1","330","0.5","1800/800","+7 Intelligence","+150 Health","+90 Gold/Min","10% Spell Lifesteal","+20% Magic Resistance","+40 Movement Speed","?-4s Ancient Seal Cooldown","+14 Mana Regen")],"slardar": [("guardian sprint","slithereen crush","bash of the deep","corrosive haze"),("21 + 3.1","17 + 2.4","15 + 1.5","51-59","5.4","290","0.5","1800/800","+175 Mana","+6 Health Regen","+25 Attack Speed","+225 Damage","+7 Armor","+35 Damage","?+10% Bash Chance","+20 Strength")],"slark": [("dark pact","pounce","essence shift","shadow dance"),("20 + 1.9","21 + 1.5","16 + 1.7","54-62","2.0","300","0.5","1800/1800","+15 Damage","10% Lifesteal","+15 Strength","+15 Agility","+25 Attack Speed","10% Cooldown Reduction","?+3s Pounce Leash","+12 All Stats")],"sniper": [("shrapnel","headshot","take aim","assassinate"),("16 + 2.0","21 + 2.7","15 + 2.6","36-42","2.0","290","0.7","1800/800","+15 Attack Speed","+5 Mana Regen","+200 health","?+20 Shrapnel DPS","25% Cooldown Reduction","+8 Armor","?+4 Shrapnel Charges","+100 Attack Range")],"spectre": [("spectral dagger","desolate","dispersion","haunt"),("20 + 2.3","23 + 1.8","16 + 1.9","46-50","3.3","290","0.4","1800/800","+5 Armor","+20 Damage","+25 Movement Speed","+8 All Stats","+20 Strength","+30 Attack Speed","?-10s Spectral Dagger Cooldown","+400 Health")],"spirit breaker": [("charge of darkness","empowering haste","greater bash","nether strike"),("29 + 2.7","17 + 1.7","14 + 1.8","60-70","5.4","290","0.4","1800/800","+20 Movement Speed","+5 All Stats","+5 Armor","+20 Damage","?+30% Greater Bash Damage","+120 Gold/Min","?+500 Charge Speed","?+17% Greater Bash Chance")],"storm spirit": [("static remnant","electric vortex","overload","ball lightning"),("19 + 1.8","22 + 1.8","24 + 3.0","46-56","5.1","285","0.8","1800/800","+3 Mana Regen","+20 Damage","+10 Intelligence","+200 Health","+8 Armor","+40 Attack Speed","?+0.75 Electric Vortex","+10% Spell Amplification")],"sven": [("storm hammer","great cleave","warcry","gods strength"),("23 + 3.0","21 + 2.0","16 + 1.3","64-66","5.0","290","0.6","1800/800","+225 Mana","+6 Strength","+8 All Stats","+20 Movement Speed","+20% Evasion","+30 Attack Speed","?-8s Storm Hammer Cooldown","+65 Damage")],"techies": [("proximity mines","statis trap","blast off","minefield sign","remote mines"),("17 + 2.3","14 + 1.3","22 + 2.9","29-31","7.0","270","0.5","1800/800","+2 Mana Regen","+20 Movement Speed","+200 Cast Range","+30% XP Gain","?+400 Blast Off Damage","+120 Gold/Min","+250 Damage","20% Cooldown Reduction")],"templar assassin": [("refraction","meld","psi blades","psionic trap"),("18 + 2.4","23 + 2.3","20 + 2.0","53-59","4.3","305","0.7","1800/800","+20 Movement Speed","+25 Attack Speed","+12% Evasion","+6 All Stats","+40 Damage","+275 Health","?+3 Refraction Instances","?-8 Meld Armor Reduction")],"terrorblade": [("reflection","conjure image","metamorphosis","sunder"),("15 + 1.7","22 + 3.2","19 + 1.8","48-54","10.1","315","0.5","1800/800","+15 Attack Speed","+6 Health Regen","+200 Health","+25 Damage","+25 Movement Speed","+15 Agility","?-30 Sunder Cooldown","+15 All Stats")],"tidehunter": [("gush","kraken shell","anchor smash","ravage"),("22 + 3.3","15 + 1.5","16 + 1.7","47-53","3.1","305","0.4","1800/800","+150 Health","+50 Damage","+35% XP Gain","+7 Armor","+15 Strength","+6 Mana Regen","?-6 Gush Armor","20% Cooldown Reduction")],"timbersaw": [("whirling death","timber chain","reactive armor","chakram"),("21 + 2.1","16 + 1.3","21 + 2.4","47-51","0.3","290","0.6","1800/800","+20% XP Gain","+150 Health","+20 Intelligence","+14 Health Regen","+150 Cast Range","+5% Spell Amplification","+20 Strength","?+6% Whirling Death Attribute Reduction")],"tinker": [("laser","heatseeking missile","march of the machines","rearm"),("17 + 2.3","13 + 1.2","30 + 2.2","52-58","3.9","305","0.6","1800/800","+6 Armor","+8 Intelligence","+4% Spell Amplification","+225 Health","+15% Magic Resistance","+75 Cast Range","?+100 Laser Damage","20% Spell Lifesteal")],"tiny": [("avalanche","toss","craggy exterior","grow"),("26 + 3.3","9 + 0.9","17 + 1.6","70-76","0.3","285","0.5","1800/800","+14 Intelligence","+8 Strength","+40 Movement Speed","+60 Damage","+14 Mana Regen","+25 Attack Speed","?+200 Avalanche Damage","20% Cooldown Reduction")],"treant": [("natures guise","leech seed","living armor","eyes in the forest","overgrowth"),("25 + 3.6","15 + 2.0","17 + 1.8","87-95","1.1","270","0.5","1800/800","+2 Mana Regen","+30 Attack Speed","+25 Movement Speed","+90 Gold/Min","+90 Damage","15% Cooldown Reduction","?+5 Living Armor Block Instances","?+40 Leech Speed Damage/Heal")],"troll warlord": [("berserkers rage","whirling axes","fervor","battle trance"),("20 + 2.5","21 + 2.5","13 + 1.0","38-56","2.0","300","0.5","1800/800","+10 Agiliy","+7 Strength","+6 Armor","+15 Movement Speed","+40 Damage","+350 Health","+350 Health","?-7s Whirling Axes Cooldown")],"tusk": [("ice shards","snowball","frozen sigil","walrus kick","walrus punch"),("23 + 2.6","23 + 2.1","18 + 1.7","50-54","3.3","300","0.7","1800/800","+35 Damage","+40% XP Gain","+90 Gold/Min","?+150 Snowball Damage","+12% Magic Resistance","+6 Armor","?+150% Walrus Punch Crit","+700 Health")],"underlord":[("firestorm","pit of malice","atrophy aura","dark rift"),("25 + 2.9","12 + 1.3","17 + 2.6","62-68","307","290","0.6","1800/800","+2 Mana Regen","+5 Armor","+12% Spell Amplification","+40 Movement Speed","+125 Cast Range","+60 Attack Speed","?+0.4 Pit of Malice Root","+50 Health Regen")],"undying": [("decay","soul rip","tombstone","flesh golem"),("22 + 2.4","10 + 0.8","27 + 2.8","57-65","4.4","310","0.6","1800/800","+90 Gold/Min","+15 Health Regen","+300 Health","+35% XP Gain","+30 Movement Speed","+50 Tombstone Zombie Damage","?-2s Decay Cooldown","+15 Armor")],"ursa": [("earthshock","overpower","fury swipes","enrage"),("23 + 3.0","18 + 2.1","16 + 1.5","42-46","5.6","310","0.5","1800/800","+10% Magic Resistance","+25 Damage","+20 Attack Speed","+5 Armor","+250 Health","+15 Movement Speed","?+10 Fury Swipes Damage","+14 All Stats")],"vengeful spirit": [("magic missile","wave of terror","vengeance aura","nether swap"),("18 + 2.9","27 + 3.3","13 + 1.5","39-53","3.9","300","0.6","1800/800","+25 Attack Speed","+8% Magic Resistance","?+100 Magic Missle Damage","+8 All Stats","+35 Movement Speed","+65 Damage","?Magic Missile Pierces Spell Immunity","?+20% Vengeance Aura Damage")],"venomancer": [("venomous gale","poison sting","plague ward","poison nova"),("18 + 1.9","22 + 2.8","17 + 1.8","41-43","3.1","285","0.4","1800/800","+30 Movement Speed","+30% XP Gain","+150 Cast Range","+200 Health","+15% Magic Resistance","+75 Damage","?3x Plague Ward HP/Damage","?+14% Poison Sting Slow")],"viper": [("poison attack","nethertoxin","corrosive skin","viper strike"),("20 + 2.4","21 + 2.9","15 + 1.8","44-46","2.0","285","0.4","1800/800","+175 Health","+15 Damage","+16 Agility","+15 Strength","+75 Attack Range","?Poison Attack Affects Buildings","?+80 Viper Strike DPS","+20 Armor")],"visage": [("grave chill","soul assumption","gravekeepers cloak", "summon familiars"),("22 + 2.7","11 + 1.3","24 + 2.5","46-55","-0.4","285","0.5","1800/800","+30% XP Gain","+90 Gold/Min","+100 Cast Range","+50 Damage","?Soul Assumption Double Strike","+300 Health","?+120 Familiars Movement Speed","+20% Spell Amplification")],"warlock": [("fatal bonds","shadow word","upheaval","chaotic offering"),("22 + 2.8","10 + 1.0","24 + 2.7","46-56","2.4","295","0.4","1800/800","+6 All Stats","+20% XP Gain","?-4s Shadow Word Cooldown","+150 Cast Range","?Summons a Golem on death","+350 Health","?+15 Chaotic Offering Golems Armor","?Magic Immunity fr Chaotic Offering Golems")],"weaver": [("the swarm","shukuchi","geminate attack","time lapse"),("15 + 1.8","14 + 2.8","15 + 1.8","50-60","1.0","285","0.5","1800/800","?+30 Shukuchi Damage","+6 Strength","+7 All Stats","+25 Damage","+15 Agility","+200 Health","?+200 Shukuchi Movement Speed","+35% Magic Resistance")],"windranger": [("shackleshot","powershot","windrun","focus fire"),("15 + 2.8","17 + 1.4","22 + 2.6","44-56","1.4","295","0.6","1800/800","+30% Windrun Slow","+4 Mana Regen","+20 Intelligence","+40 Movement Speed","?+120 Powershot Damage","?Windrun Grants Invisibility","30% Cooldown Reduction","+150 Attack Range")],"winter wyvern": [("arctic burn","splinter blast","cold embrace","winters curse"),("24 + 2.4","16 + 1.9","25 + 3.1","38-45","1.3","285","0.4","1800/800","+7 Strength","+8 Intelligence","+50 Damage","+20 Movement Speed","?+1s Cold Embrace Duration","+120 Gold/Min","?-3s Splinter Blast Cooldown","?+15% Arctic Burn Slow")],"witch doctor": [("paralyzing cask","voodoo restoration","maledict","death ward"),("16 + 2.1","13 + 1.4","24 + 2.9","51-61","0.9","305","0.4","1800/800","+25% XP Gain","+200 Health","?+2 Cask Bounces","+90 Damage","+15% Magic Resistance","+8 Armor","?+20 Voodoo Restoration Heal","?+175 Death Ward Attack Range")],"wraith king": [("wraithfire blast","vampiric aura","mortal strike","reincarnation"),("22 + 3.2","18 + 1.7","18 + 1.6","61-63","2.6","300","0.4","1800/800","+10 Intelligence","+15 Damage","?+50 Wraithfire Blast DPS","+15 Movement Speed","?+10% Vampiric Aura Lifesteal","+40 Attack Speed","?Reincarnation Casts Wraithfire Blast","?No Reincarnation Mana Cost")],"zeus": [("arc lightning","lightning bolt","static field","nimbus","thundergods wrath"),("19 + 2.6","11 + 1.2","22 + 2.7","43-51","1.6","300","0.6","1800/800","+25 Movement Speed","+2 Mana Regen","+15% Magic Resistance","+7 Armor","?+0.5 Lighting Bolt Ministun","?+75 Arc Lightning Damage","?+2% Static Field Damage","+200 Cast Range")]}

spellCost = {"mist coil" : ("50/60/70/80","4.5"),"aphotic shield" : ("115","12/10/8/6"),"curse of avernus" : (-1,-1),"borrowed time" : ("0","60/50/40"),"acid spray" : ("130/140/150/160","22"),"unstable concoction" : ("120","22/20/18/16"),"greevils greed" : (-1,-1),"chemical rage" : ("50/100/150","55"),"cold feet" : ("125","10/9/8/7"),"ice vortex" : ("80/90/100/110","4"),"chilling touch" : ("110/120/130/140","50/42/34/26"),"ice blast" : ("100/125/150","40"),"mana break" : (-1,-1),"blink" : ("60","12/9/7/5"),"spell shield" : (-1,-1),"mana void" : ("125/200/275","70"),"flux" : ("75","18"),"magnetic field" : ("80/90/100/110","35/30/25/20"),"spark wraith" : ("80","4"),"tempest double" : ("0","60/50/40"),"berserkers call" : ("80/90/100/110","16/14/12/10"),"battle hunger" : ("75","20/15/10/5"),"counter helix" : (-1,"0.45/0.4/0.35/0.3"),"culling blade" : ("60/120/180","75/65/55"),"enfeeble" : ("95","8"),"brain sap" : ("70/100/130/160","14/13/12/11"),"nightmare" : ("165","22/19/16/13"),"fiends grip" : ("200/300/400","100"),"sticky napalm" : ("20","3"),"flamebreak" : ("110/120/130/140","17"),"firefly" : ("100","40"),"flaming lasso" : ("225","100/80/60"),"wild axes" : ("105/110/115/120","13"),"inner beast" : ("25","42/38/34/30"),"primal roar" : ("150/175/200","80/75/70"),"bloodrage" : ("0","12/10/8/6"),"blood rite" : ("100","18/16/14/12"),"thirst" : (-1,-1),"rupture" : ("150/200/250","60"),"shuriken toss" : ("120/130/140/150","10"),"jinada" : (-1,"12/10/8/6"),"shadow walk" : ("65","15"),"track" : ("65","4"),"thunder clap" : ("90/105/130/150","13"),"drunken haze" : ("25","8/7/6/5"),"drunken brawler" : (-1,-1),"primal split" : ("125/150/175","140/120/100"),"hurl boulder" : ("0","50/100/150"),"dispel magic" : ("75","4"),"cyclone" : ("150","8"),"viscous nasal goo" : ("25","1.5"),"quill spray" : ("35","3"),"bristleback" : (-1,-1),"warpath" : (-1,-1),"spawn spiderlings" : ("120","10"),"spin web" : (-1,"50"),"incapacitating bite" : (-1,-1),"insatiable hunger" : ("100","45"),"hoof stomp" : ("130","13"),"double edge" : ("0","5"),"return" : (-1,-1),"stampede" : ("100","90/75/60"),"chaos bolt" : ("140","10"),"reality rift" : ("50","18/14/10/6"),"chaos strike" : (-1,-1),"phantasm" : ("125/200/275","130"),"penitence" : ("70","14/13/12/11"),"test of faith" : ("90/100/110/120","16"),"holy persuasion" : ("100","10"),"hand of god" : ("200/300/400","160/140/120"),"strafe" : ("90","40/35/30/25"),"searing arrows" : ("10",-1),"skeleton walk" : ("75","20/19/18/17"),"death pact" : ("100","85"),"battery assault" : ("100","32/28/24/20"),"power cogs" : ("50/60/70/80","15"),"rocket flare" : ("50","20/18/16/14"),"hookshot" : ("150","70/55/40"),"crystal nova" : ("100/120/140/160","12/11/10/9"),"frostbite" : ("140/145/150/155","9/8/7/6"),"arcane aura" : (-1,-1),"freezing field" : ("200/400/600","110/100/90"),"vacuum" : ("100/130/160/190","32"),"ion shell" : ("100/110/120/130","9"),"surge" : ("50","13/12/11/10"),"wall of replica" : ("125/250/375","100"),"poison touch" : ("70","15/13/11/7"),"shallow grave" : ("150","60/45/30/15"),"shadow wave" : ("90/100/110/120","12/10/8/6"),"weave" : ("100","40"),"crypt swarm" : ("105/120/140/165","8/7/6/5"),"silence" : ("80","15/14/13/12"),"spirit siphon" : ("70/65/60/55",-1),"exorcism" : ("200/300/400","145"),"thunder strike" : ("130","12/11/10/9"),"glimpse" : ("100","60/46/32/18"),"kinetic field" : ("70","13/12/11/10"),"static storm" : ("125/175/225","90/80/70"),"devour" : ("40/50/60/70","70/60/50/40"),"scorched earth" : ("60/65/70/75","55"),"infernal blade" : ("40","16/12/8/4"),"doom" : ("150/200/250","145"),"breathe fire" : ("100/110/120/130","14/13/12/11"),"dragon tail" : ("100","12/11/10/9"),"dragon blood" : (-1,-1),"elder dragon form" : ("50","115"),"frost arrows" : ("12",-1),"gust" : ("90","16/15/14/13"),"precision aura" : (-1,"100"),"marksmanship" : (-1,-1),"boulder smash" : ("100","22/18/14/10"),"rolling boulder" : ("50","16/12/8/4"),"geomagnetic grip" : ("100","13"),"stone remnant" : (-1,"30"),"enchant remnant" : ("150","45"),"magnetize" : ("100","100/90/80"),"fissure" : ("125/140/155/170","15"),"enchant totem" : ("20/30/40/50","5"),"aftershock" : (-1,-1),"echo slam" : ("145/205/265","150/130/110"),"echo stomp" : ("100","14/13/12/11"),"astral spirit" : ("80/90/100/110","16"),"natural order" : (-1,-1),"earth splitter" : ("125/175/225","100"),"searing chains" : ("110","14/12/10/8"),"slight of fist" : ("50","30/22/14/6"),"flame guard" : ("80/90/100/110","35"),"fire remnant" : ("0","35"),"untouchable" : (-1,-1),"enchant" : ("65","30/24/18/12"),"natures attendants" : ("125","45"),"impetus" : ("55/60/65",-1),"malefice" : ("110/130/150/160","15"),"demonic conversion" : ("170","35"),"midnight pulse" : ("95/110/125/140","35"),"black hole" : ("275/325/375","200/180/160"),"time walk" : ("40","24/18/12/6"),"time dilation" : ("75","40/34/28/22"),"time lock" : (-1,-1),"chronosphere" : ("150/225/300","140/125/110"),"rocket barrage" : ("90","7/6.5/6/5.5"),"homing missile" : ("120/130/140/150","20/17/14/11"),"flak cannon" : ("50","30"),"call down" : ("125","55/40/45"),"inner vitality" : ("170","22/18/14/10"),"burning spear" : (-1,-1),"berserkers blood" : (-1,-1),"life break" : (-1,"12"),"cold snap" : ("100","20"),"ghost walk" : ("200","45"),"ice wall" : ("175","25"),"deafening blast" : ("300","40"),"alacrity" : ("60","17"),"tornado" : ("150","30"),"emp" : ("125","30"),"chaos meteor" : ("200","55"),"forge spirit" : ("75","30"),"sun strike" : ("175","25"),"tether" : ("60","12"),"spirits" : ("150","20/18/16/14"),"overcharge" : (-1,"2"),"relocate" : ("100","100/80/60"),"dual breath" : ("135/140/155/170","10"),"ice path" : ("90","12/11/10/9"),"liquid fire" : (-1,"20/15/10/4"),"macropyre" : ("220/330/440","60"),"blade fury" : ("120/110/100/90","42/34/26/18"),"healing ward" : ("140","60"),"blade dance" : (-1,-1),"omnislash" : ("200/275/350","130/120/110"),"illuminate" : ("150/160/170/180","10"),"mana leak" : ("160","16/14/12/10"),"chakra magic" : ("25/35/45/55","17/16/15/14"),"recall" : ("100","15"),"blinding light" : ("50","20/16/12"),"spirit form" : ("100","80/70/60"),"torrent" : ("90/100/110/120","16/14/12/10"),"tidebringer" : (-1,"13/10/7/4"),"x marks the spot" : ("50","26/20/14/8"),"ghostship" : ("125/175/225","60/50/40"),"overwhelming odds" : ("100/110/120/130","15"),"press the attack" : ("110","16/15/14/13"),"moment of courage" : (-1,"2.3/1.8/1.3/0.8"),"duel" : ("75","50"),"split earth" : ("100/125/140/160","9"),"diabolic edict" : ("95/120/135/155","22"),"lightning storm" : ("90/100/110/120","4"),"pulse nova" : ("70/90/110",-1),"frost blast" : ("125/150/170/190","8"),"ice armor" : ("50","5"),"sacrifice" : ("25","60/46/32/18"),"chain frost" : ("200/325/500","100/80/60"),"rage" : ("75","16"),"feast" : (-1,-1),"open wounds" : ("140/130/120/110","24/20/16/12"),"assimilate" : ("50","50"),"infest" : ("50","100/75/50"),"dragon slave" : ("110/115/130/145","8"),"light strike array" : ("100/110/120/130","7"),"fiery soul" : (-1,-1),"laguna blade" : ("280/420/680","70/60/50"),"earth spike" : ("100/120/140/160","12"),"hex" : ("125/150/175/200","30/24/18/12"),"mana drain" : ("10","16/12/8/4"),"finger of death" : ("200/420/650","160/100/40"),"summon spirit bear" : ("75","120"),"rabid" : ("50","35"),"savage roar" : ("50","38/32/26/20"),"battle cry" : ("50","60"),"true form" : ("25",-1),"druid form" : ("25",-1),"lucent beam" : ("90/100/110/120","6"),"moon glaive" : (-1,-1),"lunar blessing" : (-1,-1),"eclipse" : ("150/200/250","140"),"summon wolves" : ("145","30"),"howl" : ("40","60/55/50/45"),"feral impulse" : (-1,-1),"shapeshift" : ("100","120/90/60"),"shockwave" : ("90","10/9/8/7"),"empower" : ("30/50/70/90","8"),"skewer" : ("80","25"),"reverse polarity" : ("200/250/300","120"),"split shot" : (-1,-1),"mystic snake" : ("140/150/160/170","11"),"mana shield" : (-1,-1),"stone gaze" : ("200","90"),"earthbind" : ("100","20/16/12/8"),"poof" : ("80","12/10/8/6"),"geostrike" : (-1,-1),"divided we stand" : (-1,-1),"starstorm" : ("100/120/140/160","12"),"sacred arrow" : ("100","17"),"leap" : ("40/35/30/20","30/26/22/18"),"moonlight shadow" : ("75","140/120/100"),"boundless strike" : ("100","22"),"tree dance" : (-1,"1.2"),"primal spring" : ("130/120/110/100","19/17/15/13"),"jingu mastery" : (-1,-1),"mischief" : (-1,"3"),"wukongs command" : ("100","130/110/90"),"waveform" : ("140/155/160/165","11"),"adaptive strike" : ("80","10"),"morph" : (-1,-1),"hybrid" : ("200","60"),"replicate" : ("25","80"),"mirror image" : ("70/80/90/100","40"),"ensnare" : ("100","12"),"rip tide" : ("80/90/100/110","10"),"song of the siren" : ("100","160/120/80"),"sprout" : ("70/90/110/130","11/10/9/8"),"teleportation" : ("50","50/40/30/20"),"natures call" : ("130/140/150/160","37"),"wrath of nature" : ("175/225/275","90/75/60"),"death pulse" : ("125/145/165/185","8/7/6/5"),"ghost shroud" : ("50","28/24/20/16"),"heartstopper aura" : (-1,-1),"reapers scythe" : ("175/340/500","90/80/70"),"void" : ("80/90/100/110","8"),"crippling fear" : ("50","12"),"hunter in the night" : ("80","30/26/22/18"),"darkness" : (-1,"160/120/80"),"impale" : ("95/115/13/155","14"),"mana burn" : ("100","28/20/12/4"),"burrow" : (-1,-1),"spiked carapace" : ("40","25/20/15/10"),"vendetta" : ("160/210/260","70/60/50"),"fireblast" : ("75/85/95/105","12"),"ignite" : ("90","15"),"bloodlust" : ("65","20"),"multicast" : (-1,-1),"purification" : ("85/100/115/130","11/10/9/8"),"repel" : ("50","30/26/22/18"),"degen aura" : (-1,-1),"guardian angel" : ("125/175/250","160"),"fortunes end" : ("110","15/12/9/6"),"fates edict" : ("50","16/13/10/7"),"purifying flames" : ("80/85/90/95","2.25"),"false promise" : ("100","100/65/30"),"arcane orb" : ("100/120/140/160",-1),"astral imprisonment" : ("120/140/160/180","22/18/14/10"),"essence aura" : (-1,-1),"sanitys eclipse" : ("175/250/325","160"),"stifling dagger" : ("30/25/20/15","6"),"phantom strike" : ("50","14/11/8/5"),"blur" : (-1,-1),"coup de grace" : (-1,-1),"spirit lance" : ("125/130/135/140","7"),"doppelganger" : ("50","25/20/15/10"),"phantom rush" : (-1,"16/12/8/4"),"juxtapose" : (-1,-1),"icarus dive" : (-1,"36"),"fire spirits" : ("80/90/100/110","45/40/35/30"),"sun ray" : ("100","26"),"supernova" : ("200","110"),"illusory orb" : ("80/100/120/140","14/13/12/11"),"waning rift" : ("100/110/120/130","16/15/14/13"),"phase shift" : (-1,"6"),"dream coil" : ("100/150/200","70/65/60"),"meat hook" : ("110/120/130/140","14/13/12/11"),"rot" : (-1,-1),"flesh heap" : (-1,-1),"dismember" : ("100/130/170","30/25/20"),"nether blast" : ("85/105/125/145","5"),"decrepify" : ("60","15/12/9/6"),"nether ward" : ("80","35"),"life drain" : ("125/175/225","22"),"shadow strike" : ("110","16/12/8/4"),"blink" : ("60","15/12/9/6"),"scream of pain" : ("110/120/130/140","7"),"sonic wave" : ("250/360/500","135"),"plasma field" : ("125","14"),"static link" : ("50","32/30/28/26"),"unstable current" : (-1,-1),"eye of the storm" : ("100/150/200","80/70/60"),"smoke screen" : ("90","11"),"blaink strike" : ("50","16/12/8/4"),"cloak and dagger" : (-1,"6/5/4/3"),"tricks of the trade" : ("75","40/35/30"),"telekinesis" : ("125","22"),"fade bolt" : ("120/130/140/150","16/14/12/10"),"null field" : (-1,-1),"spell steal" : ("25","20/18/16"),"burrowstrike" : ("110/120/130/140","11"),"sand storm" : ("60/50/40/30","34/26/18/10"),"caustic finale" : (-1,-1),"epicenter" : ("150/225/300","120/110/100"),"disruption" : ("120","27/24/21/18"),"soul catcher" : ("50/60/70/80","13/12/11/10"),"shadow poison" : ("50","2.5"),"demonic purge" : ("200","40"),"shadowraze" : ("90","10"),"necromastery" : (-1,-1),"presence of the dark lord" : (-1,-1),"requiem of souls" : ("150/175/200","120/110/100"),"ether shock" : ("95/105/135/160","8"),"hex" : ("110/140/170/200","13"),"shackles" : ("140/150/160/170","10"),"mass serpent ward" : ("200/350/600","120"),"arcane curse" : ("75/95/115/135","20/18/16/14"),"glaives of wisdom" : ("15",-1),"last word" : ("115","30/24/18/12"),"global silence" : ("250/375/500","130"),"arcane bolt" : ("70","5/4/3/2"),"concussive shot" : ("95","18/16/14/12"),"ancient seal" : ("80/90/100/110","14"),"mystic flare" : ("350/575/800","60/40/20"),"guardian sprint" : (-1,"17"),"slithereen crush" : ("80/95/105/115","8"),"bash of the deep" : (-1,-1),"corrosive haze" : ("25","5"),"dark pact" : ("55/50/45/40","9/8/7/6"),"pounce" : ("75","20/16/12/8"),"essence shift" : (-1,-1),"shadow dance" : ("120","60"),"shrapnel" : ("50","55"),"headshot" : (-1,-1),"take aim" : (-1,-1),"assassinate" : ("175/275/375","20/15/10"),"spectral dagger" : ("130/140/150/160","16"),"desolate" : (-1,-1),"dispersion" : (-1,-1),"haunt" : ("150","180/150/120"),"charge of darkness" : ("100","12"),"empowering haste" : (-1,"12"),"greater bash" : (-1,"1.5"),"nether strike" : ("125/150/175","80/70/60"),"static remnant" : ("100","3.5"),"electric vortex" : ("85","21/20/19/18"),"overload" : (-1,-1),"ball lightning" : (-1,-1),"storm hammer" : ("140","13"),"great cleave" : (-1,-1),"warcry" : ("25","34/28/22/16"),"gods strength" : ("100/150/200","80"),"proximity mines" : ("110/130/150/170","12"),"statis trap" : ("80/110/140/160","20/16/13/10"),"blast off" : ("100/125/150/175","35"),"minefield sign" : (-1,"360"),"remote mines" : ("200/240/300","10"),"refraction" : ("100","17"),"meld" : ("50","6"),"psi blades" : (-1,-1),"psionic trap" : ("15","11/8/5"),"reflection" : ("50","22/20/18/16"),"conjure image" : ("70","16"),"metamorphosis" : ("100","140"),"sunder" : ("120/80/40","200/100/0"),"gush" : ("90/100/110/120","12"),"kraken shell" : (-1,-1),"anchor smash" : ("30/40/50/60","7/6/5/4"),"ravage" : ("150/225/325","150"),"whirling death" : ("70","6"),"timber chain" : ("60/70/80/90","4"),"reactive armor" : (-1,-1),"chakram" : ("100/150/200","8"),"laser" : ("95/120/145/170","14"),"heatseeking missile" : ("120/140/160/180","25"),"march of the machines" : ("145/150/165/190","35"),"rearm" : ("100/200/300",-1),"avalanche" : ("120","17"),"toss" : ("120","8"),"craggy exterior" : (-1,-1),"grow" : (-1,-1),"natures guise" : (-1,-1),"leech seed" : ("80/95/110/125","16/13/10/7"),"living armor" : ("50","30/24/18/12"),"eyes in the forest" : ("100","35"),"overgrowth" : ("150/175/200","100/85/70"),"berserkers rage" : (-1,-1),"whirling axes" : ("50","19/16/13/10"),"fervor" : (-1,-1),"battle trance" : ("75","35"),"ice shards" : ("100/105/110/115","19/16/13/10"),"snowball" : ("75","21/20/19/10"),"frozen sigil" : ("75","50"),"walrus kick" : ("100","8"),"walrus punch" : ("50/75/100","36/24/12"),"firestorm" : ("100/110/120/130","12"),"pit of malice" : ("100/115/130/145","32/28/24/20"),"atrophy aura" : (-1,-1),"dark rift" : ("75/150/225","130/120/110"),"decay" : ("70/90/110/130","10/8/6/4"),"soul rip" : ("100/110/120/130","24/18/12/6"),"tombstone" : ("120/130/140/150","70"),"flesh golem" : ("100","75"),"earthshock" : ("75","5"),"overpower" : ("75","10"),"fury swipes" : (-1,-1),"enrage" : (-1,"50/40/30"),"magic missile" : ("110/120/130/140","13/12/11/10"),"wave of terror" : ("40","22/20/18/16"),"vengeance aura" : (-1,-1),"nether swap" : ("100/150/200","45"),"venomous gale" : ("125","21/20/19/18"),"poison sting" : (-1,-1),"plague ward" : ("20","5"),"poison nova" : ("200/300/400","140/120/100"),"poison attack" : (-1,"20"),"nethertoxin" : (-1,-1),"corrosive skin" : (-1,-1),"viper strike" : ("125/175/250","50/40/30"),"grave chill" : ("90","16/14/12/10"),"soul assumption" : ("170/160/150/140","4"),"gravekeepers cloak" : (-1,-1),"summon familiars" : ("150","130"),"fatal bonds" : ("140","24/22/20/18"),"shadow word" : ("90/110/130/150","16"),"upheaval" : ("100/110/120/130","50/46/42/38"),"chaotic offering" : ("250/375/500","170"),"the swarm" : ("70/80/90/100","35/30/25/20"),"shukuchi" : ("60","12/10/8/6"),"geminate attack" : (-1,"7/6/5/3"),"time lapse" : ("150/75/0","60/50/40"),"shackleshot" : ("90/100/110/120","12"),"powershot" : ("90/100/110/120","12/11/10/9"),"windrun" : ("60","12"),"focus fire" : ("75/100/125","60"),"arctic burn" : ("120/110/100/90","50/40/30/20"),"splinter blast" : ("120/130/140/150","7"),"cold embrace" : ("75","24/21/18/15"),"winters curse" : ("250","80"),"paralyzing cask" : ("110/120/130/140","20/18/16/14"),"voodoo restoration" : ("20/30/40/50",-1),"maledict" : ("105/110/115/120","20"),"death ward" : ("200","80"),"wraithfire blast" : ("140","8"),"vampiric aura" : (-1,-1),"mortal strike" : (-1,-1),"reincarnation" : ("160","240/140/40"),"arc lightning" : ("65/70/75/80","1.6"),"lightning bolt" : ("75/95/115/135","6"),"static field" : (-1,-1),"nimbus" : ("275","35"),"thundergods wrath" : ("225/325/450","90")}








vokimages= {"q" : Image.open('d:/streamdata/quas.png', 'r'), "w":Image.open('d:/streamdata/wex.png', 'r'), "e" : Image.open('d:/streamdata/exort.png', 'r')}
invokeDict = {"cold snap" : "qqq","ghost walk":"qqw","ice wall":"qqe","deafening blast":"qwe","alacrity":"wwe","tornado":"wwq","emp":"www","chaos meteor":"eew","forge spirit":"eeq","sun strike":"eee"}

secretShop = ("vitality booster","hyperstone","eagle","point booster","reaver","energy booster","talisman of evasion","relic","platemail","demon edge","mystic staff","ultimate orb")


itemDict = {"clarity" : ("https://cdn.steamstatic.com/apps/dota2/images/items/clarity_lg.png" , "clarity"),
"faerie" : ("https://cdn.steamstatic.com/apps/dota2/images/items/faerie_fire_lg.png" , "faerie","fearie","fire","fairy"),
"mango" : ("https://cdn.steamstatic.com/apps/dota2/images/items/enchanted_mango_lg.png" , "enchanted","mango"),
"tango" : ("tps://cdn.steamstatic.com/apps/dota2/images/items/tango_lg.png" , "tango"),
"salve" : ("https://cdn.steamstatic.com/apps/dota2/images/items/flask_lg.png" , "flask","salve"),
"smoke" : ("https://cdn.steamstatic.com/apps/dota2/images/items/smoke_of_deceit_lg.png" , "smoke","deceit","deciet"),
"town" : ("https://cdn.steamstatic.com/apps/dota2/images/items/tpscroll_lg.png" , "tp","town","portal","tpscroll"),
"dust" : ("https://cdn.steamstatic.com/apps/dota2/images/items/dust_lg.png" , "dust","appearance"),
"animal" : ("https://cdn.steamstatic.com/apps/dota2/images/items/courier_lg.png" , "animal","courier"),
"flying" : ("https://cdn.steamstatic.com/apps/dota2/images/items/flying_courier_lg.png" , "flying"),
"observer" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ward_observer_lg.png" , "observer","obs"),
"sentry" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ward_sentry_lg.png" , "sentry"),
"tome" : ("https://cdn.steamstatic.com/apps/dota2/images/items/tome_of_knowledge_lg.png" , "tome", "knowledge"),
"bottle" : ("https://cdn.steamstatic.com/apps/dota2/images/items/bottle_lg.png" , "bottle"),
"ironwood" : ("https://cdn.steamstatic.com/apps/dota2/images/items/branches_lg.png" , "ironwood","branch"),
"gauntlets" : ("https://cdn.steamstatic.com/apps/dota2/images/items/gauntlets_lg.png" , "gauntlets"),
"slippers" : ("https://cdn.steamstatic.com/apps/dota2/images/items/slippers_lg.png" , "slippers"),
"mantle" : ("https://cdn.steamstatic.com/apps/dota2/images/items/mantle_lg.png" , "mantle"),
"circlet" : ("https://cdn.steamstatic.com/apps/dota2/images/items/circlet_lg.png" , "circlet","nobility"),
"belt" : ("https://cdn.steamstatic.com/apps/dota2/images/items/belt_of_strength_lg.png" , "belt"),
"elvenskin" : ("https://cdn.steamstatic.com/apps/dota2/images/items/boots_of_elves_lg.png" , "elvenskin"),
"robe" : ("https://cdn.steamstatic.com/apps/dota2/images/items/robe_lg.png" , "robe","magi"),
"ogre" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ogre_axe_lg.png" , "ogre","club"),
"alacrity" : ("https://cdn.steamstatic.com/apps/dota2/images/items/blade_of_alacrity_lg.png" , "alacrity"),
"wizardry" : ("https://cdn.steamstatic.com/apps/dota2/images/items/staff_of_wizardry_lg.png" , "wizardry"),
"protection" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ring_of_protection_lg.png" , "protection"),
"stout" : ("https://cdn.steamstatic.com/apps/dota2/images/items/stout_shield_lg.png" , "stout"),
"quelling" : ("https://cdn.steamstatic.com/apps/dota2/images/items/quelling_blade_lg.png" , "quelling"),
"raindrop" : ("https://cdn.steamstatic.com/apps/dota2/images/items/infused_raindrop_lg.png" , "infused", "raindrop"),
"blight" : ("https://cdn.steamstatic.com/apps/dota2/images/items/blight_stone_lg.png" , "blight","stone","blightstone"),
"venom" : ("https://cdn.steamstatic.com/apps/dota2/images/items/orb_of_venom_lg.png" , "venom"),
"blades" : ("https://cdn.steamstatic.com/apps/dota2/images/items/blades_of_attack_lg.png" , "blades", "attack"),
"chainmail" : ("https://cdn.steamstatic.com/apps/dota2/images/items/chainmail_lg.png" , "chainmail","chain"),
"quarterstaff" : ("https://cdn.steamstatic.com/apps/dota2/images/items/quarterstaff_lg.png" , "quarterstaff"),
"will" : ("https://cdn.steamstatic.com/apps/dota2/images/items/helm_of_iron_will_lg.png" , "will"),
"dominator": ("https://cdn.steamstatic.com/apps/dota2/images/items/helm_of_the_dominator_lg.png","dominator"),
"broadsword" : ("https://cdn.steamstatic.com/apps/dota2/images/items/broadsword_lg.png" , "broadsword"),
"claymore" : ("https://cdn.steamstatic.com/apps/dota2/images/items/claymore_lg.png" , "claymore"),
"javelin" : ("https://cdn.steamstatic.com/apps/dota2/images/items/javelin_lg.png" , "javelin"),
"mithril hammer" : ("https://cdn.steamstatic.com/apps/dota2/images/items/mithril_hammer_lg.png" , "mithril","hammer"),
"wind lace" : ("https://cdn.steamstatic.com/apps/dota2/images/items/wind_lace_lg.png" , "wind","lace"),
"magic stick" : ("https://cdn.steamstatic.com/apps/dota2/images/items/magic_stick_lg.png" , "stick"),
"sage's mask" : ("https://cdn.steamstatic.com/apps/dota2/images/items/sobi_mask_lg.png" , "sobi","sage","sages","mask"),
"ring of regen" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ring_of_regen_lg.png" , "regen"),
"speed" : ("https://cdn.steamstatic.com/apps/dota2/images/items/boots_lg.png" , "boots","speed"),
"gloves" : ("https://cdn.steamstatic.com/apps/dota2/images/items/gloves_lg.png" , "gloves","haste"),
"cloak" : ("https://cdn.steamstatic.com/apps/dota2/images/items/cloak_lg.png" , "cloak"),
"ring of health" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ring_of_health_lg.png" , "health"),
"void stone" : ("https://cdn.steamstatic.com/apps/dota2/images/items/void_stone_lg.png" , "void"),
"gem" : ("https://cdn.steamstatic.com/apps/dota2/images/items/gem_lg.png" , "gem","true","sight","truesight"),
"morbid" : ("	https://cdn.steamstatic.com/apps/dota2/images/items/lifesteal_lg.png" , "lifesteal","morbid"),
"amulet" : ("https://cdn.steamstatic.com/apps/dota2/images/items/shadow_amulet_lg.png" , "amulet"),
"ghost" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ghost_lg.png" , "ghost"),
"blink" : ("https://cdn.steamstatic.com/apps/dota2/images/items/blink_lg.png" , "blink","dagger"),
"magic wand" : ("https://cdn.steamstatic.com/apps/dota2/images/items/magic_wand_lg.png" , "wand"),
"null talisman" : ("https://cdn.steamstatic.com/apps/dota2/images/items/null_talisman_lg.png" , "null","talisman"),
"wraith band" : ("https://cdn.steamstatic.com/apps/dota2/images/items/wraith_band_lg.png" , "wraith","band"),
"poor man's shield" : ("https://cdn.steamstatic.com/apps/dota2/images/items/poor_mans_shield_lg.png" , "poor","mans","man"),
"bracer" : ("https://cdn.steamstatic.com/apps/dota2/images/items/bracer_lg.png" , "bracer"),
"soul ring" : ("https://cdn.steamstatic.com/apps/dota2/images/items/soul_ring_lg.png" , "soul"),
"phase boots" : ("https://cdn.steamstatic.com/apps/dota2/images/items/phase_boots_lg.png" , "phase"),
"power treads" : ("https://cdn.steamstatic.com/apps/dota2/images/items/power_treads_lg.png" , "treads", "power"),
"oblivion staff" : ("https://cdn.steamstatic.com/apps/dota2/images/items/oblivion_staff_lg.png" , "oblivion", "staff"),
"perseverance" : ("https://cdn.steamstatic.com/apps/dota2/images/items/pers_lg.png" , "perseverance"),
"hand of midas" : ("https://cdn.steamstatic.com/apps/dota2/images/items/hand_of_midas_lg.png" , "hand", "midas"),
"boots of travel" : ("https://cdn.steamstatic.com/apps/dota2/images/items/travel_boots_lg.png" , "travel"),
"moon shard" : ("https://cdn.steamstatic.com/apps/dota2/images/items/moon_shard_lg.png" , "moon","shard"),
"ring of basilius" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ring_of_basilius_lg.png" , "basilius"),
"iron talon" : ("https://cdn.steamstatic.com/apps/dota2/images/items/iron_talon_lg.png" , "talon"),
"headdress" : ("https://cdn.steamstatic.com/apps/dota2/images/items/headdress_lg.png" , "headdress"),
"buckler" : ("https://cdn.steamstatic.com/apps/dota2/images/items/buckler_lg.png" , "buckler"),
"urn of shadows" : ("https://cdn.steamstatic.com/apps/dota2/images/items/urn_of_shadows_lg.png" , "urn","shadows"),
"tranquil boots" : ("https://cdn.steamstatic.com/apps/dota2/images/items/tranquil_boots_lg.png" , "tranquil"),
"ring of aquila" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ring_of_aquila_lg.png" , "aquila"),
"medallion of courage" : ("https://cdn.steamstatic.com/apps/dota2/images/items/medallion_of_courage_lg.png" , "medallion","courage"),
"arcane boots" : ("https://cdn.steamstatic.com/apps/dota2/images/items/arcane_boots_lg.png" , "arcane"),
"drum of endurance" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ancient_janggo_lg.png" , "drum","endurance","janggo"),
"mekansm" : ("https://cdn.steamstatic.com/apps/dota2/images/items/mekansm_lg.png" , "mekansm"),
"vlads" : ("https://cdn.steamstatic.com/apps/dota2/images/items/vladmir_lg.png" , "vlads","vladimir","vladimirs","offering"),
"pipe of insight" : ("https://cdn.steamstatic.com/apps/dota2/images/items/pipe_lg.png" , "pipe","insight"),
"guardian greaves" : ("https://cdn.steamstatic.com/apps/dota2/images/items/guardian_greaves_lg.png" , "guardian","greaves"),
"glimmer cape" : ("https://cdn.steamstatic.com/apps/dota2/images/items/glimmer_cape_lg.png" , "glimmer","cape"),
"force staff" : ("https://cdn.steamstatic.com/apps/dota2/images/items/force_staff_lg.png" , "force"),
"veil of discord" : ("https://cdn.steamstatic.com/apps/dota2/images/items/veil_of_discord_lg.png" , "viel","veil", "discord"),
"aether lens" : ("https://cdn.steamstatic.com/apps/dota2/images/items/aether_lens_lg.png" , "aether","lens"),
"necronomicon" : ("https://cdn.steamstatic.com/apps/dota2/images/items/necronomicon_lg.png" , "necro","book","necrobook", "necronomicon"),
"dagon" : ("https://cdn.steamstatic.com/apps/dota2/images/items/dagon_lg.png" , "dagon"),
"cyclone" : ("https://cdn.steamstatic.com/apps/dota2/images/items/cyclone_lg.png" , "euls","eul","divinity","cyclone"),
"solar crest" : ("https://cdn.steamstatic.com/apps/dota2/images/items/solar_crest_lg.png" , "solar","crest"),
"rod of atos" : ("https://cdn.steamstatic.com/apps/dota2/images/items/rod_of_atos_lg.png" , "rod", "atos"),
"orchid" : ("https://cdn.steamstatic.com/apps/dota2/images/items/orchid_lg.png" , "orchid","malevolence"),
"ultimate scepter" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ultimate_scepter_lg.png" , "ultimate","aghanims","ags","aghs","agha","aga","aghanim"),
"refresher" : ("https://cdn.steamstatic.com/apps/dota2/images/items/refresher_lg.png" , "refresher"),
"sheepstick" : ("https://cdn.steamstatic.com/apps/dota2/images/items/sheepstick_lg.png" , "sheepstick","scythe","vyse"),
"octarine core" : ("https://cdn.steamstatic.com/apps/dota2/images/items/octarine_core_lg.png" , "core","octarine"),
"crystalys" : ("https://cdn.steamstatic.com/apps/dota2/images/items/lesser_crit_lg.png" , "crystalys","crit"),
"armlet" : ("https://cdn.steamstatic.com/apps/dota2/images/items/armlet_lg.png" , "armlet", "mordiggian"),
"invis blade" : ("https://cdn.steamstatic.com/apps/dota2/images/items/invis_sword_lg.png" , "invis","shadow","blade"),
"basher" : ("https://cdn.steamstatic.com/apps/dota2/images/items/basher_lg.png" , "skull","basher"),
"battle fury" : ("https://cdn.steamstatic.com/apps/dota2/images/items/bfury_lg.png" , "battle", "fury","bfury"),
"ethereal blade" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ethereal_blade_lg.png" , "ethereal"),
"silver edge" : ("https://cdn.steamstatic.com/apps/dota2/images/items/silver_edge_lg.png" , "silver"),
"radiance" : ("https://cdn.steamstatic.com/apps/dota2/images/items/radiance_lg.png" , "radiance"),
"mkb" : ("https://cdn.steamstatic.com/apps/dota2/images/items/monkey_king_bar_lg.png" , "mkb","monkey"),
"daedalus" : ("https://cdn.steamstatic.com/apps/dota2/images/items/greater_crit_lg.png" , "deadalus", "daedalus","buriza"),
"bfly" : ("https://cdn.steamstatic.com/apps/dota2/images/items/butterfly_lg.png" , "butterfly","bfly"),
"rapier" : ("https://cdn.steamstatic.com/apps/dota2/images/items/rapier_lg.png" , "divine", "rapier"),
"abyssal blade" : ("https://cdn.steamstatic.com/apps/dota2/images/items/abyssal_blade_lg.png" , "abyssal"),
"bloodthorn" : ("https://cdn.steamstatic.com/apps/dota2/images/items/bloodthorn_lg.png" , "bloodthorn"),
"hood" : ("https://cdn.steamstatic.com/apps/dota2/images/items/hood_of_defiance_lg.png" , "hood", "defiance"),
"vanguard" : ("https://cdn.steamstatic.com/apps/dota2/images/items/vanguard_lg.png" , "vanguard"),
"blade mail" : ("https://cdn.steamstatic.com/apps/dota2/images/items/blade_mail_lg.png" , "mail","blademail"),
"soul booster" : ("https://cdn.steamstatic.com/apps/dota2/images/items/soul_booster_lg.png" , "soul", "booster"),
"crimson guard" : ("https://cdn.steamstatic.com/apps/dota2/images/items/crimson_guard_lg.png" , "crimson"),
"bkb" : ("https://cdn.steamstatic.com/apps/dota2/images/items/black_king_bar_lg.png" , "bkb","black"),
"lotus orb" : ("https://cdn.steamstatic.com/apps/dota2/images/items/lotus_orb_lg.png" , "lotus"),
"shiva's guard" : ("https://cdn.steamstatic.com/apps/dota2/images/items/shivas_guard_lg.png" , "shivas","shiva"),
"bloodstone" : ("https://cdn.steamstatic.com/apps/dota2/images/items/bloodstone_lg.png" , "bloodstone"),
"manta" : ("https://cdn.steamstatic.com/apps/dota2/images/items/manta_lg.png" , "manta","style"),
"linken's sphere" : ("https://cdn.steamstatic.com/apps/dota2/images/items/sphere_lg.png" , "sphere","linken","linkens"),
"hurricane pike" : ("https://cdn.steamstatic.com/apps/dota2/images/items/hurricane_pike_lg.png" , "hurricane","pike"),
"assault" : ("https://cdn.steamstatic.com/apps/dota2/images/items/assault_lg.png" , "assault","cuirass"),
"heart" : ("https://cdn.steamstatic.com/apps/dota2/images/items/heart_lg.png" , "heart", "tarrasque"),
"mom" : ("https://cdn.steamstatic.com/apps/dota2/images/items/mask_of_madness_lg.png" , "madness", "mom"),
"dragon lance" : ("https://cdn.steamstatic.com/apps/dota2/images/items/dragon_lance_lg.png" , "dragon", "lance"),
"sange" : ("https://cdn.steamstatic.com/apps/dota2/images/items/sange_lg.png" , "sange"),
"yasha" : ("https://cdn.steamstatic.com/apps/dota2/images/items/yasha_lg.png" , "yasha"),
"echo sabre" : ("https://cdn.steamstatic.com/apps/dota2/images/items/echo_sabre_lg.png" , "echo","sabre"),
"maelstrom" : ("https://cdn.steamstatic.com/apps/dota2/images/items/maelstrom_lg.png" , "maelstrom"),
"diffusal blade" : ("https://cdn.steamstatic.com/apps/dota2/images/items/diffusal_blade_lg.png" , "diffusal"),
"heaven's halberd" : ("https://cdn.steamstatic.com/apps/dota2/images/items/heavens_halberd_lg.png" , "halberd", "heavens"),
"sny" : ("https://cdn.steamstatic.com/apps/dota2/images/items/sange_and_yasha_lg.png" , "sange", "yasha","sny"),
"mjollnir" : ("https://cdn.steamstatic.com/apps/dota2/images/items/mjollnir_lg.png" , "mjollnir"),
"satanic" : ("https://cdn.steamstatic.com/apps/dota2/images/items/satanic_lg.png" , "satanic"),
"energy booster" : ("https://cdn.steamstatic.com/apps/dota2/images/items/energy_booster_lg.png" , "energy"),
"point booster" : ("https://cdn.steamstatic.com/apps/dota2/images/items/point_booster_lg.png" , "point", "pb"),
"vitality booster" : ("https://cdn.steamstatic.com/apps/dota2/images/items/vitality_booster_lg.png" , "vitality","vit"),
"platemail" : ("https://cdn.steamstatic.com/apps/dota2/images/items/platemail_lg.png" , "plate","platemail"),
"talisman of evasion" : ("https://cdn.steamstatic.com/apps/dota2/images/items/talisman_of_evasion_lg.png" , "talisman",),
"hyperstone" : ("https://cdn.steamstatic.com/apps/dota2/images/items/hyperstone_lg.png" , "hyperstone"),
"ultimate orb" : ("https://cdn.steamstatic.com/apps/dota2/images/items/ultimate_orb_lg.png" , "ultimate"),
"demon edge" : ("https://cdn.steamstatic.com/apps/dota2/images/items/demon_edge_lg.png" , "demon"),
"mystic staff" : ("https://cdn.steamstatic.com/apps/dota2/images/items/mystic_staff_lg.png" , "mystic"),
"reaver" : ("https://cdn.steamstatic.com/apps/dota2/images/items/reaver_lg.png" , "reaver"),
"eagle" : ("https://cdn.steamstatic.com/apps/dota2/images/items/eagle_lg.png" , "eagle" , "eaglesong"),
"relic" : ("https://cdn.steamstatic.com/apps/dota2/images/items/relic_lg.png" , "sacred", "relic"),
"recipe":  ("https://cdn.steamstatic.com/apps/dota2/images/items/recipe_lg.png","recipe","recipie","ricipie","recipe","paper")}

#dont ask about -1 cooldown
itemCost = {"clarity" : (50,-190,-1),
"faerie" : (70,0,5),
"mango" : (100,-150,-1),
"tango" : (125,-1,-1),
"salve" : (110,-1,-1),
"smoke" : (50,-1,-1),
"town" : (50,75,80),
"dust" : (180,-1,30),
"animal" : (100,-1,-1),
"flying" : (150,-1,-1),
"observer" : (60,-1,-1),
"sentry" : (100,-1,-1),
"tome" : (150,-1,-1),
"bottle" : (650,-60,-1),
"ironwood" : (50,-1,-1),
"gauntlets" : (150,-1,-1),
"slippers" : (150,-1,-1),
"mantle" : (150,-1,-1),
"circlet" : (165,-1,-1),
"belt" : (450,-1,-1),
"elvenskin" : (450,-1,-1),
"robe" : (450,-1,-1),
"ogre" : (1000,-1,-1),
"alacrity" : (1000,-1,-1),
"wizardry" : (1000,-1,-1),
"protection" : (175,-1,-1),
"stout" : (200,-1,-1),
"quelling" : (200,-1,4),
"raindrop" :  (225,0,7),
"blight" :  (300,-1,-1),
"venom" : (275,-1,-1),
"blades" : (420,-1,-1),
"chainmail" :  (550,-1,-1),
"quarterstaff" : (875,-1,-1),
"will" : (900,-1,-1),
"dominator":  (2025,0,60),
"broadsword" : (1200,-1,-1),
"claymore" : (1400,-1,-1),
"javelin" :  (1500,-1,-1),
"mithril hammer" : (1600,-1,-1),
"wind lace" : (250,-1,-1),
"magic stick" :  (200,-1,13),
"sage's mask" : (325,-1,-1),
"ring of regen" : (325,-1,-1),
"speed" : (400,-1,-1),
"gloves" :  (500,-1,-1),
"cloak" : (550,-1,-1),
"ring of health" : (850,-1,-1),
"void stone" : (850,-1,-1),
"gem" : (900,-1,-1),
"morbid" : (1100,-1,-1),
"amulet" : (1300,0,7),
"ghost" : (1500,0,20),
"blink" : (2250,0,12),
"magic wand" : (465,-1,13),
"null talisman" : (470,-1,-1),
"wraith band" : (485,-1,-1),
"poor man's shield" : (500,-1,-1),
"bracer" :  (490,-1,-1),
"soul ring" : (750,-150,30),
"phase boots" : (1240,-1,8),
"power treads" : (1350,-1,-1),
"oblivion staff" : (1650,-1,-1),
"perseverance" :  (1700,-1,-1),
"hand of midas" : (2150,0,100),
"boots of travel" : (2400,75,45),
"moon shard" : (4000,-1,-1),
"ring of basilius" : (500,-1,-1),
"iron talon" :  (500,0,20),
"headdress" : (675,-1,-1),
"buckler" : (800,10,25),
"urn of shadows" : (875,0,7),
"tranquil boots" : (975,-1,13),
"ring of aquila" : (985,-1,-1),
"medallion of courage" : (1175,0,7),
"arcane boots" : (1300,-135,55),
"drum of endurance" : (1640,0,30),
"mekansm" : (2375,225,60),
"vlads" : (2275,-1,-1),
"pipe of insight" : (3200,100,60),
"guardian greaves" : (5375,-160,40),
"glimmer cape" : (1850,90,14),
"force staff" : (2250,25,20),
"veil of discord" : (2340,50,20),
"aether lens" : (2350,-1,-1),
"necronomicon" :  (2650,50,90),
"dagon" : (-1,180,-1),
"cyclone" : (2750,175,23),
"solar crest" :  (2625,0,7),
"rod of atos" : (3080,50,16),
"orchid" : (4075,100,18),
"ultimate scepter" : (4200,-1,-1),
"refresher" : (5200,375,195),
"sheepstick" : (5700,100,22),
"octarine core" : (5900,-1,-1),
"crystalys" : (2120,-1,-1),
"armlet" : (2370,-1,-1),
"invis blade" : (2700,75,28),
"basher" :  (2700,-1,2.3),
"battle fury" :  (4500,-1,4),
"ethereal blade" : (4700,100,20),
"silver edge" :  (5550,75,24),
"radiance" :  (5150,-1,-1),
"mkb" : (5200,-1,-1),
"daedalus" : (5320,-1,-1),
"bfly" : (5525,0,25),
"rapier" : (6000,-1,-1),
"abyssal blade" : (6400,75,35),
"bloodthorn" :  (7195,100,18),
"hood" : (1725,75,60),
"vanguard" : (2150,-1,-1),
"blade mail" :  (2200,25,20),
"soul booster" :  (3200,-1,-1),
"crimson guard" :  (3550,0,46),
"bkb" :  (3975,0,-1),
"lotus orb" : (4000,75,15),
"shiva's guard" : (4750,100,30),
"bloodstone" : (4850,0,300),
"manta" : (5000,125,45),
"linken's sphere" : (4850,0,13),
"hurricane pike" : (4650,25,15),
"assault" :  (5250,-1,-1),
"heart" : (5200,-1,7),
"mom" : (1975,25,20),
"sange" : (1950,-1,-1),
"yasha" : (1950,-1,-1),#itemCost = {itemName : gold, mana, cooldown}
"echo sabre" : (2650,-1,5),
"maelstrom" : (2800,-1,-1),
"diffusal blade" : (3150,0,4),
"heaven's halberd" : (3400,100,18),
"sny" : (3900,-1,-1),
"mjollnir" : (5700,50,35),
"satanic" : (5700,0,35),
"energy booster" :  (900,-1,-1),
"point booster" : (1200,-1,-1),
"vitality booster" : (1100,-1,-1),
"platemail" : (1400,-1,-1),
"talisman of evasion" : (1450,-1,-1),
"hyperstone" : (2000,-1,-1),
"ultimate orb" : (2150,-1,-1),
"demon edge" : (2200,-1,-1),
"mystic staff" : (2700,-1,-1),
"reaver" : (3000,-1,-1),
"eagle" : (3200,-1,-1),
"relic" : (3800,-1,-1)}
#6 bkb cooldowns, 5 dagon cooldowns,10 recipes?

itemParts = {"magic wand" : ("magic stick", "ironwood","ironwood","circlet"),
"null talisman" : ("circlet", "recipe","mantle"),
"wraith band" : ("circlet", "recipe","slippers"),
"poor man's shield" : ("slippers","slippers","stout"),
"bracer" : ("circlet", "recipe","gauntlets"),
"soul ring" : ("ring of regen", "sage's mask","mango"),
"phase boots" : ("speed","blades","blades"),
"power treads" : ("speed","gloves","belt"),
"oblivion staff" : ("quarterstaff","sage's mask","robe"),
"perseverance" : ("ring of health", "void stone"),
"hand of midas" : ("gloves", "recipe"),
"boots of travel" : ("speed" , "recipe"),
"moon shard" : ("hyperstone","hyperstone"),
"ring of basilius" : ("protection", "sage's mask"),
"iron talon" : ("protection","quelling","recipe"),
"headdress" : ("ring of regen","ironwood","recipe"),
"buckler" : ("chainmail","ironwood","recipe"),
"urn of shadows" : ("raindrop","protection","circlet","recipe"),
"tranquil boots" : ("speed","protection","ring of regen"),
"ring of aquila" : ("circlet", "recipe","slippers","protection", "sage's mask"),
"medallion of courage" : ("sage's mask", "blight","chainmail"),
"arcane boots" : ("energy booster","speed"),
"drum of endurance" : ("circlet", "recipe","gauntlets", "sage's mask","wind lace","recipe"),
"mekansm" : ("ring of regen","ironwood","recipe","chainmail","ironwood","recipe","recipe"),
"vlads" : ("ring of regen","ironwood","recipe","protection", "sage's mask","morbid"),
"pipe of insight" : ("ring of health", "ring of regen","cloak","ring of regen","ironwood","recipe","recipe"),
"guardian greaves" : ("speed", "energy booster","ring of regen","ironwood","recipe","chainmail","ironwood","recipe","recipe","recipe"),
"glimmer cape" : ("amulet","cloak"),
"force staff" : ("wizardry","ring of health","recipe"),
"veil of discord" : ("circlet", "recipe","mantle","circlet", "recipe","mantle","will","recipe"),
"aether lens" : ("energy booster","recipe","void stone"),
"necronomicon" : ("recipe","recipe","recipe","wizardry","belt"),
"dagon" : ("circlet", "recipe","mantle","wizardry","recipe","recipe","recipe","recipe","recipe"),
"cyclone" : ("recipe","wind lace","wizardry","void stone"),
"solar crest" : ("sage's mask", "blight","chainmail","talisman of evasion"),
"rod of atos" : ("wizardry","circlet", "recipe","gauntlets","circlet", "recipe","gauntlets","recipe"),
"orchid" : ("quarterstaff","sage's mask","robe","quarterstaff","sage's mask","robe","recipe"),
"ultimate scepter" : ("point booster","wizardry","ogre","alacrity"),
"refresher" : ("ring of health","void stone","ring of health","void stone","recipe"),
"sheepstick" : ("mystic staff","ultimate orb","void stone"),
"octarine core" : ("point booster","energy booster","vitality booster","mystic staff"),
"crystalys" : ("broadsword","blades","recipe"),
"armlet" : ("recipe","will","blades","chainmail"),
"invis blade" : ("amulet","claymore"),
"basher" : ("javelin","belt","recipe"),
"battle fury" : ("quelling","claymore","broadsword","ring of health","void stone"),
"ethereal blade" : ("eagle","ghost"),
"silver edge" : ("amulet","claymore","ultimate orb","recipe"), 	
"radiance" : ("relic","recipe"),
"mkb" : ("javelin","javelin","demon edge"),
"daedalus" : ("broadsword","blades","recipe","demon edge","recipe"),
"bfly" : ("eagle","quarterstaff","talisman of evasion"),
"rapier" : ("demon edge","relic"),
"abyssal blade" : ("javelin","belt","recipe","stout","vitality booster","ring of health","recipe"),
"bloodthorn" : ("quarterstaff","sage's mask","robe","quarterstaff","sage's mask","robe","recipe","broadsword","blades","recipe","recipe"),
"hood" : ("cloak","ring of health","ring of regen"),
"vanguard" : ("vitality booster","stout","ring of health"),
"blade mail" : ("chainmail","robe","broadsword"),
"soul booster" : ("energy booster", "vitality booster", "point booster"),
"crimson guard" : ("vitality booster","stout","ring of health","chainmail","ironwood","recipe","recipe"),
"bkb" : ("recipe","ogre","mithril hammer"),
"lotus orb" : ("void stone","ring of health", "platemail", "recipe"),
"shiva's guard" : ("recipe","mystic staff", "platemail"),
"bloodstone" : ("energy booster","ring of regen", "sage's mask","recipe", "point booster", "vitality booster","recipe"),
"manta" : ("ultimate orb","alacrity","elvenskin", "recipe","recipe"),
"linken's sphere" : ("ultimate orb", "recipe","ring of health", "void stone"),
"hurricane pike" : ("wizardry","ring of regen","recipe","ogre","elvenskin","elvenskin","recipe"),
"assault" : ("hyperstone","platemail","chainmail","recipe"),
"heart" : ("reaver","vitality booster","vitality booster"),
"mom" : ("morbid","quarterstaff"),
"dragon lance" : ("ogre","elvenskin","elvenskin"),
"sange" : ("ogre","belt","recipe"),
"yasha" : ("alacrity","elvenskin","recipe"),
"echo sabre" : ("ogre","quarterstaff","sage's mask","robe"),
"maelstrom" : ("mithril hammer","gloves","recipe"),
"diffusal blade" : ("alacrity","alacrity","robe","recipe"),
"heaven's halberd" : ("ogre","belt","recipe","talisman of evasion"),
"sny" : ("ogre","belt","recipe","alacrity","elvenskin","recipe"),
"mjollnir" : ("mithril hammer","gloves","recipe","hyperstone","recipe"),
"dominator": ("gloves", "ring of regen","ironwood","recipe","ring of health")}

def trimRedundancyLists():
	if len(prevGameTalent) > 100:
		prevGameTalent.remove(prevGameTalent[0])
	if len(prevGameStats) > 100:
		prevGameStats.remove(prevGameStats[0])
	if len(prevGameSpeed) > 100:
		prevGameSpeed.remove(prevGameSpeed[0])
	if len(prevGameHasAbility) > 400:
		prevGameHasAbility.remove(prevGameHasAbility[0])
	if len(prevGameWhatItemorComponents) > 70:
		prevGameWhatItemorComponents.remove(prevGameWhatItemorComponents[0])
	if len(prevGameInvoke) > 5:
		prevGameInvoke.remove(prevGameInvoke[0])
	if len(prevGameGoldCost) > 120:
		prevGameGoldCost.remove(prevGameGoldCost[0])
	if len(prevGameManaCostSpell) > 300:
		prevGameManaCostSpell.remove(prevGameManaCostSpell[0])
	if len(prevGameManaCostItem) > 32:
		prevGameManaCostItem.remove(prevGameManaCostItem[0])
	if len(prevGameCooldownItem) > 32:
		prevGameCooldownItem.remove(prevGameCooldownItem[0])
	if len(prevGameCooldownSpell) > 322:
		prevGameCooldownSpell.remove(prevGameCooldownSpell[0])


if __name__ == "__main__":
	try:
		# make everything try:except to handle internet outages 
		readbuffer = ""
		s=socket.socket( )
		
		server = "irc.chat.twitch.tv"
		udaobnfgaiygvbai = 6667
		#PASS = "oauth:" OAUTH REDACTED
		NICK = "dotafeeding"
		stream = "dotafeeding"
		
		s.connect((server, udaobnfgaiygvbai ))
		
		s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
		s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
		s.send(bytes("JOIN #" + stream + " \r\n", "UTF-8"))
		
		s.setblocking(0)
							
		msgnum = 0
		currentTime = time.time()
		skipVote = currentTime
		vlcCheck = currentTime
		gameRound = currentTime - 45
		suggestRound = currentTime
		suggestRoundTime = 120 #change this to song length
		suggestionList= []
		songMaintenance = currentTime - 120
		mainThread = currentTime - 3.22
		paidSong = []
		score = {}
		prevItems = []
		currentSongVotes = {}
		cachefiles = []
		roundTimer = 20
		prevGameStats = []
		prevGameSpeed = []
		prevGameTalent = []
		prevGameHasAbility = []
		prevGameWhatItemorComponents = []
		prevGameInvoke = []
		prevGameGoldCost = []
		prevGameManaCostSpell = []
		prevGameManaCostItem = []
		prevGameCooldownSpell = []
		prevGameCooldownItem = []
		firstTimerun = 1
		firsttimerun = 0
		songQueuer = currentTime - 20
		songTime = 10
		songName = 1
		prevSongs = []
		cachedDuration= {}
		cacheRank = {}
		wonalready = {}
		skippedalready = []
		
		cost = 322
		readChat = time.time()
		votedalready = []
		queryInterval = currentTime + 3
		displayTimer = currentTime-60
		displayTimer2 = currentTime-4
			
		currentSolution = Image.open('d:/streamdata/blankBackup.png', 'r')
		suggestions = {} # chatter or chatterDonor item
		with open("D:/streamdata/banned") as banned:
			banned = banned.readlines()
		banned = [x.strip() for x in banned] 
		roundDuration = 32
		with open("D:/streamdata/balance") as balanced:
			balanced = balanced.readlines()
		balanced = [x.strip() for x in balanced] 
		newbalance = {}
		psa = 0
		for x in balanced:
			x, y = x.split("^%^")
			if x in newbalance:
				newbalance[x]+= float(y)
			else:
				newbalance[x] = float(y)
		balance = newbalance
		
		nospam = []
		nospamdonor = []
		
		printOut = []
		rpm = 1
		rpmUpdate = time.time()
		while 1:
		
			
			currentTime = time.time()
					
			if currentTime - rpmUpdate > 30:
			
				rpm = 0
				doubleCheck = []
				for ch in chatter:
					if ch[1] not in doubleCheck and time.time() - ch[3] < 360:
						doubleCheck.append(ch[1])
						rpm += 1
				rpm = rpm
						
				rpmUpdate = time.time()
			
			if currentTime - songMaintenance > 40:
				"""
				^%^65.mp3
				^%^ = exit to dump data
				65 = chance enumeration
				"""
				
				cachefiles = []
				path = "D:\\music"
				for entry in os.scandir(path):
					entry = entry.name
					acceptableFiles = ["mp3"] #even if it's a video, rename to mp3 regardless
					try:
						if entry[-3:] in acceptableFiles:
							if entry not in cachefiles:
								cachefiles.append(entry)
					except:
						pass
				with open("D:/streamdata/banned") as banned:
					banned = banned.readlines()
				
				banned = [x.strip() for x in banned] 
				for song in cachefiles:
					try:
						data = song.split("^%^")
						cacheRank[data[0]] = data[1][:-4]
						if firsttimerun == 0 or data[0] not in currentSongVotes:
							currentSongVotes[data[0]] = data[1][:-4]
						if cacheRank[data[0]] != currentSongVotes[data[0]]:
							cmd = "ren \""
							cmd += path
							cmd+= "\\"
							cmd += song
							cmd += "\" \""
							cmd+= data[0]
							cmd += "^%^"
							cmd += str(currentSongVotes[data[0]])
							cmd += ".mp3\""
							os.system(cmd)
							cacheRank[data[0]] = currentSongVotes[data[0]]
					except:
						cmd = "ren \""
						cmd += path
						cmd+= "\\"
						cmd += song
						cmd += "\" \""
						cmd+=  song
						cmd = cmd[:-4]
						cmd += "^%^"
						cmd += "25.mp3\""
						os.system(cmd)
						xxx = song[:-4]
						cacheRank[xxx] = "25"
						currentSongVotes[xxx] = 25
				firsttimerun = 1
				songMaintenance = time.time()
			
			
						
			
			if currentTime - songQueuer  > songTime:
				skippedalready = []
				votedalready= []
				totalenumeration = 0
				skipDouble = 0
				for song in currentSongVotes:
					try:
						totalenumeration += int(currentSongVotes[song])
					except:
						print(song)
						pass
				enumcount = random.randrange(0,totalenumeration)
				for song in currentSongVotes:
					try:
						if int(currentSongVotes[song]) > 0:
							enumcount -= int(currentSongVotes[song])
					except:
						pass
					if enumcount <= 0 and song not in prevItems:
						cmd = "\"D:\\music\\"
						cmd += song
						cmd += "^%^"
						cmd += str(cacheRank[song])
						cmd += ".mp3\""
						songTime = duration(song)
						break
				try:
					song = paidSong[0]
					paidSong.remove(paidSong[0])
					cmd = "\"D:\\music\\"
					cmd += song
					cmd += "^%^"
					cmd += str(cacheRank[song])
					cmd += ".mp3\""
					songTime = duration(song)
					displayTimer -= 60
				except:
					pass
				currentSong= song
				try:
					os.startfile(cmd)
				except:
					songTime=5
				prevItems.append(song)
				cmd = "Now Playing: "
				cmd+= song
				cmd+= "\n"
				with open("d:/streamdata/displayqueue","a") as displayqueue:
					displayqueue.write(cmd)
				if len(prevItems) > 7:
					prevItems.remove(prevItems[0])
				songQueuer = time.time()
			#need to skip? set "songTime" to zero.
			
			if currentTime - displayTimer > 60:
				PSA = ["Updated to Patch 7.06e. (July 2)","Type \"play [song]\" to spend 322 points and throw a suggestion to the log.","You can also suggest songs (and support me) through donate.lota.gg.","Approved songs can be played instantly for 322 points, just say \"play [song]\".", "Vote to skip a song by typing \"skip\", \"end\", or \"next\".","Visit youtube.com/dotafeeding for more of Icefrog's Blessings.","Enable me to serve the Dota community at patreon.com/Lota","Skipping a song will reduce or end the chance it will be played."]
				
				printOut.append("Current Song - " + currentSong)
				printOut.append(PSA[psa])
				psa += 1
				if psa == len(PSA):
					psa = 0
				#print out printOut and roundDuration timer
				
				W,H = 750,200
				w,h = 1000,700
				size = 500
				
				maxWidth = 0
				maxMsg =""
				for msg in printOut:
					if len(msg) > maxWidth:
						maxWidth = len(msg)
						maxMsg = msg
				
				textDisplay = Image.open('d:/streamdata/blankPrint.png', 'r')
				displayOut = ""
				for x in printOut:
					displayOut += x + "\n"
				while w> 750:
					font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
					w,h = font.getsize(maxMsg)
					size -= 1
				draw = ImageDraw.Draw(textDisplay)
				draw.text(((0, 0)), displayOut, font=font, fill=(200,200,200))
				textDisplay.save('d:/streamdata/printOut.png',"png")
					
				printOut = []
				
				
				displayTimer = time.time()
						
			
			if currentTime - displayTimer2 > 1:
				
				timeDisplay = Image.open('d:/streamdata/blankTimer.png', 'r')
				timeLeft = str(int(roundDuration - (currentTime - gameRound) ))
				W,H = 125,125
				font = ImageFont.truetype('D:/streamdata/DINPro-Medium.otf', 110)
				w,h = font.getsize(timeLeft)
				draw = ImageDraw.Draw(timeDisplay)
				if float(timeLeft) <0:
					timeLeft = "32"
				draw.text( ((0, 0)), timeLeft, font=font, fill=((200,200,200)) )
				timeDisplay.save('d:/streamdata/timeDisplay.png',"png")
				
					
				
				displayTimer2 = time.time()
						
						
			if currentTime -  mainThread  > 3.22: 
				
			
				
				if currentTime - gameRound > roundDuration: 
					trimRedundancyLists()
					currentSolution.save('d:/streamdata/questionSolution.png',	"png")
					
					#display prominently first to score within 5 seconds of the first correct answer 
					#display everyone else below
					#give points based on (correct chatters/active chatters) (reasonable points given towards 322 song purchase). bonus points for early scorers 
					bonusWinner = Image.open('d:/streamdata/blankWinner.png', 'r')
					plebWinner = Image.open('d:/streamdata/blankWinner.png', 'r')
					bonusWinners = []
					plebWinners = []
					onlyOnce = 1
					for user in wonalready:
						if onlyOnce:
							onlyOnce =0
							bonusWinners.append(min(wonalready,key=wonalready.get))
						if bonusWinners[0] == user:
							pass
						elif wonalready[bonusWinners[0]] - wonalready[user] < 5:
							bonuswinners.append(user)
						else:
							plebWinners.append(user)
							
					plebPoints = (rpm / (len(wonalready) + 1))*3.2
					if plebPoints < 32.2:
						plebPoints = 32.2
					bonusPoints = plebPoints * 3.22
					bonusOut = str(bonusPoints)[:7] + " won by "
					plebOut = str(plebPoints)[:7] + " won by "
					resize = 0
					for pleb in plebWinners:
						if resize + len(pleb) > 48:
							plebout += "\n" + pleb + ", "
							resize = 0
						else:
							plebout += pleb + ", "
							resize +=len(pleb) + 2
						try:
							balance[ch[1]] += 0
						except:
							balance[ch[1]] = 0
							
						plebout = plebout[:-2]
						plebout+= "."
						balance[ch[1]] += plebPoints
						cmd = ch[1]
						cmd+= "^%^"
						cmd+= str(balance[ch[1]])
						cmd+= "\n"
						with open("d:/streamdata/balance","a") as balanced:
							balanced.write(cmd)
					for bonus in bonusWinners:
						if resize + len(bonus) > 48:
							bonusOut += "\n" + bonus + ", "
							resize = 0
						else:
							bonusOut += bonus + ", "
							resize +=len(bonus) + 2
						try:
							balance[ch[1]] += 0
						except:
							balance[ch[1]] = 0
						bonusOut = bonusOut[:-2]
						bonusOut += "."
						balance[ch[1]] += bonusPoints
						cmd = ch[1]
						cmd+= "^%^"
						cmd+= str(balance[ch[1]])
						cmd+= "\n"
						with open("d:/streamdata/balance","a") as balanced:
							balanced.write(cmd)
					if plebWinners == []:
						plebOut+= "nobody."
					if bonusWinners == []:
						bonusOut+= "nobody."
						
					W,H = 1920,200
					w,h = 1000,1000
					size = 50
					while w > 1920 or h > 200:
						font = ImageFont.truetype('D:/streamdata/DINPro-Light.otf', size)
						w,h = font.getsize(bonusOut)
						size -= 1
					draw = ImageDraw.Draw(bonusWinner)
					draw.text((0, (H-h)/2), bonusOut, font=font, fill=(170,170,170))
					bonusWinner.save('d:/streamdata/bonusWinner.png',"png")
					
					W,H = 1920,200
					w,h = 1000,1000
					size = 50
					size = 50
					while w > 1920 or h > 200:
						font = ImageFont.truetype('D:/streamdata/DINPro-Light.otf', size)
						w,h = font.getsize(plebOut)
						size -= 1
					draw = ImageDraw.Draw(plebWinner)
					draw.text((0, (H-h)/2), plebOut, font=font, fill=(100,100,100))
					plebWinner.save('d:/streamdata/plebWinner.png',"png")
					
					wonalready = {}
					rand = random.randint(0,100)
					
					
					
					if rand < 2:
						answer, question = random.choice(list(invokeDict.items()))
						while answer in prevGameInvoke:
							answer, question = random.choice(list(invokeDict.items()))
						invoke = "".join(random.sample(question, len(question)))
						question = "Which spell is invoked with " + invoke + "?"

						currentQuestion = Image.open('d:/streamdata/blankBackup.png', 'r')

						w,h = 1000,1000
						size = 200
						while w > 700 or h > 200:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(question)
							size -= 1
						draw = ImageDraw.Draw(currentQuestion)
						draw.text((2, 35), question, font=font, fill=(200,200,200))
						currentQuestion.paste(vokimages[invoke[0]], (79,131))
						currentQuestion.paste(vokimages[invoke[1]], (286,131))
						currentQuestion.paste(vokimages[invoke[2]], (493,131))

						currentSolution = currentQuestion.copy()
						w,h = 1000,1000
						size = 200
						while w > 700 or h > 500:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(answer)
							size -= 1
						draw = ImageDraw.Draw(currentSolution)
						draw.text((0, 270), answer, font=font, fill=(225,225,225))

						currentQuestion.save('d:/streamdata/questionCurrent.png',"png")
						
						potentialAnswers = [answer]
						prevGameInvoke.append(answer)
					elif rand <17:
						out = []
						while len(out)<2:
							answer, question = random.choice(list(spellCost.items()))
							question = question[1]
							while answer in prevGameCooldownSpell or question == -1:
								answer, question = random.choice(list(spellCost.items()))
								question = question[1]

							getAnswers = {}
							if question.count('/') != 0:
								test = question.split('/')
								descending = float(test[0]) - float(test[1]) > 0
								answerdiff = sorted(question.split('/'),reverse=True)
								sum=-1
								for value in answerdiff:
									if sum == -1:
										sum = 0 #inititalive
										oldVal = value
									else:
										sum += float(oldVal) - float(value)
									oldVal = value
								answerdiff = sum
									
							nameList = {}
							for spell in spellCost:
								if spellCost[spell][1] != -1 and spell != answer and spellCost[spell][1] != question and question.count('/') == spellCost[spell][1].count('/'):
									if question.count('/') != 0:
										tester = spellCost[spell][1].split('/')
										descendinger = float(tester[0]) - float(tester[1]) > 0
										if descending == descendinger:
											tester = sorted(tester,reverse=True)
											sum=-1
											for value in tester:
												if sum == -1:
													sum = 0 #inititalive
													oldVal = value
												else:
													sum += float(oldVal) - float(value)
												oldVal = value
											fsohnsonh = sorted([answerdiff, sum])
											getAnswers[spellCost[spell][1]] =  float(fsohnsonh[1]) - float(fsohnsonh[0])
											nameList[spellCost[spell][1]] = spell
									else:
										fsohnsonh = sorted([float(spellCost[spell][1]), float(question)])
										getAnswers[spellCost[spell][1]] =  float(fsohnsonh[1]) - float(fsohnsonh[0])
										nameList[spellCost[spell][1]] = spell
							x= 10
							while x > 0:
								try:
									x-= 1
									if len(min(getAnswers,key=getAnswers.get)) == len(question) and min(getAnswers,key=getAnswers.get).count('/') == question.count('/'):
										out.append(nameList[min(getAnswers,key=getAnswers.get)])
									getAnswers.pop(min(getAnswers,key=getAnswers.get), None)
								except:
									pass
							if len(out) < 2:
								break
							answerChoices = out
							answerChoices.append(answer)
							answerChoices = sorted(answerChoices)
							
							question = "Which spell has a cooldown of " + question + "?"

							currentQuestion = Image.open('d:/streamdata/blankBackup.png', 'r')
							W,H = 700,500
							w,h = 1000,1000
							size = 200
							while w > 700 or h > 200:
								font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
								w,h = font.getsize(question)
								size -= 1
							draw = ImageDraw.Draw(currentQuestion)
							draw.text((2, 19), question, font=font, fill=(200,200,200))
							tempChoices = ""
							newLine = 0
							for choice in answerChoices:
								newLine += len(choice)
								if newLine > 20 or (newLine + len(choice)) > 35:
									tempChoices += choice + "\n"
									newLine = 0
									lastop = 0
								else:
									tempChoices += choice + "   |  "
									newLine += 6
									lastop=1
							answerChoices = tempChoices
							if lastop:
								answerChoices = tempChoices[:-6]
							
							
							w,h = 1000,1000
							size = 300
							while w > 690 or h > 262:
								font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
								w,h = draw.textsize(answerChoices, font=font)
								size -= 1
							
							w, h = draw.textsize(answerChoices, font=font)
							draw.text(((W-w)/2, 100), answerChoices, font=font, fill=(190,190,190))
							
							currentQuestion.save('d:/streamdata/questionCurrent.png',"png")
							
							currentSolution = currentQuestion.copy()
							w,h = 1000,1000
							size = 500
							while w > 700 or h > 138:
								font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
								w,h = font.getsize(answer)
								size -= 1
							draw = ImageDraw.Draw(currentSolution)
							draw.text(((W-w)/2, 362), answer, font=font, fill=(225,225,225))
					
						potentialAnswers = [answer]
						prevGameCooldownSpell.append(answer) 
					elif rand < 30:
						answer, question = random.choice(list(heroInfoDict.items()))
						question = question[1]
						while answer in prevGameTalent:
							answer, question = random.choice(list(heroInfoDict.items()))
							question = question[1]

						currentQuestion = Image.open('d:/streamdata/blankTalent.png', 'r')

						currentSolution = currentQuestion.copy()

						leftTalents= [385,296,203,113]
						rightTalents= [385,296,203,113]

						currentTalent = 9
						draw = ImageDraw.Draw(currentQuestion)
						for talent in leftTalents:
							cTalent = question[currentTalent]
							color = 200
							if cTalent[0] == "?":
								cTalent = cTalent[1:]
								if random.randint(0,10) > 5:
									newShuf = ""
									for t in cTalent.split(" "):
										newShuf += ''.join(random.sample(t,len(t))).lower() + " "
									cTalent = newShuf
								else:
									cTalent = ''.join(random.sample(cTalent,len(cTalent))).lower()
								color = 123
							W,H = 700,500
							w,h = 1000,1000
							size = 30
							while w > 310 or h > 78:
								font = ImageFont.truetype('D:/streamdata/DINPro-Light.otf', size)
								w,h = draw.textsize(cTalent, font=font)
								size -= 1
							draw.text((383, talent + (78-h)/2), cTalent, font=font, fill=(color,color,color))
							currentTalent+=2
						currentTalent = 8

						for talent in rightTalents:
							cTalent = question[currentTalent]
							color = 200
							if cTalent[0] == "?":
								cTalent = cTalent[1:]
								if random.randint(0,10) > 5:
									newShuf = ""
									for t in cTalent.split(" "):
										newShuf += ''.join(random.sample(t,len(t))).lower() + " "
									cTalent = newShuf
								else:
									cTalent = ''.join(random.sample(cTalent,len(cTalent))).lower()
								color = 100
							W,H = 700,500
							w,h = 1000,1000
							size = 30
							while w > 310 or h > 78:
								font = ImageFont.truetype('D:/streamdata/DINPro-Light.otf', size)
								w,h = draw.textsize(cTalent, font=font)
								size -= 1
							
							
							draw.text((6 + (305-w), talent + (78-h)/2), cTalent, font=font, fill=(color,color,color))
							currentTalent+=2



						questionq = "Whose talent tree is this?"
						W,H = 700,500
						w,h = 1000,1000
						size = 200
						while w > 700 or h > 112:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(questionq)
							size -= 1
						draw = ImageDraw.Draw(currentQuestion)
						draw.text(((W-w)/2, 0), questionq, font=font, fill=(200,200,200))

						currentQuestion.save('d:/streamdata/questionCurrent.png',"png")



						color = 200
						currentTalent = 9
						draw = ImageDraw.Draw(currentSolution)
						for talent in leftTalents:
							cTalent = question[currentTalent]
							if cTalent[0] == "?":
								cTalent = cTalent[1:]
							W,H = 700,500
							w,h = 1000,1000
							size = 30
							while w > 310 or h > 78:
								font = ImageFont.truetype('D:/streamdata/DINPro-Light.otf', size)
								w,h = draw.textsize(cTalent, font=font)
								size -= 1
							draw.text((383, talent + (78-h)/2), cTalent, font=font, fill=(color,color,color))
							currentTalent+=2
						currentTalent = 8

						for talent in rightTalents:
							cTalent = question[currentTalent]
							if cTalent[0] == "?":
								cTalent = cTalent[1:]
							W,H = 700,500
							w,h = 1000,1000
							size = 30
							while w > 310 or h > 78:
								font = ImageFont.truetype('D:/streamdata/DINPro-Light.otf', size)
								w,h = draw.textsize(cTalent, font=font)
								size -= 1
							
							
							draw.text((6 + (305-w), talent + (78-h)/2), cTalent, font=font, fill=(color,color,color))
							currentTalent+=2



						question = answer
						W,H = 700,500
						w,h = 1000,1000
						size = 200
						while w > 700 or h > 100:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(question)
							size -= 1
						draw.text(((W-w)/2, 0), question, font=font, fill=(200,200,200))
						potentialAnswers = heroDict[answer]
						prevGameTalent.append(answer)
					elif rand <45:
						out = []
						while len(out)<2:
							answer, question = random.choice(list(spellCost.items()))
							question = question[0]
							while answer in prevGameManaCostSpell or question == -1:
								answer, question = random.choice(list(spellCost.items()))
								question = question[0]

							getAnswers = {}
							if question.count('/') != 0:
								test = question.split('/')
								descending = float(test[0]) - float(test[1]) > 0
								answerdiff = sorted(question.split('/'),reverse=True)
								sum=-1
								for value in answerdiff:
									if sum == -1:
										sum = 0 #inititalive
										oldVal = value
									else:
										sum += float(oldVal) - float(value)
									oldVal = value
								answerdiff = sum
									
							nameList = {}
							for spell in spellCost:
								if spellCost[spell][0] != -1 and spell != answer and spellCost[spell][0] != question and question.count('/') == spellCost[spell][0].count('/'):
									if question.count('/') != 0:
										tester = spellCost[spell][0].split('/')
										descendinger = float(tester[0]) - float(tester[1]) > 0
										if descending == descendinger:
											tester = sorted(tester,reverse=True)
											sum=-1
											for value in tester:
												if sum == -1:
													sum = 0 #inititalive
													oldVal = value
												else:
													sum += float(oldVal) - float(value)
												oldVal = value
											fsohnsonh = sorted([answerdiff, sum])
											getAnswers[spellCost[spell][0]] =  float(fsohnsonh[1]) - float(fsohnsonh[0])
											nameList[spellCost[spell][0]] = spell
									else:
										fsohnsonh = sorted([float(spellCost[spell][0]), float(question)])
										getAnswers[spellCost[spell][0]] =  float(fsohnsonh[1]) - float(fsohnsonh[0])
										nameList[spellCost[spell][0]] = spell
							x= 10
							while x > 0:
								try:
									x-= 1
									if len(min(getAnswers,key=getAnswers.get)) == len(question) and min(getAnswers,key=getAnswers.get).count('/') == question.count('/'):
										out.append(nameList[min(getAnswers,key=getAnswers.get)])
									getAnswers.pop(min(getAnswers,key=getAnswers.get), None)
								except:
									pass
							if len(out) < 2:
								break
							answerChoices = out
							answerChoices.append(answer)
							answerChoices = sorted(answerChoices)
							
							question = "Which spell has a mana cost of " + question + "?"

							currentQuestion = Image.open('d:/streamdata/blankBackup.png', 'r')
							W,H = 700,500
							w,h = 1000,1000
							size = 200
							while w > 700 or h > 200:
								font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
								w,h = font.getsize(question)
								size -= 1
							draw = ImageDraw.Draw(currentQuestion)
							draw.text((2, 19), question, font=font, fill=(200,200,200))
							tempChoices = ""
							newLine = 0
							for choice in answerChoices:
								newLine += len(choice)
								if newLine > 20 or (newLine + len(choice)) > 35:
									tempChoices += choice + "\n"
									newLine = 0
									lastop = 0
								else:
									tempChoices += choice + "   |  "
									newLine += 6
									lastop=1
							answerChoices = tempChoices
							if lastop:
								answerChoices = tempChoices[:-6]
							
							
							w,h = 1000,1000
							size = 300
							while w > 690 or h > 262:
								font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
								w,h = draw.textsize(answerChoices, font=font)
								size -= 1
							
							w, h = draw.textsize(answerChoices, font=font)
							draw.text(((W-w)/2, 100), answerChoices, font=font, fill=(190,190,190))
							
							currentQuestion.save('d:/streamdata/questionCurrent.png',"png")
							
							currentSolution = currentQuestion.copy()
							w,h = 1000,1000
							size = 500
							while w > 700 or h > 138:
								font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
								w,h = font.getsize(answer)
								size -= 1
							draw = ImageDraw.Draw(currentSolution)
							draw.text(((W-w)/2, 362), answer, font=font, fill=(225,225,225))
							
							potentialAnswers = [answer]
						prevGameManaCostSpell.append(answer)
					elif rand <50:
						out = []

						answer, question = random.choice(list(itemCost.items()))
						question = question[0]
						while answer in prevGameGoldCost or question == -1:
							answer, question = random.choice(list(itemCost.items()))
							question = question[0]

						getAnswers = {}
							

						nameList = {}
						for item in itemCost:
							if itemCost[item][0] != -1 and item != answer and itemCost[item][0] != question:
								if float(question) - float(itemCost[item][0]) > 0:
									getAnswers[itemCost[item][0]] = float(question) - float(itemCost[item][0])
									
								else:
									getAnswers[itemCost[item][0]] = float(itemCost[item][0]) - float(question)
								nameList[itemCost[item][0]] = item
						x= 7
						while x > 0:
							try:
								x-= 1
								out.append(nameList[min(getAnswers,key=getAnswers.get)])
								getAnswers.pop(min(getAnswers,key=getAnswers.get), None)
							except:
								pass
						answerChoices = out
						answerChoices.append(answer)
						answerChoices = sorted(answerChoices)
						question = "Which item costs " + str(question) + " gold?"

						currentQuestion = Image.open('d:/streamdata/blankBackup.png', 'r')
						W,H = 700,500
						w,h = 1000,1000
						size = 200
						while w > 700 or h > 200:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(question)
							size -= 1
						draw = ImageDraw.Draw(currentQuestion)
						draw.text((2, 19), question, font=font, fill=(200,200,200))
						tempChoices = ""
						newLine = 0
						for choice in answerChoices:
							newLine += len(choice)
							if newLine > 20 or (newLine + len(choice)) > 35:
								tempChoices += choice + "\n"
								newLine = 0
								lastop = 0
							else:
								tempChoices += choice + "   |  "
								newLine += 6
								lastop=1
						answerChoices = tempChoices
						if lastop:
							answerChoices = tempChoices[:-6]


						w,h = 1000,1000
						size = 300
						while w > 690 or h > 262:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = draw.textsize(answerChoices, font=font)
							size -= 1

						w, h = draw.textsize(answerChoices, font=font)
						draw.text(((W-w)/2, 100), answerChoices, font=font, fill=(190,190,190))

						currentQuestion.save('d:/streamdata/questionCurrent.png',"png")

						currentSolution = currentQuestion.copy()
						w,h = 1000,1000
						size = 500
						while w > 700 or h > 138:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(answer)
							size -= 1
						draw = ImageDraw.Draw(currentSolution)
						draw.text(((W-w)/2, 362), answer, font=font, fill=(225,225,225))


						potentialAnswers = [itemDict[answer]]
						prevGameGoldCost.append(answer)
					elif rand <59:
						out = []

						answer, question = random.choice(list(heroInfoDict.items()))
						question = question[1][5]
						
						while answer in prevGameSpeed or question == -1:
							answer, question = random.choice(list(heroInfoDict.items()))
							question = question[1][5]

						getAnswers = {}
							

						nameList = {}
						for item in heroInfoDict:
							if heroInfoDict[item][1][5] != -1 and item != answer and heroInfoDict[item][1][5] != question:
								if float(question) - float(heroInfoDict[item][1][5]) > 0:
									getAnswers[heroInfoDict[item][1][5]] = float(question) - float(heroInfoDict[item][1][5])
									
								else:
									getAnswers[heroInfoDict[item][1][5]] = float(heroInfoDict[item][1][5]) - float(question)
								nameList[heroInfoDict[item][1][5]] = item
						x= 7
						while x > 0:
							try:
								x-= 1
								out.append(nameList[min(getAnswers,key=getAnswers.get)])
								getAnswers.pop(min(getAnswers,key=getAnswers.get), None)
							except:
								pass
						answerChoices = out
						answerChoices.append(answer)
						answerChoices = sorted(answerChoices)
						question ="which hero has " + str(question) + " base movement speed?"

						currentQuestion = Image.open('d:/streamdata/blankBackup.png', 'r')
						W,H = 700,500
						w,h = 1000,1000
						size = 200
						while w > 700 or h > 200:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(question)
							size -= 1
						draw = ImageDraw.Draw(currentQuestion)
						draw.text((2, 19), question, font=font, fill=(200,200,200))
						tempChoices = ""
						newLine = 0
						for choice in answerChoices:
							newLine += len(choice)
							if newLine > 20 or (newLine + len(choice)) > 35:
								tempChoices += choice + "\n"
								newLine = 0
								lastop = 0
							else:
								tempChoices += choice + "   |  "
								newLine += 6
								lastop=1
						answerChoices = tempChoices
						if lastop:
							answerChoices = tempChoices[:-6]


						w,h = 1000,1000
						size = 300
						while w > 690 or h > 262:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = draw.textsize(answerChoices, font=font)
							size -= 1

						w, h = draw.textsize(answerChoices, font=font)
						draw.text(((W-w)/2, 100), answerChoices, font=font, fill=(190,190,190))

						currentQuestion.save('d:/streamdata/questionCurrent.png',"png")

						currentSolution = currentQuestion.copy()
						w,h = 1000,1000
						size = 500
						while w > 700 or h > 138:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(answer)
							size -= 1
						draw = ImageDraw.Draw(currentSolution)
						draw.text(((W-w)/2, 362), answer, font=font, fill=(225,225,225))


						potentialAnswers = [heroDict[answer]]

						prevGameSpeed.append(answer)
					elif rand <72:
						out = []

						answer, question = random.choice(list(itemCost.items()))
						question = question[1]
						while answer in prevGameManaCostItem or question == -1:
							answer, question = random.choice(list(itemCost.items()))
							question = question[1]

						getAnswers = {}
							

						nameList = {}
						for item in itemCost:
							if itemCost[item][1] != -1 and item != answer and itemCost[item][1] != question:
								if float(question) - float(itemCost[item][1]) > 0:
									getAnswers[itemCost[item][1]] = float(question) - float(itemCost[item][1])
									
								else:
									getAnswers[itemCost[item][1]] = float(itemCost[item][1]) - float(question)
								nameList[itemCost[item][1]] = item
						x= 7
						while x > 0:
							try:
								x-= 1
								out.append(nameList[min(getAnswers,key=getAnswers.get)])
								getAnswers.pop(min(getAnswers,key=getAnswers.get), None)
							except:
								pass
						answerChoices = out
						answerChoices.append(answer)
						answerChoices = sorted(answerChoices)
						question = "Which item costs " + str(question) + " mana per use?"

						currentQuestion = Image.open('d:/streamdata/blankBackup.png', 'r')
						W,H = 700,500
						w,h = 1000,1000
						size = 200
						while w > 700 or h > 200:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(question)
							size -= 1
						draw = ImageDraw.Draw(currentQuestion)
						draw.text((2, 19), question, font=font, fill=(200,200,200))
						tempChoices = ""
						newLine = 0
						for choice in answerChoices:
							newLine += len(choice)
							if newLine > 20 or (newLine + len(choice)) > 35:
								tempChoices += choice + "\n"
								newLine = 0
								lastop = 0
							else:
								tempChoices += choice + "   |  "
								newLine += 6
								lastop=1
						answerChoices = tempChoices
						if lastop:
							answerChoices = tempChoices[:-6]


						w,h = 1000,1000
						size = 300
						while w > 690 or h > 262:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = draw.textsize(answerChoices, font=font)
							size -= 1

						w, h = draw.textsize(answerChoices, font=font)
						draw.text(((W-w)/2, 100), answerChoices, font=font, fill=(190,190,190))

						currentQuestion.save('d:/streamdata/questionCurrent.png',"png")

						currentSolution = currentQuestion.copy()
						w,h = 1000,1000
						size = 500
						while w > 700 or h > 138:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(answer)
							size -= 1
						draw = ImageDraw.Draw(currentSolution)
						draw.text(((W-w)/2, 362), answer, font=font, fill=(225,225,225))


						potentialAnswers = [itemDict[answer]]
						prevGameManaCostItem.append(answer)

					elif rand <81:
						out = []

						answer, question = random.choice(list(itemCost.items()))
						question = question[2]
						while answer in prevGameCooldownItem or question == -1:
							answer, question = random.choice(list(itemCost.items()))
							question = question[2]

						getAnswers = {}
							

						nameList = {}
						for item in itemCost:
							if itemCost[item][2] != -1 and item != answer and itemCost[item][2] != question:
								if float(question) - float(itemCost[item][2]) > 0:
									getAnswers[itemCost[item][2]] = float(question) - float(itemCost[item][2])
									
								else:
									getAnswers[itemCost[item][2]] = float(itemCost[item][2]) - float(question)
								nameList[itemCost[item][2]] = item
						x= 7
						while x > 0:
							try:
								x-= 1
								out.append(nameList[min(getAnswers,key=getAnswers.get)])
								getAnswers.pop(min(getAnswers,key=getAnswers.get), None)
							except:
								pass
						answerChoices = out
						answerChoices.append(answer)
						answerChoices = sorted(answerChoices)
						question = "Which item has a cooldown of " + str(question) + " seconds?"

						currentQuestion = Image.open('d:/streamdata/blankBackup.png', 'r')
						W,H = 700,500
						w,h = 1000,1000
						size = 200
						while w > 700 or h > 200:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(question)
							size -= 1
						draw = ImageDraw.Draw(currentQuestion)
						draw.text((2, 19), question, font=font, fill=(200,200,200))
						tempChoices = ""
						newLine = 0
						for choice in answerChoices:
							newLine += len(choice)
							if newLine > 20 or (newLine + len(choice)) > 35:
								tempChoices += choice + "\n"
								newLine = 0
								lastop = 0
							else:
								tempChoices += choice + "   |  "
								newLine += 6
								lastop=1
						answerChoices = tempChoices
						if lastop:
							answerChoices = tempChoices[:-6]


						w,h = 1000,1000
						size = 300
						while w > 690 or h > 262:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = draw.textsize(answerChoices, font=font)
							size -= 1

						w, h = draw.textsize(answerChoices, font=font)
						draw.text(((W-w)/2, 100), answerChoices, font=font, fill=(190,190,190))

						currentQuestion.save('d:/streamdata/questionCurrent.png',"png")

						currentSolution = currentQuestion.copy()
						w,h = 1000,1000
						size = 500
						while w > 700 or h > 138:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(answer)
							size -= 1
						draw = ImageDraw.Draw(currentSolution)
						draw.text(((W-w)/2, 362), answer, font=font, fill=(225,225,225))


						potentialAnswers = [itemDict[answer]]
						prevGameCooldownItem.append(answer)
					else:
						out = []

						answer, question = random.choice(list(heroInfoDict.items()))
						question = question[1][0:8]
						while answer in prevGameStats or question == -1:
							answer, question = random.choice(list(heroInfoDict.items()))
							question = question[1][0:8]

						getAnswers = {}
						nameList = {}
						for item in heroInfoDict:	
							sum = 0
							if heroInfoDict[item][1][5] != -1 and item != answer and heroInfoDict[item][1][5] != question:
								if float(question[0][-2:]) - float(heroInfoDict[item][1][0][-2:]) > 0:
									sum = float(question[0][-2:]) - float(heroInfoDict[item][1][0][-2:])
									
								else:
									sum =  float(heroInfoDict[item][1][0][-2:]) - float(question[0][-2:])
								if float(question[1][-2:]) - float(heroInfoDict[item][1][1][-2:]) > 0:
									sum = float(question[1][-2:]) - float(heroInfoDict[item][1][1][-2:])
									
								else:
									sum =  float(heroInfoDict[item][1][1][-2:]) - float(question[1][-2:])
								if float(question[2][-2:]) - float(heroInfoDict[item][1][2][-2:]) > 0:
									sum = float(question[2][-2:]) - float(heroInfoDict[item][1][2][-2:])
									
								else:
									sum =  float(heroInfoDict[item][1][2][-2:]) - float(question[2][-2:])
								nameList[item] = sum

						x= 7
						while x > 0:
							try:
								x-= 1
								out.append(min(nameList,key=nameList.get))
								nameList.pop(min(nameList,key=nameList.get), None)
							except:
								pass
						answerChoices = out
						answerChoices.append(answer)
						answerChoices = sorted(answerChoices)


						tempChoices = ""
						newLine = 0
						for choice in answerChoices:
							newLine += len(choice)
							if newLine > 20 or (newLine + len(choice)) > 35:
								tempChoices += choice + "\n"
								newLine = 0
								lastop = 0
							else:
								tempChoices += choice + "   |  "
								newLine += 6
								lastop=1
						answerChoices = tempChoices
						if lastop:
							answerChoices = tempChoices[:-6]
						#(str,agi,int,atk,armor,ms,turnrate,vision,
						currentQuestion = Image.open('d:/streamdata/blankStats.png', 'r')
						draw = ImageDraw.Draw(currentQuestion)

						W,H = 700,500

						font = ImageFont.truetype('D:/streamdata/DINPro-Bold.otf', 34)
						draw.text((78, 48) ,question[0][:2], font=font, fill=((255,255,255)))
						draw.text((78, 119) ,question[1][:2], font=font, fill=((255,255,255)))
						draw.text((78, 190) ,question[2][:2], font=font, fill=((255,255,255)))

						font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', 30)
						draw.text((120, 50) ,("+" + question[0][-3:] + " per level"), font=font, fill=((161,169,158)))
						draw.text((120, 121) ,("+" + question[1][-3:] + " per level"), font=font, fill=((161,169,158)))
						draw.text((120, 192) ,("+" + question[2][-3:] + " per level"), font=font, fill=((161,169,158)))


						font = ImageFont.truetype('D:/streamdata/DINPro-Medium.otf', 32)
						w,h = draw.textsize(question[3], font=font)

						draw.text(( (466-w ), 48) ,question[3], font=font, fill=((230,230,230)))
						w,h = draw.textsize(question[4], font=font)
						draw.text(( (466-w ), 99) ,question[4], font=font, fill=((230,230,230)))
						w,h = draw.textsize(question[5], font=font)
						draw.text(( (466-w ), 149) ,question[5], font=font, fill=((230,230,230)))
						w,h = draw.textsize(question[6], font=font)
						draw.text(( (466-w ), 199) ,question[6], font=font, fill=((230,230,230)))

						currentSolution = currentQuestion.copy()

						w,h = 1000,1000
						size = 300
						while w > 690 or h > 239:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = draw.textsize(answerChoices, font=font)
							size -= 1

						w, h = draw.textsize(answerChoices, font=font)
						draw.text(((W-w)/2, 257), answerChoices, font=font, fill=(190,190,190))

						currentQuestion.save('d:/streamdata/questionCurrent.png',"png")


						w,h = 1000,1000
						size = 500
						while w > 700 or h > 239:
							font = ImageFont.truetype('D:/streamdata/DINPro-Regular.otf', size)
							w,h = font.getsize(answer)
							size -= 1
						draw = ImageDraw.Draw(currentSolution)
						draw.text(((W-w)/2, ( 246+ ((252 -h)/2 ))), answer, font=font, fill=(225,225,225))


						potentialAnswers = [heroDict[answer]]
						prevGameStats.append(answer)
					temp =[]
					try:
						if isinstance(potentialAnswers[0], str) == False:
							for ans in potentialAnswers[0]:
								temp.append(ans)
							potentialAnswers = temp
					except:
						pass
					print(potentialAnswers)
					
					roundDuration = 32
					gameRound = time.time()
				
				
				#chatter = (msgID,userID,message,time)
				for ch in chatter:
					if ch[0] not in nospam and ch[1] not in banned:
						#print(ch[2])
						nospam.append(ch[0])
						if "skip" in ch[2].split(" ") or "end" in ch[2].split(" ") or "next" in ch[2].split(" ") and ch[1] not in skippedalready:
							skippedalready.append(ch[1])
							skipDouble += 1
						signal = ["play","suggest","queue","listen","request"]		
						cmd = re.sub("[^a-zA-Z]+", " ",str(ch[2])).lower()
						cmd = cmd.split(" ")
						tryPlayNext = 0
						for sig in signal:
							if sig == cmd[0]:
								signal = 1
								break
						if signal == 1:					
							for track in currentSongVotes:
								trakbak = track
								track = re.sub("[^a-zA-Z]+", " ",track).lower()
								track = track.split(" ")
								if fuzz.ratio(str(trakbak),str(ch[2]) ) > 85:
								
									currentSongVotes[trakbak] = float(currentSongVotes[trakbak]) + .1
									tryPlayNext = trakbak
									break
								breaker = 0
								for c in cmd:
									for t in track:
										if fuzz.partial_ratio(c, t)> 85:
											track.remove(t)
											break
								if len(track) ==0:
									currentSongVotes[trakbak] = float(currentSongVotes[trakbak]) + .1
									tryPlayNext = trakbak
									break
							if tryPlayNext != 0:
								cost = 322
								
								try:
									balance[ch[1]] += 0
								except:
									balance[ch[1]] = 0
								if balance[ch[1]] >cost:
									balance[ch[1]] -= cost
									cmd = ch[1]
									cmd+= "^%^-"
									cmd+= str(cost)
									cmd+= "\n"
									with open("d:/streamdata/balance","a") as balanced:
										balanced.write(cmd)
									paidSong.append(tryPlayNext)
									cmd = ch[1]
									cmd+= " paid "
									cmd+= str(cost)
									cmd+= " points to play "
									cmd+= tryPlayNext
									printOut.append(cmd)
							else:
								cost = 322
								try:
									balance[ch[1]] += 0
								except:
									balance[ch[1]] = 0
								if balance[ch[1]] >cost:
									balance[ch[1]] -= cost
									cmd = ch[1]
									cmd+= "^%^-"
									cmd+= str(cost)
									cmd+= "\n"
									with open("d:/streamdata/balance","a") as balanced:
										balanced.write(cmd)
									songTime = 0
									cmd = ch[1]
									cmd+= " paid "
									cmd+= str(cost)
									cmd+= " points to "
									cmd+= ch[2]
									printOut.append(cmd)
									
									suggestion = ch[1]
									suggestion+= " suggested "
									suggestion+= ch[2]
									suggestion+= "\n"
									with open("d:/streamdata/requests","a") as requests:
										requests.write(suggestion)
								displayTimer -= 60
						#item game logic #chatter = (msgID,userID,message,time)
						
						
						
						if " " in ch[2]:
							msg = ch[2].split(" ")
						else:
							msg = [ch[2]]
						maxlen = 0
						
						temp = []
						for answer in potentialAnswers:
							maxlen += len(answer) + 5
						won = 0
						if len(ch[2]) < maxlen:
							for answer in potentialAnswers:
								if fuzz.ratio(answer, ch[2]) > 70:
									won = 1
								for word in msg:
									
									if word in potentialAnswers:
										won= 1
									if fuzz.ratio(answer, word) > 70:
										won =1
									if word == answer:
										won=1
						if ch[1] not in wonalready and won:
							print(ch[1] + " : " + ch[2])
							wonalready[ch[1]] = ch[3]
							
				try:
					if skipDouble > rpm/1.5 and skipDouble > 7: 
						songTime = 0
						currentSongVotes[song] = str(float(currentSongVotes[song]) - ( float(skipDouble)/ float(rpm) ))
						cmd = "Song skipped by vote."
						printOut.append(cmd)
				except:
					pass
				
				mainThread = time.time()
			
			try:
				readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
				temp = str.split(readbuffer, "\n")
				readbuffer=temp.pop( )
			except:
				pass
			if temp != []:
				for line in temp:
					if (line[:4] == "PING"):
						s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
					x = 0
					out = ""
					line = str.rstrip(line)
					line = str.split(line)
					
					
					for index, i in enumerate(line):
						if x == 0:
							user = line[index]
							user = user.split('!')[0]
							user = user[0:12] + ": "
						if x == 3:
							out += line[index]
							out = out[1:]
						if x >= 4:
							out += " " + line[index]
						x = x + 1
						
					
					# Respond to ping, squelch useless fee5dback given by twitch, print output and read to list
					if user == "PING: ":
						pass
					elif user == ":tmi.twitch.tv: ":
						pass
					elif user == ":tmi.twitch.: ":
						pass
					elif user == ":%s.tmi.twitch.tv: " % "dotafeeding":
						pass
					else:
						try:
							if out[0:1] != '!':
								msgnum += 1
								out = out.lower()
								out = re.sub(r'[^a-z0-9/s]', " ", out)
								chat = (msgnum,user[1:-2],out,time.time())
								chatter.append(chat)#chatter = (msgID,userID,message,time)
						except:
							pass
				temp= []
			readChat = time.time()
	except:
		try:
			s.close()
		except:
			pass
		startt = "start cmd /K C:\\Drive\\Code\\music\\launch.py"
		os.system(startt)