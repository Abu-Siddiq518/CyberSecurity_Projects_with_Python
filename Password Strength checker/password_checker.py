import re
import math

COMMON = {
    "password","passw0rd","letmein","welcome","qwerty","qwertyuiop","asdfgh",
    "zxcvbn","iloveyou","dragon","monkey","football","admin","login",
    "abc123","123456","123456789","111111","000000","1q2w3e","sunshine"
}

DICT_ROOTS = {
    "pass","love","admin","root","secret","god","hello","welcome","user","test",
    "india","bharat","krishna","ganesh","ram","tech","guest","default","system"
}

KEY_SEQS = [
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiopasdfghjklzxcvbnm",
    "0123456789"
]

LEET_MAP = str.maketrans({
    '0':'o','1':'l','3':'e','4':'a','5':'s','7':'t','8':'b','9':'g','@':'a','$':'s','!':'i'
})

def normalize_leet(s: str) -> str:
    return s.lower().translate(LEET_MAP)

def has_seq(s: str, min_len=4) -> bool:
    s_lower = s.lower()
    for base in KEY_SEQS:
        for i in range(len(base) - min_len + 1):
            chunk = base[i:i+min_len]
            if chunk in s_lower or chunk[::-1] in s_lower:
                return True
    return False

def entropy_bits(pw: str) -> float:
    pool = 0
    if re.search(r'[a-z]', pw): pool += 26
    if re.search(r'[A-Z]', pw): pool += 26
    if re.search(r'\d', pw):    pool += 10
    if re.search(r'[^\w]', pw): pool += 33
    pool = max(pool, 1)
    return len(pw) * math.log2(pool)

def evaluate_password(pw: str) -> dict:
    score = 0
    tips = []

    if not pw:
        return {"score": 0, "label": "Very Weak", "entropy": 0.0, "tips": ["Password is empty."]}

    L = len(pw)
    if L >= 20: score += 30
    elif L >= 16: score += 24
    elif L >= 12: score += 18
    elif L >= 8: score += 10
    else: score += 2; tips.append("Use at least 12–16 characters.")

    lowers = bool(re.search(r'[a-z]', pw))
    uppers = bool(re.search(r'[A-Z]', pw))
    digits = bool(re.search(r'\d', pw))
    symbols = bool(re.search(r'[^\w]', pw))

    variety_points = 0
    variety_points += 6 if lowers else 0
    variety_points += 6 if uppers else 0
    variety_points += 6 if digits else 0
    variety_points += 7 if symbols else 0
    score += variety_points

    if sum([lowers, uppers, digits, symbols]) < 3:
        tips.append("Mix at least three types: lower, UPPER, digits, symbols.")

    if lowers and not uppers:
        tips.append("Add uppercase letters.")
    if uppers and not lowers:
        tips.append("Add lowercase letters.")
    if not digits:
        tips.append("Add a few digits.")
    if not symbols:
        tips.append("Add symbols (e.g., !@#).")

    if re.search(r'(.)\1\1', pw):
        score -= 10
        tips.append("Avoid repeating characters like 'aaa' or '111'.")
    if has_seq(pw, 4):
        score -= 12
        tips.append("Avoid common sequences (e.g., 1234, abcd, qwerty).")

    norm = normalize_leet(pw)
    if norm in COMMON:
        score -= 25
        tips.append("Do not use common passwords.")
    for root in DICT_ROOTS:
        if root in norm and len(root) >= 4:
            score -= 10
            tips.append(f"Avoid dictionary words like '{root}'.")
            break

    if re.fullmatch(r'[A-Za-z]+', pw) or re.fullmatch(r'\d+', pw):
        score -= 10
        tips.append("Don’t use only letters or only digits.")

    score = max(0, min(100, score + 30))

    if score < 25:
        label = "Very Weak"
    elif score < 45:
        label = "Weak"
    elif score < 65:
        label = "Fair"
    elif score < 85:
        label = "Strong"
    else:
        label = "Very Strong"

    bits = round(entropy_bits(pw), 1)
    tips = list(dict.fromkeys(tips))

    return {"score": score, "label": label, "entropy": bits, "tips": tips}
