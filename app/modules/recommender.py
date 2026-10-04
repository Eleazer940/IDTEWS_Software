from app.config import RECOMMENDATIONS
class Recommender:
 @staticmethod
 def get_recommendations(c):return list(RECOMMENDATIONS.get(c,[]))
 @staticmethod
 def explain(c,features,feature_importance):
  x=sorted(feature_importance,key=feature_importance.get,reverse=True)[:2]
  return f"The Decision Tree classified this student as {c}. Important model factors include {', '.join(x)}. Recommendations should support professional academic judgement."
