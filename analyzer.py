from typing import List
from models import Product, ChannelRecommendation


class ProductAnalyzer:
    def recommend_channels(self, product: Product) -> List[ChannelRecommendation]:
        recommendations = []
        
        # Analyze based on target audience and stage
        keywords = (product.description + " " + product.target_audience).lower()
        
        # Reddit scoring
        reddit_score = 7
        reddit_reason = "Good for niche communities and early feedback"
        if "developer" in keywords or "technical" in keywords:
            reddit_score = 9
            reddit_reason = "Excellent for technical audiences in r/programming, r/SideProject"
        recommendations.append(ChannelRecommendation(
            channel="Reddit",
            score=reddit_score,
            reason=reddit_reason
        ))
        
        # Hacker News scoring
        hn_score = 6
        hn_reason = "Suitable for tech-savvy early adopters"
        if product.stage == "mvp" or "developer" in keywords or "startup" in keywords:
            hn_score = 9
            hn_reason = "Perfect for Show HN - technical audience loves MVPs"
        recommendations.append(ChannelRecommendation(
            channel="Hacker News",
            score=hn_score,
            reason=hn_reason
        ))
        
        # Twitter scoring
        twitter_score = 7
        twitter_reason = "Good for building in public and quick feedback"
        if product.stage == "launched":
            twitter_score = 8
            twitter_reason = "Great for announcements and viral potential"
        recommendations.append(ChannelRecommendation(
            channel="Twitter",
            score=twitter_score,
            reason=twitter_reason
        ))
        
        # Product Hunt scoring
        ph_score = 5
        ph_reason = "Better for polished products with good UI"
        if product.stage == "launched":
            ph_score = 9
            ph_reason = "Ideal for official launches with complete products"
        recommendations.append(ChannelRecommendation(
            channel="Product Hunt",
            score=ph_score,
            reason=ph_reason
        ))
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        return recommendations
