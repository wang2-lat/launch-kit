from typing import Dict
from models import Product


class TemplateGenerator:
    def generate(self, product: Product, channel: str) -> Dict[str, str]:
        channel = channel.lower()
        
        if channel == "reddit":
            return self._reddit_template(product)
        elif channel == "hacker news" or channel == "hn":
            return self._hn_template(product)
        elif channel == "twitter":
            return self._twitter_template(product)
        elif channel == "product hunt" or channel == "producthunt":
            return self._ph_template(product)
        else:
            return self._generic_template(product)
    
    def _reddit_template(self, product: Product) -> Dict[str, str]:
        return {
            "title": f"I built {product.name} - {product.description[:60]}",
            "body": f"""Hey everyone!

I've been working on {product.name} for the past few months. It's designed for {product.target_audience}.

**What it does:**
{product.description}

**Current stage:** {product.stage}

I'd love to hear your thoughts and feedback. What features would make this more useful for you?

Happy to answer any questions!""",
            "cta": "Try it out and let me know what you think!"
        }
    
    def _hn_template(self, product: Product) -> Dict[str, str]:
        return {
            "title": f"Show HN: {product.name} – {product.description[:70]}",
            "body": f"""Hi HN,

I built {product.name} to solve a problem I faced: finding the right users for technical products.

Target users: {product.target_audience}

Key features:
- {product.description}

This is currently in {product.stage} stage. I'm looking for early feedback from the community.

Technical stack and architecture decisions available in the repo/docs.

What would you change or add?""",
            "cta": "Check it out and share your feedback"
        }
    
    def _twitter_template(self, product: Product) -> Dict[str, str]:
        return {
            "title": f"Launching {product.name} 🚀",
            "body": f"""Just launched {product.name}!

{product.description}

Built for {product.target_audience}

Currently: {product.stage}

What do you think? 👇""",
            "cta": "Try it now → [link]"
        }
    
    def _ph_template(self, product: Product) -> Dict[str, str]:
        return {
            "title": f"{product.name} - {product.description[:80]}",
            "body": f"""**The Problem:**
{product.target_audience} struggle with [specific pain point]

**The Solution:**
{product.name} helps you {product.description}

**Key Features:**
• Feature 1: [describe]
• Feature 2: [describe]
• Feature 3: [describe]

**Why Now:**
We're in {product.stage} stage and looking for early adopters to shape the product.

**What's Next:**
Your feedback will directly influence our roadmap.""",
            "cta": "Get early access"
        }
    
    def _generic_template(self, product: Product) -> Dict[str, str]:
        return {
            "title": f"Introducing {product.name}",
            "body": f"{product.description}\n\nBuilt for {product.target_audience}.\n\nCurrently in {product.stage} stage.",
            "cta": "Learn more"
        }
