from collections import Counter
from typing import List, Tuple

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


most_popular_new_interests(users_interests)

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


print(len(user_interest_vectors))
print(len(user_similarities))