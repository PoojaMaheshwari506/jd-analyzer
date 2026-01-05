from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from roles import ROLES
from skills import ROLE_SKILLS, GENERIC_SKILLS
# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- PRECOMPUTE ROLE EMBEDDINGS ----------------
ROLE_EMBEDDINGS = {
    role: model.encode(" ".join(keywords))
    for role, keywords in ROLES.items()
}

# ---------------- PRECOMPUTE SKILL EMBEDDINGS ----------------
SKILL_EMBEDDINGS = {
    role: model.encode(skills)
    for role, skills in ROLE_SKILLS.items()
}


# ---------------- ROLE DETECTION ----------------
def detect_role(jd_embedding):
    role_scores = {}

    for role, role_embedding in ROLE_EMBEDDINGS.items():
        score = cosine_similarity(
            [jd_embedding], [role_embedding]
        )[0][0]
        role_scores[role] = score

    return max(role_scores, key=role_scores.get)


# ---------------- SENIORITY DETECTION ----------------
def detect_seniority(jd_text: str) -> str:
    text = jd_text.lower()

    if "intern" in text:
        return "Intern"
    if "senior" in text or "lead" in text or "5+" in text:
        return "Senior"
    if "2+" in text or "3+" in text:
        return "Mid"

    return "Junior"


# ---------------- SKILL EXTRACTION ----------------
from skills import ROLE_SKILLS, GENERIC_SKILLS

def extract_skills(jd_embedding, role):
    # 1️⃣ Try role-based skills first
    skills = ROLE_SKILLS.get(role, [])
    skill_embeddings = SKILL_EMBEDDINGS.get(role)

    matched = []

    if skills and skill_embeddings is not None:
        similarities = cosine_similarity([jd_embedding], skill_embeddings)[0]
        matched = [
            skill for skill, score in zip(skills, similarities)
            if score > 0.30
        ]

    # 2️⃣ FALLBACK: generic skills
    if len(matched) < 2:
        generic_embeddings = model.encode(GENERIC_SKILLS)
        similarities = cosine_similarity([jd_embedding], generic_embeddings)[0]

        matched = [
            skill for skill, score in zip(GENERIC_SKILLS, similarities)
            if score > 0.35
        ]

    required = matched[:4]
    nice_to_have = matched[4:]

    return required, nice_to_have



# ---------------- MAIN ANALYSIS ----------------
def analyze_jd(jd_text: str):
    # ✅ Compute JD embedding ONCE
    jd_embedding = model.encode(jd_text)

    role = detect_role(jd_embedding)
    seniority = detect_seniority(jd_text)
    required, nice = extract_skills(jd_embedding, role)

    skill_count = len(required) + len(nice)
    word_count = len(jd_text.split())
    if skill_count >= 6 or word_count > 120:
        complexity = "High"
    elif skill_count >= 3:
        complexity = "Medium"
    else:
        complexity = "Low"

    return {
        "role": role,
        "seniority": seniority,
        "required_skills": required,
        "nice_to_have": nice,
        "complexity": complexity
    }
