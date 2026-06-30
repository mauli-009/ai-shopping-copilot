from groq import Groq
from app.config import settings

import json

# One shared Groq client for the whole app
client = Groq(api_key=settings.GROQ_API_KEY)

# Free, fast, capable model. Good default for this project.
MODEL = "llama-3.3-70b-versatile"


def ai_test(prompt: str) -> str:
    """Simple text completion — used to verify Groq works."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content





def analyze_product(product: dict) -> dict:
    """Analyze a clothing product and return structured insights as a dict."""
    system_prompt = (
        "You are a fashion shopping assistant. Analyze the clothing product "
        "and respond with ONLY a valid JSON object, no markdown, no extra text. "
        "Use this exact schema:\n"
        "{\n"
        '  "worth_buying": boolean,\n'
        '  "score": number (0-10, one decimal),\n'
        '  "fabric": string (short, e.g. "Premium Cotton"),\n'
        '  "value_for_money": string (one short sentence),\n'
        '  "suitable_for": [array of short strings, e.g. "Casual", "College"],\n'
        '  "recommendation": string (one actionable sentence)\n'
        "}"
    )

    user_prompt = (
        f"Title: {product.get('title')}\n"
        f"Brand: {product.get('brand')}\n"
        f"Price: {product.get('price')}\n"
        f"Description: {product.get('description')}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,                       # lower = more consistent
        response_format={"type": "json_object"},  # forces valid JSON
    )

    raw = response.choices[0].message.content
    return json.loads(raw)   # safe because json_object mode guarantees valid JSON


def summarize_reviews(product_title: str, reviews: list[str]) -> dict:
    """Turn raw reviews into structured pros/cons."""
    system_prompt = (
        "You are a shopping assistant. Summarize the customer reviews into a "
        "JSON object only, no markdown, no extra text. Use this exact schema:\n"
        "{\n"
        '  "pros": [array of short strings],\n'
        '  "cons": [array of short strings],\n'
        '  "overall_sentiment": string (e.g. "Mostly Positive"),\n'
        '  "common_complaint": string (the single most frequent issue, or "None")\n'
        "}"
    )
    joined = "\n".join(f"- {r}" for r in reviews)
    user_prompt = f"Product: {product_title}\n\nReviews:\n{joined}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)



def style_score(product: dict) -> dict:
    """Rate a product across style dimensions."""
    system_prompt = (
        "You are a fashion expert. Rate this clothing item. Respond with a JSON "
        "object only, no markdown. Use this exact schema, all scores 0-10 with one decimal:\n"
        "{\n"
        '  "overall": number,\n'
        '  "versatility": number,\n'
        '  "comfort": number,\n'
        '  "trend": number,\n'
        '  "quality": number,\n'
        '  "summary": string (one short sentence)\n'
        "}"
    )
    user_prompt = (
        f"Title: {product.get('title')}\n"
        f"Brand: {product.get('brand')}\n"
        f"Price: {product.get('price')}\n"
        f"Description: {product.get('description')}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def shopping_chat(product: dict, question: str) -> str:
    """Answer a shopping question about a specific product."""
    system_prompt = (
        "You are a helpful, honest shopping assistant. Answer the user's question "
        "about this clothing product concisely and practically. Be direct about "
        "whether something is worth buying. Keep it under 4 sentences."
    )
    context = (
        f"Product context:\n"
        f"Title: {product.get('title')}\n"
        f"Brand: {product.get('brand')}\n"
        f"Price: {product.get('price')}\n"
        f"Description: {product.get('description')}\n\n"
        f"User question: {question}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ],
        temperature=0.6,
    )
    return response.choices[0].message.content