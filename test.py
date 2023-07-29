from collections import Counter, defaultdict
from typing import List, Tuple, Dict


users_interests = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]

# 1. Recommend what is popular
popular_interests = Counter(interest
                            for user_interests in users_interests
                            for interest in user_interests)


def most_popular_new_interests(user_interests: List[str],
                               max_results: int = 5) -> List[Tuple[str, int]]:
    suggestions = [(interest, frequency)
                   for interest, frequency in popular_interests.most_common()
                   if interest not in user_interests]

    return suggestions[:max_results]


# 2. User-Based Collaborative Filtering
unique_interests = sorted({interest
                           for user_interests in users_interests
                           for interest in user_interests})

print(f"The unique interests are: {unique_interests}")


def make_user_interest_vector(user_interests: List[str]) -> List[int]:
    return [1 if interest in user_interests else 0
            for interest in unique_interests]

user_interest_vectors = [make_user_interest_vector(user) for user in users_interests]


from scratch.nlp import cosine_similarity
user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                      for interest_vector_j in user_interest_vectors]
                     for interest_vector_i in user_interest_vectors]


def most_similar_users_to(user_id: int)->List[Tuple]:
    pairs = [(user, similarity) for user,similarity in enumerate(user_similarities[user_id]) if user != user_id and similarity > 0]
    return sorted(pairs, key=lambda pair: pair[-1], reverse=True)

def user_based_suggestions(user_id: int, include_current_interests: bool = False):
    # Sum up the similarities
    suggestions: Dict[str, float] = defaultdict(float)
    print(most_similar_users_to(user_id))
    for other_user_id, similarity in most_similar_users_to(user_id):
        for interest in users_interests[other_user_id]:
            suggestions[interest] += similarity

    # Convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda pair: pair[-1],  # weight
                         reverse=True)

    # And (maybe) exclude already interests
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]

print(user_based_suggestions(1))